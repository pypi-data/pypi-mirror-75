"""Running and parsing blast results."""
import json
import logging
import os
import pathlib
import re
from contextlib import contextmanager
from typing import Any, Dict, Iterator, Optional, Tuple

import attr
import click
from me_finder.context import ExecutionContext
from me_finder.errors import DependencyError, ExitCodeError
from me_finder.shell import _get_executable_path, run_shell
from mgedb import MGEdb

LOG = logging.getLogger(__name__)

# Errors
class BlastError(Exception):
    """Generic blast errror."""
    pass


class BlastDatabaseError(BlastError):
    """Errors related to database."""
    pass


@attr.s(auto_attribs=True, frozen=True, slots=True)
class BlastHsp:
    """HSP information container."""

    query_start: int
    query_end: int
    subject_start: int
    subject_end: int
    e_value: float
    num_gaps: int
    identity: float
    expected: float
    num_subs: int
    hit_strand: int
    cigar: str
    query_seq: str
    subject_seq: str
    midline: str

    def __len__(self):
        """Length of HSP."""
        return  self.subject_end - self.subject_start + 1


@attr.s(auto_attribs=True, frozen=True, slots=True)
class BlastHit:
    """Blast hit."""

    query_name: str
    query_len: int
    subject_name: str
    subject_len: int
    depth: Optional[float]
    hsps: Tuple[BlastHsp, ...]


@contextmanager
def database_environment(db_path: str) -> Iterator[None]:
    """Set db_path as blast database environment variable within context.

    Restore original BLASTDB environment on exit."""
    original_db_path = os.environ.get('BLASTDB')
    os.environ['BLASTDB'] = db_path
    LOG.info(f'Set BLASTDB environment variable to: {db_path}')
    yield
    LOG.info(f'Resetting BLASTDB environment variable to: {original_db_path}')
    if original_db_path is None:
        del os.environ['BLASTDB']
    else:
        os.environ['BLASTDB'] = original_db_path


def _blast_aln_to_vcf_snp(reference, alternative):
    """Parse blast alignment and return SNP positions in vcf 4.2 format.

    Positions are 1 indexed.
    """

    def _format_snp():
        """Format current snp event."""
        if curr_event == 'S':
            reference_snp = reference[idx - 1]
            alternative_snp = alternative[idx - 1]
            pos = idx - insertion_modifier
        elif curr_event == 'D':
            reference_snp = reference[last_match_pos:idx]
            alternative_snp = alternative[last_match_pos]
            pos = last_match_pos + 1 - insertion_modifier
        elif curr_event == 'I':
            reference_snp = reference[last_match_pos]
            alternative_snp = alternative[last_match_pos:idx]
            pos = last_match_pos + 1 - insertion_modifier
        else:
            # sanity check
            raise ValueError(curr_event)

        return pos, {'ref': reference_snp, 'alt': alternative_snp}

    reference = reference.upper()
    alternative = alternative.upper()
    assert len(reference) == len(alternative)

    # persitant variables between iterations
    last_match_pos = 0  # last position of a match
    insertion_modifier = 0  # for normalization of positions

    # keep track of current motif
    curr_event = None
    curr_insertion_size = 0  # count size of current inseriton

    snps = {}  # result container
    for idx in range(len(reference)):
        # store current nucleotide
        ref_nt = reference[idx]
        alt_nt = alternative[idx]
        # detect insertion, deletion and substitution events
        if ref_nt == alt_nt:
            event = 'M'
        elif ref_nt == '-':
            event = 'I'
            curr_insertion_size += 1
        elif alt_nt == '-':
            event = 'D'
        elif ref_nt != alt_nt:
            event = 'S'
        # report snps based on events
        if curr_event is None:  # first event
            curr_event = event
            if event != 'M':
                idx = 1
                pos, snp = _format_snp()  # record snp
                snps[pos] = snp
                idx = 0
                # add current insertion size to modifier
                insertion_modifier += curr_insertion_size
                curr_insertion_size = 0
        elif event != curr_event:  # if current event changes and is not match
            if curr_event != 'M':
                pos, snp = _format_snp()  # record snp
                snps[pos] = snp
                # add current insertion size to modifier
                insertion_modifier += curr_insertion_size
                curr_insertion_size = 0
            curr_event = event
        # update postion
        if curr_event == 'M':
            last_match_pos = idx  # set new match pos
    return snps


def _parse_alignment(qseq, hseq):
    """Parse blast alignment and return SNP positions in vcf 4.2 format.

    Positions are 1 indexed.
    """
    snps = {}
    for pos, (alt, ref) in enumerate(zip(qseq, hseq), start=1):
        if alt == ref:
            continue
        snps[pos] = {'ref': ref, 'alt': alt, 'pos': pos}
    return snps


def _blast_aln_to_cigar(reference, target):
    """Convert blast alignement to CIGAR string.

    operations
    ----------
    M 	match
    I 	insert a gap into the reference sequence
    D 	insert a gap into the target (delete from reference)
    F 	frameshift forward in the reference sequence
    R 	frameshift reverse in the reference sequence
    """
    cigar = []
    curr_operation = None
    length = 1
    for ref, alt in zip(reference, target):
        # identify operation
        if ref == alt:
            operation = 'M'
        elif ref == '-':
            operation = 'I'
        elif alt == '-':
            operation = 'D'
        elif ref != alt:
            operation = 'M'
        else:
            # sanity check
            raise ValueError(f'ref: {ref}, alt: {alt}')

        if curr_operation is None:
            curr_operation = operation
        elif operation != curr_operation:
            cigar.append(f'{curr_operation}{length}')
            curr_operation = operation
            length = 1
        else:
            length += 1
    cigar.append(f'{curr_operation}{length}')
    return ' '.join(cigar)


