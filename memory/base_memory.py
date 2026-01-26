"""
Base module for memory management in Agentic AI system.
Provides abstract class and sample implementations for ShortTermMemory, LongTermMemory, and RAGMemory.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseMemory(ABC):
    """Abstract base class for memory modules."""
    @abstractmethod
    def store(self, data: Any) -> None:
        pass

    @abstractmethod
    def retrieve(self, query: Any) -> Any:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

class ShortTermMemory(BaseMemory):
    def __init__(self):
        self.buffer = []

    def store(self, data: Any) -> None:
        self.buffer.append(data)

    def retrieve(self, query: Any = None) -> Any:
        return self.buffer[-1] if self.buffer else None

    def clear(self) -> None:
        self.buffer.clear()

class LongTermMemory(BaseMemory):
    def __init__(self):
        self.storage = {}

    def store(self, data: Dict) -> None:
        key = data.get('id')
        if key:
            self.storage[key] = data

    def retrieve(self, query: Any) -> Any:
        return self.storage.get(query)

    def clear(self) -> None:
        self.storage.clear()

class RAGMemory(BaseMemory):
    def __init__(self):
        self.embeddings = []

    def store(self, data: Any) -> None:
        self.embeddings.append(data)

    def retrieve(self, query: Any) -> Any:
        # Placeholder: implement vector search logic here
        return None

    def clear(self) -> None:
        self.embeddings.clear()

# You can extend these classes or add new memory types as needed.
