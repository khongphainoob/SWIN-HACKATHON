"""Memory abstractions and reference implementations.

Defines ``BaseMemory`` plus simple short-term, long-term, and placeholder RAG
memory classes used as project scaffolding.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseMemory(ABC):
    """Abstract base class for memory modules."""
    @abstractmethod
    def store(self, data: Any) -> None:
        """Persist a memory item."""
        pass

    @abstractmethod
    def retrieve(self, query: Any) -> Any:
        """Retrieve one or more memory items by query."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Remove all stored memory state."""
        pass

class ShortTermMemory(BaseMemory):
    """Simple in-process buffer storing recent memory entries."""

    def __init__(self):
        """Initialize empty short-term buffer."""
        self.buffer = []

    def store(self, data: Any) -> None:
        """Append one item to short-term buffer."""
        self.buffer.append(data)

    def retrieve(self, query: Any = None) -> Any:
        """Return the most recent item or ``None`` when empty."""
        return self.buffer[-1] if self.buffer else None

    def clear(self) -> None:
        """Clear the short-term buffer."""
        self.buffer.clear()

class LongTermMemory(BaseMemory):
    """Dictionary-backed memory keyed by ``id``."""

    def __init__(self):
        """Initialize empty long-term store."""
        self.storage = {}

    def store(self, data: Dict) -> None:
        """Store one dictionary item when it contains an ``id`` key."""
        key = data.get('id')
        if key:
            self.storage[key] = data

    def retrieve(self, query: Any) -> Any:
        """Retrieve one stored item by key."""
        return self.storage.get(query)

    def clear(self) -> None:
        """Clear all long-term memory entries."""
        self.storage.clear()

class RAGMemory(BaseMemory):
    """Placeholder memory for embedding-backed retrieval flows."""

    def __init__(self):
        """Initialize empty embedding collection."""
        self.embeddings = []

    def store(self, data: Any) -> None:
        """Store one embedding or retrieval record."""
        self.embeddings.append(data)

    def retrieve(self, query: Any) -> Any:
        """Placeholder retrieval method for future vector search."""
        # Placeholder: implement vector search logic here
        return None

    def clear(self) -> None:
        """Clear stored embeddings."""
        self.embeddings.clear()

# You can extend these classes or add new memory types as needed.