def _parse_hits_json(blast_result: Dict[str, Any]) -> Iterator[BlastHit]:
    """Parse hits from blast result in json format."""
    for query in blast_result['BlastOutput2']:
        query_name = query['report']['results']['search']['query_title']
        query_len = query['report']['results']['search']['query_len']
        for hit in query['report']['results']['search']['hits']:
            hsps = []
            for hsp in hit['hsps']:
                q_start, q_end = sorted([hsp['query_from'], hsp['query_to']])
                s_start, s_end = sorted([hsp['hit_from'], hsp['hit_to']])
                hsp = BlastHsp(
                    query_start=q_start,
                    query_end=q_end,
                    subject_start=s_start,
                    subject_end=s_end,
                    e_value=hsp['evalue'],
                    num_gaps=hsp['gaps'],
                    identity=hsp['identity'] / hsp['align_len'],
                    expected=hsp['evalue'],
                    num_subs=hsp['align_len'] -
                    (hsp['identity'] + hsp['gaps']),
                    hit_strand=1 if hsp['hit_strand'] == 'Plus' else -1,
                    cigar=_blast_aln_to_cigar(hsp['qseq'], hsp['hseq']),
                    query_seq=hsp['qseq'],
                    midline=hsp['midline'],
                    subject_seq=hsp['hseq'])
                hsps.append(hsp)
            yield BlastHit(query_name=query_name,
                           query_len=query_len,
                           subject_len=hit['len'],
                           subject_name=hit['description'][0]['title'],
                           depth=_parse_cov(query_name),
                           hsps=tuple(hsps))


def _element_length(hsps) -> int:
    """Estimate the putative element length.

    Estimated to be from first hsp start to last hsp end pos.
    """
    elem_start = min(h['query_start'] for h in hsps)
    elem_end = max(h['query_end'] for h in hsps)
    return elem_end - elem_start + 1


def _parse_cov(node: str) -> Optional[float]:
    """Parse kmer coverage of contig from contig header."""
    match = re.search(r'cov_(\d+(\.\d+)?)', node)
    if match:
        return float(match.group(1))
    return None


def _get_exec_path(path: str) -> Optional[str]:
    """Get path to executalbe, if not found raise usage error."""
    try:
        exec_path = _get_executable_path(path)
    except DependencyError:
        err_message = f'{path} executable not found in PATH'
        LOG.error(err_message)
        raise click.UsageError(
            f'{err_message}, please specify path with --{path}-path')
    return exec_path


def make_database(db: MGEdb, makedb_exec, path=None) -> None:
    """Make blast database from MGEdb in path specifed in BLASTDB env variable."""
    db_dir = pathlib.Path(os.environ.get('BLASTDB'))  # type: ignore
    # set input path
    seq_file = db.record_sequences_path if path is None else path
    db_name = seq_file.name[:-len(seq_file.suffix)]
    # full path to database
    blast_db_path = db_dir.joinpath(db_name)

    # Get makeblastdb path
    exec_path = _get_exec_path(makedb_exec)

    LOG.info(f'make blast database, path: {blast_db_path}')
    run_shell(exec_path, '-in', seq_file, '-dbtype',
              'nucl', '-title', db_name, '-out', blast_db_path)


def run_blast(ctx: ExecutionContext, db_name: str, contigs: str) -> str:
    """Search contigs for moitfs in database with blastn."""
    # check if blast results already exists
    blast_result_path: str = ctx.file_path('blast', '%s_blast.json' % db_name)
    if os.path.isfile(blast_result_path):
        LOG.info(f'using cached blast result: {blast_result_path}')
        return blast_result_path

    # Get BLAST path
    blast_path = _get_exec_path(ctx.blastn_path)

    # read blastn config
    blast_cfg = ctx.config['blast']
    # TODO check filtering of low complexity regions and number of hits thresholds
    LOG.info(f'running blastn, db: {db_name}')
    try:
        run_shell(blast_path, '-query', contigs, '-out', blast_result_path,
                  '-db', db_name, '-num_threads', ctx.num_threads,
                  '-word_size', blast_cfg.getint('word_size'), '-soft_masking',
                  blast_cfg.getboolean('soft_masking'), '-task',
                  blast_cfg.get('task'), '-outfmt', 15)
    except ExitCodeError as error:
        if os.path.getsize(blast_result_path) == 0:
            os.remove(blast_result_path)
        if 'database error' in error.stderr.lower():
            raise BlastDatabaseError
        raise click.UsageError(
            f'Error running blastn; {error.stderr}; cmd: {error.cmd}')
    ctx.check_path(blast_result_path)  # verify that files has been generated
    return blast_result_path


def iter_blast_hits(blast_result_path: str) -> Iterator[BlastHit]:
    """Read blast result file and iterate over hits."""
    with open(blast_result_path) as file:  # blast xml fmt
        with open(blast_result_path) as fileh:
            js_output = json.load(fileh)
            for hit in _parse_hits_json(js_output):
                yield hit


def blastdb_exist(ctx: ExecutionContext, db_name: str) -> bool:
    """Check if blastdb with db_name exists."""
    db_path = pathlib.Path(ctx.idx_db_path)
    return all(db_path.joinpath('{db_name}.{suffix}').is_file()
               for suffix in ['nin', 'nhr', 'nsq'])
