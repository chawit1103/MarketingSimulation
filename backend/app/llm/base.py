"""Abstract LLM provider interface — all providers must implement this."""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import json
import re
import logging

logger = logging.getLogger('mirofish.llm')


class BaseLLMProvider(ABC):
    """All LLM providers must implement this interface.

    Provides a uniform chat() and chat_json() API regardless of backend.
    """

    def __init__(
        self,
        model: str,
        api_key: str,
        base_url: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        timeout: int = 600,
    ):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Send chat completion request. Returns response text."""
        ...

    def chat_json(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Send chat request and parse JSON response.

        Default implementation calls chat() then parses JSON.
        Override if provider has native JSON mode support.
        """
        response = self.chat(
            messages=messages,
            temperature=temperature or 0.3,
            max_tokens=max_tokens or self.max_tokens,
            **kwargs,
        )

        # Clean markdown code fences that LLMs sometimes wrap JSON in
        cleaned = response.strip()
        cleaned = re.sub(r'^```(?:json)?\s*\n?', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\n?```\s*$', '', cleaned)
        cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            # Try extracting JSON from within text
            m = re.search(r'\{[\s\S]*\}', cleaned)
            if m:
                try:
                    return json.loads(m.group(0))
                except json.JSONDecodeError:
                    pass
            raise ValueError(
                f"Invalid JSON from LLM ({self.model}): {cleaned[:300]}..."
            )

    def _clean_thinking(self, text: str) -> str:
        """Remove <think>...</think> blocks that some models emit."""
        return re.sub(r'<think>[\s\S]*?</think>', '', text).strip()
