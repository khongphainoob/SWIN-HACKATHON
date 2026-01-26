"""
Abstract base class for Agent modules in the Agentic AI system.
"""
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    @abstractmethod
    def act(self, *args, **kwargs):
        pass
