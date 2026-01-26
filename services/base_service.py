"""
Abstract base class for Service modules in the Agentic AI system.
"""
from abc import ABC, abstractmethod

class BaseService(ABC):
    @abstractmethod
    def connect(self, *args, **kwargs):
        pass
