"""Configuration values for the local document Q&A server."""

from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    """Runtime settings used across ingestion, retrieval, and MCP serving."""

    pdf_dir: Path = PROJECT_ROOT / "data" / "pdfs"
    index_dir: Path = PROJECT_ROOT / "index"
    collection_name: str = "docquery_documents"
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    default_top_k: int = 5
    chunk_size: int = 900
    chunk_overlap: int = 150


settings = Settings()
