# LangChain Tooling & Data Services Design

This document explains the purpose, interfaces, and LangChain alignment for each Python module added/modified in this project.

## tools/base_tool.py
- **What it does:** Wraps `langchain_core.tools.BaseTool` to give every custom tool a shared logger and relaxed Pydantic v2 config (`extra="allow"`, `arbitrary_types_allowed=True`). Adds a default `logger` field.
- **Why it fits LangChain:** Tools in LangChain must inherit from `BaseTool` (or implement the same model interface) to be serializable and runnable inside agents/executors. Using the LangChain base keeps compatibility with tool invocation (`.invoke`, `.batch`, pipelines) and Pydantic validation.

## tools/search_tool.py (SearchNewsTool)
- **What it does:** Fetches news for a ticker/keyword using `yfinance` when available, otherwise a lightweight Yahoo Finance HTTP endpoint. Normalizes timestamps to ISO 8601. Exposes `Args` schema for validation and can be invoked via LangChain (`tool.invoke`).
- **LangChain alignment:** Implements `_run`, sets `args_schema`, `name`, `description`, and `return_direct` so the tool can be auto-routed by LangChain agents. Accepts dependency injection of `fetcher` to stay deterministic in tests and sandboxed runs.

## tools/database_tool.py (DatabaseTool)
- **What it does:** SQLite-backed portfolio store with actions: `get`, `select`, `upsert`, `delete`. Enforces schema creation, ISO timestamps, symbol uppercasing, and basic validation. Supports imperative helpers plus LangChain `_run` path.
- **LangChain alignment:** Uses `args_schema` and `_run` to make database operations callable from chains/agents while keeping return values JSON-serializable. `return_direct=True` allows immediate response streaming when used in tool-using agents.

## tools/function_tools/summarize_tool.py (SummarizeTool)
- **What it does:** Lightweight extractive summarizer using frequency scoring, stopwords filtering, and sentence ranking. Returns top-N sentences.
- **LangChain alignment:** Declares `args_schema`, `_run`, `return_direct` for plug-and-play in LangChain tool collections; pure-Python logic keeps the tool fast and dependency-light for synchronous agent calls.

## services/vector_store_service.py (TfidfVectorStore)
- **What it does:** In-memory TF‑IDF `VectorStore` that returns LangChain `Document` objects and supports `from_texts`, `similarity_search`, and `similarity_search_with_score`.
- **LangChain alignment:** Implements the abstract `VectorStore` contract (methods `from_texts`, `similarity_search`) so it can be dropped into retrievers, LCEL chains, or agents. Uses cosine similarity over TF‑IDF vectors—simple, dependency-free, and deterministic for tests.

## data/embedding_pipeline.py
- **What it does:** CLI pipeline that loads the Kaggle Financial Sentiment CSV, builds a `TfidfVectorStore`, and writes JSONL rows containing text, metadata, vector, and vocabulary into `data/embeddings/`.
- **LangChain alignment:** Reuses the same vector store interface used at runtime, ensuring parity between offline preprocessing and online retrieval. Output vectors are deterministic and portable.

## utils/logger.py
- **What it does:** Provides `get_logger` to create non-propagating, leveled loggers with consistent formatting.
- **LangChain alignment:** Tools/services accept an optional logger; this helper ensures safe default logging without forcing users to configure logging globally.

## utils/retry.py
- **What it does:** Decorator for exponential backoff retries.
- **LangChain alignment:** Useful for wrapping network-bound tool/service calls used inside chains without coupling to external libraries.

## utils/helpers.py
- **What it does:** Formatting helpers (currency, percent), safe nested getter, whitespace normalizer, date parsing, and cosine similarity.
- **LangChain alignment:** Keeps small, serializable utility functions close to tools/services, avoiding heavyweight dependencies while supporting retrieval and response formatting in chains.

## tests/
- **What they cover:** Unit tests for helpers, summarizer, search tool, database tool, and vector store. Tests exercise `tool.invoke` and LangChain-facing interfaces to guard compatibility with LCEL/agents.

## Design Choices for LangChain Compatibility
- **Pydantic v2 schemas:** Every tool defines an inner `Args` model and sets `args_schema` so LangChain can validate inputs and auto-generate tool descriptions for agents.
- **`_run` over `execute`:** LangChain invokes `_run`/`_arun`; keeping a thin `execute` wrapper preserves old imperative use while making tools runnable in LCEL.
- **`return_direct=True`:** Lets agent executors return tool output immediately when appropriate (search, summarize, DB ops), mirroring common LangChain tool patterns.
- **Serializable returns:** Tools return plain dict/list/str types to remain JSON-serializable for agent messaging and tracing.
- **Dependency-light:** TF‑IDF vector store and summarizer avoid heavy ML deps, speeding local runs and tests while remaining pluggable with LangChain retrievers if you later swap to an embedding model-backed store.

