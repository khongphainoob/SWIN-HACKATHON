"""Lightweight extractive summarization tool.

Detailed documentation
----------------------
Purpose
    Produce concise extractive summaries by scoring sentences with term
    frequencies (stopword-filtered) and selecting the top-N sentences in their
    original order.

Interfaces
    - ``Args`` schema: ``text`` (str), ``max_sentences`` (int>0).
    - ``_run``: LangChain entry; returns summary string.
    - ``execute``: Backwards-compatible imperative wrapper.

Behavior
    - Normalizes whitespace, splits on punctuation, excludes common stopwords,
      scores sentences by summed word frequencies, and returns the highest
      scoring sentences.

Why this fits LangChain
    - Implements ``args_schema`` and ``_run`` for immediate tool registration
      in agents/LCEL.
    - ``return_direct=True`` allows agent responses to stream the summary
      directly.
    - No heavy dependencies; deterministic for synchronous tool calls.
"""
from __future__ import annotations

import re
from collections import Counter
from typing import Any, List

from pydantic import BaseModel, Field
from tools.base_tool import BaseTool
from utils.helpers import normalize_whitespace
from utils.logger import get_logger


STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "but",
    "to",
    "of",
    "in",
    "on",
    "for",
    "with",
    "as",
    "is",
    "are",
    "was",
    "were",
    "be",
    "by",
    "that",
    "this",
    "it",
    "from",
    "at",
    "which",
    "has",
    "have",
    "had",
}


def _split_sentences(text: str) -> List[str]:
    pattern = r"(?<=[.!?])\s+"
    sentences = re.split(pattern, text)
    return [s.strip() for s in sentences if s.strip()]


def _tokenize(text: str) -> List[str]:
    return re.findall(r"\b\w+\b", text.lower())


class SummarizeTool(BaseTool):
    """Summarize long text into key sentences."""

    name: str = "summarize"
    description: str = "Extractive summarization using frequency scoring."
    return_direct: bool = True

    class Args(BaseModel):
        text: str = Field(..., description="Text to summarize")
        max_sentences: int = Field(3, gt=0, description="Maximum sentences in the summary")

    args_schema: Any = Args

    def __init__(self, *, logger: Any = None) -> None:
        super().__init__(logger=logger or get_logger(self.__class__.__name__))

    def _run(self, text: str, max_sentences: int = 3, **_: Any) -> str:
        if not text or not isinstance(text, str):
            raise ValueError("text must be a non-empty string")
        if max_sentences <= 0:
            raise ValueError("max_sentences must be positive")

        clean_text = normalize_whitespace(text)
        sentences = _split_sentences(clean_text)
        if len(sentences) <= max_sentences:
            return clean_text

        # Build term frequencies excluding stopwords.
        word_freq = Counter()
        for word in _tokenize(clean_text):
            if word in STOPWORDS:
                continue
            word_freq[word] += 1

        if not word_freq:
            return " ".join(sentences[:max_sentences])

        # Score sentences by sum of word frequencies.
        scored = []
        for idx, sent in enumerate(sentences):
            score = sum(word_freq[w] for w in _tokenize(sent) if w in word_freq)
            scored.append((score, idx, sent))

        # Pick top sentences by score, preserving original order.
        top = sorted(scored, key=lambda x: (-x[0], x[1]))[:max_sentences]
        top_sorted = sorted(top, key=lambda x: x[1])
        summary = " ".join(s for _, _, s in top_sorted)
        return summary

    # Backwards-compatible wrapper
    def execute(self, text: str, max_sentences: int = 3) -> str:  # pragma: no cover
        return self._run(text=text, max_sentences=max_sentences)
