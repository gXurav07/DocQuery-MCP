"""PDF loading utilities.

This module extracts text page by page. Keeping page boundaries is important
because citations should point users back to a document and page number.
"""

from pathlib import Path

import fitz

from docquery_mcp.schemas import PdfPage


def load_pdf_pages(pdf_path: Path) -> list[PdfPage]:
    """Extract text from every page in a single PDF file."""

    pages: list[PdfPage] = []

    with fitz.open(pdf_path) as document:
        for page_index in range(document.page_count):
            page = document.load_page(page_index)
            raw_text = page.get_text("text")
            text = raw_text.strip() if isinstance(raw_text, str) else ""
            if not text:
                continue

            pages.append(
                PdfPage(
                    document_name=pdf_path.name,
                    page_number=page_index + 1,
                    text=text,
                )
            )

    return pages


def load_pdf_directory(pdf_dir: Path) -> list[PdfPage]:
    """Extract text from all PDFs in a directory."""

    pdf_paths = sorted(pdf_dir.glob("*.pdf"))
    pages: list[PdfPage] = []

    for pdf_path in pdf_paths:
        pages.extend(load_pdf_pages(pdf_path))

    return pages
