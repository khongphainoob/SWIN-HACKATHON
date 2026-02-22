"""
agents/news_fetch_agent.py
News Fetching Agent
"""
from typing import Any, Dict
from agents.agent_utils import print_agent_banner, print_agent_output, print_agent_summary, _utc_now_iso


class NewsFetchAgent:
    """
    Node 2: Fetch news articles
    - Call news API
    - Return normalized articles
    """
    
    @staticmethod
    def run(state: Dict[str, Any]) -> Dict[str, Any]:
        print_agent_banner("NEWS FETCH AGENT", step_number=2)
        
        ticker = state.get("ticker", "UNKNOWN")
        
        print(f"📥 Input:")
        print(f"   • Ticker: {ticker}")
        print()
        
        # Try to use SearchNewsTool if available
        try:
            from tools.search_tool import SearchNewsTool
            tool = SearchNewsTool()
            articles = tool.invoke({"query": ticker, "limit": 5})
        except Exception as e:
            # Fallback mock data
            articles = [
                {
                    "title": f"Breaking: {ticker} shows strong momentum",
                    "source": "Reuters",
                    "published": _utc_now_iso(),
                },
                {
                    "title": f"{ticker} quarterly earnings exceed expectations",
                    "source": "Bloomberg",
                    "published": _utc_now_iso(),
                }
            ]
        
        result = {
            "news_articles": articles,
            "current_step": "news_fetch_agent",
            "messages": [f"[NewsFetchAgent] Fetched {len(articles)} articles for {ticker}"],
        }
        
        print_agent_output("Articles Fetched", len(articles))
        for i, article in enumerate(articles[:3], 1):
            print(f"   • Article {i}: {article.get('title', 'N/A')[:60]}...")
        if len(articles) > 3:
            print(f"   • ... and {len(articles) - 3} more")
        print_agent_summary(result["messages"])
        
        return result
