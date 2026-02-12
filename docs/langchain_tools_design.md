# LangChain Design Reference

This document explains how each implemented module aligns with LangChain interfaces, how modules compose into a RAG workflow, and where to extend next.

## 1. Tooling Layer (`tools/`)

### `tools/base_tool.py`
Purpose:
- Shared base class for custom tools.
- Inherits from `langchain_core.tools.BaseTool`.

LangChain contract:
- Uses tool metadata (`name`, `description`) and `_run` for sync execution.
- Supports `invoke` and schema validation through Pydantic models.

Why it matters:
- Any subclass can be plugged directly into LangChain agent executors.

### `tools/search_tool.py` (`SearchNewsTool`)
Purpose:
- Fetch news by ticker/keyword from Yahoo Finance.
- Prefer `yfinance`, fallback to Yahoo HTTP search endpoint.

Input schema:
- `query: str`
- `limit: int > 0`

Output:
- `List[Dict[str, Any]]` with keys: `title`, `link`, `publisher`, `published`, `type`

LangChain contract:
- Declares `args_schema` and `_run`.
- Called via `tool.invoke({...})`.

Notes:
- Timestamps are normalized when possible.
- Output is already suitable for downstream RAG services.

### `tools/database_tool.py` (`DatabaseTool`)
Purpose:
- Local SQLite portfolio CRUD operations.

Supported actions:
- `get`, `upsert`, `delete`, `select`

LangChain contract:
- Action-routed through `_run`.
- Returns serializable dictionaries/lists for agent messaging.

### `tools/function_tools/summarize_tool.py` (`SummarizeTool`)
Purpose:
- Lightweight extractive summarization.

LangChain contract:
- Uses `args_schema` + `_run`.
- Works as a deterministic utility tool in chains.

## 2. Retrieval and Sentiment Services (`services/`)

### `services/vector_store_service.py` (`TfidfVectorStore`)
Purpose:
- Minimal in-memory vector store implementing LangChain `VectorStore`.

Key methods:
- `from_texts(...)`
- `add_texts(...)`
- `similarity_search(...)`
- `similarity_search_with_score(...)`

Retrieval details:
- TF-IDF vectors built in pure Python.
- Similarity uses cosine similarity.

Why it matters:
- Supports local RAG and testability without external vector databases.

### `services/news_sentiment_service.py` (`NewsSentimentRAGService`)
Purpose:
- Predict sentiment from search output using retrieval over labeled sentiment data.

RAG steps:
1. Build retrieval index from `data/data.csv` (`Sentence`, `Sentiment`).
2. For each article title/summary, retrieve top-k similar labeled samples.
3. Compute weighted label vote from retrieved neighbors.
4. Return per-article sentiment and aggregate portfolio-level sentiment signal.

Public API:
- `predict_text(text, evidence_k=3)`
- `predict_article(article, evidence_k=3)`
- `predict_from_search_results(articles, evidence_k=3)`

Output shape:
- Per-article: `sentiment`, `confidence`, `sentiment_score`, `retrieved_examples`
- Aggregate: `overall_sentiment`, `overall_score`, `counts`, `articles`, `skipped`

## 3. Data Pipeline (`data/`)

### `data/embedding_pipeline.py`
Purpose:
- Build embeddings JSONL from Kaggle sentiment CSV using the same TF-IDF implementation as runtime retrieval.

Why this matters for LangChain:
- Offline preprocessing and online retrieval use the same vector logic.
- Reduces train/serve mismatch for local experiments.

## 4. End-to-End Flow

```text
Ticker query -> SearchNewsTool -> article list
           -> NewsSentimentRAGService -> per-article sentiment + aggregate sentiment
```

Optional additions:
- Attach `DatabaseTool` to include user holdings context.
- Add `SummarizeTool` before/after sentiment scoring for user-facing reports.
- Wrap flow in a LangGraph orchestrator node graph.

## 5. Interface Conventions

- Tool calls use `.invoke({...})`.
- Tool/service outputs should be JSON-serializable.
- Keep `_run` synchronous unless async is required.
- Prefer explicit schemas (`args_schema`) for agent reliability.

## 6. Testing Strategy

Current tests cover:
- Tools (`search`, `database`, `summarize`)
- Retrieval (`TfidfVectorStore`)
- RAG sentiment (`NewsSentimentRAGService`)
- Utility helpers

Recommended additions:
- Golden tests for sentiment drift on fixed fixture inputs.
- Contract tests for tool payload shape.
- Integration tests for future LangGraph orchestrator.

## 7. Known Gaps and Planned Extensions

- Agent and orchestrator modules are currently scaffold-only.
- No production retriever backend yet (Chroma/Pinecone/FAISS).
- No LLM reasoning layer yet for explanation synthesis.

This codebase is intentionally local-first and deterministic, then extendable to full agentic LangChain/LangGraph deployment.
