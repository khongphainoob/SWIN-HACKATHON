"""End-to-end demo for news retrieval and RAG sentiment scoring.

Fetches live market news with ``SearchNewsTool`` and scores sentiment using
``NewsSentimentRAGService``.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.news_sentiment_service import NewsSentimentRAGService
from tools.search_tool import SearchNewsTool


def main() -> None:
    """Run a live demo of search + RAG sentiment analysis for one ticker."""
    tool = SearchNewsTool()
    sentiment_service = NewsSentimentRAGService()

    articles = tool.invoke({"query": "NVDA", "limit": 5})
    report = sentiment_service.predict_from_search_results(articles, evidence_k=2)

    print("Overall sentiment:", report["overall_sentiment"], "| score:", report["overall_score"])
    print("Counts:", report["counts"])
    print()
    for article in report["articles"]:
        print(article.get("published"), "-", article.get("title"))
        print("Sentiment:", article["sentiment"], "| confidence:", article["confidence"])
        print(article.get("link"))
        print("---")


if __name__ == "__main__":
    main()
