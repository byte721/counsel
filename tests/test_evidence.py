"""Tests for evidence index."""
from __future__ import annotations

from counsel.evidence.index import DefenseEvidence, EvidenceIndex, EvidenceRole


def test_index_starts_empty():
    idx = EvidenceIndex()
    assert len(idx) == 0
    assert idx.total_weight() == 0


def test_index_filter_by_role():
    idx = EvidenceIndex()
    idx.add(DefenseEvidence(id="e1", role=EvidenceRole.EXCULPATORY, summary="a"))
    idx.add(DefenseEvidence(id="e2", role=EvidenceRole.MITIGATING, summary="b"))
    idx.add(DefenseEvidence(id="e3", role=EvidenceRole.EXCULPATORY, summary="c"))
    assert len(idx.by_role(EvidenceRole.EXCULPATORY)) == 2
    assert len(idx.by_role(EvidenceRole.MITIGATING)) == 1


def test_index_total_weight():
    idx = EvidenceIndex()
    idx.add(DefenseEvidence(id="e1", role=EvidenceRole.EXCULPATORY, summary="a", weight=1.5))
    idx.add(DefenseEvidence(id="e2", role=EvidenceRole.MITIGATING, summary="b", weight=2.0))
    assert idx.total_weight() == 3.5
