# a2a_protocol.py

from typing import Any, Dict
from .base_protocol import BaseProtocol

class A2AMessage:
    """Standard message schema for A2A protocol communication."""
    def __init__(self, sender: str, receiver: str, content: Any, metadata: Dict[str, Any] = None):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "content": self.content,
            "metadata": self.metadata
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'A2AMessage':
        return A2AMessage(
            sender=data.get("sender", ""),
            receiver=data.get("receiver", ""),
            content=data.get("content"),
            metadata=data.get("metadata", {})
        )

class A2AProtocol(BaseProtocol):
    """Protocol implementation for A2A using the standard message schema."""
    def send(self, message: A2AMessage) -> None:
        # Implement sending logic here
        pass

    def receive(self) -> A2AMessage:
        # Implement receiving logic here
        pass
