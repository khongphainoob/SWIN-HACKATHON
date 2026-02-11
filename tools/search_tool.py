"""News search tool using Yahoo Finance or a pluggable fetcher.

Detailed documentation
----------------------
Purpose
    Fetch recent market news for a ticker or keyword, normalize timestamps, and
    return lightweight dicts suitable for agent responses or downstream
    summarization.

Interfaces
    - ``Args`` schema: ``query`` (str), ``limit`` (int>0).
    - ``_run``: LangChain entry point; returns a list of article dicts.
    - ``execute``: Backwards-compatible imperative wrapper.
    - ``fetcher``: Injectable callable to support offline tests or alternate
      data sources. Defaults to ``yfinance`` if installed, else HTTP fallback.

Why this fits LangChain
    - Inherits ``BaseTool`` so it can be registered in tool lists and called
      via ``agent_executor`` or LCEL ``Runnable`` chains.
    - Defines ``args_schema``, ``name``, ``description``, and
      ``return_direct=True`` for auto tool description generation and direct
      streaming of results when used with agent executors.
"""
from __future__ import annotations

import datetime as _dt
from typing import Any, Callable, Dict, List, Optional

import requests
from pydantic import BaseModel, Field

from tools.base_tool import BaseTool
from utils.logger import get_logger


def _yfinance_fetcher(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Fetch news via yfinance if installed."""
    try:
        import yfinance as yf  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise RuntimeError(
            "yfinance is required for the default news fetcher. "
            "Install with `pip install yfinance` or provide a custom fetcher."
        ) from exc

    ticker = yf.Ticker(query)
    news_items = ticker.news or []
    results: List[Dict[str, Any]] = []
    for item in news_items[:limit]:
        results.append(
            {
                "title": item.get("title"),
                "link": item.get("link"),
                "publisher": item.get("publisher"),
                "published": item.get("providerPublishTime"),
                "type": "ticker",
            }
        )
    return results


def _http_fallback_fetcher(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Very lightweight fallback using Yahoo Finance search endpoint."""
    url = "https://query1.finance.yahoo.com/v1/finance/search"
    params = {"q": query, "lang": "en-US", "newsCount": limit}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    payload = resp.json()
    news_items = payload.get("news", []) or payload.get("items", [])
    results: List[Dict[str, Any]] = []
    for item in news_items[:limit]:
        results.append(
            {
                "title": item.get("title"),
                "link": item.get("link"),
                "publisher": item.get("publisher") or item.get("provider"),
                "published": item.get("providerPublishTime")
                or item.get("pubDate")
                or item.get("published_at"),
                "type": "keyword",
            }
        )
    return results


class SearchNewsTool(BaseTool):
    """Searches Yahoo Finance news for a ticker or free‑text query."""

    name: str = "search_news"
    description: str = "Fetch market news for a ticker or keyword using Yahoo Finance."
    return_direct: bool = True
    fetcher: Optional[Callable[[str, int], List[Dict[str, Any]]]] = None

    class Args(BaseModel):
        query: str = Field(..., description="Ticker symbol or keyword to search")
        limit: int = Field(5, gt=0, description="Max number of articles to return")

    args_schema: Any = Args

    def __init__(
        self,
        *,
        fetcher: Optional[Callable[[str, int], List[Dict[str, Any]]]] = None,
        logger: Optional[Any] = None,
    ) -> None:
        # Prefer user-supplied fetcher, else try yfinance, else HTTP fallback.
        resolved_fetcher = fetcher or self._resolve_default_fetcher()
        super().__init__(fetcher=resolved_fetcher, logger=logger or get_logger(self.__class__.__name__))

    def _resolve_default_fetcher(
        self,
    ) -> Callable[[str, int], List[Dict[str, Any]]]:
        try:  # pragma: no cover - depends on optional lib
            import yfinance  # noqa: F401

            return _yfinance_fetcher
        except ImportError:
            return _http_fallback_fetcher

    def _run(self, query: str, limit: int = 5, **_: Any) -> List[Dict[str, Any]]:
        if not query or not isinstance(query, str):
            raise ValueError("query must be a non-empty string")
        if limit <= 0:
            raise ValueError("limit must be > 0")

        if self.logger:
            self.logger.debug("Searching news for query=%s, limit=%s", query, limit)

        articles = self.fetcher(query, limit)

        # Normalize timestamps to ISO 8601 strings when possible.
        normalized: List[Dict[str, Any]] = []
        for item in articles:
            published = item.get("published")
            if isinstance(published, (int, float)):
                try:
                    published = (
                        _dt.datetime.fromtimestamp(published, _dt.timezone.utc)
                        .isoformat()
                        .replace("+00:00", "Z")
                    )
                except (OverflowError, OSError, ValueError):
                    pass
            normalized.append(
                {
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "publisher": item.get("publisher"),
                    "published": published,
                    "type": item.get("type"),
                }
            )

        return normalized

    # Backwards-compatible imperative usage
    def execute(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:  # pragma: no cover
        return self._run(query=query, limit=limit)
