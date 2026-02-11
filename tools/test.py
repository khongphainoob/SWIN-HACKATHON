try:
    articles = self.fetcher(query, limit)
except Exception:
    articles = _yfinance_fetcher(query, limit)