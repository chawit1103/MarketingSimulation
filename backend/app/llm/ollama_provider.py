"""
Ollama LLM provider implementing the BaseLLMProvider interface.

Ollama exposes an OpenAI-compatible API at ``/v1``, so we use the ``openai``
SDK for chat completions.  Special handling:
- Dummy ``api_key`` (Ollama doesn't require auth locally).
- ``num_ctx`` is passed via ``extra_body`` to prevent prompt truncation (Ollama
  defaults to 2048 tokens which is often too small).
- ``<think>`` block cleanup for models that emit chain-of-thought.

Refactored from ``backend/app/utils/llm_client.py``.
"""

from typing import Dict, Any, List, Optional

from openai import OpenAI

from .base import BaseLLMProvider

import logging
import os

logger = logging.getLogger("mirofish.llm.ollama")


class OllamaProvider(BaseLLMProvider):
    """Ollama LLM provider (local, OpenAI-compatible API)."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # Ensure we have a dummy API key since Ollama doesn't require one
        self.api_key = self.api_key or "ollama"

        # Default to localhost if no base_url is given
        self.base_url = self.base_url or "http://localhost:11434/v1"

        self._client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
        )

        # Context window size — prevents prompt truncation.
        # Ollama defaults to only 2048; we default to 8192.
        self._num_ctx: Optional[int] = None
        raw = os.environ.get("OLLAMA_NUM_CTX")
        if raw:
            try:
                self._num_ctx = int(raw)
            except ValueError:
                logger.warning(
                    "Invalid OLLAMA_NUM_CTX=%r, ignoring", raw,
                )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Send a chat-completion request.

        All extra keyword arguments are forwarded directly to
        ``client.chat.completions.create`` so that callers can inject
        provider-specific parameters (e.g. ``response_format``).
        """
        try:
            request_kwargs: Dict[str, Any] = {
                "model": self.model,
                "messages": messages,
                "temperature": kwargs.pop("temperature", self.temperature),
                "max_tokens": kwargs.pop("max_tokens", self.max_tokens),
            }

            # Inject Ollama-specific num_ctx via extra_body
            if self._num_ctx is not None:
                request_kwargs.setdefault("extra_body", {})
                request_kwargs["extra_body"].setdefault("options", {})
                request_kwargs["extra_body"]["options"]["num_ctx"] = self._num_ctx

            # Merge any remaining caller-provided kwargs
            request_kwargs.update(kwargs)

            response = self._client.chat.completions.create(**request_kwargs)
            content = response.choices[0].message.content or ""
            return self._clean_thinking(content)

        except Exception as exc:
            logger.error(
                "Ollama chat request failed (model=%s, base_url=%s): %s",
                self.model, self.base_url, exc,
            )
            raise RuntimeError(
                f"Ollama chat request failed for model '{self.model}': {exc}"
            ) from exc

    def chat_json(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Send a chat request with native JSON mode enabled.

        Calls ``chat()`` with ``response_format={"type": "json_object"}``,
        then manually parses JSON (same logic as base class, to avoid a
        second API call from polymorphic dispatch).
        """
        import json
        import re

        response = self.chat(
            messages=messages,
            temperature=temperature or 0.3,
            max_tokens=max_tokens or self.max_tokens,
            response_format={"type": "json_object"},
            **kwargs,
        )

        # Reuse the base-class JSON parsing (handles code fences,
        # partial extraction, etc.)
        cleaned = response.strip()
        cleaned = re.sub(r"^```(?:json)?\s*\n?", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\n?```\s*$", "", cleaned)
        cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            m = re.search(r"\{[\s\S]*\}", cleaned)
            if m:
                try:
                    return json.loads(m.group(0))
                except json.JSONDecodeError:
                    pass
            raise ValueError(
                f"Invalid JSON from Ollama ({self.model}): {cleaned[:300]}..."
            )
