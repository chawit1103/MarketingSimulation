"""Google Gemini LLM provider — uses google-genai SDK."""

import json
import logging
from typing import Dict, Any, List, Optional

from google import genai
from google.genai import types as genai_types

from .base import BaseLLMProvider

logger = logging.getLogger('mirofish.llm')


class GoogleProvider(BaseLLMProvider):
    """LLM provider for Google Gemini models via the google-genai SDK."""

    def __init__(
        self,
        model: str = "gemini-2.5-flash",
        api_key: str = "",
        base_url: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        timeout: int = 600,
    ):
        super().__init__(
            model=model,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
        )
        self.client = genai.Client(api_key=api_key)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _extract_system_message(
        self, messages: List[Dict[str, str]]
    ) -> tuple[Optional[str], List[Dict[str, str]]]:
        """Split out the system message from the messages list.

        Returns (system_text, remaining_messages).
        """
        if messages and messages[0].get("role") == "system":
            return messages[0]["content"], messages[1:]
        return None, messages

    def _build_contents(
        self, messages: List[Dict[str, str]]
    ) -> List[genai_types.Content]:
        """Convert a list of role/content dicts into Google Content objects."""
        contents: List[genai_types.Content] = []
        for msg in messages:
            role = msg.get("role", "user")
            text = msg.get("content", "")
            # Map standard roles to Google roles
            if role == "assistant":
                google_role = "model"
            elif role == "user":
                google_role = "user"
            else:
                # Fallback: treat unknown roles as user
                google_role = "user"
            contents.append(
                genai_types.Content(
                    role=google_role,
                    parts=[genai_types.Part(text=text)],
                )
            )
        return contents

    def _render_messages(self, messages: List[Dict[str, str]]) -> str:
        """Render messages as a plain-text transcript for logging / empty-contents fallback."""
        lines: List[str] = []
        for msg in messages:
            role = msg.get("role", "user").upper()
            lines.append(f"[{role}] {msg.get('content', '')}")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Core API
    # ------------------------------------------------------------------

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """Send a chat completion request to Google Gemini.

        Converts standard messages format to Google Content objects,
        extracts system instructions, and returns the response text.
        """
        system_text, conversation = self._extract_system_message(messages)

        contents = self._build_contents(conversation)

        config_kwargs: Dict[str, Any] = {
            "temperature": temperature if temperature is not None else self.temperature,
            "max_output_tokens": max_tokens if max_tokens is not None else self.max_tokens,
        }
        if system_text:
            config_kwargs["system_instruction"] = system_text

        config = genai_types.GenerateContentConfig(**config_kwargs)

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=config,
            )
            text = response.text or ""
            return self._clean_thinking(text)
        except Exception as e:
            err_msg = (
                f"Google Gemini API error (model={self.model}): {e}. "
                f"Messages preview: {self._render_messages(messages)[:200]}"
            )
            logger.error(err_msg)
            raise RuntimeError(err_msg) from e

    def chat_json(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Send a chat request and return parsed JSON.

        Prepends a JSON-output instruction to the system message to
        increase the likelihood of well-formed JSON, then falls back
        to the base class JSON-parsing logic.
        """
        json_instruction = (
            "You must respond with valid JSON only. "
            "Do not include markdown fences, explanations, or any other text. "
            "Output raw JSON."
        )

        modified_messages: List[Dict[str, str]] = []
        system_found = False
        for msg in messages:
            if msg.get("role") == "system":
                modified_messages.append({
                    "role": "system",
                    "content": f"{msg['content']}\n\n{json_instruction}",
                })
                system_found = True
            else:
                modified_messages.append(msg)

        if not system_found:
            modified_messages.insert(0, {
                "role": "system",
                "content": json_instruction,
            })

        response = self.chat(
            messages=modified_messages,
            temperature=temperature if temperature is not None else 0.3,
            max_tokens=max_tokens or self.max_tokens,
            **kwargs,
        )

        cleaned = response.strip()

        # Strip markdown fences
        import re
        cleaned = re.sub(r'^```(?:json)?\s*\n?', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\n?```\s*$', '', cleaned)
        cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            # Try extracting a JSON object from within the text
            m = re.search(r'\{[\s\S]*\}', cleaned)
            if m:
                try:
                    return json.loads(m.group(0))
                except json.JSONDecodeError:
                    pass
            raise ValueError(
                f"Invalid JSON from Google Gemini ({self.model}): {cleaned[:300]}..."
            )
