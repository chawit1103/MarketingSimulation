"""Embedding Provider Factory — creates providers from runtime settings with caching."""

import logging
from typing import Dict

from .embedding_base import AbstractEmbeddingProvider
from ..models.settings import SettingsManager, EmbeddingProviderType

logger = logging.getLogger('mirofish.embedding_factory')

_provider_cache: Dict[str, AbstractEmbeddingProvider] = {}


class EmbeddingProviderFactory:
    """Creates and caches embedding providers based on runtime settings.

    Usage:
        provider = EmbeddingProviderFactory.get_provider()

    Cache is invalidated automatically when settings change.
    """

    @classmethod
    def invalidate_cache(cls):
        """Clear cached provider (called when settings change via API)."""
        global _provider_cache
        _provider_cache.clear()
        logger.info("Embedding provider cache invalidated (settings changed)")

    @classmethod
    def get_provider(cls) -> AbstractEmbeddingProvider:
        """Get the configured embedding provider.

        Returns:
            AbstractEmbeddingProvider instance (cached)
        """
        cache_key = "embedding_default"
        if cache_key in _provider_cache:
            return _provider_cache[cache_key]

        settings = SettingsManager().get()
        emb_config = settings.embedding

        provider = cls._create(
            emb_config.provider,
            emb_config.model,
            emb_config,
        )
        _provider_cache[cache_key] = provider

        logger.info(
            "Created embedding provider: %s/%s",
            emb_config.provider.value, emb_config.model,
        )
        return provider

    @classmethod
    def _create(
        cls,
        provider_type: EmbeddingProviderType,
        model: str,
        emb_config,
    ) -> AbstractEmbeddingProvider:
        """Instantiate the correct provider class based on type."""
        common = {
            "model": model,
            "api_key": emb_config.api_key,
            "base_url": emb_config.base_url,
        }

        if provider_type == EmbeddingProviderType.OPENAI:
            from .embedding_openai import OpenAIEmbeddingProvider
            return OpenAIEmbeddingProvider(**common)

        elif provider_type == EmbeddingProviderType.GOOGLE:
            from .embedding_google import GoogleEmbeddingProvider
            return GoogleEmbeddingProvider(**common)

        elif provider_type == EmbeddingProviderType.OLLAMA:
            from .embedding_ollama import OllamaEmbeddingProvider
            return OllamaEmbeddingProvider(**common)

        else:
            raise ValueError(f"Unknown embedding provider type: {provider_type}")
