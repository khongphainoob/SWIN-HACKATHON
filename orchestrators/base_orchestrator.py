"""Base orchestrator abstraction.

Defines the ``orchestrate()`` contract for coordinating multi-step workflows.
"""
from abc import ABC, abstractmethod

class BaseOrchestrator(ABC):
    """Abstract parent for workflow orchestrators."""

    @abstractmethod
    def orchestrate(self, *args, **kwargs):
        """Coordinate execution across tools, services, and agents."""
        pass
