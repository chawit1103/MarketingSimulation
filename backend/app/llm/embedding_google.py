"""Google embedding provider using the Gemini Embedding API."""

import logging
from typing import List

from google import genai

from .embedding_base import AbstractEmbeddingProvider

logger = logging.getLogger('mirofish.embedding')


class GoogleEmbeddingProvider(AbstractEmbeddingProvider):
    """Embedding provider backed by Google's Gemini Embedding API.

    Uses models like text-embedding-004, embedding-001, etc.
    """

    def __init__(self, model: str, api_key: str = "", base_url: str = None, timeout: int = 60):
        super().__init__(model=model, api_key=api_key, base_url=base_url, timeout=timeout)
        self._client = genai.Client(api_key=api_key)

    def embed(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        try:
            response = self._client.models.embed_content(
                model=self.model,
                contents=text,
            )
            return response.embeddings[0].values
        except Exception as e:
            logger.error(f"Google embed failed: {e}")
            raise

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts.

        Google's embed_content doesn't support batch natively,
        so we loop over texts individually.
        """
        return [self.embed(t) for t in texts]
