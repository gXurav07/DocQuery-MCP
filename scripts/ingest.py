"""Build the local Chroma index from PDFs."""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from docquery_mcp.config import settings
from docquery_mcp.ingest import ingest_documents


def parse_args() -> argparse.Namespace:
    """Parse command-line options for ingestion."""

    parser = argparse.ArgumentParser(description="Index PDFs for DocQuery MCP.")
    parser.add_argument(
        "--pdf-dir",
        type=Path,
        default=settings.pdf_dir,
        help=f"Directory containing PDFs. Default: {settings.pdf_dir}",
    )
    parser.add_argument(
        "--index-dir",
        type=Path,
        default=settings.index_dir,
        help=f"Directory where Chroma stores the index. Default: {settings.index_dir}",
    )
    parser.add_argument(
        "--keep-existing",
        action="store_true",
        help="Append to the existing Chroma collection instead of recreating it.",
    )
    return parser.parse_args()


def main() -> None:
    """Run ingestion and print a short summary."""

    args = parse_args()
    result = ingest_documents(
        pdf_dir=args.pdf_dir,
        index_dir=args.index_dir,
        reset_index=not args.keep_existing,
    )

    print("Ingestion complete")
    print(f"PDFs indexed: {result.pdf_count}")
    print(f"Pages indexed: {result.page_count}")
    print(f"Chunks indexed: {result.chunk_count}")
    print(f"Index directory: {result.index_dir}")


if __name__ == "__main__":
    main()
