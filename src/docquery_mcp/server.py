"""MCP server exposing document Q&A tools."""

from __future__ import annotations

import sys
from dataclasses import asdict
from pathlib import Path
from typing import TYPE_CHECKING, Any

if __package__ is None or __package__ == "":
    src_dir = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(src_dir))

from mcp.server.fastmcp import FastMCP

from docquery_mcp.config import settings
from docquery_mcp.schemas import QueryResult

if TYPE_CHECKING:
    from docquery_mcp.answerer import ExtractiveAnswerer
    from docquery_mcp.retriever import DocumentRetriever


mcp = FastMCP("docquery-mcp")

_retriever: DocumentRetriever | None = None
_answerer: ExtractiveAnswerer | None = None


def get_retriever() -> DocumentRetriever:
    """Create the retriever only when the first query arrives."""

    global _retriever
    if _retriever is None:
        from docquery_mcp.retriever import DocumentRetriever

        _retriever = DocumentRetriever()
    return _retriever


def get_answerer() -> ExtractiveAnswerer:
    """Create the answerer only when the first query arrives."""

    global _answerer
    if _answerer is None:
        from docquery_mcp.answerer import ExtractiveAnswerer

        _answerer = ExtractiveAnswerer()
    return _answerer


def serialize_result(result: QueryResult) -> dict[str, Any]:
    """Convert a QueryResult dataclass into an MCP-friendly dictionary."""

    return asdict(result)


@mcp.tool()
def query_documents(question: str, top_k: int = settings.default_top_k) -> dict:
    """Answer a natural language question using the indexed PDF documents.

    Args:
        question: The user's natural language question.
        top_k: Number of relevant chunks to retrieve from the document index.
    """

    retrieved_chunks = get_retriever().retrieve(question=question, top_k=top_k)
    result = get_answerer().answer(question=question, retrieved_chunks=retrieved_chunks)
    return serialize_result(result)


def main() -> None:
    """Run the MCP server over stdio for local MCP clients."""

    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        print("DocQuery MCP server stopped.", file=sys.stderr)


if __name__ == "__main__":
    main()
