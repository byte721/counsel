"""BriefStore: persists defense briefs to disk.

Briefs are stored as JSON for the structured record and as text for human
reading and posting. Each brief lives in its own directory keyed by client
handle and a draft timestamp.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

from counsel.defense.brief import DefenseBrief

log = logging.getLogger(__name__)


class BriefStore:
    """File-based persistence for DefenseBriefs."""

    def __init__(self, root: Path | str = "briefs"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, brief: DefenseBrief) -> Path:
        """Save a brief and return the path to its directory."""
        slug = self._slug(brief.client_handle)
        ts = brief.drafted_at.strftime("%Y-%m-%dT%H%M%S")
        directory = self.root / f"{slug}_{ts}"
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "brief.json").write_text(self._render_json(brief))
        (directory / "brief.txt").write_text(brief.render())
        log.info("brief saved: %s", directory)
        return directory

    @staticmethod
    def _slug(handle: str) -> str:
        return handle.lstrip("@").lower().replace(" ", "_")

    @staticmethod
    def _render_json(brief: DefenseBrief) -> str:
        payload = {
            "client_handle": brief.client_handle,
            "drafted_at": brief.drafted_at.isoformat(),
            "theory": {
                "headline": brief.theory.headline,
                "archetype": brief.theory.archetype.value,
                "key_claims": brief.theory.key_claims,
                "weaknesses": brief.theory.weaknesses,
            },
            "factual_recitation": brief.factual_recitation,
            "responses": [
                {
                    "allegation_id": r.allegation_id,
                    "response_text": r.response_text,
                    "cited_evidence_ids": r.cited_evidence_ids,
                }
                for r in brief.responses
            ],
            "closing": brief.closing,
        }
        return json.dumps(payload, indent=2)





