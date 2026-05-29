# Project Spec RAG Manager

This tool parses Word (.docx) and Excel (.xlsx) specifications and builds/queries a local RAG database using either ChromaDB or SQLite.

## CLI Features & Ingestion

- **Multi-format Support**: Ingests Word (.docx) documents (preserving paragraph styles and markdown tables) and Excel (.xlsx) spreadsheets (ingesting worksheet rows dynamically as structured key-value pairs).
- **Batching Support**: Automatically chunks large quantities of records into sub-batches of 2000 items to bypass ChromaDB's max batch limit of 5461 entries.

## CLI Usage

### Build / Refresh Database

To build a ChromaDB vector database (this will also automatically generate the SQLite database at the same time):
```powershell
python ./.agent/skills_internal/skill_rag/skill_rag.py --config ./rag_doc_gg/rag_project_gg.json --build --db-type chroma
```

To build only the SQLite database:
```powershell
python ./.agent/skills_internal/skill_rag/skill_rag.py --config ./rag_doc_gg/rag_project_gg.json --build --db-type sqlite
```

### Querying the Database

Query using ChromaDB (semantic search):
```powershell
python ./.agent/skills_internal/skill_rag/skill_rag.py --config ./rag_doc_gg/rag_project_gg.json --query "your question here" --db-type chroma
```

Query using SQLite (keyword search):
```powershell
python ./.agent/skills_internal/skill_rag/skill_rag.py --config ./rag_doc_gg/rag_project_gg.json --query "your question here" --db-type sqlite
```

## CLI Parameters

- `--config`: Absolute or relative path to the project configuration JSON file (e.g., `./rag_doc_gg/rag_project_gg.json`).
- `--db-type`: Choice of `"chroma"` or `"sqlite"` (Default: `"chroma"`). Note: `"chroma"` option builds both ChromaDB and SQLite databases during the build phase.
- `--build`: Refreshes and rebuilds the database index from scratch.
- `--query`: Query string to execute against the spec database.