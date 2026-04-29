"""
OpenRouter LLM provider — OpenAI-compatible API.

OpenRouter uses an OpenAI-compatible chat completions API and requires
specific HTTP headers for attribution (HTTP-Referer and X-Title).
"""

import logging

from openai import OpenAI

from .openai_provider import OpenAIProvider

logger = logging.getLogger("mirofish.llm.openrouter")


class OpenRouterProvider(OpenAIProvider):
    """OpenRouter LLM provider (OpenAI-compatible API with attribution headers)."""

    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("base_url", "https://openrouter.ai/api/v1")
        super().__init__(**kwargs)

        # Re-create the client with OpenRouter-required attribution headers.
        # These are required by OpenRouter's terms of service.
        self._client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
            default_headers={
                "HTTP-Referer": "http://localhost:3001",
                "X-Title": "MiroFish MultiLang",
            },
        )
