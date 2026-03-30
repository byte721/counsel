"""DefenseBrief: the written defense Counsel produces.

A brief is structured. There is a theory at the top, factual recitation, a
section per allegation responding to it on the theory's terms, and a closing.
Counsel does not produce verdicts. Counsel produces briefs.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from counsel.framing.theory import DefenseTheory


@dataclass
class AllegationResponse:
    """Counsel's response to one allegation."""

    allegation_id: str
    response_text: str
    cited_evidence_ids: list[str] = field(default_factory=list)


@dataclass
class DefenseBrief:
    """The complete written defense."""

    client_handle: str
    theory: DefenseTheory
    factual_recitation: str
    responses: list[AllegationResponse]
    closing: str
    drafted_at: datetime = field(default_factory=datetime.utcnow)

    def render(self) -> str:
        """Format the brief as a structured plain-text document."""
        lines: list[str] = []
        lines.append(f"DEFENSE BRIEF FOR {self.client_handle}")
        lines.append(f"Drafted: {self.drafted_at.isoformat()}")
        lines.append("")
        lines.append("THEORY OF THE DEFENSE:")
        lines.append(self.theory.render_one_line())
        if self.theory.key_claims:
            lines.append("")
            lines.append("Supporting claims:")
            for claim in self.theory.key_claims:
                lines.append(f"  - {claim}")
        lines.append("")
        lines.append("FACTUAL RECITATION:")
        lines.append(self.factual_recitation)
        lines.append("")
        lines.append("RESPONSES TO ALLEGATIONS:")
        for resp in self.responses:
            lines.append(f"  [{resp.allegation_id}] {resp.response_text}")
        lines.append("")
        lines.append("CLOSING:")
        lines.append(self.closing)
        lines.append("")
        return "\n".join(lines)






