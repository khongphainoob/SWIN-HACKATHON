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
# On Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -U pip
pip install -r requirements.txt
```

**📦 Core Dependencies:**
- `langchain-core` - LangChain abstractions
- `langgraph` - Agentic workflow orchestration
- `pydantic` - Data validation
- `yfinance` - Market data
- `pytest` - Testing framework
- `python-dotenv` - Environment variable management

See [INSTALL.md](INSTALL.md) for detailed installation guide.

### 3. Configure API Keys (Required)

**Quick Setup (< 2 min):**

```powershell
# 1. Create .env file
copy .env.example .env

# 2. Get free API key (choose one)
# Option A: Gemini (recommended, free)
#   → https://makersuite.google.com/app/apikey
#   → Login → Create API Key → Copy to .env

# Option B: Groq (fast, free)
#   → https://console.groq.com/
#   → Sign Up → API Keys → Create → Copy to .env

# 3. Edit .env and paste your key
# GEMINI_API_KEY=AIzaSy...
# or
# GROQ_API_KEY=gsk_...

# 4. (Optional) Interactive setup
python setup_api_keys.py
```

**Test API connection:**
```powershell
python test_streamlit_ready.py
```

Expected: `✅ GEMINI_API_KEY found` or `✅ GROQ_API_KEY found`

📖 **Full guide:** [API_SETUP_GUIDE.md](API_SETUP_GUIDE.md) | **Quick ref:** [API_QUICKSTART.md](API_QUICKSTART.md)

### 4. Run tests
```bash
pytest tests/ -v
```

### 4. Run demos
```bash
# Basic RAG sentiment demo
python scripts/test_news.py

# LangGraph agentic workflow demo
python demo_langgraph_workflow.py

# Full sentiment advisor demo
python demo_sentiment_advisor.py
```

**Demo workflow:**
- `SearchNewsTool.invoke({"query": "NVDA", "limit": 5})`
- `NewsSentimentRAGService.predict_from_search_results(...)`
- LangGraph multi-agent orchestration with conditional routing

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
