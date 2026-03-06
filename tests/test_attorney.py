"""Tests for DefenseAttorney with a stubbed ChatClient."""
from __future__ import annotations

import json

import pytest

from counsel.cases.allegation import Allegation, AllegationSeverity
from counsel.cases.client import Client
from counsel.defense.attorney import DefenseAttorney
from counsel.evidence.index import DefenseEvidence, EvidenceIndex, EvidenceRole
from counsel.framing.theory import TheoryArchetype


class _StubChatClient:
    """Mimics ChatClient.chat() without making network calls."""

    def __init__(self, response: str):
        self.response = response

    async def chat(self, system: str, user: str, **kwargs) -> str:
        return self.response


def _ok_response() -> str:
    return json.dumps({
        "theory_headline": "client acted within their authority",
        "theory_archetype": "justification",
        "key_claims": [
            "the action was lawful",
            "the action was disclosed",
            "the accuser lacks standing",
        ],
        "factual_recitation": "client took action X. accuser asserts harm. record shows process was followed.",
        "responses": [
            {
                "allegation_id": "alleg_1",
                "response_text": "no breach occurred. process was followed.",
                "cited_evidence_ids": ["e1"],
            }
        ],
        "closing": "the record supports the client's actions. dismissal is appropriate.",
    })


@pytest.mark.asyncio
async def test_attorney_drafts_brief():
    stub = _StubChatClient(_ok_response())
    attorney = DefenseAttorney.__new__(DefenseAttorney)
    attorney.client = stub
    from counsel.defense.attorney import AttorneyConfig
    attorney.config = AttorneyConfig()

    client = Client(handle="@client")
    client.allegations.append(
        Allegation(
            id="alleg_1",
            accuser="@accuser",
            summary="did the thing",
            severity=AllegationSeverity.SERIOUS,
        )
    )
    evidence = EvidenceIndex()
    evidence.add(DefenseEvidence(id="e1", role=EvidenceRole.EXCULPATORY, summary="record shows X"))

    brief = await attorney.represent(client, evidence)
    assert brief.client_handle == "@client"
    assert brief.theory.archetype == TheoryArchetype.JUSTIFICATION
    assert len(brief.responses) == 1
    assert brief.responses[0].cited_evidence_ids == ["e1"]


@pytest.mark.asyncio
async def test_attorney_handles_code_fences_in_response():
    response_in_fences = "```json\n" + _ok_response() + "\n```"
    stub = _StubChatClient(response_in_fences)
    attorney = DefenseAttorney.__new__(DefenseAttorney)
    attorney.client = stub
    from counsel.defense.attorney import AttorneyConfig
    attorney.config = AttorneyConfig()

    client = Client(handle="@x")
    brief = await attorney.represent(client)
    assert brief.theory.archetype == TheoryArchetype.JUSTIFICATION


@pytest.mark.asyncio
async def test_attorney_invalid_json_raises():
    stub = _StubChatClient("not json at all")
    attorney = DefenseAttorney.__new__(DefenseAttorney)
    attorney.client = stub
    from counsel.defense.attorney import AttorneyConfig
    attorney.config = AttorneyConfig()

    client = Client(handle="@x")
    with pytest.raises(RuntimeError, match="invalid json"):
        await attorney.represent(client)

