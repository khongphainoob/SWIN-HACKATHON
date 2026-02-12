"""Base protocol abstraction.

Defines a minimal communication contract for structured message exchange
between components.
"""
from abc import ABC, abstractmethod

class BaseProtocol(ABC):
    """Abstract parent for message protocol implementations."""

    @abstractmethod
    def communicate(self, message):
        """Transform, validate, or route a protocol message."""
        pass
