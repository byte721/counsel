"""Allegation: a single accusation against the client.

Distinct from a 'charge' in that it does not need to be formal. CT pile-ons,
court filings, leaked emails, and live testimony all qualify as allegations
that defense counsel may need to respond to.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


class AllegationSeverity(StrEnum):
    NUISANCE = "nuisance"
    MATERIAL = "material"
    SERIOUS = "serious"
    CRITICAL = "critical"


@dataclass
class Allegation:
    """A single accusation. May or may not be true. Counsel does not decide."""

    id: str
    accuser: str
    summary: str
    severity: AllegationSeverity = AllegationSeverity.MATERIAL
    source_urls: list[str] = field(default_factory=list)
    asserted_at: datetime | None = None
    notes: str = ""

    def is_critical(self) -> bool:
        return self.severity == AllegationSeverity.CRITICAL

    def is_substantive(self) -> bool:
        return self.severity in (AllegationSeverity.SERIOUS, AllegationSeverity.CRITICAL)

