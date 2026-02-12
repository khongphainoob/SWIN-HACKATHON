"""Base script abstraction.

Defines the ``run()`` contract for executable scripts and demos.
"""
from abc import ABC, abstractmethod

class BaseScript(ABC):
    """Abstract parent for runnable project scripts."""

    @abstractmethod
    def run(self, *args, **kwargs):
        """Run script-specific logic."""
        pass
