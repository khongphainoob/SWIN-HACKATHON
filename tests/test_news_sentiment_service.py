"""Unit tests for RAG-based news sentiment prediction service."""

import csv
import tempfile
import unittest
from pathlib import Path

from services.news_sentiment_service import NewsSentimentRAGService


class NewsSentimentRAGServiceTestCase(unittest.TestCase):
    """Covers per-article and aggregate sentiment behavior in RAG service."""

    def setUp(self):
        """Build a deterministic temporary labeled dataset for tests."""
        self.tmpdir = tempfile.TemporaryDirectory()
        self.dataset_path = Path(self.tmpdir.name) / "sentiment.csv"

        rows = [
            ("record profit and strong growth beat estimates", "positive"),
            ("shares rally after strong revenue and raised guidance", "positive"),
            ("company faces lawsuit and reports heavy losses", "negative"),
            ("weak outlook and declining demand trigger selloff", "negative"),
            ("company announces board meeting next quarter", "neutral"),
            ("management confirms conference schedule with no guidance change", "neutral"),
        ]

        with self.dataset_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Sentence", "Sentiment"])
            writer.writeheader()
            for sentence, sentiment in rows:
                writer.writerow({"Sentence": sentence, "Sentiment": sentiment})

        self.service = NewsSentimentRAGService(dataset_path=self.dataset_path, retriever_k=3)

    def tearDown(self):
        """Clean temporary dataset resources."""
        self.tmpdir.cleanup()

    def test_predict_from_search_results(self):
        """Mixed inputs should produce mixed counts and neutral aggregate."""
        articles = [
            {"title": "record profit and strong growth at the company"},
            {"title": "company hit by lawsuit and heavy losses"},
            {"title": "company announces board meeting for next quarter"},
        ]

        result = self.service.predict_from_search_results(articles, evidence_k=2)
        self.assertEqual(result["counts"]["positive"], 1)
        self.assertEqual(result["counts"]["negative"], 1)
        self.assertEqual(result["counts"]["neutral"], 1)
        self.assertEqual(result["overall_sentiment"], "neutral")
        self.assertEqual(len(result["articles"]), 3)
        self.assertEqual(len(result["skipped"]), 0)

        self.assertEqual(result["articles"][0]["sentiment"], "positive")
        self.assertEqual(result["articles"][1]["sentiment"], "negative")
        self.assertEqual(result["articles"][2]["sentiment"], "neutral")

    def test_skip_invalid_article(self):
        """Articles without usable text should be skipped gracefully."""
        result = self.service.predict_from_search_results([{"link": "http://example.com"}])
        self.assertEqual(result["overall_sentiment"], "neutral")
        self.assertEqual(result["overall_score"], 0.0)
        self.assertEqual(result["articles"], [])
        self.assertEqual(len(result["skipped"]), 1)

    def test_predict_text_returns_evidence(self):
        """Direct text prediction should include retrieved evidence snippets."""
        prediction = self.service.predict_text("record profit beat estimates", evidence_k=2)
        self.assertEqual(prediction["sentiment"], "positive")
        self.assertGreater(prediction["confidence"], 0.0)
        self.assertEqual(len(prediction["retrieved_examples"]), 2)


if __name__ == "__main__":
    unittest.main()
