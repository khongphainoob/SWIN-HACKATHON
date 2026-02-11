"""RAG sentiment inference service for financial news.

Consumes article payloads (for example from ``SearchNewsTool``), retrieves
similar labeled examples, and returns per-article and aggregate sentiment.
"""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from services.vector_store_service import TfidfVectorStore
from utils.helpers import normalize_whitespace
from utils.logger import get_logger


class NewsSentimentRAGService:
    """Predict sentiment from news headlines using retrieval over labeled text."""

    SUPPORTED_LABELS = ("positive", "neutral", "negative")
    SENTIMENT_TO_SCORE = {"positive": 1.0, "neutral": 0.0, "negative": -1.0}
    TIE_BREAK_PRIORITY = {"neutral": 2, "positive": 1, "negative": 0}

    def __init__(
        self,
        dataset_path: Path | str = Path("data/data.csv"),
        *,
        text_col: str = "Sentence",
        label_col: str = "Sentiment",
        retriever_k: int = 5,
        logger: Optional[Any] = None,
    ) -> None:
        """Initialize the service and build the retrieval index from labeled data."""
        if retriever_k <= 0:
            raise ValueError("retriever_k must be > 0")

        self.dataset_path = Path(dataset_path)
        self.text_col = text_col
        self.label_col = label_col
        self.retriever_k = retriever_k
        self.logger = logger or get_logger(self.__class__.__name__)
        self.vector_store = self._build_vector_store()

    def _build_vector_store(self) -> TfidfVectorStore:
        """Load labeled rows and index them in a TF-IDF vector store."""
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Dataset not found: {self.dataset_path}")

        texts: List[str] = []
        metadatas: List[Dict[str, Any]] = []
        with self.dataset_path.open(newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                text = normalize_whitespace((row.get(self.text_col) or "").strip())
                label = str(row.get(self.label_col) or "").strip().lower()
                if not text:
                    continue
                if label not in self.SUPPORTED_LABELS:
                    continue
                texts.append(text)
                metadatas.append({"label": label})

        if not texts:
            raise ValueError(
                f"No usable labeled rows found in {self.dataset_path} "
                f"with text_col={self.text_col} label_col={self.label_col}"
            )

        ids = [str(i) for i in range(len(texts))]
        store = TfidfVectorStore(logger=self.logger)
        store.add_texts(texts, ids=ids, metadatas=metadatas)
        self.logger.info("Loaded %s labeled samples for RAG sentiment", len(texts))
        return store

    def _pick_label(self, weights: Dict[str, float], counts: Dict[str, int]) -> str:
        """Select a final sentiment label from weighted and count-based votes."""
        total_weight = sum(weights.values())
        if total_weight > 0:
            return max(
                self.SUPPORTED_LABELS,
                key=lambda label: (
                    weights.get(label, 0.0),
                    counts.get(label, 0),
                    self.TIE_BREAK_PRIORITY[label],
                ),
            )

        return max(
            self.SUPPORTED_LABELS,
            key=lambda label: (counts.get(label, 0), self.TIE_BREAK_PRIORITY[label]),
        )

    def predict_text(self, text: str, *, evidence_k: int = 3) -> Dict[str, Any]:
        """Predict sentiment for free-form text and return retrieval evidence."""
        if not isinstance(text, str) or not text.strip():
            raise ValueError("text must be a non-empty string")
        if evidence_k <= 0:
            raise ValueError("evidence_k must be > 0")

        query = normalize_whitespace(text)
        retrieved = self.vector_store.similarity_search_with_score(query, k=self.retriever_k)

        weights: Dict[str, float] = {label: 0.0 for label in self.SUPPORTED_LABELS}
        counts: Dict[str, int] = {label: 0 for label in self.SUPPORTED_LABELS}
        examples: List[Dict[str, Any]] = []

        for doc, score in retrieved:
            label = str(doc.metadata.get("label") or "neutral").lower()
            if label not in self.SUPPORTED_LABELS:
                continue

            safe_score = max(score, 0.0)
            weights[label] += safe_score
            counts[label] += 1
            if len(examples) < evidence_k:
                examples.append(
                    {
                        "label": label,
                        "score": round(safe_score, 6),
                        "text": doc.page_content,
                    }
                )

        sentiment = self._pick_label(weights, counts)
        total_weight = sum(weights.values())
        if total_weight > 0:
            confidence = weights[sentiment] / total_weight
        else:
            retrieved_count = sum(counts.values()) or 1
            confidence = counts[sentiment] / retrieved_count

        confidence = round(confidence, 6)
        sentiment_score = round(self.SENTIMENT_TO_SCORE[sentiment] * confidence, 6)
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "sentiment_score": sentiment_score,
            "retrieved_examples": examples,
        }

    def predict_article(self, article: Dict[str, Any], *, evidence_k: int = 3) -> Dict[str, Any]:
        """Predict sentiment for a single article dictionary."""
        if not isinstance(article, dict):
            raise ValueError("article must be a dictionary")

        text_parts: List[str] = []
        title = article.get("title")
        summary = article.get("summary") or article.get("description")

        if isinstance(title, str) and title.strip():
            text_parts.append(title.strip())
        if isinstance(summary, str) and summary.strip():
            text_parts.append(summary.strip())

        if not text_parts:
            raise ValueError("article must include non-empty title or summary/description")

        prediction = self.predict_text(". ".join(text_parts), evidence_k=evidence_k)
        merged = dict(article)
        merged.update(prediction)
        return merged

    def predict_from_search_results(
        self,
        articles: Sequence[Dict[str, Any]],
        *,
        evidence_k: int = 3,
    ) -> Dict[str, Any]:
        """Score a list of articles and return aggregate sentiment statistics."""
        if evidence_k <= 0:
            raise ValueError("evidence_k must be > 0")

        predictions: List[Dict[str, Any]] = []
        skipped: List[Dict[str, Any]] = []
        counts: Counter[str] = Counter()
        signed_scores: List[float] = []

        for idx, article in enumerate(articles):
            try:
                prediction = self.predict_article(article, evidence_k=evidence_k)
            except ValueError as exc:
                skipped.append({"index": idx, "error": str(exc), "article": article})
                continue

            predictions.append(prediction)
            counts[prediction["sentiment"]] += 1
            signed_scores.append(prediction["sentiment_score"])

        overall_score = sum(signed_scores) / len(signed_scores) if signed_scores else 0.0
        overall_score = round(overall_score, 6)
        if overall_score > 0.15:
            overall_sentiment = "positive"
        elif overall_score < -0.15:
            overall_sentiment = "negative"
        else:
            overall_sentiment = "neutral"

        return {
            "overall_sentiment": overall_sentiment,
            "overall_score": overall_score,
            "counts": {
                "positive": counts.get("positive", 0),
                "neutral": counts.get("neutral", 0),
                "negative": counts.get("negative", 0),
            },
            "articles": predictions,
            "skipped": skipped,
        }
