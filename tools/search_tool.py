"""Market news search tool with Yahoo Finance backends.

Fetches articles for a ticker/keyword and returns normalized payloads suitable
for downstream summarization and sentiment analysis.
"""
from __future__ import annotations

import datetime as _dt
from typing import Any, Callable, Dict, List, Optional

import requests
from pydantic import BaseModel, Field

from tools.base_tool import BaseTool
from utils.logger import get_logger


def _normalize_published(published: Any) -> Any:
    """Normalize timestamps to ISO 8601 Z if possible."""
    if isinstance(published, (int, float)):
        try:
            return (
                _dt.datetime.fromtimestamp(published, _dt.timezone.utc)
                .isoformat()
                .replace("+00:00", "Z")
            )
        except (OverflowError, OSError, ValueError):
            return published
    return published


def _extract_from_yfinance_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    yfinance news structure changed.
    New-ish structure (common):
      { "content": { "title": "...", "canonicalUrl": {"url": "..."}, "contentType": "STORY", ... } }
    Old structure (common):
      { "title": "...", "link": "...", "publisher": "...", "providerPublishTime": 1234567890, ... }
    """
    content = item.get("content") or {}

    title = (
        content.get("title")
        or item.get("title")
    )

    link = (
        (content.get("canonicalUrl") or {}).get("url")
        or content.get("clickThroughUrl")  # sometimes present
        or item.get("link")
        or item.get("url")
    )

    publisher = (
        # sometimes nested provider info exists
        (content.get("provider") or {}).get("displayName")
        or (content.get("provider") or {}).get("name")
        or item.get("publisher")
        or item.get("provider")
    )

    published = (
        # sometimes ISO string
        content.get("pubDate")
        or content.get("publishedAt")
        # sometimes epoch
        or item.get("providerPublishTime")
        or item.get("published")
    )

    news_type = (
        content.get("contentType")
        or item.get("type")
        or "ticker"
    )

    return {
        "title": title,
        "link": link,
        "publisher": publisher,
        "published": _normalize_published(published),
        "type": news_type,
    }


def _yfinance_fetcher(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Fetch news via yfinance if installed."""
    try:
        import yfinance as yf  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "yfinance is required for the default news fetcher. "
            "Install with `pip install yfinance` or provide a custom fetcher."
        ) from exc

    news_items = (yf.Ticker(query).news or [])[:limit]
    return [_extract_from_yfinance_item(item) for item in news_items]


def _http_fallback_fetcher(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Fallback using Yahoo Finance search endpoint."""
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
                "published": _normalize_published(
                    item.get("providerPublishTime")
                    or item.get("pubDate")
                    or item.get("published_at")
                ),
                "type": "keyword",
            }
        )
    return results


class SearchNewsTool(BaseTool):
    """LangChain tool that fetches normalized market news results."""

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
        """Initialize the tool with an injected fetcher or default backend."""
        resolved_fetcher = fetcher or self._resolve_default_fetcher()
        super().__init__(
            fetcher=resolved_fetcher,
            logger=logger or get_logger(self.__class__.__name__),
        )

    def _resolve_default_fetcher(self) -> Callable[[str, int], List[Dict[str, Any]]]:
        """Choose yfinance fetcher when available, otherwise HTTP fallback."""
        try:  # pragma: no cover
            import yfinance  # noqa: F401

            return _yfinance_fetcher
        except ImportError:
            return _http_fallback_fetcher

    def _run(self, query: str, limit: int = 5, **_: Any) -> List[Dict[str, Any]]:
        """Validate inputs and fetch news articles for the given query."""
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        if limit <= 0:
            raise ValueError("limit must be > 0")

        if getattr(self, "logger", None):
            self.logger.debug("Searching news for query=%s, limit=%s", query, limit)

        # fetcher returns already-normalized dicts in our implementation
        return self.fetcher(query.strip(), limit)


if __name__ == "__main__":
    tool = SearchNewsTool()
    for article in tool._run(query="BTC", limit=5):
        print(article)
