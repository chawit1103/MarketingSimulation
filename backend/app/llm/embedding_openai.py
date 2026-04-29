"""OpenAI embedding provider using the OpenAI Embeddings API."""

import logging
from typing import List

from openai import OpenAI

from .embedding_base import AbstractEmbeddingProvider

logger = logging.getLogger('mirofish.embedding')


class OpenAIEmbeddingProvider(AbstractEmbeddingProvider):
    """Embedding provider backed by OpenAI's embeddings API.

    Supports models like text-embedding-3-small, text-embedding-3-large,
    text-embedding-ada-002, and compatible third-party endpoints.
    """

    def __init__(self, model: str, api_key: str = "", base_url: str = None, timeout: int = 60):
        super().__init__(model=model, api_key=api_key, base_url=base_url, timeout=timeout)
        self._client = OpenAI(
            api_key=api_key,
            base_url=base_url or 'https://api.openai.com/v1',
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
            logger.error(f"OpenAI embed failed: {e}")
            raise

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts in a single API call.

        OpenAI natively supports batch embedding — all texts are sent at once.
        """
        if not texts:
            return []

        try:
            response = self._client.embeddings.create(
                model=self.model,
                input=texts,
            )
            # Sort by index to preserve input order
            sorted_data = sorted(response.data, key=lambda d: d.index)
            return [d.embedding for d in sorted_data]
        except Exception as e:
            logger.error(f"OpenAI batch embed failed (n={len(texts)}): {e}")
            raise
