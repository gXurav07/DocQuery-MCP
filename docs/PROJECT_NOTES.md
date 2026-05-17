# Repository Structure

This document covers the repository layout.

## Repository Layout

```text
src/docquery_mcp/
  server.py        MCP server and query_documents tool
  ingest.py        Startup/manual indexing pipeline
  pdf_loader.py    PDF text extraction
  chunking.py      Page-to-chunk splitting
  embeddings.py    SentenceTransformer wrapper
  vector_store.py  ChromaDB persistence and search
  retriever.py     Question-to-context retrieval
  answerer.py      Grounded extractive answer formatting
  schemas.py       Shared dataclasses

scripts/
  build_index.py       Optional manual index builder
  qa_loop.py           Optional interactive local smoke test
  run_mcp_server.sh    Stable launcher for MCP clients

tests/
  Unit tests for chunking, PDF loading, answer formatting, and tool registration
```
