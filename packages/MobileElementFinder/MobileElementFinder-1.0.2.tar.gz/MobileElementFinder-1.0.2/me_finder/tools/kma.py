"""Find mobile in raw sequences with KMA."""
import gzip
import logging
import os
from typing import Iterator, Optional, Tuple

import numpy as np

import attr
import click
from me_finder.context import ExecutionContext
from me_finder.errors import DatabaseError, DependencyError, KMAError
from me_finder.shell import _get_executable_path, run_shell

LOG = logging.getLogger(__name__)


def index_fasta_file(ctx: ExecutionContext, fasta_path: str,
                     output_db_path: str):
    """Index fasta file with KMA for performing KMA alignements."""
    if not os.path.isfile(fasta_path):  # sanity check
        raise FileNotFoundError(fasta_path)

    # no need to recreate database if it already exists
    if os.path.isfile(f'{output_db_path}.comp.b'):
        return

    # Get KMA path
    try:
        kma_path = _get_executable_path(ctx.kma_path)
    except DependencyError:
        err_message = 'kma executable not found in PATH'
        LOG.error(err_message)
        raise click.UsageError(
            f'{err_message}, please specify path with --kma-path')
    LOG.info(f'Creating index in: {output_db_path}')
    run_shell(kma_path, 'index', '-i', fasta_path, '-o', output_db_path)


def count_read_depth(alignment_file, template):
    """Count depth of reads aligning to template."""
    template_length = len(template)

    cnt = np.zeros(template_length, dtype=int)
    with open(alignment_file, 'rb') as o:
        for line in o:
            _, start, end, template, _ = line.rsplit(b'\t', 4)
            start = int(start) - 1
            end = int(end) - 1
            cnt[start:end] += 1
    return cnt


@attr.s(auto_attribs=True, frozen=True, slots=True)
class KmaResult():
    """Results from a KMA analysis.

    Stores the paths to the different result files.
    """
    overview: str
    consensus_seq: str
    fragments: str
    basecount_matrix: Optional[str]
    vcf_file: Optional[str]


def run_kma(ctx: ExecutionContext, db_path: str) -> KmaResult:
    """Search contigs for moitfs in database with blastn."""
    # check if database has been indexed
    db_name = os.path.basename(db_path)

    try:
        ctx.check_path(f'{db_path}.comp.b')
    except FileNotFoundError:
        raise DatabaseError(f'No index found for database: {db_name}')

    # Get KMA path
    try:
        kma_path = _get_executable_path(ctx.kma_path)
    except DependencyError:
        err_message = 'kma executable not found in PATH'
        LOG.error(err_message)
        raise click.UsageError(
            f'{err_message}, please specify path with --kma-path')
    else:
        kma_path = ctx.kma_path

    # read kma config
    kma_cfg = ctx.config['kma']

    # Check if output already exist
    output_path = ctx.file_path('kma', f'{db_name}_result')

    # If matrix shall be outputed, validate output file
    mtrx_path = ctx.file_path(f'{output_path}.mat.gz') if kma_cfg.getboolean(
        'matrix') else None
    vcf_path = ctx.file_path(f'{output_path}.vcf.gz') if kma_cfg.getboolean(
        'vcf') else None

    if os.path.isdir(output_path):
        return KmaResult(
            overview=ctx.check_path(f'{output_path}.res'),
            consensus_seq=ctx.check_path(f'{output_path}.fsa'),
            fragments=ctx.check_path(f'{output_path}.frag.gz'),
            basecount_matrix=mtrx_path,
            vcf_file=vcf_path,
        )

    input_files = ['-ipe'] + ctx.fq_files if len(
        ctx.fq_files) == 2 else ['-i'] + ctx.fq_files

    # Set special output commands
    flags = []
    if kma_cfg.getboolean('matrix'):
        flags.append('-matrix')
    if kma_cfg.getboolean('vcf'):
        flags.append('-vcf')
    if kma_cfg.getboolean('all_mappings'):
        flags.append('-a')
        success_phrase = 'Score collection done'
    else:
        success_phrase = 'KMA mapping done'

    # Run KMA
    LOG.info(f'Running KMA')
    proc = run_shell(kma_path,
                     '-t_db',
                     db_path,
                     '-o',
                     output_path,
                     '-t',
                     ctx.num_threads,
                     '-reward',
                     kma_cfg.getint('aln_reward'),
                     '-penalty',
                     kma_cfg.getint('aln_penalty'),
                     '-gapopen',
                     kma_cfg.getint('aln_gapopen'),
                     '-gapextend',
                     kma_cfg.getint('aln_gapextend'),
                     '-per',
                     kma_cfg.getint('aln_pairing'),
                     *flags,
                     *input_files,
                     check=False)
    # workaround for kma havign default return code 1
    if success_phrase not in proc.stderr:
        raise KMAError(f'exit code error: {proc.cmd}')
    # log progress
    LOG.info(f'KMA output written to: {os.path.dirname(output_path)}')
    LOG.debug(proc.stderr)  # write output for debug

    return KmaResult(
        overview=ctx.check_path(f'{output_path}.res'),
        consensus_seq=ctx.check_path(f'{output_path}.fsa'),
        fragments=ctx.check_path(f'{output_path}.frag.gz'),
        basecount_matrix=mtrx_path,
        vcf_file=vcf_path,
    )


ReadDepth = Iterator[Tuple[str, np.matrix]]


def _read_depth_matrix(matrix_file) -> ReadDepth:
    """Calculare the read depth of template form KMA matrix file.

    Return the per base nucleotide read depth matrix for each template.
    The order of the matrix are A, C, G, T, *, -
    """
    LOG.info('read depth matrix')
    with gzip.open(matrix_file, 'rt') as mtrx:
        title = None
        raw_depth = []
        for line in mtrx:
            line = line.strip()
            if line.startswith('#'):
                # return counts related to a template
                if title is not None:
                    # return matrix with nt combinations.
                    yield title, np.asmatrix(raw_depth, dtype=np.uint16)
                    raw_depth = []
                    title = None
                title = line[1:]
            else:
                if line:  # skip empty lines
                    raw_depth.append(line.split('\t')[1:])
    depth_mtrx = np.asmatrix(raw_depth, dtype=np.uint16)
    return title, depth_mtrx  # final iteration


def get_read_depth(ctx: ExecutionContext, template_path: str) -> ReadDepth:
    """Infer MGE read depth."""
    # index written sequences with kma
    kma_index_path: str = ctx.file_path('kma', 'index', 'predicted_mges')
    index_fasta_file(ctx, template_path, kma_index_path)

    # run kma
    kma_result: KmaResult = run_kma(ctx, kma_index_path)

    return _read_depth_matrix(kma_result.basecount_matrix)
