"""
Abstract base class for Protocol modules in the Agentic AI system.
"""
from abc import ABC, abstractmethod

class BaseProtocol(ABC):
    @abstractmethod
    def communicate(self, message):
        pass
