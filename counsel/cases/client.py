"""Client: the party Counsel has been retained to defend.

Counsel does not pick clients. The user picks. Counsel builds the best defense
the public record will support, regardless of merit.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from counsel.cases.allegation import Allegation


@dataclass
class Client:
    """A defendant Counsel has been retained to defend."""

    handle: str
    legal_name: str | None = None
    role: str = ""
    public_corpus_id: str | None = None
    allegations: list[Allegation] = field(default_factory=list)
    notes: str = ""

    @property
    def has_critical_allegations(self) -> bool:
        return any(a.is_critical() for a in self.allegations)

    def serious_count(self) -> int:
        return sum(1 for a in self.allegations if a.is_substantive())

