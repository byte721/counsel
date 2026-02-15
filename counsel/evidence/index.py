"""EvidenceIndex: stores exculpatory and mitigating evidence for a client.

Distinct from a generic evidence store: items here are tagged with how they
SERVE the defense (exculpatory, mitigating, impeaching, foundational).
Evidence that doesn't serve the defense is simply not indexed here. Counsel
does not store inculpatory evidence against its own client.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class EvidenceRole(StrEnum):
    """How a piece of evidence serves the defense."""

    EXCULPATORY = "exculpatory"
    MITIGATING = "mitigating"
    IMPEACHING = "impeaching"
    FOUNDATIONAL = "foundational"


@dataclass
class DefenseEvidence:
    """One piece of evidence Counsel intends to use."""

    id: str
    role: EvidenceRole
    summary: str
    source_url: str | None = None
    cited_at: datetime | None = None
    weight: float = 1.0
    rebuttal_anticipated: str = ""


class EvidenceIndex:
    """Index of evidence supporting one client's defense."""

    def __init__(self) -> None:
        self._items: list[DefenseEvidence] = []

    def add(self, item: DefenseEvidence) -> None:
        self._items.append(item)

    @property
    def items(self) -> list[DefenseEvidence]:
        return list(self._items)

    def by_role(self, role: EvidenceRole) -> list[DefenseEvidence]:
        return [item for item in self._items if item.role == role]

    def total_weight(self) -> float:
        return sum(item.weight for item in self._items)

    def __len__(self) -> int:
        return len(self._items)




