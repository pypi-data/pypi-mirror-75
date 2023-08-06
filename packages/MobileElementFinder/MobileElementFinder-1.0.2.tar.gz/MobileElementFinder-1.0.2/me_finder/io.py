"""IO functions of mge finder."""

import datetime
import json
import logging
import os
import re
import subprocess
from csv import DictWriter
from itertools import groupby
from typing import Any, Dict, List, Optional, TextIO, Tuple, Union

import cattr
import numpy as np
from BCBio import GFF
from Bio.SeqIO.FastaIO import SimpleFastaParser
from me_finder import __version__ as mgefinder_version
from mgedb import MGEdb, Sequence, Sequences
from mgedb import __version__ as mgedb_version
from mgedb.db import MgeType
from mgedb.io import chunk
from mgedb.sequence import reverse_complement
from tabulate import tabulate

from .context import ExecutionContext
from .errors import CoordinateError, CoordOutOfBoundsError
from .result import MgeResult

LOG = logging.getLogger(__name__)


def decompose_cn_mge_id(cn_mge_id):
    """Build mge_id for composite transposons."""
    return cn_mge_id.split('_')


class ContigSequences:
    """Get contig sequences."""
    def __init__(self, path: str) -> None:
        self._file_path: str = path
        self._fa = None  # type: Optional[Dict[str, int]]

    def _read_fa(self) -> Dict[str, Sequence]:
        """Read and index fasta."""
        if self._fa is None:
            self._fa = {s.title: s for s in read_fasta_file(self._file_path)}
        return self._fa

    def sub_sequence(self, start: int, end: int, strand: int,
                     contig: str) -> Sequence:
        """Get sub-sequence from start-end from contig with header."""
        if start < 0 or end < 0:
            raise CoordinateError

        contig = self._read_fa()[contig].seq

        if start > len(contig) or end > len(contig):
            raise CoordOutOfBoundsError

        # convert to zero index
        seq = contig[start:end]
        seq = seq if strand == 1 else reverse_complement(seq)
        return Sequence(title=None, seq=seq)

    def __len__(self):
        """Return num sequences."""
        return len(self._read_fa())

    def __iter__(self) -> Sequence:
        """Iterate over read sequences."""
        for seq in self._read_fa().values():
            yield seq


