"""Command line interface for mge finder."""
import logging
import os
import tempfile
from configparser import ConfigParser
from itertools import product
from typing import Optional

import click
from mgedb import MGEdb, Sequences
from pkg_resources import resource_filename

from .context import ExecutionContext
from .converters import convert_to_biopython
from .io import (ContigSequences, abbreviate_result, write_cge_results_file,
                 write_csv_format, write_fasta, write_gff3, write_json_format)
from .predictor import MgeFinderResult, predict_mges
from .tools import (ReadDepth, database_environment, get_read_depth,
                    make_blast_database, run_blast)
from .tools.blast import BlastDatabaseError
from .version import __version__ as version

# setupt default working directory
_DEFAULT_WD = os.path.join(tempfile.gettempdir(), 'mge_finder')

# Options
SHARED_OPTIONS = [
    click.option('--makeblastdb-path',
                 default='makeblastdb',
                 type=str,
                 help='Path to Blast, if the executable is not in PATH'),
    click.option('--db-path',
                 type=click.Path(resolve_path=True),
                 default=os.path.join(_DEFAULT_WD, 'database'),
                 help='Path to MGEdb')
]


def _get_fname(sample_path: str) -> str:
    """Get sample file name without suffixes from path."""
    # Generate list of expected suffixes
    SEQ_SUFFIXES = ['fa', 'fasta', 'fna']
    COMPRESSED_SUFFIXES = ['', 'gz', 'gzip']
    expected_suffixes = ['.'.join(suffix) if suffix[-1] else suffix[0]
                         for suffix in product(SEQ_SUFFIXES, COMPRESSED_SUFFIXES)]

    fname = os.path.basename(sample_path)
    # strip suffixes from sample name
    sample_name = None
    for suffix in expected_suffixes:
        if fname.endswith(suffix):
            sample_name = fname.replace('.' + suffix, '')
    if sample_name is None:  # fallback stratery if no suffix could be matched
        sample_name = '.'.join(fname.split('.')[:-1])
    return sample_name


def _print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(version)
    ctx.exit()


def add_options(options):
    """Add cli options to commands."""
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


class ConfigFileParam(click.Path):
    """Custom class for reading config files."""
    def __init__(self):
        """Initialize click Path function."""
        super().__init__(exists=True, dir_okay=False)

    def convert(self, value, param, ctx):
        """Convert to path and return fastq reader."""
        path = super().convert(value, param, ctx)
        cfg = ConfigParser()
        cfg.read(path, encoding='utf-8')
        return cfg


@click.group()
@click.option('-q', '--quiet', is_flag=True, help='Suppress logging output.')
@click.option('--version',
              is_flag=True,
              callback=_print_version,
              expose_value=False,
              is_eager=True)
def cli(quiet):
    """Mobile Genetic Element Finder.

    Find mobile elements in raw sequence data.
    """
    if quiet:
        logging.getLogger().setLevel(logging.ERROR)


@cli.command()
@click.option('-c',
              '--contig',
              type=click.Path(exists=True, resolve_path=True),
              help='Specify pre-assembled contigs to perform analysis on.')
@click.option('-f',
              '--fq-file',
              multiple=True,
              type=click.Path(exists=True, resolve_path=True),
              help='Sequencing files in fastq format. Only used for annotating sequence depth in GFF files (Optional)')
@click.option('--config',
              type=ConfigFileParam(),
              default=resource_filename(__name__, 'config.ini'),
              help='Path to user defined config')
@click.option('-j',
              '--json',
              is_flag=True,
              help='Write output in json format.')
@click.option('-g',
              '--gff',
              is_flag=True,
              help='Write MGE location on contig in gff format.')
@click.option('-t',
              '--threads',
              type=int,
              default=1,
              help='Number of threads [default: 1]')
@click.option('--min-coverage', type=float, help=f'Minimum coverage')
@click.option('--max-evalue', type=int, help=f'Maximum alignment e-value')
@click.option('--temp-dir',
              type=click.Path(resolve_path=True),
              default=_DEFAULT_WD,
              help='Set directory for temporary files.')
@click.option('--kma-path',
              type=str,
              default='kma',
              help='Path to KMA, if the executable is not in PATH')
@click.option('--blastn-path',
              default='blastn',
              type=str,
              help='Path to Blast, if the executable is not in PATH')
