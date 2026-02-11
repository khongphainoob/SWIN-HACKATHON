"""Shared base class for custom LangChain tools.

Extends ``langchain_core.tools.BaseTool`` with default logger injection and
Pydantic settings used across this project.
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
        """Initialize tool and inject default logger when missing."""
        if data.get("logger") is None:
            data["logger"] = get_logger(self.__class__.__name__)
        super().__init__(**data)

    async def _arun(self, *args, **kwargs):  # pragma: no cover - sync by default
        """Async hook placeholder; sync execution is the default in this project."""
        raise NotImplementedError("Async execution is not implemented for this tool.")
