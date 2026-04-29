"""Ollama embedding provider using the Ollama API via OpenAI-compatible client."""

import logging
from typing import List

from openai import OpenAI

from .embedding_base import AbstractEmbeddingProvider

logger = logging.getLogger('mirofish.embedding')


class OllamaEmbeddingProvider(AbstractEmbeddingProvider):
    """Embedding provider backed by a local Ollama server.

    Uses the OpenAI-compatible /v1/embeddings endpoint.
    Default base URL: http://localhost:11434
    """

    def __init__(self, model: str, api_key: str = "", base_url: str = None, timeout: int = 60):
        super().__init__(model=model, api_key=api_key, base_url=base_url, timeout=timeout)
        self._client = OpenAI(
            api_key=api_key or "ollama",  # Ollama doesn't require a real key
            base_url=(base_url or 'http://localhost:11434') + '/v1',
            timeout=timeout,
        )

    def embed(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        try:
            response = self._client.embeddings.create(
                model=self.model,
                input=text,
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Ollama embed failed: {e}")
            raise

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts in a single API call.

        Ollama supports batch embeddings natively via the OpenAI-compatible endpoint.
        """
        if not texts:
            return []

        try:
            response = self._client.embeddings.create(
                model=self.model,
                input=texts,
            )
            sorted_data = sorted(response.data, key=lambda d: d.index)
            return [d.embedding for d in sorted_data]
        except Exception as e:
            logger.error(f"Ollama batch embed failed (n={len(texts)}): {e}")
            raise
