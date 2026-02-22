# Dependency Guide

## Overview
This document explains the purpose of each dependency in the SWIN Sentiment System.

---

## Core Dependencies

### 1. LangChain & LangGraph

#### `langchain-core` (0.1.0 - 0.3.0)
**Purpose:** Core abstractions for LangChain framework
**Used in:**
- `tools/base_tool.py` - BaseTool interface
- `services/vector_store_service.py` - VectorStore interface
- `services/news_sentiment_service.py` - Document handling

**Why needed:**
- Provides standard interfaces (`BaseTool`, `VectorStore`, `Document`)
- Enables tool calling and retrieval patterns
- Compatible with LangChain ecosystem

**Alternative:** None - required for LangChain compatibility

---

#### `langgraph` (0.0.20 - 0.2.0)
**Purpose:** State-based agentic workflow orchestration
**Used in:**
- `orchestrators/langgraph_workflow.py` - Complete workflow implementation

**Why needed:**
- Enables complex multi-agent workflows with conditional routing
- Provides state management and checkpointing
- Supports human-in-the-loop patterns

**Alternative:** 
- Manual state management (more complex)
- Traditional orchestrators (less flexible)

---

### 2. Data Validation

#### `pydantic` (2.0.0 - 3.0.0)
**Purpose:** Data validation and settings management
**Used in:**
- All tool `Args` schemas
- Configuration validation
- Type-safe data structures

**Why needed:**
- Runtime validation of inputs/outputs
- Type hints with validation
- JSON schema generation
- Settings management

**Alternative:** 
- Manual validation (error-prone)
- `dataclasses` (no runtime validation)

---

#### `pydantic-settings` (2.0.0 - 3.0.0)
**Purpose:** Settings management for Pydantic v2
**Used in:**
- Configuration loading from environment
- YAML config parsing with validation

**Why needed:**
- Environment variable management
- Type-safe configuration
- Hierarchical settings

**Alternative:** Manual env parsing + validation

---

### 3. HTTP & APIs

#### `requests` (2.31.0 - 3.0.0)
**Purpose:** HTTP client for API calls
**Used in:**
- `tools/search_tool.py` - Fallback news fetcher
- Future API integrations

**Why needed:**
- Standard HTTP library
- Robust error handling
- Session management
- Widely adopted

**Alternative:** 
- `httpx` (async-first)
- `urllib3` (lower-level)

---

#### `yfinance` (0.2.30 - 0.3.0)
**Purpose:** Yahoo Finance API wrapper
**Used in:**
- `tools/search_tool.py` - Market news fetching
- `orchestrators/langgraph_workflow.py` - Market data

**Why needed:**
- Free market data and news
- No API key required
- Real-time quotes
- Historical data

**Alternative:**
- Alpha Vantage (requires API key)
- Polygon.io (paid)
- IEX Cloud (limited free tier)

---

### 4. Configuration

#### `PyYAML` (6.0.0 - 7.0.0)
**Purpose:** YAML parser for configuration files
**Used in:**
- `services/llm_service.py` - Model config loading
- `configs/model_config.yaml` - System settings

**Why needed:**
- Human-readable config format
- Comments support
- Nested structures
- Industry standard

**Alternative:**
- JSON (no comments)
- TOML (less flexible)
- Python files (less safe)

---

## Testing Dependencies

#### `pytest` (7.4.0 - 9.0.0)
**Purpose:** Testing framework
**Used in:**
- `tests/` - All unit tests

**Why needed:**
- Modern testing framework
- Rich plugin ecosystem
- Fixtures and parametrization
- Better assertions than unittest

**Alternative:** 
- `unittest` (stdlib, more verbose)
- `nose2` (older framework)

---

#### `pytest-cov` (4.1.0 - 5.0.0)
**Purpose:** Coverage reporting for pytest
**Why needed:**
- Track test coverage
- Identify untested code
- CI/CD integration

---

#### `pytest-mock` (3.12.0 - 4.0.0)
**Purpose:** Mocking utilities for pytest
**Why needed:**
- Mock external APIs in tests
- Isolate unit tests
- Fixture-based mocking

---

## Optional Dependencies

### LLM Providers

#### `google-generativeai`
**Purpose:** Google Gemini API client
**When to install:** Using Gemini models
**Cost:** Pay-per-use
**Setup:** Requires `GOOGLE_API_KEY`

---

#### `openai`
**Purpose:** OpenAI GPT API client
**When to install:** Using GPT models
**Cost:** Pay-per-use
**Setup:** Requires `OPENAI_API_KEY`

