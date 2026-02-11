"""Embedding pipeline for the Kaggle Financial Sentiment dataset.

Detailed documentation
----------------------
Purpose
    Convert the Kaggle Financial Sentiment CSV into a TF-IDF vector store using
    the same ``TfidfVectorStore`` used at runtime, then persist vectors +
    vocabulary as JSONL for fast loading.

Usage
    python3 data/embedding_pipeline.py --csv path/to/dataset.csv \\
        --text-col Sentence --label-col Sentiment

Inputs
    - CSV with text column (default ``Sentence``) and label column (default
      ``Sentiment``).

Outputs
    - JSONL file in ``data/embeddings/`` containing: ``id``, ``text``,
      ``metadata`` (label), ``vector`` (TF-IDF array), ``vocabulary`` snapshot.

Why this fits LangChain
    - Uses the same ``TfidfVectorStore`` interface as runtime retrieval, so
      offline preprocessing and online querying stay aligned.
    - Produces deterministic vectors without extra dependencies, keeping local
      agent demos lightweight.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Dict, List

from services.vector_store_service import TfidfVectorStore
from utils.logger import get_logger


def build_embeddings(
    csv_path: Path,
    text_col: str,
    label_col: str,
    output_path: Path,
) -> None:
    logger = get_logger("embedding_pipeline")
    texts: List[str] = []
    ids: List[str] = []
    metadatas: List[Dict[str, Any]] = []

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            text = row.get(text_col)
            label = row.get(label_col)
            if not text:
                continue
            texts.append(text)
            ids.append(str(idx))
            metadatas.append({"label": label})

    store = TfidfVectorStore()
    store.add_texts(texts, ids=ids, metadatas=metadatas)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as out:
        for doc, vec in zip(store.documents, store.vectors):
            record = {
                "id": doc.id,
                "text": doc.page_content,
                "metadata": doc.metadata,
                "vector": vec,
                "vocabulary": store.vocabulary,
            }
            out.write(json.dumps(record))
            out.write("\n")

    logger.info("Wrote %s embeddings to %s", len(store.documents), output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build sentiment embeddings.")
    parser.add_argument("--csv", type=Path, required=True, help="Path to Kaggle CSV file")
    parser.add_argument("--text-col", default="Sentence", help="Name of text column")
    parser.add_argument("--label-col", default="Sentiment", help="Name of label column")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/embeddings/financial_sentiment_embeddings.jsonl"),
        help="Where to store embeddings JSONL",
    )
    args = parser.parse_args()

    build_embeddings(args.csv, args.text_col, args.label_col, args.output)


if __name__ == "__main__":
    main()
