# Embeddings Artifacts

This directory stores generated embedding files used by retrieval workflows.

## Default Output
`financial_sentiment_embeddings.jsonl`

Each line contains:
- `id`: row id
- `text`: original sentence
- `metadata`: label metadata (for example `{"label": "positive"}`)
- `vector`: TF-IDF vector
- `vocabulary`: vocabulary snapshot used to build that vector

## Generate
```bash
python3 data/embedding_pipeline.py \
  --csv data/data.csv \
  --text-col Sentence \
  --label-col Sentiment \
  --output data/embeddings/financial_sentiment_embeddings.jsonl
```

## Notes
- Regenerate when the source dataset changes.
- Keep pipeline/runtime vectorization logic aligned.
