"""Functions for finding and validating MGEs. """
import logging
import math
from collections import defaultdict
from configparser import ConfigParser
from itertools import chain, groupby
from typing import Dict, Iterator, List, Optional, Tuple, Union

import attr
from mgedb import MGEdb, Sequence, Sequences
from mgedb.db import MgeType
from mypy_extensions import TypedDict

from .context import ExecutionContext
from .errors import CoordOutOfBoundsError
from .io import ContigSequences
from .result import (Alignment, MgeFinderResult, MgeResult, PredictionEvidence,
                     TemplateSequence)
from .tools import BlastHit, BlastHsp, iter_blast_hits

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


def _calc_tot_aln_cov(group: HspBin, hit: BlastHit) -> Union[int, float]:
    """Calculate total alignement coverage of group of hsps."""
    tot_len = sum(_hsp_len(hsp) for hsp in group)
    num_gaps = sum(int(hsp.num_gaps) for hsp in group)
    subject_len = int(hit.subject_len)
    return (tot_len - num_gaps) / subject_len


def _avg_seq_ident(group: HspBin, hit: BlastHit) -> float:
    """Calculate total alignement coverage of group of hsps."""
    ident_nt = sum(float(hsp.identity) * _hsp_len(hsp) for hsp in group)
    return ident_nt / sum(_hsp_len(hsp) for hsp in group)


def _hsp_len(hsp: BlastHsp) -> int:
    """Get hsp length."""
    r_start, r_end = sorted([hsp.query_end, hsp.query_start])
    return r_end - r_start + 1


def _get_element_coord(mge: ElementHit) -> ElementCoordinate:
    """Get start and end coordinates from hit."""
    if isinstance(mge, MgeResult):
        return mge.start, mge.end
    elif isinstance(mge, ElementHit):
        start = min(mge.hsps, key=lambda x: x.query_start).query_start
        end = max(mge.hsps, key=lambda x: x.query_end).query_end
        return start, end
    else:
        raise ValueError


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


def _group_hsps(hit: BlastHit) -> HspBinS:
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

    hsps = [h for h in hit.hsps]
    ref_hsp_idx = hsps.index(max(hsps, key=_hsp_len))
    bins = [[hsps.pop(ref_hsp_idx)]]
    # TODO add evalue validation of hsps
    for _ in range(len(hsps)):
        hsp = hsps.pop()
        h_elem = (hsp.query_start, hsp.query_end)
        has_been_added = False
        # try adding hsp to existing bins
        for curr_bin in bins:
            if any(
                    _is_contained(h_elem, (b.query_start, b.query_end))
                    for b in curr_bin):
                has_been_added = True
                break

            try:
                bin_elem = _get_possible_elem_coord(curr_bin,
                                                    hit.subject_len,
                                                    padding=1.1)
            except CoordOutOfBoundsError as err:
                LOG.debug('%s, skipping bin' % err.args[0])
                continue

            if _is_contained(h_elem, bin_elem) and not has_been_added:
                # if overlapping with putative mge length
                curr_bin.append(hsp)
                has_been_added = True

        if not has_been_added:
            # add to new bin
            bins.append([hsp])

    # TODO check for overlaping subject sequences
    return tuple(tuple(g) for g in bins)  # to imutable


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


def _pad_mge_coord(elem: ElementHit, padding: float) -> Tuple[int, int]:
    """Get range around element padded with X%."""
    start, end = _get_element_coord(elem)
    length = (end - start) * padding
    nstart = start - (length / 2) if start - (length / 2) >= 0 else 0
    return round(nstart), round(end + (length / 2))


def _get_mge_hit(blast_hit: ElementHit) -> Dict[str, str]:
    """Parse MGE name, allele no and accession number from blast hit."""
    name, allele, accnr = blast_hit.subject_name.split('|')
    return {'name': name, 'seq_no': allele, 'accession': accnr}


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


def _has_preserved_ir(mge_hit, db):
    """Check if MGE has preserved IR."""
    if len(mge_hit.hsps) > 1:
        first_hit, *_, last_hit =  sorted(mge_hit.hsps, key=lambda x: x.subject_start)
    else:
        first_hit = mge_hit.hsps[0]
        last_hit = mge_hit.hsps[0]

    min_segment_length = 60
    min_ir_aln_length = 20
    # get expected MGE length from MGEdb
    mge_info = _get_mge_hit(mge_hit)
    expected_len = len(db.records[mge_info['name']].sequences[int(mge_info['seq_no']) - 1])
    preserved_irl = not any([min_ir_aln_length < first_hit.subject_start,  # check if irl is preserved
                             len(first_hit) < min_segment_length])  # assert lenght of hsp
    preserved_irr = not any([min_ir_aln_length < (expected_len - last_hit.subject_end),  # check if irr is preserved
                             len(last_hit) < min_segment_length])  # assert lenght of hsp
    return any([preserved_irl, preserved_irr])


