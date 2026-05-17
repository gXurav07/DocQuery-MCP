# Setup and Testing

This guide covers installing dependencies, running tests, starting the MCP server, and using the local manual QA loop.

## Setup

1. Create and activate a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install the project.

```bash
pip install -e ".[dev]"
```

3. Put the provided PDFs in:

```text
data/pdfs/
```

4. Run tests.

```bash
pytest
```

5. Start the MCP server.

```bash
python -m docquery_mcp.server
```

The server rebuilds the document index during startup. The first run may take longer because `sentence-transformers` downloads and caches the embedding model.

For MCP clients that require a single executable command, use:

```bash
scripts/run_mcp_server.sh
```

## Optional Manual QA

You can test retrieval without an MCP client:

```bash
python scripts/build_index.py
python scripts/qa_loop.py
```

Type a question, then type `exit` to stop.

## Verification Commands

```bash
python -m compileall src/docquery_mcp scripts tests
pytest
ruff check src tests scripts
```

Expected test result:

```text
9 passed
```

## Generated Files

These are intentionally not committed:

- `.venv/` or other virtual environments
- `index/` ChromaDB data
- `*.egg-info/`
- `__pycache__/`
- local editor/MCP config files
