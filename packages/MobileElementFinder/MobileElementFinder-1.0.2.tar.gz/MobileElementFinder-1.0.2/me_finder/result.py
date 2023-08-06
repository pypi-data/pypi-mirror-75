"""Type definitions and data containers for results."""
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple

import attr
import numpy as np
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


# Type definitions
MgeFinderResult = Tuple[MgeResult, ...]
