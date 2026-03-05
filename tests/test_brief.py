"""Tests for DefenseBrief rendering and BriefStore persistence."""
from __future__ import annotations

import json
import tempfile
from datetime import datetime

from counsel.defense.brief import AllegationResponse, DefenseBrief
from counsel.framing.theory import DefenseTheory, TheoryArchetype
from counsel.io.store import BriefStore


def _sample_brief() -> DefenseBrief:
    return DefenseBrief(
        client_handle="@elonmusk",
        theory=DefenseTheory(
            headline="the founding agreement was honored",
            archetype=TheoryArchetype.JUSTIFICATION,
            key_claims=["claim a", "claim b"],
        ),
        factual_recitation="the record shows X.",
        responses=[
            AllegationResponse(
                allegation_id="alleg_1",
                response_text="no breach occurred",
                cited_evidence_ids=["e1"],
            ),
        ],
        closing="dismissal appropriate.",
        drafted_at=datetime(2026, 4, 28, 12, 0, 0),
    )


def test_brief_render_contains_sections():
    brief = _sample_brief()
    text = brief.render()
    assert "DEFENSE BRIEF FOR @elonmusk" in text
    assert "THEORY OF THE DEFENSE" in text
    assert "FACTUAL RECITATION" in text
    assert "RESPONSES TO ALLEGATIONS" in text
    assert "CLOSING" in text


def test_store_creates_files():
    with tempfile.TemporaryDirectory() as tmp:
        store = BriefStore(root=tmp)
        brief = _sample_brief()
        path = store.save(brief)
        assert (path / "brief.json").exists()
        assert (path / "brief.txt").exists()


def test_store_json_roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        store = BriefStore(root=tmp)
        brief = _sample_brief()
        path = store.save(brief)
        data = json.loads((path / "brief.json").read_text())
        assert data["client_handle"] == "@elonmusk"
        assert data["theory"]["archetype"] == "justification"
        assert len(data["responses"]) == 1
