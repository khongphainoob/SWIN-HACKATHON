# LangChain Financial News Sentiment System

## Overview
This repository is a LangChain-oriented project for financial news analysis.
It combines:
- Tool calling (`SearchNewsTool`, `DatabaseTool`, `SummarizeTool`)
- Retrieval (`TfidfVectorStore`)
- RAG sentiment inference (`NewsSentimentRAGService`)

Primary use case:
1. Fetch market news for a ticker.
2. Retrieve similar labeled sentiment examples from the Kaggle financial sentiment dataset.
3. Return per-article and aggregate sentiment for decision support.

## Current Capabilities
- LangChain-compatible custom tools in `tools/`
- Lightweight TF-IDF vector store in `services/vector_store_service.py`
- RAG sentiment service for news outputs in `services/news_sentiment_service.py`
- Local embedding build pipeline in `data/embedding_pipeline.py`
- Unit tests for core tools/services in `tests/`

## Repository Layout
- `agents/`: Agent interfaces and agent scaffolding
- `orchestrators/`: Orchestrator interfaces (LangGraph-ready scaffold)
- `protocols/`: Protocol interfaces for structured agent communication
- `tools/`: LangChain tools and tool-specific utility modules
- `services/`: Retrieval and analysis services used by tools/agents
- `memory/`: Memory abstractions and sample implementations
- `data/`: Dataset and embedding outputs
- `scripts/`: Demo scripts and local execution entry points
- `docs/`: Technical design notes
- `tests/`: Unit tests for LangChain interfaces and business logic

## Quickstart
### 1. Create environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -U pip
pip install langchain-core pydantic requests yfinance pytest
```

### 3. Run tests
```bash
python3 -m pytest -q
```

### 4. Run end-to-end demo
```bash
python3 scripts/test_news.py
```

The demo does:
- `SearchNewsTool.invoke({"query": "NVDA", "limit": 5})`
- `NewsSentimentRAGService.predict_from_search_results(...)`

## LangChain Usage Pattern
Use `.invoke(...)` for tools and return JSON-serializable payloads.

```python
from tools.search_tool import SearchNewsTool
from services.news_sentiment_service import NewsSentimentRAGService

search_tool = SearchNewsTool()
sentiment_service = NewsSentimentRAGService()

articles = search_tool.invoke({"query": "AAPL", "limit": 5})
report = sentiment_service.predict_from_search_results(articles, evidence_k=3)
print(report["overall_sentiment"], report["counts"])
```

## Design Principles
- Keep dependencies small and local-first.
- Keep interfaces compatible with `langchain_core` (`BaseTool`, `VectorStore`, `invoke`).
- Keep outputs deterministic and testable when possible.
- Keep intermediate results JSON-serializable for tracing and agent handoff.

## Next Steps
See `Task.md` for the LangChain roadmap (agent graph, protocols, memory, and production hardening).
