"""Functions for detecting MGEs from sequence alignments."""
import logging
import math
from configparser import ConfigParser
from itertools import groupby
from typing import Iterator, List, Tuple

import attr
from me_finder.context import ExecutionContext
from me_finder.io import ContigSequences
from mgedb import Sequence, Sequences

from .parse import (Alignments, _get_element_coord, _get_mge_hit,
                    _is_overlapping)
from .types import (Alignment, ElementCoordinate, ElementHit, MgeFinderResult,
                    MgeResult, PredictionEvidence, TemplateSequence)

LOG = logging.getLogger(__name__)


def _is_valid_hit(hit: ElementHit, cfg: ConfigParser) -> bool:
    """Validate good hits."""
    if hit.tot_aln_cov < cfg.getfloat('validation', 'coverage'):
        return False

    # combined hsp len is larger than reference seqeunce
    if (hit.subject_len * 1.05) < hit.element_len:
        return False

    # if no hit is significant
    if not any(h.e_value == 0 for h in hit.hsps):
        evals = (math.log10(h.e_value) for h in hit.hsps)
        if max(evals) > cfg.getfloat('validation', 'e_value'):
            return False

    # if hit.avg_seq_id < cfg.getfloat('validation', 'identity'):
    #     return False

    return True


def _get_alignment_coords_elem(mge: ElementHit) -> ElementCoordinate:
    """Get start and end coordinates from hit."""
    if isinstance(mge, MgeResult):
        return mge.start, mge.end
    elif isinstance(mge, ElementHit):
        start = min(mge.hsps, key=lambda x: x.query_start).query_start
        end = max(mge.hsps, key=lambda x: x.query_end).query_end
        return start, end
    else:
        raise ValueError


def _bin_hits(hits: Iterator[ElementHit]):
    """Bin hits based on their corrdinates.

    First hit is considered as representative of a bin.
    Other hits are binned if it is contained in representative,
    If their start or end is within DISTANCE % distance from ref start and end.
    """
    bins = [[next(hits)]]
    for hit in hits:
        elem_coord = _get_element_coord(hit)
        bin_idx = None
        for idx, curr_bin in enumerate(bins):
            reprs = curr_bin[0]  # get element representative for group
            # Get approximate start and end positions
            padded_pos = _pad_mge_coord(reprs, 0)
            if _is_overlapping(elem_coord, padded_pos):
                bin_idx = idx
                break
        if bin_idx is not None:
            bins[bin_idx].append(hit)
        else:
            bins.append([hit])
        bin_idx = None
    return bins


def _pad_mge_coord(elem: ElementHit, padding: float) -> Tuple[int, int]:
    """Get range around element padded with X%."""
    start, end = _get_element_coord(elem)
    length = (end - start) * padding
    nstart = start - (length / 2) if start - (length / 2) >= 0 else 0
    return round(nstart), round(end + (length / 2))


def _detect_mges(ctx: ExecutionContext, raw_mges, contigs: ContigSequences) -> Tuple[MgeFinderResult, Sequences, Alignments]:
    """Find valid mobile element from blast reult and annotate output.

    HSPs for each hit is combined and the total alignment is summarized. The quality of the total
    alignment is evaluated were only valid hits are kept.

    Returns a tuple with [prediction resultr, sequence, alignments]

    """
    LOG.info('detecting MGEs')
    cfg = ctx.config  # read config
    # get mge records
    valid_mges = (mge for mge in raw_mges if _is_valid_hit(mge, cfg))
    mge_records = ctx.mge_db.records  # read records to memeory

    mge_sequences: List[Sequence] = []
    mge_headers = []  # store fasta headers of selected seqs
    mges: List[MgeResult] = []
    alignments: List[Alignment] = []
    mge_indexer = 1
    for _, hits in groupby(valid_mges, key=lambda x: x.query_name):
        for hit_bin in _bin_hits(hits):
            best_hit = max(hit_bin,
                           key=lambda h:
                           (h.tot_aln_cov, h.avg_seq_id, h.subject_len))
            header_info = _get_mge_hit(best_hit)
            entry = mge_records[header_info['name']]

            start, end = _get_element_coord(best_hit)
            mge_seq = contigs.sub_sequence(start - 1, end, 1,
                                           best_hit.query_name)

            # store fasta header
            header = '|'.join([
                header_info['name'], header_info['seq_no'],
                header_info['accession']
            ])
            mge_headers.append(header)
            # add header to sequence
            mge_seq = attr.evolve(mge_seq, title=header)

            # Prevent that duplicated sequences are added
            # TODO clean up
            if mge_seq in mge_sequences:
                # store id of previously stored sequence
                mge_id = int(mge_sequences[mge_seq].title.split('|')[1])
            else:
                header = f'{header_info["name"]}|{mge_indexer}'
                mge_id = mge_indexer
                # if header in (s.title for s in mge_sequences):
                #     pass
                mge_sequences.append(Sequence(title=header,
                                                  seq=mge_seq.seq))
            template = entry.sequences[int(header_info['seq_no']) - 1]

            template = TemplateSequence(accession=template.accession,
                                        start=template.start,
                                        end=template.end)
            truncation_level = best_hit.truncation_level()
            # make entry
            mges.append(
                MgeResult(
                    mge_id=str(mge_id),
                    name=entry.name,
                    synonyms=entry.synonyms,
                    family=entry.family,
                    group=entry.group,
                    type=entry.type,
                    reference_link=entry.link,
                    evidence=PredictionEvidence.PREDICTED,
                    template=template,
                    reference=entry.references,
                    alias=entry.synonyms,
                    seq_no=int(header_info['seq_no']),
                    trunc_5p=truncation_level['trunc_5p'],
                    trunc_3p=truncation_level['trunc_3p'],
                    start=start,
                    end=end,
                    strand=best_hit.hsps[0].hit_strand,
                    contig=best_hit.query_name,
                    contig_length=best_hit.query_length,
                    identity=best_hit.avg_seq_id,
                    coverage=best_hit.tot_aln_cov,
                    depth=best_hit.depth,
                    e_value=best_hit.e_value,
                    gaps=best_hit.n_gaps,
                    substitutions=best_hit.n_subs,
                    allele_seq_length=len(mge_seq),
                    template_length=best_hit.subject_len,
                    num_hsps=len(best_hit.hsps),
                    carried_motifs=[],
                    cigar=best_hit.cigar))
            for hsp_no, hsp in enumerate(best_hit.hsps, start=1):
                alignments.append(
                    Alignment(name=entry.name,
                              mge_id=str(mge_id),
                              hsp_no=hsp_no,
                              subject_start=hsp.subject_start,
                              subject_end=hsp.subject_end,
                              query_seq=hsp.query_seq,
                              midline=hsp.midline,
                              subject_seq=hsp.subject_seq))
            mge_indexer += 1
    # TODO simplify this function
    return tuple(mges), tuple(mge_sequences), tuple(alignments)
