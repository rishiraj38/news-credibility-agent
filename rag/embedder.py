"""
Embedding model wrapper for RAG system.
Uses sentence-transformers for lightweight, local embeddings.
"""

from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODEL


class Embedder:
    """Wrapper around sentence-transformers for document embeddings."""

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        """Initialize the embedding model."""
        self.model_name = model_name
        self._model = None

    @property
    def model(self) -> SentenceTransformer:
        """Lazy load the model to avoid startup delay."""
        if self._model is None:
            print(f"Loading embedding model: {self.model_name}")
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def embed(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        return self.model.encode(text, convert_to_numpy=True).tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        if not texts:
            return []
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=len(texts) > 10
        )
        return embeddings.tolist()

    @property
    def dimension(self) -> int:
        """Get the embedding dimension."""
        # MiniLM-L6-v2 produces 384-dimensional embeddings
        sample = self.embed("test")
        return len(sample)


# Global embedder instance for reuse
_embedder_instance = None


def get_embedder() -> Embedder:
    """Get or create the global embedder instance."""
    global _embedder_instance
    if _embedder_instance is None:
        _embedder_instance = Embedder()
    return _embedder_instance
