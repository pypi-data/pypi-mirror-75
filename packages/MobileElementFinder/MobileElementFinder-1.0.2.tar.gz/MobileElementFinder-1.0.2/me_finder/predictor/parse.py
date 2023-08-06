"""Functions for processing alignements to MGEs to process overlapping hits."""

import logging
from typing import Dict, List, Tuple, Union

from me_finder.errors import CoordOutOfBoundsError
from me_finder.tools import BlastHit, BlastHsp, iter_blast_hits

from .types import Alignment, ElementCoordinate, ElementHit, HspBin, MgeResult

LOG = logging.getLogger(__name__)

# Type declarations
Alignments = Tuple[Alignment, ...]
HspBins = Tuple[HspBin, ...]


def _get_mge_hit(blast_hit: ElementHit) -> Dict[str, str]:
    """Parse MGE name, allele no and accession number from blast hit."""
    name, allele, accnr = blast_hit.subject_name.split('|')
    return {'name': name, 'seq_no': allele, 'accession': accnr}


def _is_contained(first: ElementCoordinate, second: ElementCoordinate) -> bool:
    """Is first element nested in second element.

    Each element consists of a list with paired start, end values.
    """
    f_start, f_end = first
    s_start, s_end = second
    return s_start <= f_start and f_end <= s_end


def _is_overlapping(first: ElementCoordinate,
                    second: ElementCoordinate,
                    allowed_overlap: int = 5) -> bool:
    """Check if first gene is overlapping second."""
    if allowed_overlap < 0:
        raise ValueError('Allowed overlap must be > 0')
    # if nested, call as overlapping
    if _is_contained(first, second):
        return True
    # check overlap
    frange = set(range(first[0], first[1]))
    srange = set(range(second[0], second[1]))
    return allowed_overlap < len(frange & srange)


def _get_element_coord(mge: ElementHit) -> ElementCoordinate:
    """Get start and end coordinates from hit."""
    if isinstance(mge, MgeResult):
        start = mge.start
        end = mge.end
    elif isinstance(mge, ElementHit):
        start = min(mge.hsps, key=lambda x: x.query_start).query_start
        end = max(mge.hsps, key=lambda x: x.query_end).query_end
    else:
        raise ValueError
    return start, end


def _calc_tot_aln_cov(group: HspBin, hit: BlastHit) -> Union[int, float]:
    """Calculate total alignement coverage of group of hsps."""
    tot_len = sum(len(hsp) for hsp in group)
    num_gaps = sum(int(hsp.num_gaps) for hsp in group)
    subject_len = int(hit.subject_len)
    return (tot_len - num_gaps) / subject_len


def _avg_seq_ident(group: HspBin, hit: BlastHit) -> float:
    """Calculate total alignement coverage of group of hsps."""
    ident_nt = sum(float(hsp.identity) * len(hsp) for hsp in group)
    return ident_nt / sum(len(hsp) for hsp in group)


def _get_possible_elem_coord(hsps: List[BlastHsp],
                             subject_length: int,
                             padding=1) -> Tuple[int, int]:
    """Get the possible start, end positions for given element.

    Possible positions while still containing given HSPs.
    Extra flexibility can be given by assigning the percentage of padding
    to be added to each coordinate.
    """
    seg_start = min(hsps, key=lambda x: x.query_start).query_start
    seg_end = max(hsps, key=lambda x: x.query_end).query_end
    hsps_len = seg_end - seg_start
    if hsps_len > subject_length:
        # sanity check
        raise CoordOutOfBoundsError(
            f'sum(HSPs len): {hsps_len} > subject len: {subject_length}')

    exp_start = int(seg_end - (subject_length * padding))
    return (
        exp_start if exp_start > 0 else 0,  # cant be less than 0
        int(seg_start + (subject_length * padding)))


def _hsp_is_overlapping_with_previous(new_hsp, previous_hsps):
    """Check if HPS is overlaping with previously added HSPs."""
    max_overlap = 10
    new_hsp_query_coord = (new_hsp.query_start, new_hsp.query_end)
    new_hsp_subject_coord = (new_hsp.subject_start, new_hsp.subject_end)
    for prev_hsp in previous_hsps:
        prev_hsp_query_coord = (prev_hsp.query_start, prev_hsp.query_end)
        prev_hsp_subject_coord = (prev_hsp.subject_start, prev_hsp.subject_end)
        # hps is overlapping with previously added hsps
        # both, location on contig and segment of MGE
        is_overlapping = any([_is_overlapping(new_hsp_query_coord, prev_hsp_query_coord, allowed_overlap=max_overlap),
                _is_overlapping(new_hsp_subject_coord, prev_hsp_subject_coord, allowed_overlap=max_overlap)])
        if is_overlapping:
            return True
    return False


