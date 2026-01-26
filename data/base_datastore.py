"""
Abstract base class for DataStore modules in the Agentic AI system.
"""
from abc import ABC, abstractmethod

class BaseDataStore(ABC):
    @abstractmethod
    def load(self, *args, **kwargs):
        pass
