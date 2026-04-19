"""
FAISS Vector Store for RAG retrieval.
Stores and retrieves fact-check documents based on semantic similarity.
"""

import json
import faiss
import numpy as np
from pathlib import Path
from typing import Optional

from config.settings import FAISS_INDEX_PATH, TOP_K_RETRIEVAL
from rag.embedder import get_embedder, Embedder
from rag.data_loader import get_fact_check_data, format_doc_for_retrieval

# Minimum similarity score (0.0 - 1.0) to consider a match relevant
SIMILARITY_THRESHOLD = 0.50


class FAISSVectorStore:
    """FAISS-based vector store for fact-check retrieval."""

    def __init__(self, index_path: str = FAISS_INDEX_PATH):
        """Initialize the vector store."""
        self.index_path = Path(index_path)
        self.embedder: Optional[Embedder] = None
        self.index = None
        self.documents = []
        self.doc_embeddings = []

    def initialize(self):
        """Initialize the vector store with fact-check data."""
        print("Initializing FAISS vector store...")

        # Get embedder
        self.embedder = get_embedder()

        # Load or create index
        if self._load_index():
            print(f"Loaded existing index from {self.index_path}")
        else:
            print("Creating new index with fact-check data...")
            self._build_index()
            self._save_index()

    def _build_index(self):
        """Build FAISS index from fact-check database."""
        # Get all fact-check documents
        fact_data = get_fact_check_data()

        # Format documents for storage
        self.documents = [format_doc_for_retrieval(doc) for doc in fact_data]

        # Generate embeddings
        print(f"Generating embeddings for {len(self.documents)} documents...")
        embeddings = np.array(self.embedder.embed_batch(self.documents), dtype=np.float32)

        # Normalize embeddings for Cosine Similarity (using Inner Product index)
        faiss.normalize_L2(embeddings)
        self.doc_embeddings = embeddings.tolist()

        # Create FAISS index (using Inner Product / Cosine Similarity)
        dimension = self.embedder.dimension
        self.index = faiss.IndexFlatIP(dimension)

        # Add embeddings to index
        self.index.add(embeddings)

        print(f"Index built with {self.index.ntotal} documents")

    def _load_index(self) -> bool:
        """Try to load existing index from disk."""
        index_file = self.index_path / "faiss.index"
        docs_file = self.index_path / "documents.json"
        embeds_file = self.index_path / "embeddings.npy"

        if not (index_file.exists() and docs_file.exists() and embeds_file.exists()):
            return False

        try:
            # Load documents
            with open(docs_file, 'r') as f:
                self.documents = json.load(f)

            # Load embeddings
            self.doc_embeddings = np.load(embeds_file).tolist()

            # Load FAISS index
            self.index = faiss.read_index(str(index_file))

            # Initialize embedder
            self.embedder = get_embedder()

            return True
        except Exception as e:
            print(f"Error loading index: {e}")
            return False

    def _save_index(self):
        """Save index to disk."""
        # Create directory if needed
        self.index_path.mkdir(parents=True, exist_ok=True)

        # Save documents
        docs_file = self.index_path / "documents.json"
        with open(docs_file, 'w') as f:
            json.dump(self.documents, f, indent=2)

        # Save embeddings
        embeds_file = self.index_path / "embeddings.npy"
        np.save(embeds_file, np.array(self.doc_embeddings))

        # Save FAISS index
        index_file = self.index_path / "faiss.index"
        faiss.write_index(self.index, str(index_file))

        print(f"Index saved to {self.index_path}")

    def retrieve(self, query: str, top_k: int = TOP_K_RETRIEVAL) -> list[dict]:
        """Retrieve top-k most relevant documents for a query."""
        if self.index is None or self.embedder is None:
            self.initialize()

        # Generate query embedding
        query_embedding = np.array(
            self.embedder.embed(query),
            dtype=np.float32
        ).reshape(1, -1)

        # Normalize query embedding for Cosine Similarity
        faiss.normalize_L2(query_embedding)

        # Search index
        k = min(top_k, self.index.ntotal)
        scores, indices = self.index.search(query_embedding, k)

        # Build results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.documents):
                score = float(scores[0][i])
                
                # Filter results based on similarity threshold
                if score < SIMILARITY_THRESHOLD:
                    continue
                    
                # Convert score to percentage for UI (0.0-1.0 -> 0-100)
                results.append({
                    "document": self.documents[idx],
                    "score": score,
                    "match_percentage": round(score * 100, 1),
                    "doc_index": int(idx)
                })

        return results

    def retrieve_for_claims(self, claims: list[str], top_k: int = TOP_K_RETRIEVAL) -> dict:
        """Retrieve relevant documents for multiple claims."""
        results = {}
        for claim in claims:
            results[claim] = self.retrieve(claim, top_k)
        return results

    def search(self, query: str, top_k: int = TOP_K_RETRIEVAL) -> list[dict]:
        """Alias for retrieve method."""
        return self.retrieve(query, top_k)

    @property
    def document_count(self) -> int:
        """Return number of documents in the index."""
        return self.index.ntotal if self.index else 0


# Global vector store instance
_vector_store_instance = None


def get_vector_store() -> FAISSVectorStore:
    """Get or create the global vector store instance."""
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = FAISSVectorStore()
        _vector_store_instance.initialize()
    return _vector_store_instance


def initialize_vector_store():
    """Initialize the vector store (call at app startup)."""
    return get_vector_store()
