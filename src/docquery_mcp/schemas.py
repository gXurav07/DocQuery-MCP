"""Shared data models for the document Q&A pipeline.

These classes describe the objects that move between ingestion, retrieval,
answer generation, and the MCP tool response.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PdfPage:
    """Text extracted from one page of a PDF."""

    document_name: str
    page_number: int
    text: str


@dataclass(frozen=True)
class DocumentChunk:
    """A searchable piece of text extracted from a PDF."""

    chunk_id: str
    document_name: str
    page_number: int
    text: str


@dataclass(frozen=True)
class RetrievedChunk:
    """A document chunk returned by vector search, with its similarity score."""

    chunk: DocumentChunk
    score: float


@dataclass(frozen=True)
class SourceCitation:
    """A source reference shown to the user with every answer."""

    document_name: str
    page_number: int
    score: float
    excerpt: str


@dataclass(frozen=True)
class QueryResult:
    """The final answer payload returned by the MCP query tool."""

    answer: str
    sources: list[SourceCitation]
