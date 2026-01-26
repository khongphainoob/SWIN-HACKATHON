"""
Abstract base class for Script modules in the Agentic AI system.
"""
from abc import ABC, abstractmethod

class BaseScript(ABC):
    @abstractmethod
    def run(self, *args, **kwargs):
        pass
