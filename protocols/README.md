# Protocols Module

## Purpose
`protocols/` defines message contracts for module-to-module and agent-to-agent communication.

Current state:
- `base_protocol.py` provides a minimal abstract interface.

## LangChain and LangGraph Relevance
Protocols are useful for:
- Standardizing tool output envelopes
- Preserving traceability across graph nodes
- Enforcing schema validation at handoff boundaries

## Recommended Next Steps
- Add typed protocol objects (Pydantic models) for:
  - Tool result payloads
  - Agent decision payloads
  - Error/fallback payloads
- Add compatibility helpers for `langchain_core.messages` when moving to chat-model agent loops.
