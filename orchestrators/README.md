# Orchestrators Module

## Purpose
`orchestrators/` contains orchestration abstractions for coordinating tools, services, and agents.

Current state:
- `base_orchestrator.py` defines the abstract `orchestrate` contract.
- No concrete LangGraph orchestrator is implemented yet.

## LangGraph Direction
Recommended next implementation:
- Build `langgraph_orchestrator.py` with explicit state schema.
- Nodes: `search_news`, `score_sentiment`, `summarize`, `respond`.
- Add branching for low-confidence or missing-data fallback.

## Design Rules
- Keep orchestration deterministic where possible.
- Keep node IO structured and typed.
- Avoid direct external API calls in orchestrator; call tools/services instead.
