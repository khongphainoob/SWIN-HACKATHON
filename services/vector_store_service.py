"""TF-IDF VectorStore implementation compatible with LangChain.

Detailed documentation
----------------------
Purpose
    Provide an in-memory, dependency-light vector store that satisfies the
    ``langchain_core.vectorstores.VectorStore`` contract using TF-IDF vectors
    and cosine similarity.

Interfaces
    - ``from_texts``: Standard constructor used by retrievers/chains.
    - ``add_texts``: Add documents with optional ids and metadata.
    - ``similarity_search`` / ``similarity_search_with_score``: Retrieve top-k
      ``Document`` objects (optionally with scores).

Behavior
    - Tokenizes text, builds vocabulary, computes IDF, and stores TF-IDF
      vectors alongside ``Document`` objects.
    - Pure Python, deterministic, no external ML dependencies.

Why this fits LangChain
    - Implements required abstract methods, so it can be wrapped by
      ``VectorStoreRetriever`` or used directly inside LCEL chains.
    - Returns LangChain ``Document`` objects for compatibility with downstream
      chains/agents that expect standardized document payloads.
"""
from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from typing import Any, Dict, Iterable, List, Optional, Sequence

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore

from utils.helpers import cosine_similarity
from utils.logger import get_logger


def _tokenize(text: str) -> List[str]:
    return re.findall(r"\b\w+\b", text.lower())


class TfidfVectorStore(VectorStore):
    """In-memory TF‑IDF vector store with cosine similarity search."""

    def __init__(self, *, logger: Optional[Any] = None) -> None:
        self.logger = logger or get_logger(self.__class__.__name__)
        self.documents: List[Document] = []
        self.tokens: List[List[str]] = []
        self.vocabulary: List[str] = []
        self.idf: Dict[str, float] = {}
        self.vectors: List[List[float]] = []

    # ---- LangChain-required interface -------------------------------------------------
    @classmethod
    def from_texts(
        cls,
        texts: List[str],
        embedding: Any = None,  # unused, kept for signature compatibility
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> "TfidfVectorStore":
        store = cls(**kwargs)
        store.add_texts(texts, metadatas=metadatas, ids=ids)
        return store

    def similarity_search(
        self, query: str, k: int = 4, **kwargs: Any
    ) -> List[Document]:
        results = self._similarity(query, k)
        return [doc for doc, _score in results]

    def similarity_search_with_score(
        self, query: str, k: int = 4, **kwargs: Any
    ) -> List[tuple[Document, float]]:
        return self._similarity(query, k)

    # ---- Public API -------------------------------------------------------------------
    def add_texts(
        self,
        texts: Sequence[str],
        metadatas: Optional[Sequence[Dict[str, Any]]] = None,
        ids: Optional[Sequence[str]] = None,
    ) -> List[str]:
        if ids and len(ids) != len(texts):
            raise ValueError("ids length must match texts length")
        if metadatas and len(metadatas) != len(texts):
            raise ValueError("metadatas length must match texts length")

        start_idx = len(self.documents)
        new_ids: List[str] = []
        for i, text in enumerate(texts):
            doc_id = ids[i] if ids else str(start_idx + i)
            metadata = metadatas[i] if metadatas else {}
            tokens = _tokenize(text)
            self.documents.append(Document(page_content=text, metadata=metadata, id=doc_id))
            self.tokens.append(tokens)
            new_ids.append(doc_id)

        self._rebuild_index()
        return new_ids

    # ---- Internal helpers -------------------------------------------------------------
    def _rebuild_index(self) -> None:
        vocab_set = set()
        for tokens in self.tokens:
            vocab_set.update(tokens)
        self.vocabulary = sorted(vocab_set)

        df = defaultdict(int)
        for tokens in self.tokens:
            for token in set(tokens):
                df[token] += 1

        total_docs = len(self.tokens) or 1
        self.idf = {
            token: math.log((1 + total_docs) / (1 + df[token])) + 1.0
            for token in self.vocabulary
        }

        self.vectors = [self._vectorize(tokens) for tokens in self.tokens]

    def _vectorize(self, tokens: List[str]) -> List[float]:
        counts = Counter(tokens)
        token_count = len(tokens) or 1
        return [
            (counts[token] / token_count) * self.idf.get(token, 0.0)
            for token in self.vocabulary
        ]

    def _similarity(self, query: str, k: int) -> List[tuple[Document, float]]:
        if not self.documents:
            return []

        query_tokens = _tokenize(query)
        query_vec = self._vectorize(query_tokens)

        scored: List[tuple[Document, float]] = []
        for doc, vec in zip(self.documents, self.vectors):
            score = cosine_similarity(query_vec, vec)
            scored.append((doc, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]