@add_options(SHARED_OPTIONS)
@click.argument('output', type=click.Path(resolve_path=True))
def find(output, config, fq_file, threads, contig, kma_path, min_coverage,
         max_evalue, temp_dir, makeblastdb_path, blastn_path, db_path, json,
         gff):
    """Find mobile element in sequence data."""

    LOG = logging.getLogger(__name__)
    LOG.info('starting execution of script')

    if not os.path.isdir(temp_dir):
        os.makedirs(db_path, exist_ok=True)

    if not os.path.isdir(db_path):
        os.makedirs(db_path, exist_ok=True)

    if max_evalue:
        config.set('validation', 'e_value', str(max_evalue))

    if min_coverage:
        config.set('validation', 'coverage', str(min_coverage))

    # TODO add input validation
    if not contig:
        raise click.UsageError('No input files')

    ctx = ExecutionContext(
        fq_files=list(fq_file) if fq_file else fq_file,
        sample_name=_get_fname(fq_file[0]) if fq_file else _get_fname(contig),
        config=config,
        mge_db=MGEdb(),  # load database object
        base_wd_dir=temp_dir,
        kma_path=kma_path,
        idx_db_path=str(db_path),
        blastn_path=blastn_path,
        makeblastdb_path=makeblastdb_path,
        num_threads=threads,
        output=output)
    LOG.info(f'working directory: {ctx.dir_path()}')

    db: MGEdb = ctx.mge_db

    with database_environment(ctx.idx_db_path):  # set BLASTDB env for context
        try:
            blast_result: str = run_blast(ctx, 'mge_records', contig)
        except BlastDatabaseError:
            # if database has not been indexed
            make_blast_database(db,
                                ctx.makeblastdb_path)  # make blast database
            blast_result: str = run_blast(ctx, 'mge_records', contig)
    contig_sequence = ContigSequences(contig)
    mges, seqs, alns = predict_mges(ctx, blast_result, contig_sequence)

    if len(mges) == 0:
        LOG.info('No mobile elements found')

    # make output dir
    ctx.dir_path(os.path.dirname(ctx.output))

    # write mge sequences to fasta file
    mge_seq_path = ctx.file_path(f'{ctx.output}_mge_sequences.fna')
    LOG.info(f'Writing mge sequences to: {mge_seq_path}')
    write_fasta(mge_seq_path, seqs, force=True)

    # write result in cge format
    prediction_path = ctx.file_path(f'{ctx.output}_result.txt')
    write_cge_results_file(prediction_path, db, mges, alns)

    # write csv output format
    prediction_path = ctx.file_path(f'{ctx.output}.csv')
    abbrev_result = abbreviate_result(mges)  # for output
    write_csv_format(ctx, prediction_path, abbrev_result)

    if json:  # json output format
        prediction_path = ctx.file_path(f'{ctx.output}.json')
        write_json_format(ctx, prediction_path, mges, alns)
    if gff:  # gff output
        read_depth: Optional[ReadDepth]
        if ctx.fq_files and len(mges) != 0:
            # Align reads to contigs to infer read depth
            read_depth = get_read_depth(ctx, mge_seq_path)
        else:
            read_depth = None

        # For GFF3 output
        seq_records = convert_to_biopython(db, mges, read_depth)

        # Write sequence features in GFF format
        seq_feature_path = ctx.file_path(f'{ctx.output}.gff')
        write_gff3(seq_feature_path, seq_records)

        # Write blast alignment to vcf format
        # mge_variant_path = ctx.file_path(f'{ctx.output}.vcf')
        # write_vcf(ctx, mge_variant_path, pred_mges, read_depth)


@cli.command()
@add_options(SHARED_OPTIONS)
def index(db_path, makeblastdb_path):
    """Initialize tool by generating the database."""
    # Setup logger
    LOG = logging.getLogger(__name__)
    LOG.info('starting execution of script')

    if not os.path.isdir(db_path):
        os.makedirs(db_path, exist_ok=True)

    db = MGEdb()  # load database
    with database_environment(db_path):  # set BLASTDB env for context
        os.makedirs(db_path, exist_ok=True)
        make_blast_database(db, makeblastdb_path)  # make blast database
    click.secho(f'Created databases in: {db_path}', fg='green')
