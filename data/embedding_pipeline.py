"""CLI pipeline for generating sentiment embedding artifacts.

Reads labeled sentiment CSV rows, indexes text with ``TfidfVectorStore``, and
writes JSONL records used by local retrieval workflows.
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
    """Build TF-IDF vectors from CSV and persist records to JSONL."""
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
    """Parse CLI args and run embedding build pipeline."""
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
