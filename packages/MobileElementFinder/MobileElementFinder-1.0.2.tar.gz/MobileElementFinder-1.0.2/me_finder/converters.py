"""Convert objects between formats."""
import logging
from itertools import groupby

import numpy as np

import cattr
from Bio.Seq import Seq
from Bio.SeqFeature import FeatureLocation, SeqFeature
from Bio.SeqRecord import SeqRecord
from mgedb.db import MgeType, TransposaseRecord

from .result import PredictionEvidence

LOG = logging.getLogger(__name__)


def _annotate_depth(depth_mtrx, qual, start, end):
    """Add sequence depth of feature to qualifiers."""
    if depth_mtrx is not None:
        feature_depth = depth_mtrx[0, start:end].mean().round()
        other = qual.get('other', [])
        other.append(f'depth:{feature_depth}')
        qual['other'] = other
    return qual


def _make_sequence_feature(feature_type, seq_position, start_mod, strand_mod,
                           mge_depth):
    """Make gff feature."""
    start = int(seq_position.start)
    end = int(seq_position.end)
    qualifiers = _annotate_depth(mge_depth, {'source': 'mge_finder'}, start,
                                 end)
    return SeqFeature(FeatureLocation(seq_position.start + start_mod,
                                      seq_position.end + start_mod,
                                      seq_position.strand * strand_mod),
                      type=feature_type,
                      qualifiers=qualifiers)


def _annotate_accessory_genes(db, mge, seq_depth):
    """Annotate Mge accessory genes from MGEdb."""
    mgedb_records = db.records  # TODO reomve dependancy
    sub_features = []
    seq_no = int(mge.seq_no) - 1  # seq_no 1 indexed, make 0-indexed
    # TODO fix writing putative cn to gff
    if not mge.name in mgedb_records:
        return sub_features
    db_seq_record = mgedb_records[mge.name].sequences[seq_no]
    # correct cds strand if mge was found on oposite strand in sample
    # if found on strand -1 and annotated as 1, invert cds strand
    if mge.coverage == 1:
        if db_seq_record.irl is not None:
            if any([
                    v is not None
                    for v in cattr.unstructure(db_seq_record.irl).values()
            ]):
                # store irl
                sub_features.append(
                    _make_sequence_feature('irl', db_seq_record.irl,
                                           mge.start - 1, mge.strand,
                                           seq_depth))

        for cds in db_seq_record.cds:
            # select gene name
            if isinstance(cds, TransposaseRecord) or cds.gene is None:
                cds_name = cds.product
            else:
                cds_name = cds.gene

            cds_start, cds_end = sorted([cds.start, cds.end])
            sub_qualifiers = {
                'source': 'mge_finder',
                'name': cds_name}
            sub_qualifiers = _annotate_depth(seq_depth, sub_qualifiers,
                                             cds_start, cds_end)

            # make feature
            feature = SeqFeature(FeatureLocation(mge.start + cds_start,
                                                 mge.start + cds_end,
                                                 cds.strand * mge.strand),
                                 type='gene',
                                 qualifiers=sub_qualifiers)

            sub_features.append(feature)

        if db_seq_record.irr is not None:
            if any([
                    v is not None
                    for v in cattr.unstructure(db_seq_record.irr).values()
            ]):
                # store irr feature
                sub_features.append(
                    _make_sequence_feature('irr', db_seq_record.irr,
                                           mge.start - 1, mge.strand,
                                           seq_depth))
    return sub_features


def convert_to_biopython(db, results, depth):
    """Convert prediction results to biopython objects.

    For writing results to GFF format.
    """
    LOG.debug('convert prediction results to biopython object')
    mge_idx = 1
    depth = dict(depth) if depth is not None else None
    for contig_name, mges in groupby(results, key=lambda c: c.contig):
        seq = Seq('')
        record = SeqRecord(seq, id=contig_name)
        mge_features = []
        for mge in mges:
            # assign index for parent
            mge_id = f'MGE{mge_idx}'
            mge_idx += 1
            other_qual = []

            # get coverage matrix mobile element
            # TODO estimate coverage of composite transposon
            # TODO simplify
            name = f'{mge.name}|{mge.mge_id}'
            if depth is not None:
                if name in depth:
                    seq_depth = np.sum(depth[name], axis=1,
                                       dtype=np.uint16).flatten()
                    other_qual.append(f'depth:{seq_depth.mean().round(2)}')
                else:
                    seq_depth = None
            else:
                seq_depth = None

            # make mge as top element
            top_qualifiers = {
                'source': 'mge_finder',
                'ID': mge_id,
                'Name': mge.name,
                'Alias': mge.alias[0] if len(mge.alias) > 0 else None,
                'Gap': mge.cigar,
                'other': other_qual,
            }
            top_feature = SeqFeature(
                FeatureLocation(
                    start=mge.start - 1,  # exact start
                    end=mge.end,
                    strand=mge.strand),
                type=mge.type.name.lower(),
                qualifiers=top_qualifiers)
            # make annotated cds as sub-elements
            # annoate all elements that are not putative composite transposons
            if not (mge.type == MgeType.COMPOSITE_TRANSPOSON
                    and mge.evidence == PredictionEvidence.PUTATIVE):
                sub_features = _annotate_accessory_genes(db, mge, seq_depth)
            else:
                sub_features = []
            top_feature.sub_features = sub_features
            mge_features.append(top_feature)
        # store features in records
        record.features = mge_features
        yield record
