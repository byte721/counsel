"""DefenseTheory: the strategic frame that organizes the defense.

A theory is the one-line answer to 'what is your case.' Every piece of
evidence and every counter-argument should serve the theory. If a piece of
evidence doesn't serve it, we drop the evidence, not the theory.

Distinct from a "verdict": a theory is what we are arguing. A verdict is
what someone else decides. Counsel only does the former.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class TheoryArchetype(StrEnum):
    """The shape of a defense, not the content."""

    DENIAL = "denial"
    REFRAMING = "reframing"
    JUSTIFICATION = "justification"
    PROCEDURAL = "procedural"
    AFFIRMATIVE = "affirmative"
    MITIGATION = "mitigation"


@dataclass
class DefenseTheory:
    """The unifying frame of a defense."""

    headline: str
    archetype: TheoryArchetype
    key_claims: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)

    def render_one_line(self) -> str:
        return f"[{self.archetype.value}] {self.headline}"


