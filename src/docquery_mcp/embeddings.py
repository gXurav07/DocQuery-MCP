"""Embedding utilities for document chunks and user questions."""

from collections.abc import Sequence

import numpy as np
from sentence_transformers import SentenceTransformer

from docquery_mcp.config import settings
from docquery_mcp.schemas import DocumentChunk


class EmbeddingModel:
    """Small wrapper around SentenceTransformers.

    The rest of the app should not need to know which embedding library we use.
    It should only ask for vectors for texts, chunks, or a query.
    """

    def __init__(self, model_name: str = settings.embedding_model_name) -> None:
        self.model_name = model_name
        try:
            self._model = SentenceTransformer(model_name, local_files_only=True)
        except Exception:
            self._model = SentenceTransformer(model_name)

    def embed_texts(self, texts: Sequence[str]) -> np.ndarray:
        """Embed a list of text strings as normalized float32 vectors."""

        if not texts:
            return np.empty((0, 0), dtype=np.float32)

        embeddings = self._model.encode(
            list(texts),
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return embeddings.astype(np.float32)

    def embed_chunks(self, chunks: Sequence[DocumentChunk]) -> np.ndarray:
        """Embed document chunks using their text content."""

        return self.embed_texts([chunk.text for chunk in chunks])

    def embed_query(self, question: str) -> np.ndarray:
        """Embed one user question as a single normalized vector."""

        vectors = self.embed_texts([question])
        if vectors.shape[0] == 0:
            raise ValueError("question cannot be empty")
        return vectors[0]
