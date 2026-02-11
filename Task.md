# LangChain Project Roadmap

This roadmap reframes the original task list for a LangChain and LangGraph production path.

## Phase 1: Tooling and Retrieval Foundation
Status: mostly complete

Scope:
- `tools/base_tool.py`
- `tools/search_tool.py`
- `tools/database_tool.py`
- `tools/function_tools/summarize_tool.py`
- `services/vector_store_service.py`
- `data/embedding_pipeline.py`

Goals:
- Stable tool schemas and `_run` contracts
- Deterministic local retrieval
- Unit test coverage for core interfaces

## Phase 2: RAG Sentiment Capability
Status: complete for baseline

Scope:
- `services/news_sentiment_service.py`
- `scripts/test_news.py`
- `tests/test_news_sentiment_service.py`

Goals:
- Consume `SearchNewsTool` outputs directly
- Retrieve labeled sentiment neighbors
- Produce per-news and aggregate sentiment outputs

## Phase 3: Agent and Orchestration Layer
Status: pending

Scope:
- Implement concrete agents in `agents/`
- Implement LangGraph flow in `orchestrators/`

Recommended graph:
1. Input normalization
2. News retrieval
3. RAG sentiment scoring
4. Confidence checks and fallback
5. Final response synthesis

Deliverables:
- Typed state schema
- Node-level tests
- End-to-end integration test

## Phase 4: Protocol and Memory Hardening
Status: pending

Scope:
- Add typed message protocols in `protocols/`
- Upgrade memory implementations in `memory/`

Goals:
- Strong handoff contracts between nodes/agents
- Checkpoint-friendly state and memory serialization
- Replay and observability support

## Phase 5: Production Readiness
Status: pending

Scope:
- Configuration system in `configs/`
- Deployment scripts and containerization
- Monitoring, retry policy tuning, and evaluation harness

Goals:
- Environment-based configuration
- Operational reliability for network tools
- Offline evaluation for sentiment quality drift

## Engineering Standards
- Prefer `invoke` over ad-hoc imperative tool calls.
- Keep tool/service outputs JSON-serializable.
- Keep retrieval settings configurable (`k`, thresholds).
- Add tests with deterministic fixtures for every new module.
