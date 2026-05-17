# Vibe Coding Setup

I used Codex as an AI coding partner while building this project. I worked file by file so I could understand the system instead of generating a large codebase all at once.

## What Worked Well

- Asking Codex to propose the architecture first helped me keep the implementation small and aligned with the assignment.
- Building one module at a time made the flow easier to reason about: schemas, PDF loading, chunking, embeddings, vector store, retrieval, answer formatting, then MCP.
- Codex was useful for catching practical issues, such as Python import paths, Pylance typing warnings, MCP command configuration, and reviewer-facing README structure.

## Where I Corrected or Directed the AI

- I switched the vector store choice to ChromaDB because it is simple and assignment-friendly.
- I asked for startup indexing after re-reading the requirement that documents must be indexed at startup or on demand.
- I kept the answerer extractive for reliability rather than adding an LLM synthesis layer that could hallucinate.
- I renamed scripts and clarified command names to make the repo more understandable for a reviewer.

## My View on AI-Assisted Engineering

AI tools are strongest when used as a fast collaborator for scaffolding, debugging, and explaining tradeoffs. They do not replace engineering judgment. I still had to decide what to optimize for: local runnability, source attribution, MCP compliance, and an implementation a reviewer can understand quickly.
