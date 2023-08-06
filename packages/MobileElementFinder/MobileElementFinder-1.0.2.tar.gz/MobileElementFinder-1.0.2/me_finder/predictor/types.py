"""Stores shared type definition and data containers."""
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple

import attr
import numpy as np
from me_finder.tools import BlastHsp
from mgedb.db import MgeType


class PredictionEvidence(Enum):
    """Prediction evidence."""

    PREDICTED = auto()
    PUTATIVE = auto()


class MotifType(Enum):
    """Prediction evidence."""

    REPEAT = 'repeat'
    GENE = 'gene'


@attr.s(auto_attribs=True, frozen=True, slots=True)
class Motif:
    """Storage of coding sequence."""

    gene: str
    product: str
    start: int
    end: int
    strand: int
    coverage: float
    identity: float
    type: MotifType


@attr.s(auto_attribs=True, frozen=True, slots=True)
class TemplateSequence:
    """Alignment container."""
    accession: str
    start: List[int]
    end: List[int]


@attr.s(auto_attribs=True, frozen=True, slots=True)
class Alignment:
    """Alignment container."""
    name: str
    mge_id: str
    hsp_no: int
    query_seq: str
    subject_seq: str
    subject_start: int
    subject_end: int
    midline: str


@attr.s(auto_attribs=True, frozen=True, slots=True)
class MgeResult:
    """Container of annotated results."""

    name: str
    mge_id: str
    synonyms: List[str]
    family: str
    group: Optional[str]
    reference_link: List[Dict[str, str]]
    type: MgeType
    alias: Optional[List[str]]
    evidence: PredictionEvidence
    seq_no: int
    start: int
    end: int
    trunc_5p: int
    trunc_3p: int
    strand: int
    contig: str
    contig_length: int
    identity: float
    coverage: float
    gaps: int
    substitutions: int
    allele_seq_length: int
    template_length: int
    depth: np.array
    e_value: float
    template: TemplateSequence  # template sequence
    reference: List[str]
    num_hsps: int
    cigar: str
    carried_motifs: List[Motif]


@attr.s(auto_attribs=True, frozen=True, slots=True)
class ElementHit:
    """Contians blast hit."""

    query_name: str
    query_length: int
    subject_name: str
    tot_aln_cov: float
    avg_seq_id: float
    n_gaps: int
    n_subs: int
    element_len: int
    subject_len: int
    depth: Optional[float]
    e_value: float
    cigar: str
    hsps: Tuple[BlastHsp, ...]

    def truncation_level(self):
        """Calculate the level of truncation compared to the template sequence."""
        if len(self.hsps) > 1:  # if multiple hsps
            first_hit, *_, last_hit = sorted(self.hsps, key=lambda x: x.subject_start)
        else:
            first_hit = self.hsps[0]
            last_hit = self.hsps[0]
        # calcualte
        trunc_5p = first_hit.subject_start
        trunc_3p = self.subject_len - last_hit.subject_end
        return {'trunc_5p': trunc_5p, 'trunc_3p': trunc_3p}


# Type definitions
MgeFinderResult = Tuple[MgeResult, ...]
ElementCoordinate = Tuple[int, int]
HspBin = Tuple[BlastHsp, ...]
