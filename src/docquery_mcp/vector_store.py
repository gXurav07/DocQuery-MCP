"""Persistent vector storage backed by ChromaDB."""

from collections.abc import Sequence
from typing import Any

import chromadb
import numpy as np

from docquery_mcp.config import settings
from docquery_mcp.schemas import DocumentChunk, RetrievedChunk


class ChromaVectorStore:
    """Stores document chunks and retrieves similar chunks for a query vector."""

    def __init__(
        self,
        persist_dir: str = str(settings.index_dir),
        collection_name: str = settings.collection_name,
    ) -> None:
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self._get_or_create_collection()

    def _get_or_create_collection(self) -> Any:
        """Open the Chroma collection used by this project."""

        return self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def reset(self) -> None:
        """Delete and recreate the collection."""

        try:
            self.client.delete_collection(self.collection_name)
        except ValueError:
            pass

        self.collection = self._get_or_create_collection()

    def add_chunks(self, chunks: Sequence[DocumentChunk], embeddings: np.ndarray) -> None:
        """Store chunks and their embeddings in Chroma."""

        if not chunks:
            return
        if len(chunks) != len(embeddings):
            raise ValueError("chunks and embeddings must have the same length")

        self.collection.add(
            ids=[chunk.chunk_id for chunk in chunks],
            documents=[chunk.text for chunk in chunks],
            embeddings=embeddings.tolist(),
            metadatas=[
                {
                    "document_name": chunk.document_name,
                    "page_number": chunk.page_number,
                }
                for chunk in chunks
            ],
        )

    def query(self, query_embedding: np.ndarray, top_k: int = settings.default_top_k) -> list[RetrievedChunk]:
        """Return the most relevant chunks for a query embedding."""

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero")

        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

        ids = results.get("ids", [[]])[0]
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        retrieved: list[RetrievedChunk] = []
        for chunk_id, text, metadata, distance in zip(ids, documents, metadatas, distances, strict=False):
            score = 1.0 - float(distance)
            retrieved.append(
                RetrievedChunk(
                    chunk=DocumentChunk(
                        chunk_id=chunk_id,
                        document_name=str(metadata["document_name"]),
                        page_number=int(metadata["page_number"]),
                        text=text,
                    ),
                    score=score,
                )
            )

        return retrieved
