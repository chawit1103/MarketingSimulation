"""
DeepSeek LLM provider — OpenAI-compatible API.

DeepSeek uses the exact same API surface as OpenAI, so we simply
subclass OpenAIProvider and set the correct default base URL.
"""

import logging

from .openai_provider import OpenAIProvider

logger = logging.getLogger("mirofish.llm.deepseek")


class DeepSeekProvider(OpenAIProvider):
    """DeepSeek LLM provider (OpenAI-compatible API)."""

    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("base_url", "https://api.deepseek.com/v1")
        super().__init__(**kwargs)
