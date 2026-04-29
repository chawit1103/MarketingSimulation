"""
OpenAI LLM provider implementing the BaseLLMProvider interface.

Uses the `openai` SDK for chat completions, with native JSON mode support.
"""

from typing import Dict, Any, List, Optional

from openai import OpenAI

from .base import BaseLLMProvider

import logging

logger = logging.getLogger("mirofish.llm.openai")


class OpenAIProvider(BaseLLMProvider):
    """OpenAI-compatible LLM provider (OpenAI, DeepSeek, Groq, OpenRouter, etc.)."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self._client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
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
            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=kwargs.pop("temperature", self.temperature),
                max_tokens=kwargs.pop("max_tokens", self.max_tokens),
                **kwargs,
            )
            content = response.choices[0].message.content or ""
            return self._clean_thinking(content)
        except Exception as exc:
            logger.error(
                "OpenAI chat request failed (model=%s): %s", self.model, exc
            )
            raise RuntimeError(
                f"OpenAI chat request failed for model '{self.model}': {exc}"
            ) from exc

    def chat_json(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Send a chat request with native JSON mode enabled.

        Overrides the base-class text-parsing fallback so that the API
        returns structured JSON directly via ``response_format``.
        """
        response = self.chat(
            messages=messages,
            temperature=temperature or 0.3,
            max_tokens=max_tokens or self.max_tokens,
            response_format={"type": "json_object"},
            **kwargs,
        )

        # Fall back to the base-class JSON parsing (handles code fences,
        # partial extraction, etc.).  In practice the response is already
        # valid JSON because of ``response_format``, but this adds
        # robustness.
        cleaned = response.strip()
        import json
        import re

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
                f"Invalid JSON from LLM ({self.model}): {cleaned[:300]}..."
            )
