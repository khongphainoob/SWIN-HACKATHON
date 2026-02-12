"""Local TF-IDF vector store for retrieval workflows.

Implements the LangChain ``VectorStore`` interface in pure Python and is used
by both offline embedding generation and runtime RAG lookups.
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
    """Tokenize text into lowercase alphanumeric word tokens."""
    return re.findall(r"\b\w+\b", text.lower())


class TfidfVectorStore(VectorStore):
    """In-memory TF‑IDF vector store with cosine similarity search."""

    def __init__(self, *, logger: Optional[Any] = None) -> None:
        """Create an empty TF-IDF store with in-memory indexes."""
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
        """Instantiate a store and index the provided texts."""
        store = cls(**kwargs)
        store.add_texts(texts, metadatas=metadatas, ids=ids)
        return store

    def similarity_search(
        self, query: str, k: int = 4, **kwargs: Any
    ) -> List[Document]:
        """Return the top-k most similar documents for a query string."""
        results = self._similarity(query, k)
        return [doc for doc, _score in results]

    def similarity_search_with_score(
        self, query: str, k: int = 4, **kwargs: Any
    ) -> List[tuple[Document, float]]:
        """Return the top-k most similar documents with similarity scores."""
        return self._similarity(query, k)

    # ---- Public API -------------------------------------------------------------------
    def add_texts(
        self,
        texts: Sequence[str],
        metadatas: Optional[Sequence[Dict[str, Any]]] = None,
        ids: Optional[Sequence[str]] = None,
    ) -> List[str]:
        """Append texts to the store and rebuild TF-IDF indexes."""
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
        """Recompute vocabulary, IDF values, and document vectors."""
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
        """Convert token list into a TF-IDF vector using current vocabulary."""
        counts = Counter(tokens)
        token_count = len(tokens) or 1
        return [
            (counts[token] / token_count) * self.idf.get(token, 0.0)
            for token in self.vocabulary
        ]

    def _similarity(self, query: str, k: int) -> List[tuple[Document, float]]:
        """Compute and rank cosine similarity scores for the query."""
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
