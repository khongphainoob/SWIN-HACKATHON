This folder stores precomputed embeddings derived from the Kaggle Financial Sentiment dataset.

Generate with:

```
python data/embedding_pipeline.py --csv /path/to/financial_sentiment.csv --text-col Sentence --label-col Sentiment
```

The pipeline writes a JSONL file where each line contains:
- `id`: row identifier
- `text`: original sentence
- `metadata`: includes the sentiment label
- `vector`: TF‑IDF vector for the sentence
- `vocabulary`: vocabulary snapshot used for that vector

