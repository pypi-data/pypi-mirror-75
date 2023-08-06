"""Expose public functions for predicting MGEs to MobileElementFinder. """
from me_finder.context import ExecutionContext
from mgedb import Sequences

from .detect import _detect_mges
from .parse import Alignments, _parse_raw_mge_alignments
from .putative import _predict_putative_composite_tn
from .types import MgeFinderResult


def predict_mges(ctx: ExecutionContext, blast_result_path: str, contig_seq):
    """Predict MGEs and putative mobile elements."""
    # Detect MGEs with good alignment and infer putative mges
    raw_mge_alignments = _parse_raw_mge_alignments(blast_result_path)
    detected_mges, detected_seqs, detected_alns = _detect_mges(
        ctx, raw_mge_alignments, contig_seq)  # type: (MgeFinderResult, Sequences, Alignments)
    put_ctn, put_ctn_seqs = _predict_putative_composite_tn(ctx, detected_mges,
                                                          raw_mge_alignments,
                                                          contig_seq)  # type: (MgeFinderResult, Sequences)
    # return concatinated results
    return detected_mges + put_ctn, detected_seqs + put_ctn_seqs, detected_alns