---

#### `anthropic`
**Purpose:** Anthropic Claude API client
**When to install:** Using Claude models
**Cost:** Pay-per-use
**Setup:** Requires `ANTHROPIC_API_KEY`

---

### Vector Stores

#### `chromadb`
**Purpose:** Production-grade vector database
**When to install:** Need persistent vector storage beyond TF-IDF
**Benefits:**
- Persistent storage
- Fast similarity search
- Easy deployment

---

#### `faiss-cpu`
**Purpose:** Facebook AI Similarity Search
**When to install:** Need high-performance vector search
**Benefits:**
- Extremely fast
- Low memory footprint
- Industry standard

---

#### `sentence-transformers`
**Purpose:** State-of-the-art sentence embeddings
**When to install:** Need semantic embeddings beyond TF-IDF
**Benefits:**
- Pre-trained models
- Better semantic understanding
- Multilingual support

---

## Development Dependencies

### Code Quality

#### `black` - Code formatter
Ensures consistent code style across the project.

#### `isort` - Import sorter
Organizes imports automatically.

#### `flake8` - Linter
Catches code smells and style issues.

#### `pylint` - Static analyzer
Deep code analysis and suggestions.

---

### Type Checking

#### `mypy` - Static type checker
Catches type errors before runtime.

#### `types-*` - Type stubs
Type information for third-party libraries.

---

### Documentation

#### `sphinx` - Documentation generator
Generate API documentation.

#### `myst-parser` - Markdown parser
Write docs in Markdown format.

---

## Dependency Management Best Practices

### Version Pinning Strategy

**Flexible ranges:** Used for most dependencies to allow bug fixes
```
langchain-core>=0.1.0,<0.3.0
```

**Why:** Balance between stability and getting security updates

**Exact versions:** Use in production deployment
```
langchain-core==0.2.5
```

**Why:** Ensure identical environments across deployments

---

### Installation Profiles

#### Minimal (Production)
```bash
pip install -r requirements.txt
```
**Size:** ~50MB
**Use case:** Production deployment, Docker images

#### Development
```bash
pip install -r requirements-dev.txt
```
**Size:** ~150MB
**Use case:** Local development, testing, code quality

#### Full (All features)
```bash
pip install -e ".[all]"
```
**Size:** ~500MB+
**Use case:** Experimentation, research, all optional features

---

## Troubleshooting Common Issues

### Issue: `pip install` fails on Windows

**Cause:** Missing C++ Build Tools
**Solution:**
```bash
# Install Visual Studio Build Tools
# Or use conda environment
conda create -n swin python=3.10
conda activate swin
pip install -r requirements.txt
```

---

### Issue: `langgraph` import error

**Cause:** Version incompatibility
**Solution:**
```bash
pip install --upgrade langgraph langchain-core
```

---

### Issue: `yfinance` rate limiting

**Cause:** Too many requests
**Solution:** Add retry logic or use cached data
```python
from utils.retry import retry

@retry(max_attempts=3, delay=2.0)
def fetch_news(ticker):
    return tool.invoke({"query": ticker})
```

---

### Issue: Memory usage with vector stores

**Cause:** Large embedding datasets
**Solution:** Use incremental loading or switch to disk-based store
```python
# Use FAISS with disk persistence
import faiss
index = faiss.read_index("embeddings.index")
```

---

## Updating Dependencies

### Check for updates:
```bash
pip list --outdated
```

### Update specific package:
```bash
pip install --upgrade langchain-core
```

### Update all:
```bash
pip install --upgrade -r requirements.txt
```

### Lock current versions:
```bash
pip freeze > requirements-lock.txt
```

---

## Security Considerations

1. **Regularly update dependencies** for security patches
2. **Use virtual environments** to isolate dependencies
3. **Scan for vulnerabilities:**
   ```bash
   pip install safety
   safety check
   ```
4. **Review dependency licenses** before production use
5. **Pin versions in production** for reproducibility

---

## License Information

| Package | License | Commercial Use |
|---------|---------|----------------|
| langchain-core | MIT | ✅ Yes |
| langgraph | MIT | ✅ Yes |
| pydantic | MIT | ✅ Yes |
| requests | Apache 2.0 | ✅ Yes |
| yfinance | Apache 2.0 | ✅ Yes |
| PyYAML | MIT | ✅ Yes |
| pytest | MIT | ✅ Yes |

**Note:** Always verify current license terms before production deployment.

---

## Further Reading

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [yfinance GitHub](https://github.com/ranaroussi/yfinance)
