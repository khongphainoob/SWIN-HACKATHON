"""
agents/base_agent.py
BaseAgent: Lớp cơ sở cho tất cả agents - định nghĩa interface chung.

Mục tiêu (LangGraph-ready):
- Hỗ trợ dependency injection (LLMService / VectorMemory / ConversationMemory)
- Có wrapper run() an toàn: try/except + validate + log
- Có step(state) để dùng trực tiếp như 1 LangGraph node (state in/out)
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from datetime import datetime, timezone

from services.llm_service import LLMService
from memory.vector_memory import VectorMemory
from memory.conversation_memory import ConversationMemory


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class Agent(ABC):
    """
    Lớp cơ sở cho tất cả agents.

    Mỗi agent có:
    - LLM Service để gọi API
    - Memory để lưu context (portfolio, user profile, history, cooldown)
    - Methods để execute task và validate output

    LangGraph usage:
    - Có thể gọi Agent.step(state) như 1 node: input state -> output state (merged).
    """

    def __init__(
        self,
        name: str,
        description: str,
        config_path: str = None,
        *,
        user_id: str = "default_user",
        llm_service: Optional[LLMService] = None,
        vector_memory: Optional[VectorMemory] = None,
        conversation_memory: Optional[ConversationMemory] = None,
    ):
        self.name = name
        self.description = description

        # Dependency injection để orchestrator/graph share chung resource
        self.llm_service = llm_service or LLMService(config_path)
        self.vector_memory = vector_memory or VectorMemory()
        self.conversation_memory = conversation_memory or ConversationMemory(user_id=user_id)

        self.execution_log: List[Dict[str, Any]] = []

    @abstractmethod
    def execute(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Thực hiện task của agent."""
        raise NotImplementedError

    @abstractmethod
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate output của agent."""
        raise NotImplementedError

    def run(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Wrapper an toàn:
        - Bắt exception
        - Validate output
        - Log consistent
        """
        try:
            output = self.execute(task, context=context)
            ok = self.validate_output(output)
            self.log_execution(task, output, status="success" if ok else "failed")
            return output
        except Exception as e:
            output = {"error": str(e)}
            self.log_execution(task, output, status="failed")
            return output

    def step(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        State in/out helper để dùng trực tiếp trong LangGraph.

        Convention gợi ý:
        - state["task"] là dict task
        - state["context"] là dict context
        Nếu không có, sẽ fallback:
        - task = state.get("task", {})
        - context = state.get("context") hoặc toàn bộ state (trừ task/context)
        """
        task = state.get("task", {}) or {}
        if "context" in state and isinstance(state["context"], dict):
            context = state["context"]
        else:
            # context = state without task/context keys
            context = {k: v for k, v in state.items() if k not in ("task", "context")}

        output = self.run(task, context=context)

        # Merge output vào state
        new_state = dict(state)
        # Lưu output vào "last_output" để debug dễ, và merge key top-level cho graph route
        new_state["last_output"] = output
        if isinstance(output, dict):
            new_state.update(output)
        return new_state

    def log_execution(self, task: Dict[str, Any], output: Dict[str, Any], status: str = "success"):
        """Ghi lại quá trình thực hiện task vào log."""
        self.execution_log.append(
            {
                "agent": self.name,
                "task": task,
                "output": output,
                "status": status,
                "timestamp_utc": _utc_now_iso(),
            }
        )

    def report(self) -> str:
        """Tạo báo cáo về hoạt động của agent."""
        report_text = f"Agent: {self.name}\n"
        report_text += f"Description: {self.description}\n"
        report_text += f"Total executions: {len(self.execution_log)}\n"
        if self.execution_log:
            successful = sum(1 for log in self.execution_log if log["status"] == "success")
            failed = sum(1 for log in self.execution_log if log["status"] == "failed")
            report_text += f"Successful: {successful}, Failed: {failed}\n"
        return report_text

    def set_vector_memory(self, vector_memory: VectorMemory):
        """Thiết lập vector memory (để chia sẻ giữa agents)."""
        self.vector_memory = vector_memory

    def set_conversation_memory(self, conversation_memory: ConversationMemory):
        """Thiết lập conversation memory (để chia sẻ giữa agents)."""
        self.conversation_memory = conversation_memory
