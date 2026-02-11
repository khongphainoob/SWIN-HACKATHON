"""
memory/vector_memory.py
VectorMemory: Lưu trữ portfolio, watchlist, và cache tin tức.
(MVP) Chưa triển khai similarity search bằng embedding thật.
"""
from __future__ import annotations

from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import json
import os


@dataclass
class PortfolioItem:
    """Một mục trong danh mục đầu tư người dùng."""
    ticker: str
    quantity: float
    avg_cost: float
    current_price: float
    allocation_pct: float  # 0..100
    sector: str
    country: str


@dataclass
class NewsItem:
    """Một tin tức được lưu trong vector memory."""
    news_id: str
    headline: str
    content: str
    source: str
    timestamp: str
    tickers_mentioned: List[str]
    sentiment_score: float
    embedding: Optional[List[float]] = None


class VectorMemory:
    """Lưu trữ portfolio và tin tức."""

    def __init__(self):
        self.portfolio: Dict[str, PortfolioItem] = {}
        self.news_cache: Dict[str, NewsItem] = {}
        self.ticker_watchlist: List[str] = []

    def set_portfolio(self, portfolio_items: List[PortfolioItem], *, replace: bool = True):
        """
        Lưu danh mục đầu tư của user.

        replace=True: coi đây là snapshot mới -> xoá danh mục cũ (tránh ticker đã bán vẫn còn).
        """
        if replace:
            self.portfolio = {item.ticker: item for item in portfolio_items}
        else:
            for item in portfolio_items:
                self.portfolio[item.ticker] = item

    def get_portfolio(self) -> Dict[str, PortfolioItem]:
        """Lấy danh mục đầu tư."""
        return self.portfolio

    def get_portfolio_allocation(self, ticker: str) -> float:
        """Lấy % allocation của ticker trong portfolio."""
        return float(self.portfolio.get(ticker).allocation_pct) if ticker in self.portfolio else 0.0

    def add_news(self, news_item: NewsItem):
        """Thêm tin tức vào cache."""
        self.news_cache[news_item.news_id] = news_item

    def find_relevant_news(self, ticker: str) -> List[NewsItem]:
        """
        Tìm tin tức liên quan đến ticker.
        (MVP) Lọc theo tickers_mentioned.
        """
        t = str(ticker).upper()
        return [n for n in self.news_cache.values() if t in [x.upper() for x in (n.tickers_mentioned or [])]]

    def set_watchlist(self, tickers: List[str]):
        """Lưu danh sách tickers mà user follow."""
        self.ticker_watchlist = [str(t).upper() for t in (tickers or [])]

    def get_watchlist(self) -> List[str]:
        """Lấy watchlist."""
        return self.ticker_watchlist

    def save_to_file(self, filepath: str, *, include_news_cache: bool = True, news_limit: int = 200):
        """Lưu memory vào file JSON."""
        data = {
            "portfolio": {t: asdict(item) for t, item in self.portfolio.items()},
            "watchlist": self.ticker_watchlist,
        }

        if include_news_cache:
            # Lưu tối đa news_limit tin gần nhất (theo timestamp string, MVP: sort lexicographically)
            news_items = list(self.news_cache.values())
            news_items.sort(key=lambda n: n.timestamp or "", reverse=True)
            news_items = news_items[: max(0, int(news_limit))]
            data["news_cache"] = {n.news_id: asdict(n) for n in news_items}

        dirpath = os.path.dirname(filepath)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_from_file(self, filepath: str):
        """Tải memory từ file JSON."""
        if not os.path.exists(filepath):
            return

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Replace toàn bộ snapshot
        self.portfolio = {}
        for ticker, info in (data.get("portfolio", {}) or {}).items():
            self.portfolio[ticker] = PortfolioItem(
                ticker=info["ticker"],
                quantity=float(info.get("quantity", 0.0)),
                avg_cost=float(info.get("avg_cost", 0.0)),
                current_price=float(info.get("current_price", 0.0)),
                allocation_pct=float(info.get("allocation_pct", 0.0)),
                sector=info.get("sector", ""),
                country=info.get("country", ""),
            )

        self.ticker_watchlist = [str(t).upper() for t in (data.get("watchlist", []) or [])]

        self.news_cache = {}
        for news_id, info in (data.get("news_cache", {}) or {}).items():
            self.news_cache[news_id] = NewsItem(
                news_id=info["news_id"],
                headline=info.get("headline", ""),
                content=info.get("content", ""),
                source=info.get("source", ""),
                timestamp=info.get("timestamp", ""),
                tickers_mentioned=info.get("tickers_mentioned", []) or [],
                sentiment_score=float(info.get("sentiment_score", 0.0)),
                embedding=info.get("embedding"),
            )
