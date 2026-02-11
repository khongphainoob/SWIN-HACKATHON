"""Base datastore abstraction.

Defines the loading contract for dataset providers used by services and
pipelines.
"""
from abc import ABC, abstractmethod

class BaseDataStore(ABC):
    """Abstract parent for dataset loader implementations."""

    @abstractmethod
    def load(self, *args, **kwargs):
        """Load dataset content into memory or another target structure."""
        pass
