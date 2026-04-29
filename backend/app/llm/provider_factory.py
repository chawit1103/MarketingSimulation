"""LLM Provider Factory — creates providers from runtime settings with caching."""
import logging
from typing import Dict
from .base import BaseLLMProvider
from ..models.settings import SettingsManager, ProviderType

logger = logging.getLogger('mirofish.llm_factory')

_provider_cache: Dict[str, BaseLLMProvider] = {}


class LLMProviderFactory:
    """Creates and caches LLM providers based on runtime settings.

    Usage:
        provider = LLMProviderFactory.get_provider()         # default
        provider = LLMProviderFactory.get_provider('ner')    # task-specific
        provider = LLMProviderFactory.get_provider('report') # task-specific

    Cache is invalidated automatically when settings change.
    """

    @classmethod
    def invalidate_cache(cls):
        """Clear all cached providers (called when settings change via API)."""
        global _provider_cache
        _provider_cache.clear()
        logger.info("LLM provider cache invalidated (settings changed)")

    @classmethod
    def get_provider(cls, task: str = "default") -> BaseLLMProvider:
        """Get LLM provider for a specific task.

        Args:
            task: 'default', 'ner', 'report', 'simulation', 'ontology'

        Returns:
            BaseLLMProvider instance (cached per task)
        """
        cache_key = f"llm_{task}"
        if cache_key in _provider_cache:
            return _provider_cache[cache_key]

        settings = SettingsManager().get()
        llm_config = settings.llm

        # Check for task-specific override
        provider_type = llm_config.provider
        model = llm_config.model

        task_override = None
        if task != "default":
            task_override = getattr(settings.task_llm, task, None)

        if task_override:
            if task_override.provider:
                provider_type = task_override.provider
            if task_override.model:
                model = task_override.model

        provider = cls._create(provider_type, model, llm_config)
        _provider_cache[cache_key] = provider

        logger.info(
            "Created LLM provider: %s/%s for task '%s' (temp=%.1f, timeout=%ds)",
            provider_type.value, model, task,
            llm_config.temperature, llm_config.timeout,
        )
        return provider

    @classmethod
    def _create(
        cls,
        provider_type: ProviderType,
        model: str,
        llm_config,
    ) -> BaseLLMProvider:
        """Instantiate the correct provider class based on type."""
        common = {
            "model": model,
            "api_key": llm_config.api_key,
            "temperature": llm_config.temperature,
            "max_tokens": llm_config.max_tokens,
            "timeout": llm_config.timeout,
        }
        base_url = llm_config.base_url

        if provider_type == ProviderType.OPENAI:
            from .openai_provider import OpenAIProvider
            return OpenAIProvider(base_url=base_url, **common)

        elif provider_type == ProviderType.ANTHROPIC:
            from .anthropic_provider import AnthropicProvider
            return AnthropicProvider(base_url=base_url, **common)

        elif provider_type == ProviderType.GOOGLE:
            from .google_provider import GoogleProvider
            return GoogleProvider(base_url=base_url, **common)

        elif provider_type == ProviderType.DEEPSEEK:
            from .deepseek_provider import DeepSeekProvider
            return DeepSeekProvider(base_url=base_url, **common)

        elif provider_type == ProviderType.GROQ:
            from .groq_provider import GroqProvider
            return GroqProvider(base_url=base_url, **common)

        elif provider_type == ProviderType.OPENROUTER:
            from .openrouter_provider import OpenRouterProvider
            return OpenRouterProvider(base_url=base_url, **common)

        elif provider_type == ProviderType.OLLAMA:
            from .ollama_provider import OllamaProvider
            return OllamaProvider(base_url=base_url, **common)

        # --- OpenAI-compatible providers (all use OpenAIProvider) ---
        elif provider_type == ProviderType.XAI:
            from .openai_provider import OpenAIProvider
            return OpenAIProvider(base_url=base_url or "https://api.x.ai/v1", **common)

        elif provider_type == ProviderType.MISTRAL:
            from .openai_provider import OpenAIProvider
            return OpenAIProvider(base_url=base_url or "https://api.mistral.ai/v1", **common)

        elif provider_type == ProviderType.TOGETHER:
            from .openai_provider import OpenAIProvider
            return OpenAIProvider(base_url=base_url or "https://api.together.xyz/v1", **common)

        elif provider_type == ProviderType.GLM:
            from .openai_provider import OpenAIProvider
            return OpenAIProvider(base_url=base_url or "https://open.bigmodel.cn/api/paas/v4", **common)

        elif provider_type == ProviderType.MINIMAX:
            from .openai_provider import OpenAIProvider
            return OpenAIProvider(base_url=base_url or "https://api.minimax.chat/v1", **common)

        elif provider_type == ProviderType.KIMI:
            from .openai_provider import OpenAIProvider
            return OpenAIProvider(base_url=base_url or "https://api.moonshot.cn/v1", **common)

        elif provider_type == ProviderType.DASHSCOPE:
            from .openai_provider import OpenAIProvider
            return OpenAIProvider(base_url=base_url or "https://dashscope-intl.aliyuncs.com/compatible-mode/v1", **common)

        elif provider_type == ProviderType.HUGGINGFACE:
            from .openai_provider import OpenAIProvider
            return OpenAIProvider(base_url=base_url or "https://api-inference.huggingface.co/v1", **common)

        elif provider_type == ProviderType.BEDROCK:
            raise NotImplementedError(
                "Amazon Bedrock uses IAM-based authentication (not API key). "
                "Use a proxy like LiteLLM or OpenRouter to access Bedrock models via OpenAI-compatible API."
            )

        elif provider_type == ProviderType.VERCEL:
            from .openai_provider import OpenAIProvider
            return OpenAIProvider(base_url=base_url, **common)

        else:
            raise ValueError(f"Unknown provider type: {provider_type}")
