"""SQLite portfolio management tool.

Implements CRUD-style operations behind a LangChain tool interface for user
holdings data.
"""
from __future__ import annotations

import sqlite3
import time
from contextlib import contextmanager
from typing import Any, Dict, Iterable, List, Optional

from pydantic import BaseModel, Field
from tools.base_tool import BaseTool
from utils.logger import get_logger


class DatabaseTool(BaseTool):
    """Provides simple CRUD operations on a portfolio database."""

    name: str = "portfolio_db"
    description: str = "Read/write portfolio holdings from a local SQLite database."
    return_direct: bool = True
    db_path: str = "data/portfolio.db"

    class Args(BaseModel):
        action: str = Field(..., description="One of: get, upsert, delete, select")
        user_id: str = Field(..., description="Portfolio owner identifier")
        symbol: Optional[str] = Field(None, description="Ticker symbol for upsert/delete")
        shares: Optional[float] = Field(None, ge=0, description="Number of shares for upsert")
        avg_cost: Optional[float] = Field(None, ge=0, description="Average cost for upsert")
        query: Optional[str] = Field(None, description="Custom SELECT query (select action only)")
        params: Optional[List[Any]] = Field(None, description="Query params for custom SELECT")

    args_schema: Any = Args

    def __init__(self, db_path: str = "data/portfolio.db", *, logger: Optional[Any] = None) -> None:
        """Initialize the SQLite tool and ensure schema exists."""
        super().__init__(db_path=db_path, logger=logger or get_logger(self.__class__.__name__))
        self._ensure_schema()

    @contextmanager
    def _connect(self):
        """Yield a SQLite connection with row dictionaries enabled."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _ensure_schema(self) -> None:
        """Create required database tables when missing."""
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS holdings (
                    user_id TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    shares REAL NOT NULL,
                    avg_cost REAL NOT NULL,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (user_id, symbol)
                );
                """
            )
            conn.commit()

    def _select(self, query: str, params: Optional[Iterable[Any]] = None) -> List[Dict[str, Any]]:
        """Execute a SELECT and return rows as dictionaries."""
        if not query.lower().strip().startswith("select"):
            raise ValueError("Only SELECT statements are allowed for action=select")

        with self._connect() as conn:
            cur = conn.execute(query, params or [])
            rows = [dict(row) for row in cur.fetchall()]
        return rows

    def _get_portfolio(self, user_id: str) -> List[Dict[str, Any]]:
        """Return all holdings for a user."""
        sql = "SELECT user_id, symbol, shares, avg_cost, updated_at FROM holdings WHERE user_id = ?"
        return self._select(sql, (user_id,))

    def _upsert_holding(self, user_id: str, symbol: str, shares: float, avg_cost: float) -> str:
        """Insert or update a holding."""
        ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO holdings (user_id, symbol, shares, avg_cost, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(user_id, symbol) DO UPDATE SET
                    shares = excluded.shares,
                    avg_cost = excluded.avg_cost,
                    updated_at = excluded.updated_at;
                """,
                (user_id, symbol.upper(), shares, avg_cost, ts),
            )
            conn.commit()
        return "upserted"

    def _delete_holding(self, user_id: str, symbol: str) -> str:
        """Delete one holding row for the given user and symbol."""
        with self._connect() as conn:
            conn.execute("DELETE FROM holdings WHERE user_id = ? AND symbol = ?", (user_id, symbol.upper()))
            conn.commit()
        return "deleted"

    def _run(
        self,
        action: str,
        user_id: str,
        symbol: Optional[str] = None,
        shares: Optional[float] = None,
        avg_cost: Optional[float] = None,
        query: Optional[str] = None,
        params: Optional[List[Any]] = None,
        **_: Any,
    ) -> Any:
        """Route validated action input to the corresponding CRUD operation."""
        action = action.lower()
        if action == "get":
            return self._get_portfolio(user_id)
        if action == "select":
            if not query:
                raise ValueError("query is required for action=select")
            return self._select(query, params)
        if action == "upsert":
            if not symbol or shares is None or avg_cost is None:
                raise ValueError("symbol, shares, avg_cost are required for action=upsert")
            return self._upsert_holding(user_id, symbol, shares, avg_cost)
        if action == "delete":
            if not symbol:
                raise ValueError("symbol is required for action=delete")
            return self._delete_holding(user_id, symbol)
        raise ValueError("action must be one of: get, select, upsert, delete")

    # Backwards-compatible imperative usage
    def execute(self, query: str, params: Optional[Iterable[Any]] = None) -> List[Dict[str, Any]]:  # pragma: no cover
        """Imperative wrapper for raw SELECT queries."""
        return self._select(query, params)

    def get_portfolio(self, user_id: str) -> List[Dict[str, Any]]:  # pragma: no cover
        """Imperative wrapper that returns all user holdings."""
        return self._get_portfolio(user_id)

    def upsert_holding(self, user_id: str, symbol: str, shares: float, avg_cost: float) -> str:  # pragma: no cover
        """Imperative wrapper that inserts or updates one holding."""
        return self._upsert_holding(user_id, symbol, shares, avg_cost)

    def delete_holding(self, user_id: str, symbol: str) -> str:  # pragma: no cover
        """Imperative wrapper that deletes one holding."""
        return self._delete_holding(user_id, symbol)
