# Agentic AI System for Mass Retail Investors

## Overview
This project builds a multi-layer Agentic AI system to help individual investors filter market noise. It combines traditional Machine Learning (trained on Kaggle datasets) and LLM Reasoning to provide personalized advice based on portfolio and real-time market sentiment.

### Architecture
- **agents/**: Define expert agents (Planning, Sentiment, Reasoning)
- **protocols/**: Standardized communication rules between agents (MCP, A2A)
- **tools/**: Execution tools (Search News, DB Query, Yahoo Finance)
- **services/**: Infrastructure connectors (Gemini API, Vector Store)
- **orchestrators/**: Flow orchestrators (LangGraph State Machine)
- **memory/**: Context management (Short-term, Long-term, RAG)
- **data/**: Data storage (Kaggle dataset, Embeddings)
- **configs/**: Configuration files (Model, Tool, Protocol)
- **scripts/**: Startup and demo scripts

Each folder contains a README.md describing its function.