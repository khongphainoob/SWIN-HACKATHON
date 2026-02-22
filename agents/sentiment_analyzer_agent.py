"""
agents/sentiment_analyzer_agent.py
Sentiment Analysis Agent
"""
from typing import Any, Dict, List, Optional
from services.news_sentiment_service import NewsSentimentRAGService
from agents.agent_utils import print_agent_banner, print_agent_output, print_agent_summary


class SentimentAnalyzerAgent:
    """
    Node 3: NLP Sentiment Analysis
    - Analyze sentiment of news
    - Return score and label
    """
    
    POSITIVE_KEYWORDS = [
        "profit", "beat", "upgrade", "growth", "surge", "strong", "record",
        "buyback", "dividend", "exceed", "momentum", "rally"
    ]
    NEGATIVE_KEYWORDS = [
        "loss", "miss", "downgrade", "weak", "decline", "crisis", "fraud",
        "bankruptcy", "lawsuit", "recall", "crash", "plunge"
    ]

    _rag_service: Optional[NewsSentimentRAGService] = None

    @classmethod
    def _get_rag_service(cls) -> Optional[NewsSentimentRAGService]:
        if cls._rag_service is not None:
            return cls._rag_service
        try:
            cls._rag_service = NewsSentimentRAGService()
        except Exception:
            cls._rag_service = None
        return cls._rag_service
    
    @staticmethod
    def run(state: Dict[str, Any]) -> Dict[str, Any]:
        print_agent_banner("SENTIMENT ANALYZER AGENT", step_number=3)
        
        articles = state.get("news_articles", [])
        
        print(f"📥 Input:")
        print(f"   • Articles to Analyze: {len(articles)}")
        print()

        rag_service = SentimentAnalyzerAgent._get_rag_service()
        rag_result: Optional[Dict[str, Any]] = None
        rag_score = 0.0
        rag_label = "neutral"
        if rag_service is not None:
            try:
                rag_result = rag_service.predict_from_search_results(articles, evidence_k=3)
                rag_score = rag_result.get("overall_score", 0.0)
                rag_label = rag_result.get("overall_sentiment", "neutral")
            except Exception:
                rag_result = None

        finbert_score: Optional[float] = None
        finbert_label: Optional[str] = None
        finbert_article_scores: List[Dict[str, Any]] = []
        try:
            from transformers import pipeline

            classifier = pipeline(
                "text-classification",
                model="ProsusAI/finbert",
                return_all_scores=True,
            )

            for article in articles:
                title = str(article.get("title", "")).strip()
                summary = str(article.get("summary", "") or article.get("description", "")).strip()
                text = " ".join([t for t in [title, summary] if t]).strip()
                if not text:
                    continue
                scores = classifier(text[:512])[0]
                score_map = {item["label"].lower(): float(item["score"]) for item in scores}
                pos = score_map.get("positive", 0.0)
                neg = score_map.get("negative", 0.0)
                neu = score_map.get("neutral", 0.0)
                finbert_article_scores.append({
                    "title": title,
                    "positive": round(pos, 6),
                    "negative": round(neg, 6),
                    "neutral": round(neu, 6),
                })

            if finbert_article_scores:
                avg_pos = sum(a["positive"] for a in finbert_article_scores) / len(finbert_article_scores)
                avg_neg = sum(a["negative"] for a in finbert_article_scores) / len(finbert_article_scores)
                avg_neu = sum(a["neutral"] for a in finbert_article_scores) / len(finbert_article_scores)
                finbert_score = round(avg_pos - avg_neg, 6)
                if avg_pos >= max(avg_neg, avg_neu):
                    finbert_label = "positive"
                elif avg_neg >= max(avg_pos, avg_neu):
                    finbert_label = "negative"
                else:
                    finbert_label = "neutral"
        except Exception:
            finbert_score = None
            finbert_label = None

        if finbert_score is not None and rag_result is not None:
            score = 0.7 * finbert_score + 0.3 * rag_score
            label_source = "finbert_rag"
        elif finbert_score is not None:
            score = finbert_score
            label_source = "finbert"
        else:
            score = rag_score
            label_source = "rag"

        if score > 0.15:
            label = "positive"
        elif score < -0.15:
            label = "negative"
        else:
            label = "neutral"

        result = {
            "sentiment_score": round(score, 3),
            "sentiment_label": label,
            "sentiment_details": {
                "method": label_source,
                "rag_overall_score": rag_score,
                "rag_overall_label": rag_label,
                "finbert_score": finbert_score,
                "finbert_label": finbert_label,
                "finbert_article_scores": finbert_article_scores,
                "rag_evidence": (rag_result or {}).get("articles", [])[:3],
                "articles_analyzed": len(articles),
                "features_used": ["title", "summary", "retrieved_examples"],
            },
            "current_step": "sentiment_analyzer",
            "messages": [f"[SentimentAnalyzer] Score: {score:.3f} ({label}) via {label_source}"],
        }
        
        print_agent_output("Sentiment Score", round(score, 3))
        print_agent_output("Sentiment Label", label)
        print_agent_output("Analysis Method", label_source)
        if finbert_score is not None:
            print(f"   • FinBERT Score: {finbert_score:.3f}")
        if rag_result:
            print(f"   • RAG Score: {rag_score:.3f}")
        print_agent_summary(result["messages"])
        
        return result
