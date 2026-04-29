"""Anthropic Claude LLM provider using the Messages API."""

from typing import Dict, Any, List, Optional
import logging

import anthropic

from .base import BaseLLMProvider

logger = logging.getLogger("mirofish.llm.anthropic")


class AnthropicProvider(BaseLLMProvider):
    """LLM provider for Anthropic Claude models (Messages API).

    Implements chat() and chat_json() using anthropic.Anthropic client.
    Supports Claude 3 Opus, 3.5 Sonnet, 3 Haiku, and later models.
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
        super().__init__(
            model=model,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
        )
        # Build client kwargs – only pass base_url if it's set
        client_kwargs: Dict[str, Any] = {
            "api_key": api_key,
            "timeout": timeout,
        }
        if base_url:
            client_kwargs["base_url"] = base_url
        self.client = anthropic.Anthropic(**client_kwargs)

    def _extract_messages(
        self, messages: List[Dict[str, str]]
    ) -> tuple[str, List[Dict[str, Any]]]:
        """Separate system prompt(s) from chat messages.

        Returns (system_text, anthropic_messages) where:
          - system_text is the concatenated system prompts (or "")
          - anthropic_messages is a list of {"role": "user"|"assistant", "content": str}
        """
        system_parts: List[str] = []
        chat_messages: List[Dict[str, Any]] = []

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                system_parts.append(content)
            elif role in ("user", "assistant"):
                chat_messages.append({"role": role, "content": content})
            else:
                # Treat unknown roles as user
                logger.debug(
                    "Unknown message role %r — treating as user", role
                )
                chat_messages.append({"role": "user", "content": content})

        system_text = "\n\n".join(system_parts) if system_parts else ""
        return system_text, chat_messages

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Send a chat completion request and return the response text.

        Maps the standard message format to Anthropic's Messages API:
        - System messages are extracted and passed as the ``system`` parameter.
        - User and assistant messages are mapped directly.
        """
        system_msg, chat_messages = self._extract_messages(messages)

        # Allow overriding model / max_tokens / temperature per call
        model = kwargs.get("model", self.model)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)
        # temperature is not used directly by Anthropic in this call unless
        # the caller passes it through kwargs; we'll keep it simple.

        try:
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system_msg or anthropic.NOT_GIVEN,
                messages=chat_messages,
            )
        except anthropic.APIError as exc:
            logger.error("Anthropic API error: %s", exc)
            raise RuntimeError(f"Anthropic API error: {exc}") from exc
        except Exception as exc:
            logger.error("Unexpected error calling Anthropic: %s", exc)
            raise RuntimeError(f"Anthropic call failed: {exc}") from exc

        # response.content is a list of ContentBlock objects
        # Typically the first block is a TextBlock with the response text
        if not response.content:
            raise RuntimeError("Anthropic returned an empty response")

        text = response.content[0].text
        return self._clean_thinking(text)

    def chat_json(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Send a chat request and parse a JSON response.

        Prepends a JSON-mode instruction to the system message so Claude
        knows it must reply with valid JSON only.
        """
        json_instruction = "You MUST respond with valid JSON only."

        # Inject the instruction into the system message by adding a
        # system message at the front of the messages list (or prepending
        # to the first system message if one already exists).
        modified_messages: List[Dict[str, str]] = list(messages)
        for i, msg in enumerate(modified_messages):
            if msg.get("role") == "system":
                modified_messages[i] = {
                    "role": "system",
                    "content": f"{json_instruction}\n\n{msg['content']}",
                }
                break
        else:
            # No system message found — insert one
            modified_messages.insert(
                0, {"role": "system", "content": json_instruction}
            )

        # Call parent's chat_json which calls our chat() and parses JSON
        return super().chat_json(
            messages=modified_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )
