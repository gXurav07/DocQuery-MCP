"""Grounded answer generation from retrieved document chunks."""

from docquery_mcp.schemas import QueryResult, RetrievedChunk, SourceCitation


class ExtractiveAnswerer:
    """Creates a conservative answer directly from retrieved context.

    This baseline avoids unsupported claims by returning the most relevant
    excerpts with source citations. A later LLM-backed answerer can reuse the
    same input and output schema.
    """

    def answer(self, question: str, retrieved_chunks: list[RetrievedChunk]) -> QueryResult:
        """Build a grounded answer and citation list for a user question."""

        cleaned_question = question.strip()
        if not cleaned_question:
            raise ValueError("question cannot be empty")

        if not retrieved_chunks:
            return QueryResult(
                answer="I could not find relevant information in the indexed documents.",
                sources=[],
            )

        sources = [self._to_citation(chunk) for chunk in retrieved_chunks]
        answer = self._build_extractive_answer(retrieved_chunks)

        return QueryResult(answer=answer, sources=sources)

    def _build_extractive_answer(self, retrieved_chunks: list[RetrievedChunk]) -> str:
        """Create a readable answer from the top retrieved excerpts."""

        excerpts = []
        for index, retrieved in enumerate(retrieved_chunks[:3], start=1):
            chunk = retrieved.chunk
            excerpt = self._shorten(chunk.text)
            excerpts.append(
                f"{index}. {excerpt} "
                f"(Source: {chunk.document_name}, page {chunk.page_number}, "
                f"score {retrieved.score:.3f})"
            )

        return "Relevant document excerpts:\n" + "\n".join(excerpts)

    def _to_citation(self, retrieved: RetrievedChunk) -> SourceCitation:
        """Convert a retrieved chunk into a public source citation."""

        return SourceCitation(
            document_name=retrieved.chunk.document_name,
            page_number=retrieved.chunk.page_number,
            score=retrieved.score,
            excerpt=self._shorten(retrieved.chunk.text),
        )

    def _shorten(self, text: str, max_length: int = 500) -> str:
        """Trim long text while keeping excerpts readable."""

        normalized = " ".join(text.split())
        if len(normalized) <= max_length:
            return normalized

        return normalized[: max_length - 3].rstrip() + "..."
