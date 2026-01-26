"""
Abstract base class for Config modules in the Agentic AI system.
"""
from abc import ABC, abstractmethod

class BaseConfig(ABC):
    @abstractmethod
    def load(self, *args, **kwargs):
        pass
