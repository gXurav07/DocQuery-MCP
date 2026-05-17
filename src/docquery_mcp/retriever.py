"""Question retrieval over the indexed document chunks."""

from docquery_mcp.config import settings
from docquery_mcp.embeddings import EmbeddingModel
from docquery_mcp.schemas import RetrievedChunk
from docquery_mcp.vector_store import ChromaVectorStore


class DocumentRetriever:
    """Finds document chunks that are relevant to a user question."""

    def __init__(
        self,
        embedding_model: EmbeddingModel | None = None,
        vector_store: ChromaVectorStore | None = None,
    ) -> None:
        self.embedding_model = embedding_model or EmbeddingModel()
        self.vector_store = vector_store or ChromaVectorStore()

    def retrieve(
        self,
        question: str,
        top_k: int = settings.default_top_k,
    ) -> list[RetrievedChunk]:
        """Return the most relevant chunks for a natural language question."""

        cleaned_question = question.strip()
        if not cleaned_question:
            raise ValueError("question cannot be empty")

        query_embedding = self.embedding_model.embed_query(cleaned_question)
        return self.vector_store.query(query_embedding, top_k=top_k)
