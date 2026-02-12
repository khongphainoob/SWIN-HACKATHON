"""Base service abstraction.

Defines the minimal interface for reusable services that power tools and
agent workflows.
"""
from abc import ABC, abstractmethod

class BaseService(ABC):
    """Abstract parent for reusable service components."""

    @abstractmethod
    def connect(self, *args, **kwargs):
        """Initialize or connect the service to its backing resource."""
        pass
