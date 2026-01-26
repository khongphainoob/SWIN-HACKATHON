"""
Abstract base class for Tool modules in the Agentic AI system.
"""
from abc import ABC, abstractmethod

class BaseTool(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
