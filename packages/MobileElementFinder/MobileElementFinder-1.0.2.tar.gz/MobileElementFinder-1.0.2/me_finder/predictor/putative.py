"""Infer putative composite transposons from prior MGE predictions."""
import logging
from collections import defaultdict
from itertools import chain, groupby
from typing import List, Tuple

import attr
from me_finder.context import ExecutionContext
from me_finder.io import ContigSequences
from mgedb import MGEdb, Sequence, Sequences
from mgedb.db import MgeType
from mypy_extensions import TypedDict

from .parse import _get_element_coord, _get_mge_hit, _is_overlapping
from .types import (ElementHit, MgeFinderResult, MgeResult, PredictionEvidence,
                    TemplateSequence)

LOG = logging.getLogger(__name__)


def _get_putative_cn_element(*elements):
    """Get metrics for putative composite transposon element."""
    first_start = min(min(map(_get_element_coord, elements)))
    second_end = max(max(map(_get_element_coord, elements)))
    return second_end - first_start + 1


def _remove_overlapping_raw_mges(raw_mges, valid_mges):
    """Remove overlapping raw mges."""
    for r in raw_mges:
        r_start = min(r.hsps, key=lambda m: m.query_start).query_start
        r_end = min(r.hsps, key=lambda m: m.query_end).query_end
        if not any(_is_overlapping((r_start, r_end), (m.start, m.end)) for m in valid_mges):
            yield r


def _has_preserved_ir(mge_hit, cfg):
    """Check if MGE has preserved IR."""
    trunc_5p = mge_hit.truncation_level()['trunc_5p']
    trunc_3p = mge_hit.truncation_level()['trunc_3p']

    # read threshold from configs
    min_hsp_len = cfg.getint('putative_composite_transposon', 'min_ir_segment_length')
    min_aln_len = cfg.getint('putative_composite_transposon', 'min_ir_aln_length')
    preserved_irl = not any([min_aln_len < trunc_5p,  # check if irl is preserved
                             len(mge_hit.hsps[0]) < min_hsp_len])  # assert lenght of hsp
    preserved_irr = not any([min_aln_len < trunc_3p,  # check if irr is preserved
                             len(mge_hit.hsps[-1]) < min_hsp_len])  # assert lenght of hsp
    return any([preserved_irl, preserved_irr])


def _is_type(mge: ElementHit, mge_type: MgeType, db: MGEdb):
    """Check if MGE is of TYPE."""
    mge_name = _get_mge_hit(mge)['name']
    return db.records[mge_name].type == mge_type


def compose_cn_mge_id(mge_cnt, *is_elements):
    """Build mge_id for composite transposons."""
    full_is = sorted((e for e in is_elements if isinstance(e, MgeResult)),
                     key=lambda m: m.mge_id)
    if len(full_is) == 2:
        first_is, second_is = full_is
        return f'{mge_cnt}_{first_is.mge_id}_{second_is.mge_id}'
    return f'{mge_cnt}_{full_is[0].mge_id}'


def _predict_putative_composite_tn(
        ctx: ExecutionContext,
        mges: MgeFinderResult,
        raw_mges: List[ElementHit, ],
        contigs: ContigSequences,
) -> Tuple[MgeFinderResult, Sequences]:
    """Infer putative composite transposons from prediction result.

    Composite transposon is defined by two insertion sequences that are less than
    THRESHOLD - len(insertion sequence) nucleotide aparat. The threshold is defined in the config file.

    List of MgeRecords file.
    """
    LOG.info('predicting putative composite transposons')
    cfg = ctx.config
    # get raw elements that are insertion sequences and has preserev IR
    # to reduce the number of hits to bin and iterate over
    is_w_ir_per_contig = defaultdict(lambda: defaultdict(list))
    for raw_mge in raw_mges:
        mge_name = raw_mge.subject_name.split('|')[0]
        if all((_has_preserved_ir(raw_mge, cfg), _is_type(raw_mge, MgeType.INSERTION_SEQUENCE, ctx.mge_db))):
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
        COMPTN_CONTIG = 'NODE_1_length_715644_cov_13.257236'
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
                        if element_len < cfg.getint('putative_composite_transposon', 'max_len'):
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
                        if element_len < cfg.getint('putative_composite_transposon', 'max_len'):
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