def _find_version(args: List[str], pattern: str) -> str:
    """Find version of program invoked by arguments.

    Keyword Arguments:
    args: List[str, ...] -- commands invoking version
    pattern: str] -- regex pattern for version number
    """
    process = subprocess.run(args,
                             universal_newlines=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
    match = re.search(pattern, process.stdout)
    if match:
        return match.group(1)
    else:
        raise ValueError(f'regex pattern do not match version string', pattern,
                         process.stdout)


def read_fasta_file(path: str):
    """Read fasta file and return fasta sequence object."""
    with open(path) as f:
        for header, seq in SimpleFastaParser(f):
            yield Sequence(title=header, seq=seq)


def _get_versions(ctx: ExecutionContext) -> Dict[str, str]:
    """Get versions of dependandies."""
    core = {
        'mge_finder': mgefinder_version,
        'mgedb': mgedb_version,
        'blastn': _find_version([ctx.blastn_path, '-version'],
                                r'blastn: (\S+)+'),
    }
    if ctx.fq_files:  # add relevant dependancies
        assembly = {
            'kma':
            _find_version([ctx.kma_path, '--version'], r'KMA-(\S+)')}
    else:
        assembly = {}
    return {**core, **assembly}


def _csv_format_result(entry: Union[MgeResult, Dict[str, Any]]
                       ) -> Dict[str, Union[int, float, str]]:
    """Format data in MgeEntry into format suitable for csv."""
    unstructured = cattr.unstructure(entry)
    result = {}
    for fieldname, value in unstructured.items():
        if isinstance(value, (list, tuple, set)):
            value = ';'.join(value)
        elif isinstance(value, (int, float)):
            value = round(value, 3)
        result[fieldname] = value
    return result


def _write_csv_comment(file_object: TextIO, line: str, num_signs=1) -> None:
    """Print comment line."""
    comment_sign = '#' * num_signs
    print(f'{comment_sign}{line.rstrip()}', file=file_object)


def write_csv_format(ctx: ExecutionContext, output: str, result) -> None:
    """Write MGEs in csv format."""
    LOG.info(f'writing predicted mges to: {output}')
    date = datetime.datetime.now().isoformat(sep='_', timespec='minutes')
    # write metadata as preabmle lines
    with open(output, 'w') as out:
        _write_csv_comment(out, f'date: {date}')
        _write_csv_comment(out, f'sample: {ctx.sample_name}')
        for prog, version in _get_versions(ctx).items():
            _write_csv_comment(out, f'{prog} version: {version}')

        # write data as results
        frow = next(result)
        csv_writer = DictWriter(out, fieldnames=frow.keys())
        csv_writer.writeheader()
        # write first row before first row
        if not all(r is None for r in frow.values()):
            unstructured = _csv_format_result(frow)
            csv_writer.writerow(unstructured)
        for entry in result:  # type: MgeResult
            # Convert the results to dictionary
            unstructured = _csv_format_result(entry)
            csv_writer.writerow(unstructured)


def write_json_format(ctx: ExecutionContext, output: str, mges, alns) -> None:
    """Write identified records to output."""
    # prepare data
    alns_idx = {g: list(a) for g, a in groupby(alns, key=lambda x: x.mge_id)}
    result = cattr.unstructure(mges)
    for r in result:
        # get mge ids for putative composite transposons
        if r['type'] == 'cn' and r['evidence'] == 2:
            _, *mge_id = decompose_cn_mge_id(r['mge_id'])
        else:
            mge_id = [str(r['mge_id'])]

        # add alignments to results
        alns = []
        for mid in mge_id:
            for aln in alns_idx[mid]:
                alns.append(cattr.unstructure(aln))
        r['alignment'] = alns
    rv = {
        'meta': {
            'versions': _get_versions(ctx),
            'sample': ctx.sample_name,
            'date': datetime.datetime.now().isoformat(sep='_',
                                                      timespec='minutes'),
        },
        'result': result,
    }
    LOG.info(f'writing predicted mges to: {output}')
    with open(output, 'w') as out:
        json.dump(rv, out, indent=True, sort_keys=True)


def write_fasta(path: str, sequences: Sequences, width=60,
                force=False) -> None:
    """Write sequences to file in fasta format."""
    if os.path.isfile(path) and not force:
        raise FileExistsError(path)

    with open(path, 'w') as out:
        for seq in sequences:
            print(f'>{seq.title}', file=out)  # Write header
            for i in range(0, len(seq.seq), width):
                print(seq.seq[i:i + width], file=out)


def write_gff3(output: str, seq_records) -> None:
    """Write SeqRecords in GFF3 format."""
    LOG.info(f'writing mges features to: {output}')
    with open(output, 'w') as out:
        GFF.write(list(seq_records), out)


def _stringify_dict(hashtable):
    """Convert dictionary to key-value pair string."""
    kv_pairs = [f'{key}={int(value)}' for key, value in hashtable.items()]
    return ';'.join(kv_pairs)


def write_vcf(ctx, output, predicted_mges, depth):
    """Write substitutions and indel within a predicted mge to mock vcf file.

    This is strictly indented to be used for visualization
    No quality metrics are given.
    """
    LOG.info(f'writing variants in predicted mges to: {output}')
    # Col index for the different read counts
    COL_TABLE = {'A': 0, 'C': 1, 'G': 2, 'T': 3, 'N': 4, '-': 5}
    # headers
    HEADERS = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO']

    with open(output, 'w') as out:
        # write comments
        _write_csv_comment(out, 'fileformat=VCFv4.2', num_signs=2)

        date = datetime.date.strftime(ctx.timestamp, '%Y%m%d')
        _write_csv_comment(out, f'fileDate={date}', num_signs=2)

        versions = _get_versions(ctx)
        _write_csv_comment(out,
                           f'source=MgeFinder v{versions["mge_finder"]}',
                           num_signs=2)
        _write_csv_comment(
            out,
            'INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">',
            num_signs=2)
        _write_csv_comment(
            out,
            'INFO=<ID=AD,Number=1,Type=Integer,Description="Allele Depth">',
            num_signs=2)
        csv_writer = DictWriter(out, fieldnames=HEADERS, delimiter='\t')
        _write_csv_comment(out, '\t'.join(HEADERS),
                           num_signs=1)  # write headers
        for mge in predicted_mges:
            # write metadata as preabmle lines
            seq_depth = depth.get(f'{mge.name}|{mge.mge_id}',
                                  np.zeros((mge.allele_seq_length, 6)))
            # work around KMA issues
            # KMA is not predicting some of the sequences as present,
            # probably beacuse conclave algorithm is assigning the reads
            # to a similar template. Creates an empty array.
            for snp_pos in sorted(mge.snps):
                snp = mge.snps[snp_pos]
                # correct the position to zero based
                # add allele depth
                # TODO fix the parsing of kma depth matrix
                # KMA depth matrix describes the depth of the alignment string
                # insertions and deletions in the matrix introduced phasing issues which is
                # not currently accounted for. This is a major bug which makes the depth unreliable
                alt_nt_depth = []
                tot_nt_depth = []
                for pos, nt in enumerate(snp['alt']):
                    curr_pos = snp_pos - 1 + pos
                    alt_nt_depth.append(seq_depth[curr_pos, COL_TABLE[nt]])
                    tot_nt_depth.append(seq_depth[curr_pos])

                alt_depth = np.mean(alt_nt_depth)
                tot_depth = np.sum(tot_nt_depth)

                info = {'DP': tot_depth, 'AD': alt_depth}
                ref = '.' if snp['ref'] == '-' else snp['ref']
                alt = '.' if snp['alt'] == '-' else snp['alt']
                entry = {
                    'CHROM': mge.contig,
                    'POS': mge.start + snp_pos - 1,  # correct for zero index
                    'ID': '.',
                    'REF': snp['ref'],
                    'ALT': snp['alt'],
                    'QUAL': '.',
                    'FILTER': '.',
                    'INFO': _stringify_dict(info),
                }
                csv_writer.writerow(entry)


def abbreviate_result(results: Tuple[MgeResult]):
    """Abbreviate results full result keeping output for colnames."""
    LOG.debug(f'abbreviate results')
    if len(results) == 0:
        yield {
            'mge_no': None,
            'name': None,
            'synonyms': None,
            'prediction': None,
            'type': None,
            'allele_len': None,
            'depth': None,
            'e_value': None,
            'identity': None,
            'coverage': None,
            'gaps': None,
            'substitution': None,
            'contig': None,
            'start': None,
            'stop': None,
            'cigar': None,
        }

    for mge_result in results:
        yield {
            'mge_no': mge_result.mge_id,
            'name': mge_result.name,
            'synonyms': mge_result.synonyms,
            'prediction': mge_result.evidence.name.lower(),
            'type': mge_result.type.name.replace('_', ' ').lower(),
            'allele_len': mge_result.allele_seq_length,
            'depth': mge_result.depth,
            'e_value': mge_result.e_value,
            'identity': mge_result.identity,
            'coverage': mge_result.coverage,
            'gaps': mge_result.gaps,
            'substitution': mge_result.substitutions,
            'contig': mge_result.contig,
            'start': mge_result.start,
            'end': mge_result.end,
            'cigar': mge_result.cigar,
        }


def _abbrev_to_full_mge_name(abbrev: str) -> str:
    return MgeType(abbrev).name.lower().replace('_', ' ')


def write_cge_results_file(output_path: str, db: MGEdb,
                           mges: Tuple[MgeResult], alignments) -> None:
    """Write file in cge results format.

    The file is used for compatibility with front end gui.
    """
    def text_table(fh, name, mges_of_type):
        # format information in rows
        header = [
            'Mge name', 'Identity', 'Query / Template length', 'Num hsps',
            'Contig', 'Position in contig', 'Accession number'
        ]
        res = []
        if mges_of_type is None:  # add empty tbl rows
            res.append(['-', '-', '-', 'No hit found', '-', '-', '-'])
        else:
            for mge in mges_of_type:
                res.append([
                    mge.name, mge.identity,
                    f'{mge.template_length} / {mge.allele_seq_length}',
                    mge.num_hsps, mge.contig, f'{mge.start}..{mge.end}',
                    mge.template.accession,
                ])
        # get max row length to determine table spacer
        tbl = tabulate(res, headers=header, tablefmt='simple').split('\n')
        # Prepare title injection
        width = len(tbl[0])
        # Switch horisontal line
        tbl[1] = '*' * (width + 2)
        # Update table with title
        tbl = (("%s\n" * 3) % ('*' * (width + 2), '\n'.join(tbl), '=' *
                               (width + 2)))
        # add name row above table
        mge_tbl = f'{"*" * 111}\n{name}\n{tbl}'
        return mge_tbl

    LOG.info(f'Writing cge results file to: {output_path}')
    with open(output_path, 'w') as out:
        # write first sections
        print('mgefinder Results', file=out)
        out.write('\n')
        elements = [
            _abbrev_to_full_mge_name(e) for e in sorted(db.nomenclature)
        ]
        print(f'Mobile element(s): {",".join(elements)}', file=out)
        out.write('\n')
        # write the element section
        gr_mges = {
            _abbrev_to_full_mge_name(k): list(v)
            for k, v in groupby(mges, key=lambda x: x.type.value)
        }
        for e_name in elements:
            elem = gr_mges.get(e_name)
            tbl = text_table(out, e_name, elem)
            print(tbl, file=out)

        # print alignments
        print('\nExtended Output:\n', file=out)
        for aln in alignments:
            print(f'# {aln.name}, id={aln.mge_id}, hsp {aln.hsp_no}', file=out)
            width = 60
            qdesig = 'query:'
            sdesig = 'subject:'
            for qseq, mid, sseq in zip(chunk(aln.query_seq, width),
                                       chunk(aln.midline, width),
                                       chunk(aln.subject_seq, width)):
                padding = ' ' * (16 - len(sdesig))
                print(f'{sdesig}{padding}{sseq}', file=out)
                print(f'{" " * 16}{mid}', file=out)
                padding = ' ' * (16 - len(qdesig))
                print(f'{qdesig}{padding}{qseq}\n', file=out)