def _group_hsps(hit: BlastHit) -> HspBins:
    """Group HSPs that are likely part of same MGE.

    HSP considered part of mge if its wihtin len(template mge) - len(ref hsp)
    from reference hsp.

    Eg 1
    ref mge:    >--------------<
    ref mge:            >--------------<
    ref hsp:            |xxxxxx|

    Eg 2
    ref mge:   >--------------<
    ref mge:      >--------------<
    ref hsp:      |xxxxxx| |xx|
    """

    # first step, bin hsps that likely constitute seperate MGEs of the same type
    hsps = sorted(hit.hsps, key=len)
    raw_bins = [[hsps.pop()]]
    # TODO add evalue validation of hsps
    for _ in range(len(hsps)):
        hsp = hsps.pop()
        hsp_elem_query = (hsp.query_start, hsp.query_end)
        has_been_added = False
        # try adding hsp to existing bins
        # TODO if a bin could be contained by multiple MGEs, assign it to the closest one
        for curr_bin in raw_bins:
            # check if HSP is overlapping with existing HSPs in bin
            if any(_is_overlapping(hsp_elem_query, (binned_hsp.query_start, binned_hsp.query_end)) for binned_hsp in curr_bin):
                has_been_added = True
                break

            try:
                # See if the HSP could be part of the MGE
                bin_elem = _get_possible_elem_coord(curr_bin,
                                                    hit.subject_len,
                                                    padding=1.1)
            except CoordOutOfBoundsError as err:
                LOG.debug('%s, skipping bin' % err.args[0])
                continue

            if _is_contained(hsp_elem_query, bin_elem) and not has_been_added:
                # if overlapping with putative mge length
                curr_bin.append(hsp)
                has_been_added = True

        if not has_been_added:
            # add to new bin
            raw_bins.append([hsp])

    # second step, remove repeated alignment of the same part of the MGE
    non_overlapping_bins = []
    for raw_bin in raw_bins:
        first_hsp = raw_bin[0]
        first_hsp_subject_coord = (first_hsp.subject_start, first_hsp.subject_end)
        previous_bins = [first_hsp]
        for current_hsp in raw_bin[1:]:  # add HPSs that are not aligning to the same region
            current_hsp_subject_coord = (current_hsp.subject_start, current_hsp.subject_end)
            overlapping = any(_is_overlapping(current_hsp_subject_coord,
                                              (prev_b.subject_start, prev_b.subject_end))
                              for prev_b in previous_bins)
            if not overlapping:  # hsp has overlapping subject sequence with other MGE
                previous_bins.append(current_hsp)
        # store bins who subject sequence do not overlapp
        non_overlapping_bins.append(previous_bins)
    return tuple(tuple(g) for g in non_overlapping_bins)  # to imutable


def _join_cigar(hsps: HspBin) -> str:
    """Join hsp alignment cigar strings.

    Unaligned regions are denoted with N.
    """
    # get first hsp
    prev, *rest = sorted(hsps, key=lambda x: x.query_start)
    cigar = prev.cigar
    t = []
    for h in rest:
        dist_between_hsp = h.query_start - prev.query_end - 1
        t.append(dist_between_hsp)
        cigar += f' N{dist_between_hsp} {h.cigar}'
        prev = h  # store current hsp
    return cigar


def _parse_raw_mge_alignments(blast_result: str) -> Tuple[ElementHit, ]:
    """Parse raw blast alignements to raw hits to MGEs."""
    raw_mges: List[ElementHit, ] = []
    for hit in iter_blast_hits(blast_result):  # type: BlastHit
        for el_hsps in _group_hsps(hit):
            # TODO find better way of combining e-value.
            element_start_pos = min(el_hsps, key=lambda h: h.query_start).query_start
            element_end_pos = max(el_hsps, key=lambda h: h.query_end).query_end
            # summarize hit quality metrics
            element = ElementHit(tot_aln_cov=_calc_tot_aln_cov(el_hsps, hit),
                                 avg_seq_id=_avg_seq_ident(el_hsps, hit),
                                 n_gaps=sum(h.num_gaps for h in el_hsps),
                                 n_subs=sum(h.num_subs for h in el_hsps),
                                 element_len=(element_end_pos - element_start_pos) + 1,
                                 subject_len=hit.subject_len,
                                 depth=hit.depth,
                                 query_name=hit.query_name,
                                 query_length=hit.query_len,
                                 subject_name=hit.subject_name,
                                 e_value=min(h.e_value for h in el_hsps),
                                 cigar=_join_cigar(el_hsps),
                                 hsps=el_hsps)
            raw_mges.append(element)
    return tuple(raw_mges)
