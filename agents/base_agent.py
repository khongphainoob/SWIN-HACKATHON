"""Base agent abstraction.

Defines the minimal ``act()`` interface for future concrete agents.
"""
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """Abstract parent for agent implementations."""

    @abstractmethod
    def act(self, *args, **kwargs):
        """Execute one agent step based on the given input/state."""
        pass
