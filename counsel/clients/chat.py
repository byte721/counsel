"""LLM client adapters.

Counsel uses an LLM to draft defense briefs. The adapter here is a thin
async interface around the Chat Completions style API used by OpenAI and
xAI.

Different design from earlier projects in this codebase family: we use a
single ChatClient class parameterized by provider, rather than separate
classes per provider. Less surface area, easier to swap.
"""
from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass

import httpx

log = logging.getLogger(__name__)


@dataclass
class ProviderConfig:
    name: str
    base_url: str
    api_key_env: str
    default_model: str


PROVIDERS: dict[str, ProviderConfig] = {
    "openai": ProviderConfig(
        name="openai",
        base_url="https://api.openai.com/v1",
        api_key_env="OPENAI_API_KEY",
        default_model="gpt-4o",
    ),
    "xai": ProviderConfig(
        name="xai",
        base_url="https://api.x.ai/v1",
        api_key_env="XAI_API_KEY",
        default_model="grok-4",
    ),
}


class ChatClient:
    """Single client that supports multiple Chat-Completions-compatible providers."""

    def __init__(
        self,
        provider: str = "openai",
        model: str | None = None,
        timeout: float = 60.0,
        max_retries: int = 3,
    ):
        if provider not in PROVIDERS:
            raise ValueError(f"unknown provider: {provider!r}")
        self.cfg = PROVIDERS[provider]
        self.model = model or self.cfg.default_model
        self.timeout = timeout
        self.max_retries = max_retries
        self._key = os.environ.get(self.cfg.api_key_env)
        if not self._key:
            raise RuntimeError(
                f"missing api key for provider {provider!r} (env {self.cfg.api_key_env})"
            )

    async def chat(
        self,
        system: str,
        user: str,
        temperature: float = 0.4,
        max_tokens: int = 1500,
    ) -> str:
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        headers = {
            "Authorization": f"Bearer {self._key}",
            "Content-Type": "application/json",
        }
        last_err: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as http:
                    resp = await http.post(
                        f"{self.cfg.base_url}/chat/completions",
                        json=body,
                        headers=headers,
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    return data["choices"][0]["message"]["content"]
            except httpx.HTTPStatusError as exc:
                last_err = exc
                code = exc.response.status_code
                log.warning("provider=%s status=%s attempt=%d", self.cfg.name, code, attempt)
                if code in (429, 500, 502, 503, 504):
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                last_err = exc
                log.warning("provider=%s network err attempt=%d", self.cfg.name, attempt)
                await asyncio.sleep(2 ** attempt)
        raise RuntimeError(f"chat failed after {self.max_retries} retries") from last_err







