"""
Groq LLM provider — OpenAI-compatible API.

Groq exposes an OpenAI-compatible chat completions endpoint, so we
subclass OpenAIProvider and point it at the Groq base URL.
"""

import logging

from .openai_provider import OpenAIProvider

logger = logging.getLogger("mirofish.llm.groq")


class GroqProvider(OpenAIProvider):
    """Groq LLM provider (OpenAI-compatible API)."""

    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("base_url", "https://api.groq.com/openai/v1")
        super().__init__(**kwargs)
