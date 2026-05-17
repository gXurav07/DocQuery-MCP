"""Text chunking utilities for retrieved document context."""

from docquery_mcp.schemas import DocumentChunk, PdfPage


def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """Split text into overlapping character chunks."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks: list[str] = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - chunk_overlap

    return chunks


def chunk_page(page: PdfPage, chunk_size: int, chunk_overlap: int) -> list[DocumentChunk]:
    """Convert one extracted PDF page into searchable chunks."""

    text_chunks = chunk_text(page.text, chunk_size, chunk_overlap)
    chunks: list[DocumentChunk] = []

    for index, text in enumerate(text_chunks):
        chunk_id = f"{page.document_name}:page-{page.page_number}:chunk-{index + 1}"
        chunks.append(
            DocumentChunk(
                chunk_id=chunk_id,
                document_name=page.document_name,
                page_number=page.page_number,
                text=text,
            )
        )

    return chunks


def chunk_pages(
    pages: list[PdfPage],
    chunk_size: int,
    chunk_overlap: int,
) -> list[DocumentChunk]:
    """Convert many extracted PDF pages into searchable chunks."""

    chunks: list[DocumentChunk] = []

    for page in pages:
        chunks.extend(chunk_page(page, chunk_size, chunk_overlap))

    return chunks
