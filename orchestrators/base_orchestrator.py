"""
Abstract base class for Orchestrator modules in the Agentic AI system.
"""
from abc import ABC, abstractmethod

class BaseOrchestrator(ABC):
    @abstractmethod
    def orchestrate(self, *args, **kwargs):
        pass
