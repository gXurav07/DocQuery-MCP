# DocQuery MCP 📄

DocQuery MCP is a local Model Context Protocol server that answers natural language questions over a folder of PDF documents. On startup, it parses the PDFs, rebuilds a ChromaDB index, and exposes a `query_documents` MCP tool with source citations.

The implementation is intentionally local-first: no hosted vector database, no required LLM API key, and no cloud deployment needed.

Additional documentation:

- 🛠️ [Setup and Testing](docs/SETUP_AND_TESTING.md)
- 💬 [Example Interaction Log](docs/INTERACTION_LOG.md)
- 🧭 [Repository Structure](docs/PROJECT_NOTES.md)
- ✨ [Vibe Coding Setup](docs/VIBE_CODING.md)

## First Run 🚀

For a user who only wants to run the MCP server:

```bash
git clone <repo-url>
cd DocQuery-MCP

python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Put the PDFs to query in:

```text
data/pdfs/
```

Then point your MCP client at:

```text
/absolute/path/to/DocQuery-MCP/scripts/run_mcp_server.sh
```

On startup, the server rebuilds the local Chroma index and exposes the `query_documents` tool.
The first run may need internet access to download the embedding model.

## Tech Stack 🧰

- **Language:** Python 3.11+
- **MCP framework:** `mcp` Python SDK with FastMCP
- **PDF parsing:** PyMuPDF
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
- **Vector store:** ChromaDB persistent local store
- **Answering:** extractive grounded answerer using retrieved document chunks
- **Tests:** pytest

## Architecture 🏗️

```text
data/pdfs/*.pdf
    |
    v
pdf_loader.py
    Extract page-level text with document name and page number
    |
    v
chunking.py
    Split page text into overlapping searchable chunks
    |
    v
embeddings.py
    Convert chunks and questions into normalized embedding vectors
    |
    v
vector_store.py
    Persist chunks, embeddings, and metadata in ChromaDB
    |
    v
retriever.py
    Retrieve the most relevant chunks for a question
    |
    v
answerer.py
    Build a grounded answer with document/page citations
    |
    v
server.py
    Expose query_documents through MCP
```

Key design choices:

- The server rebuilds the PDF index at startup to satisfy the assignment requirement that documents be parsed and indexed at startup or on demand.
- Every chunk stores `document_name`, `page_number`, and text so answers can cite sources.
- ChromaDB is persisted under `index/`, which is generated and can be rebuilt.
- The answerer is conservative and extractive. It returns relevant excerpts instead of fabricating a synthesized answer.

## MCP Tool Format 🔌

### `query_documents`

Retrieves relevant PDF excerpts for answering a user question.

Input schema:

```json
{
  "question": "string",
  "top_k": 5
}
```

`top_k` is optional and controls how many chunks are retrieved from ChromaDB.

Output shape:

```json
{
  "answer": "Relevant document excerpts...",
  "answering_instructions": "Answer using only the retrieved_context. Cite document_name and page_number...",
  "retrieved_context": [
    {
      "document_name": "20220630.pdf",
      "page_number": 1,
      "score": 0.244,
      "excerpt": "..."
    }
  ],
  "sources": [
    {
      "document_name": "20220630.pdf",
      "page_number": 1,
      "score": 0.244,
      "excerpt": "..."
    }
  ]
}
```

Client LLM query:

```text
You have access to an MCP tool named query_documents.

When I ask a question about the indexed PDFs:
1. Call query_documents with my question. Use top_k=5 unless I ask for broader coverage.
2. Read the returned answer and sources.
3. Synthesize a concise answer in your own words using only the retrieved evidence.
4. Do not simply paste the raw retrieved excerpts unless I explicitly ask for excerpts.
5. If the retrieved context is weak, conflicting, or does not answer the question, say that clearly.
6. Include citations for important claims.

Format your response like this:

Answer:
<direct synthesized answer>

Sources:
- <document_name>, page <page_number>, score <score>: <why this source supports the answer>
- <document_name>, page <page_number>, score <score>: <why this source supports the answer>

Keep the answer grounded. Do not use outside knowledge.
```

## MCP Client Configuration ⚙️

Example Codex MCP configuration:

```toml
[mcp_servers.nexla_docquery_mcp]
command = "/absolute/path/to/DocQuery-MCP/scripts/run_mcp_server.sh"
args = []
cwd = "/absolute/path/to/DocQuery-MCP"
```

Or add it with the Codex CLI:

```bash
codex mcp add nexla_docquery_mcp -- /absolute/path/to/DocQuery-MCP/scripts/run_mcp_server.sh
```

The server rebuilds the local document index during startup, then starts the MCP stdio server.

## Tradeoffs and Future Improvements 🚧

- **Better document filtering:** If the user mentions a specific file, date, page, or section, the retriever should filter to that document first instead of relying only on semantic similarity.
- **Hybrid search:** Combine vector search with keyword search so exact names, dates, numbers, and technical terms are not missed.
- **Smarter chunking:** Use headings, paragraphs, sections, and page boundaries where possible instead of only fixed-size chunks.
- **Reranking:** Retrieve more chunks initially, then rerank them to keep only the most relevant evidence.
- **More document coverage:** Scanned PDFs would need OCR support, and future versions could support additional document types beyond PDFs.
- **Dynamic ingestion tool:** Add an MCP tool that lets a client trigger ingestion on demand after new PDFs are added, instead of requiring server restart.
- **Incremental indexing:** Startup indexing rebuilds the local Chroma collection for predictability. A future version could add safe incremental indexing by storing file fingerprints.
