# Agents Module

## Purpose
`agents/` contains agent interfaces and future agent implementations for LangChain/LangGraph execution.

Current state:
- `base_agent.py` defines the abstract contract (`act`).
- Concrete planning/reasoning/sentiment agents are not implemented yet.

## LangChain Fit
When implemented, agent classes should:
- Accept LangChain tools as dependencies.
- Use structured state inputs/outputs.
- Delegate tool execution via `invoke`.

## Recommended Agent Roles
- Planning Agent: decomposes user goals into tool/retrieval steps.
- Sentiment Agent: coordinates news retrieval and RAG sentiment scoring.
- Monitoring Agent: validates confidence, missing data, and fallback behavior.

## Implementation Guidelines
- Keep agent outputs JSON-serializable.
- Keep side effects in tools/services, not in orchestration logic.
- Add unit tests per agent for deterministic state transitions.