def _is_type(mge: ElementHit, mge_type: MgeType, db: MGEdb):
    """Check if MGE is of TYPE."""
    mge_name = _get_mge_hit(mge)['name']
    return db.records[mge_name].type == mge_type


def _identify_mges(ctx: ExecutionContext, raw_mges,
                   contigs: ContigSequences,
                   db: MGEdb) -> Tuple[MgeFinderResult, Sequences, Alignments]:
    """Find valid mobile element from blast reult and annotate output.

    HSPs for each hit is combined and the total alignment is summarized. The quality of the total
    alignment is evaluated were only valid hits are kept.

    Returns a tuple with [prediction resultr, sequence, alignments]

    """
    cfg = ctx.config  # read config
    # get mge records
    valid_mges = (mge for mge in raw_mges if _is_valid_hit(mge, cfg))
    mge_records = db.records  # read records to memeory

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


def compose_cn_mge_id(mge_cnt, *is_elements):
    """Build mge_id for composite transposons."""
    full_is = sorted((e for e in is_elements if isinstance(e, MgeResult)),
                     key=lambda m: m.mge_id)
    if len(full_is) == 2:
        first_is, second_is = full_is
        return f'{mge_cnt}_{first_is.mge_id}_{second_is.mge_id}'
    return f'{mge_cnt}_{full_is[0].mge_id}'


def _remove_overlapping_raw_mges(raw_mges, valid_mges):
    """Remove overlapping raw mges."""
    for r in raw_mges:
        r_start = min(r.hsps, key=lambda m: m.query_start).query_start
        r_end = min(r.hsps, key=lambda m: m.query_end).query_end
        if not any(_is_overlapping((r_start, r_end), (m.start, m.end)) for m in valid_mges):
            yield r


def _get_putative_cn_element(*elements):
    """Get metrics for putative composite transposon element."""
    first_start = min(min(map(_get_element_coord, elements)))
    second_end = max(max(map(_get_element_coord, elements)))
    return second_end - first_start + 1


