"""HMMer wrapper functions."""

from mge_finder.context import ExecutionContext
from mge_finder.shell import _get_executable_path, run_shell


def run_nhmmscan(ctx: ExecutionContext, db_name, sequence):
    """Run nhmmscan and parse output."""

    # TODO: remove typging ignore
    nhmmscan_path = _get_executable_path(ctx.hmmer_path)  # type: ignore
    hmm_model = ''

    result_tbl = ctx.path('annotate', 'nhmmscan.tsv')    # type: ignore
    result = run_shell(nhmmscan_path, '--tblout', result_tbl, hmm_model,
                       sequence)
    return result
