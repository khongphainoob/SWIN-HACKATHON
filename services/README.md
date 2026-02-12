# Services Module

## Purpose
`services/` contains reusable, non-agent business logic and infrastructure adapters.

Implemented services:
- `vector_store_service.py` -> `TfidfVectorStore`
- `news_sentiment_service.py` -> `NewsSentimentRAGService`

## Service Responsibilities
- Data transformation
- Retrieval/indexing
- Domain scoring logic
- Infrastructure abstraction for tools/agents

Services should not:
- Own conversational policy
- Own multi-agent state transitions

## LangChain Fit
- `TfidfVectorStore` follows the `langchain_core.vectorstores.VectorStore` interface.
- `NewsSentimentRAGService` consumes tool output and returns retrieval-grounded sentiment payloads suitable for chains/agents.

## Example Composition
```python
from tools.search_tool import SearchNewsTool
from services.news_sentiment_service import NewsSentimentRAGService

search = SearchNewsTool()
rag_sentiment = NewsSentimentRAGService()

articles = search.invoke({"query": "NVDA", "limit": 5})
report = rag_sentiment.predict_from_search_results(articles)
```
