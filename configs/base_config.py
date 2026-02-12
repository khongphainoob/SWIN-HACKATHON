"""Base configuration abstraction.

Defines the loading interface for model, tool, and runtime configuration
providers.
"""
from abc import ABC, abstractmethod

class BaseConfig(ABC):
    """Abstract parent for config providers."""

    @abstractmethod
    def load(self, *args, **kwargs):
        """Load and return configuration for a target component."""
        pass
