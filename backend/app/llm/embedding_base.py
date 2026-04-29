"""Abstract embedding provider interface — all embedding providers must implement this."""

from abc import ABC, abstractmethod
from typing import List


class AbstractEmbeddingProvider(ABC):
    """All embedding providers must implement this interface.

    Provides uniform embed() and embed_batch() APIs regardless of backend.
    """

    def __init__(self, model: str, api_key: str = "", base_url: str = None, timeout: int = 60):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Generate embedding for a single text.

        Args:
            text: Input text to embed.

        Returns:
            List of floats representing the embedding vector.
        """
        ...

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts.

        Default implementation calls embed() for each text.
        Override for batch-native APIs (e.g. OpenAI).

        Args:
            texts: List of input texts.

        Returns:
            List of embedding vectors (same order as input).
        """
        return [self.embed(t) for t in texts]
