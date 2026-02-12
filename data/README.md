# Data Module

## Purpose
`data/` contains datasets and derived artifacts used for retrieval and sentiment inference.

Key files:
- `data.csv`: labeled financial sentiment dataset (`Sentence`, `Sentiment`)
- `embedding_pipeline.py`: builds embedding JSONL artifacts
- `embeddings/`: output directory for generated vectors

## LangChain Fit
Data in this folder powers local retrieval for:
- `TfidfVectorStore`
- `NewsSentimentRAGService`

## Build Embeddings Artifact
```bash
python3 data/embedding_pipeline.py \
  --csv data/data.csv \
  --text-col Sentence \
  --label-col Sentiment \
  --output data/embeddings/financial_sentiment_embeddings.jsonl
```

## Data Quality Guidance
- Keep labels normalized to `positive|neutral|negative`.
- Remove empty or malformed rows before indexing.
- Version large generated artifacts outside git when needed.
