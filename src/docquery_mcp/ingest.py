"""Document ingestion pipeline.

Ingestion turns PDFs into searchable vectors:

PDF pages -> text chunks -> embeddings -> ChromaDB collection
"""

from dataclasses import dataclass
from pathlib import Path

from docquery_mcp.chunking import chunk_pages
from docquery_mcp.config import settings
from docquery_mcp.embeddings import EmbeddingModel
from docquery_mcp.pdf_loader import load_pdf_directory
from docquery_mcp.vector_store import ChromaVectorStore


@dataclass(frozen=True)
class IngestionResult:
    """Summary of one indexing run."""

    pdf_count: int
    page_count: int
    chunk_count: int
    index_dir: Path


def ingest_documents(
    pdf_dir: Path = settings.pdf_dir,
    index_dir: Path = settings.index_dir,
    reset_index: bool = True,
) -> IngestionResult:
    """Parse PDFs, create embeddings, and persist them in ChromaDB."""

    if not pdf_dir.exists():
        raise FileNotFoundError(f"PDF directory does not exist: {pdf_dir}")

    pdf_paths = sorted(pdf_dir.glob("*.pdf"))
    if not pdf_paths:
        raise ValueError(f"No PDF files found in: {pdf_dir}")

    index_dir.mkdir(parents=True, exist_ok=True)

    pages = load_pdf_directory(pdf_dir)
    chunks = chunk_pages(
        pages=pages,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )

    embedding_model = EmbeddingModel()
    embeddings = embedding_model.embed_chunks(chunks)

    vector_store = ChromaVectorStore(persist_dir=str(index_dir))
    if reset_index:
        vector_store.reset()

    vector_store.add_chunks(chunks, embeddings)

    return IngestionResult(
        pdf_count=len(pdf_paths),
        page_count=len(pages),
        chunk_count=len(chunks),
        index_dir=index_dir,
    )