def _infer_putative_composite_tn(
        ctx: ExecutionContext,
        mges: MgeFinderResult,
        raw_mges: List[ElementHit, ],
        contigs: ContigSequences,
        db: MGEdb,
) -> Tuple[MgeFinderResult, Sequences]:
    """Infer putative composite transposons from prediction result.

    Composite transposon is defined by two insertion sequences that are less than
    THRESHOLD - len(insertion sequence) nucleotide aparat. The threshold is defined in the config file.

    List of MgeRecords file.
    """
    cfg = ctx.config
    # get raw elements that are insertion sequences and has preserev IR
    # to reduce the number of hits to bin and iterate over
    is_w_ir_per_contig = defaultdict(lambda: defaultdict(list))
    for raw_mge in raw_mges:
        mge_name = raw_mge.subject_name.split('|')[0]
        if all((_has_preserved_ir(raw_mge, db), _is_type(raw_mge, MgeType.INSERTION_SEQUENCE, db))):
            is_w_ir_per_contig[raw_mge.query_name][mge_name].append(raw_mge)

    RawEntry = TypedDict(
        'RawEntry', {
            'mge_id': int,
            'length': int,
            '5p_flank': MgeResult,
            '3p_flank': MgeResult,
            'contig': str,
            'sequence': None,
        })
    raw_ctn = defaultdict(list)
    # find potential composite transposon
    for contig, mges_on_contig in groupby(mges, key=lambda x: x.contig):
        for _, identical_mges in groupby(mges_on_contig, key=lambda x: x.name):
            gr_mges: List[MgeResult] = list(identical_mges)  # allow for repeated iteration
            mge_id = int(max(gr_mges, key=lambda x: int(x.mge_id)).mge_id) + 1
            for mge_name, valid_mges in groupby(gr_mges, key=lambda m: m.name):
                valid_ins_seq = sorted(valid_mges, key=lambda x: x.start)
                # skip mges that are not insertion sequences
                if valid_ins_seq[0].type != MgeType.INSERTION_SEQUENCE:
                    continue
                # get relevant raw mges and remove elements that are overlapping with valid mges
                non_overlapping_is = _remove_overlapping_raw_mges(
                    is_w_ir_per_contig[contig][mge_name],
                    valid_ins_seq)
                merged_ins_seq = sorted(chain(valid_ins_seq, non_overlapping_is),
                                        key=lambda m: m.start if isinstance(m, MgeResult) else min(m.hsps, key=lambda h: h.query_start).query_start)
                # find IS segments that are within the range for being
                # predicted as a composite transposon
                for i in range(len(merged_ins_seq)):
                    reference_element = merged_ins_seq[i]
                    if not isinstance(reference_element, MgeResult):
                        continue
                    # look for mge within threshold length downstream of reference element
                    if i - 1 >= 0:
                        first_element = merged_ins_seq[i - 1]
                        element_len = _get_putative_cn_element(reference_element, first_element)
                        if element_len < cfg.getint('composite_transposon', 'max_len'):
                            # composite transposon
                            comptn_entry: RawEntry = {'mge_id': compose_cn_mge_id(mge_id, first_element, reference_element),
                                                      'length': element_len,
                                                      '5p_flank': first_element,
                                                      '3p_flank': reference_element,
                                                      'contig': contig,
                                                      'sequence': None}
                            raw_ctn[contig].append(comptn_entry)
                            mge_id += 1
                    # look for mge within threshold length upstream of reference element
                    if i != len(merged_ins_seq) - 1:  # skip if last element
                        second_element = merged_ins_seq[i + 1]
                        # if another full MGE is located upstream of the reference MGE skip it
                        # when predicting composite transposons as it will generate duplicate
                        # predictions.
                        if isinstance(second_element, MgeResult):
                            continue
                        element_len = _get_putative_cn_element(reference_element, merged_ins_seq[i + 1])
                        if element_len < cfg.getint('composite_transposon', 'max_len'):
                            # composite transposon
                            comptn_entry: RawEntry = {'mge_id': compose_cn_mge_id(mge_id, reference_element, second_element),
                                                      'length': element_len,
                                                      '5p_flank': reference_element,
                                                      '3p_flank': second_element,
                                                      'contig': contig,
                                                      'sequence': None}
                            raw_ctn[contig].append(comptn_entry)
                            mge_id += 1

    putative_ctn = []
    ctn_sequences = set()
    # annotate with sequence and create MgeMges object
    if raw_ctn:
        for fa in contigs:  # type: Sequence
            contig_name: str = fa.title
            for entry in raw_ctn.get(contig_name, []):
                start: int = _get_element_coord(entry['5p_flank'])[0] - 1
                end: int = _get_element_coord(entry['3p_flank'])[1]
                sequence = fa.seq[start:end]
                entry['sequence'] = sequence  # get sequence from contig
                full_is = entry['5p_flank'] if isinstance(entry['5p_flank'], MgeResult) else entry['3p_flank']
                cn_name = f'cn_{entry["length"]}_{full_is.name}'
                mge_id = entry['mge_id']
                header = f'{cn_name}|{mge_id}'
                ctn_sequences.add(Sequence(title=header, seq=sequence))
                # make new mge entry with putative composite transposon
                putative_ctn.append(
                    attr.evolve(full_is,
                                mge_id=mge_id,
                                name=cn_name,
                                synonyms=[],
                                type=MgeType.COMPOSITE_TRANSPOSON,
                                evidence=PredictionEvidence.PUTATIVE,
                                reference=[],
                                alias=[],
                                start=start,
                                end=end,
                                allele_seq_length=entry['length'],
                                template_length=None,
                                carried_motifs=[],
                                cigar=None))
    return tuple(putative_ctn), tuple(ctn_sequences)


def predict_mges(ctx: ExecutionContext, blast_result: str,
                 contigs: ContigSequences,
                 db: MGEdb) -> Tuple[MgeFinderResult, Sequences, ALIGNMENTS]:
    """Predict mges with annotated sequence depth."""
    # Group MGEs and format them
    raw_mges: List[ElementHit, ] = []
    for hit in iter_blast_hits(blast_result):  # type: BlastHit
        for el_hsps in _group_hsps(hit):
            # TODO find better way of combining e-value.
            # summarize hit quality metrics
            element = ElementHit(tot_aln_cov=_calc_tot_aln_cov(el_hsps, hit),
                                 avg_seq_id=_avg_seq_ident(el_hsps, hit),
                                 n_gaps=sum(h.num_gaps for h in el_hsps),
                                 n_subs=sum(h.num_subs for h in el_hsps),
                                 element_len=sum(_hsp_len(g) for g in el_hsps),
                                 subject_len=hit.subject_len,
                                 depth=hit.depth,
                                 query_name=hit.query_name,
                                 query_length=hit.query_len,
                                 subject_name=hit.subject_name,
                                 e_value=min(h.e_value for h in el_hsps),
                                 cigar=_join_cigar(el_hsps),
                                 hsps=el_hsps)
            raw_mges.append(element)

    # predict mges
    mges, mge_sequences, alignments = _identify_mges(
        ctx, raw_mges, contigs,
        db)  # type: (MgeFinderResult, Sequences, ALIGNMENTS)
    put_ctn, ctn_sequences = _infer_putative_composite_tn(
        ctx, mges, raw_mges, contigs, db)  # type: (MgeFinderResult, Sequences)
    return mges + put_ctn, mge_sequences + ctn_sequences, alignments
