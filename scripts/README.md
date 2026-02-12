# Scripts Module

## Purpose
`scripts/` contains runnable demos and entry points for local execution.

Current script:
- `test_news.py`: end-to-end demo for news retrieval plus RAG sentiment scoring.

## How to Run
From repository root:
```bash
python3 scripts/test_news.py
```

## Script Design Guidelines
- Keep scripts thin.
- Move reusable logic to `tools/` and `services/`.
- Use scripts for demonstration, smoke testing, and quick manual checks.

## Future Scripts
- `run_agent.py`: orchestrator entry point.
- `benchmark_sentiment.py`: latency/quality benchmarking.
