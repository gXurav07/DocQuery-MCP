DocQuery-MCP/
├── README.md
├── examples.md
├── pyproject.toml
├── .env.example
├── .gitignore
├── data/
│   └── pdfs/
│       └── .gitkeep
├── index/
│   └── .gitkeep
├── src/
│   └── docquery_mcp/
│       ├── __init__.py
│       ├── server.py
│       ├── config.py
│       ├── ingest.py
│       ├── pdf_loader.py
│       ├── chunking.py
│       ├── embeddings.py
│       ├── vector_store.py
│       ├── retriever.py
│       ├── answerer.py
│       ├── schemas.py
│       └── logging_config.py
├── scripts/
│   ├── ingest.py
│   └── smoke_test.py
└── tests/
    ├── test_chunking.py
    ├── test_pdf_loader.py
    ├── test_retriever.py
    └── test_tool_schema.py



chunking.py
Splits text into overlapping chunks while preserving page/document metadata.

embeddings.py
Wraps embedding model calls.

vector_store.py
Builds, saves, loads, and queries FAISS index.

retriever.py
Retrieves relevant chunks for a question.

answerer.py
Turns retrieved chunks into a grounded answer. Can use OpenAI if configured, otherwise fallback to extractive answer.

schemas.py
Typed request/response objects for tool output and citations.

scripts/ingest.py
Manual index builder.