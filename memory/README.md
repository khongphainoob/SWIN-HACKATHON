# Memory Module

## Purpose
`memory/` defines memory abstractions for agent workflows.

Current implementations in `base_memory.py`:
- `BaseMemory`
- `ShortTermMemory`
- `LongTermMemory`
- `RAGMemory` (placeholder retrieval logic)

## LangChain Fit
This module is a scaffold for integrating:
- Short-term conversation state
- Long-term user/profile memory
- Retrieval memory over embeddings/vector stores

## Integration Notes
For production LangChain/LangGraph use:
- Replace placeholder `RAGMemory.retrieve` with retriever-backed search.
- Keep memory read/write side effects isolated from tool logic.
- Define clear serialization format for checkpointing.
