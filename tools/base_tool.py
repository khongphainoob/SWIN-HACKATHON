"""LangChain-aligned base class for custom tools.

Detailed documentation
----------------------
Purpose
    Provide a single base that inherits from ``langchain_core.tools.BaseTool`` so
    all custom tools remain serializable and runnable inside LangChain agents
    and LCEL pipelines. Also injects a per-class logger and relaxed Pydantic
    config to accept extra runtime fields.

Key attributes
    - ``name`` / ``description``: Used by LangChain for tool selection & docs.
    - ``logger``: Optional logger; defaults to ``utils.logger.get_logger``.
    - ``model_config``: ``extra='allow'`` so subclasses can set custom fields
      without redefining Pydantic model config.

Why this fits LangChain
    - Extends the official ``BaseTool`` so ``invoke``, ``batch``, and agent
      tool calling work out of the box.
    - Keeps async hook ``_arun`` guarded to signal sync-only tools by default.

Usage
    Subclass ``BaseTool`` and implement ``_run`` (and optionally ``_arun``).
    Optionally add an ``Args`` Pydantic model and set ``args_schema`` for
    automatic validation and OpenAI-format tool descriptions.
"""
from __future__ import annotations

from typing import Any, Optional

from langchain_core.tools import BaseTool as LCBaseTool
from pydantic import ConfigDict

from utils.logger import get_logger


class BaseTool(LCBaseTool):
    """Extend LangChain BaseTool with a default logger."""

    logger: Optional[Any] = None

    # Pydantic v2 config
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    def __init__(self, **data: Any):  # type: ignore[override]
        if data.get("logger") is None:
            data["logger"] = get_logger(self.__class__.__name__)
        super().__init__(**data)

    async def _arun(self, *args, **kwargs):  # pragma: no cover - sync by default
        raise NotImplementedError("Async execution is not implemented for this tool.")
