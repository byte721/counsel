"""DefenseAttorney: orchestrates the defense brief generation pipeline.

Pipeline:
  1. Build a structured prompt from client + allegations + evidence
  2. Send to LLM, get structured JSON back
  3. Parse into DefenseTheory + AllegationResponse list
  4. Assemble into DefenseBrief
  5. Optionally run a refinement pass to fill theory gaps

The attorney is the only public-facing class. Everything else is internal
plumbing.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass

from counsel.cases.allegation import Allegation
from counsel.cases.client import Client
from counsel.clients.chat import ChatClient
from counsel.defense.brief import AllegationResponse, DefenseBrief
from counsel.defense.prompts import (
    ATTORNEY_SYSTEM,
    ATTORNEY_USER_TEMPLATE,
)
from counsel.evidence.index import EvidenceIndex
from counsel.framing.theory import DefenseTheory, TheoryArchetype

log = logging.getLogger(__name__)


@dataclass
class AttorneyConfig:
    provider: str = "openai"
    model: str | None = None
    temperature: float = 0.4
    max_tokens: int = 2200


class DefenseAttorney:
    """The agent that drafts the defense brief."""

    def __init__(
        self,
        client: ChatClient | None = None,
        config: AttorneyConfig | None = None,
    ):
        self.config = config or AttorneyConfig()
        self.client = client or ChatClient(
            provider=self.config.provider,
            model=self.config.model,
        )

    async def represent(
        self,
        client: Client,
        evidence: EvidenceIndex | None = None,
    ) -> DefenseBrief:
        """Draft a defense brief for the given client and evidence."""
        evidence = evidence or EvidenceIndex()
        log.info(
            "drafting brief for client=%s allegations=%d evidence=%d",
            client.handle, len(client.allegations), len(evidence),
        )
        user_prompt = self._build_prompt(client, evidence)
        raw = await self.client.chat(
            system=ATTORNEY_SYSTEM,
            user=user_prompt,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        )
        return self._parse_brief(raw, client)

    def _build_prompt(self, client: Client, evidence: EvidenceIndex) -> str:
        allegations = self._format_allegations(client.allegations)
        evidence_block = self._format_evidence(evidence)
        return ATTORNEY_USER_TEMPLATE.format(
            client_handle=client.handle,
            client_role=client.role or "(no role specified)",
            corpus_id=client.public_corpus_id or "(none)",
            allegation_block=allegations,
            evidence_block=evidence_block,
        )

    @staticmethod
    def _format_allegations(allegations: list[Allegation]) -> str:
        if not allegations:
            return "(no allegations on file)"
        lines = []
        for _i, a in enumerate(allegations, 1):
            lines.append(
                f"[{a.id}] severity={a.severity.value} accuser={a.accuser}\n"
                f"    {a.summary}"
            )
        return "\n".join(lines)

    @staticmethod
    def _format_evidence(evidence: EvidenceIndex) -> str:
        if len(evidence) == 0:
            return "(no evidence indexed)"
        lines = []
        for item in evidence.items:
            lines.append(
                f"[{item.id}] role={item.role.value} weight={item.weight}\n"
                f"    {item.summary}"
            )
        return "\n".join(lines)

    @staticmethod
    def _parse_brief(raw: str, client: Client) -> DefenseBrief:
        text = raw.strip()
        if text.startswith("```"):
            text = text.split("```", 2)[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip("`").strip()
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"attorney returned invalid json: {raw[:300]!r}") from exc

        theory = DefenseTheory(
            headline=data.get("theory_headline", ""),
            archetype=TheoryArchetype(data["theory_archetype"]),
            key_claims=list(data.get("key_claims", [])),
        )
        responses = [
            AllegationResponse(
                allegation_id=r["allegation_id"],
                response_text=r["response_text"],
                cited_evidence_ids=list(r.get("cited_evidence_ids", [])),
            )
            for r in data.get("responses", [])
        ]
        return DefenseBrief(
            client_handle=client.handle,
            theory=theory,
            factual_recitation=data.get("factual_recitation", ""),
            responses=responses,
            closing=data.get("closing", ""),
        )









