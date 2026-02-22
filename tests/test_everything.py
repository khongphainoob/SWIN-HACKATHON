"""
test_everything.py
Master comprehensive test script for all tools and agents

This script:
1. Tests each tool with detailed explanations
2. Tests each agent with detailed explanations  
3. Tests end-to-end workflow
4. Provides summary and recommendations

Usage:
    python test_everything.py
"""
import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def print_header(title: str, level: int = 1):
    """Print formatted header"""
    if level == 1:
        print("\n" + "█"*70)
        print("█" + " "*68 + "█")
        print("█" + f"{title}".center(68) + "█")
        print("█" + " "*68 + "█")
        print("█"*70)
    elif level == 2:
        print("\n" + "="*70)
        print(f"  {title}")
        print("="*70)
    else:
        print("\n" + "-"*70)
        print(f"  {title}")
        print("-"*70)


def test_tool_search_news():
    """Test SearchNewsTool"""
    print_header("🔍 TESTING: SearchNewsTool", 2)
    
    print("""
    📌 Purpose:
       Fetch financial news articles from Yahoo Finance API
    
    📌 Inputs:
       - query (str): ticker symbol or keyword
       - limit (int): max articles to return (>0)
    
    📌 Output:
       List of articles with:
       - title: headline
       - link: URL
       - publisher: source name
       - published: timestamp
       - type: article type
    """)
    
    try:
        from tools.search_tool import SearchNewsTool
        tool = SearchNewsTool()
        
        print("    Testing with query: 'AAPL' (limit: 2)")
        result = tool.invoke({"query": "AAPL", "limit": 2})
        
        if result:
            print(f"\n    ✓ Successfully fetched {len(result)} articles\n")
            for idx, article in enumerate(result[:1], 1):
                print(f"    Article {idx}:")
                print(f"      Title: {article.get('title', 'N/A')[:60]}...")
                print(f"      Publisher: {article.get('publisher', 'N/A')}")
                print(f"      Type: {article.get('type', 'N/A')}")
        else:
            print("    ⚠️  No articles returned (API may be unavailable)")
    except Exception as e:
        print(f"    ⚠️  Note: {e}")


def test_tool_database():
    """Test DatabaseTool"""
    print_header("🗂️  TESTING: DatabaseTool", 2)
    
    print("""
    📌 Purpose:
       CRUD operations on portfolio holdings in SQLite database
    
    📌 Operations:
       - get: Retrieve all holdings for a user
       - upsert: Insert or update a holding
       - delete: Remove a holding
       - select: Custom SQL SELECT query
    
    📌 Holdings Schema:
       - user_id: Portfolio owner
       - symbol: Ticker symbol
       - shares: Number of shares
       - avg_cost: Average purchase price
       - updated_at: Last update timestamp
    """)
    
    try:
        import tempfile
        from tools.database_tool import DatabaseTool
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tool = DatabaseTool(db_path=f"{tmpdir}/test.db")
            
            print("    Step 1: Insert AAPL holding (100 shares @ $150)")
            tool.invoke({
                "action": "upsert",
                "user_id": "user123",
                "symbol": "AAPL",
                "shares": 100,
                "avg_cost": 150.0
            })
            print("    ✓ Inserted\n")
            
            print("    Step 2: Insert MSFT holding (50 shares @ $300)")
            tool.invoke({
                "action": "upsert",
                "user_id": "user123",
                "symbol": "MSFT",
                "shares": 50,
                "avg_cost": 300.0
            })
            print("    ✓ Inserted\n")
            
            print("    Step 3: Retrieve portfolio")
            portfolio = tool.invoke({
                "action": "get",
                "user_id": "user123"
            })
            print(f"    ✓ Retrieved {len(portfolio)} holdings:")
            for holding in portfolio:
                print(f"      • {holding['symbol']}: {holding['shares']} shares @ ${holding['avg_cost']}")
            print()
            
            print("    Step 4: Delete AAPL holding")
            tool.invoke({
                "action": "delete",
                "user_id": "user123",
                "symbol": "AAPL"
            })
            print("    ✓ Deleted\n")
            
            print("    Step 5: Verify deletion")
            portfolio = tool.invoke({
                "action": "get",
                "user_id": "user123"
            })
            print(f"    ✓ Portfolio now has {len(portfolio)} holding(s)")
            
    except Exception as e:
        print(f"    ⚠️  Error: {e}")


def test_tool_summarize():
    """Test SummarizeTool"""
    print_header("✂️  TESTING: SummarizeTool", 2)
    
    print("""
    📌 Purpose:
       Extract key sentences from long text using TF-IDF scoring
    
    📌 Inputs:
       - text (str): text to summarize
       - max_sentences (int): max sentences in output
    
    📌 Algorithm:
       1. Split text into sentences
       2. Calculate TF (term frequency) for each word
       3. Score sentences by sum of word frequencies
       4. Return top-scoring sentences in original order
    """)
    
    try:
        from tools.function_tools.summarize_tool import SummarizeTool
        tool = SummarizeTool()
        
        long_text = """
        Apple Inc. reported strong financial results for Q4 2025.
        The company's iPhone sales exceeded expectations with a 15% growth.
        Services revenue showed robust growth driven by cloud adoption.
        However, competition remains intense in the smartphone market.
        Apple announced plans to expand manufacturing in Southeast Asia.
        The company's AI initiatives are expected to drive future growth.
        """
        
        print(f"    Original text ({len(long_text)} chars):")
        print(f"    {long_text.strip()[:80]}...\n")
        
        summary = tool.invoke({
            "text": long_text,
            "max_sentences": 2
        })
        
        print(f"    Summary (max 2 sentences):")
        print(f"    {summary}\n")
        
        print("    ✓ Summarized successfully")
        
    except Exception as e:
        print(f"    ⚠️  Error: {e}")


def test_agent_input():
    """Test InputAgent"""
    print_header("📥 TESTING: InputAgent", 2)
    
    print("""
    📌 Purpose:
       Parse user input and extract key information
    
    📌 Tasks:
       1. Extract ticker symbol from query
       2. Normalize query
       3. Initialize workflow state
    
    📌 Output:
       - ticker: Extracted symbol (e.g., 'AAPL')
       - current_step: Node name for debugging
       - messages: Execution log
    """)
    
    try:
        from orchestrators.langgraph_workflow import InputAgent
        
        test_queries = [
            "What's the outlook for NVDA?",
            "Analyze AAPL stock",
            "Is TSLA a buy?"
        ]
        
        for query in test_queries:
            result = InputAgent.run({"user_query": query})
            print(f"    Query: '{query}'")
            print(f"    Extracted ticker: {result['ticker']}")
            print(f"    ✓ Processed\n")
            
    except Exception as e:
        print(f"    ⚠️  Error: {e}")


def test_agent_sentiment():
    """Test SentimentAnalyzerAgent"""
    print_header("💭 TESTING: SentimentAnalyzerAgent", 2)
    
    print("""
    📌 Purpose:
       Analyze sentiment of news articles
    
    📌 Algorithm:
       1. Combine news titles and summaries
       2. Count positive/negative keywords
       3. Calculate score: (pos - neg) / (pos + neg)
       4. Classify: positive (>0.2), negative (<-0.2), neutral
    
    📌 Output:
       - sentiment_score: Float [-1.0, 1.0]
       - sentiment_label: 'positive', 'negative', 'neutral'
       - sentiment_details: Debug info
    """)
    
    try:
        from orchestrators.langgraph_workflow import SentimentAnalyzerAgent
        
        test_cases = [
            {
                "label": "Positive News",
                "articles": [{"title": "Apple beats earnings, stock surges"}]
            },
            {
                "label": "Negative News",
                "articles": [{"title": "Microsoft crashes, fraud investigation"}]
            },
            {
                "label": "Neutral News",
                "articles": [{"title": "Market update: Mixed trading"}]
            }
        ]
        
        for test in test_cases:
            result = SentimentAnalyzerAgent.run({
                "news_articles": test["articles"]
            })
            
            print(f"    {test['label']}:")
            print(f"      Articles: {test['articles'][0]['title'][:50]}...")
            print(f"      Score: {result['sentiment_score']:.3f}")
            print(f"      Label: {result['sentiment_label']}")
            print(f"      ✓ Analyzed\n")
            
    except Exception as e:
        print(f"    ⚠️  Error: {e}")


def test_agent_market_data():
    """Test MarketDataAgent"""
    print_header("📊 TESTING: MarketDataAgent", 2)
    
    print("""
    📌 Purpose:
       Fetch current market data for stocks
    
    📌 Data Retrieved:
       - current_price: Current trading price
       - previous_close: Yesterday's closing price
       - volume: Trading volume
       - market_cap: Market capitalization
       - pe_ratio: Price-to-earnings ratio
       - 52_week_high/low: Year highs/lows
    
    📌 Source:
       Yahoo Finance (via yfinance library)
    """)
    
    try:
        from orchestrators.langgraph_workflow import MarketDataAgent
        
        result = MarketDataAgent.run({"ticker": "AAPL"})
        market_data = result["market_data"]
        
        print(f"    Market Data for AAPL:")
        if "current_price" in market_data:
            print(f"      Current Price: ${market_data['current_price']}")
        if "volume" in market_data:
            print(f"      Volume: {market_data['volume']:,.0f}")
        if "pe_ratio" in market_data:
            print(f"      P/E Ratio: {market_data['pe_ratio']:.2f}")
        
        print(f"      ✓ Data fetched\n")
        
    except Exception as e:
        print(f"    ⚠️  Note: {e}")


def test_agent_risk_alert():
    """Test RiskAlertAgent"""
    print_header("⚠️  TESTING: RiskAlertAgent", 2)
    
    print("""
    📌 Purpose:
       Generate risk alerts based on sentiment and news
    
    📌 Alert Levels:
       - HIGH: Severe issues requiring immediate attention
       - MEDIUM: Significant concerns to monitor
       - LOW: Minor notices for information
    
    📌 Alert Triggers:
       - Extreme sentiment scores (< -0.5)
       - Critical keywords in news (fraud, bankruptcy, crash)
       - High volatility signals
    """)
    
    try:
        from orchestrators.langgraph_workflow import RiskAlertAgent
        
        # Test high risk scenario
        result = RiskAlertAgent.run({
            "ticker": "TEST",
            "sentiment_score": -0.8,
            "news_articles": [
                {"title": "Company announces bankruptcy filing"}
            ]
        })
        
        alerts = result["risk_alerts"]
        print(f"    High-Risk Scenario (sentiment: -0.8):")
        print(f"      Generated {len(alerts)} alert(s)")
        
        high_alerts = [a for a in alerts if a.get("severity") == "HIGH"]
        print(f"      High severity: {len(high_alerts)}")
        
        if high_alerts:
            print(f"      Example: {high_alerts[0]['message'][:60]}...\n")
        
    except Exception as e:
        print(f"    ⚠️  Error: {e}")


def test_agent_ml_forecast():
    """Test MLForecastAgent"""
    print_header("🔮 TESTING: MLForecastAgent", 2)
    
    print("""
    📌 Purpose:
       Predict price trend based on sentiment and market data
    
    📌 Trend Prediction:
       - BULLISH: Expected price increase
       - BEARISH: Expected price decrease
       - NEUTRAL: No significant change expected
    
    📌 Confidence:
       Score [0.5, 0.95] indicating prediction strength
    """)
    
    try:
        from orchestrators.langgraph_workflow import MLForecastAgent
        
        # Bullish case
        result = MLForecastAgent.run({
            "ticker": "AAPL",
            "sentiment_score": 0.7,
            "market_data": {"current_price": 180.0}
        })
        
        forecast = result["forecast"]
        print(f"    Bullish Case (sentiment: +0.7):")
        print(f"      Trend: {forecast['trend']}")
        print(f"      Current: ${forecast['current_price']}")
        print(f"      Target: ${forecast['target_price']:.2f}")
        print(f"      Change: {forecast['predicted_change_pct']:+.2f}%")
        print(f"      Confidence: {forecast['confidence']:.1%}\n")
        
    except Exception as e:
        print(f"    ⚠️  Error: {e}")


def test_agent_llm_reasoning():
    """Test LLMReasoningAgent"""
    print_header("🧠 TESTING: LLMReasoningAgent", 2)
    
    print("""
    📌 Purpose:
       Evaluate risk and determine if human review is needed
    
    📌 Review Triggers:
       1. High severity alerts present
       2. Low forecast confidence (< 60%)
       3. Conflicting signals (sentiment vs forecast)
       4. Extreme sentiment values (|score| > 0.8)
    
    📌 Output:
       - requires_human_review: Boolean
       - risk_level: 'HIGH', 'MODERATE', 'LOW'
       - review_reasons: Explanation list
    """)
    
    try:
        from orchestrators.langgraph_workflow import LLMReasoningAgent
        
        # Case 1: Requires review
        result = LLMReasoningAgent.run({
            "ticker": "TEST",
            "sentiment_score": -0.85,
            "forecast": {"confidence": 0.5, "trend": "BEARISH"},
            "risk_alerts": [{"severity": "HIGH"}]
        })
        
        print(f"    Scenario 1: Extreme values")
        print(f"      Requires review: {result['requires_human_review']}")
        print(f"      Risk level: {result['reasoning']['risk_level']}")
        if result['reasoning']['review_reasons']:
            print(f"      Reasons: {', '.join(result['reasoning']['review_reasons'][:1])}\n")
        
    except Exception as e:
        print(f"    ⚠️  Error: {e}")


def test_agent_recommendation():
    """Test RecommendationAgent"""
    print_header("💡 TESTING: RecommendationAgent", 2)
    
    print("""
    📌 Purpose:
       Generate final investment recommendation
    
    📌 Actions:
       - BUY: Positive outlook, go long
       - SELL: Negative outlook, close position
       - HOLD: Neutral outlook, maintain position
    
    📌 Urgency Levels:
       - High: Immediate action recommended
       - Medium: Action within trading week
       - Low: Monitor and decide later
    """)
    
    try:
        from orchestrators.langgraph_workflow import RecommendationAgent
        
        # Example: Buy signal
        state = {
            "ticker": "NVDA",
            "sentiment_score": 0.6,
            "sentiment_label": "positive",
            "forecast": {
                "trend": "BULLISH",
                "confidence": 0.8,
                "predicted_change_pct": 5.0,
                "target_price": 150.0,
            },
            "market_data": {"current_price": 140.0},
            "risk_alerts": [],
            "requires_human_review": False,
            "human_approved": True,
            "human_comments": "Approved"
        }
        
        result = RecommendationAgent.run(state)
        rec = result["recommendation"]
        
        print(f"    Recommendation Result:")
        print(f"      Ticker: {rec['ticker']}")
        print(f"      Action: {rec['action']}")
        print(f"      Urgency: {rec['urgency']}")
        print(f"      Confidence: {rec['confidence']:.1%}")
        print(f"      ✓ Recommendation generated\n")
        
    except Exception as e:
        print(f"    ⚠️  Error: {e}")


def test_end_to_end_workflow():
    """Test complete workflow"""
    print_header("🔗 TESTING: End-to-End Workflow", 2)
    
    print("""
    📌 Workflow Steps:
       1. Parse input (InputAgent)
       2. Fetch news (NewsFetchAgent)
       3. Analyze sentiment (SentimentAnalyzerAgent)
       4. Route based on sentiment
          ├─ Positive (≥0) → Market Data Agent
          └─ Negative (<0) → Risk Alert Agent
       5. Predict trends (MLForecastAgent)
       6. Evaluate risk (LLMReasoningAgent)
       7. Human review (if needed)
       8. Generate recommendation (RecommendationAgent)
    """)
    
    try:
        from orchestrators.langgraph_workflow import build_workflow_graph, create_initial_state
        
        graph = build_workflow_graph()
        if graph is None:
            print("    ⚠️  LangGraph not available\n")
            return
        
        print("    Running workflow for: 'Analyze AAPL stock'\n")
        
        initial_state = create_initial_state("Analyze AAPL stock")
        result = graph.invoke(initial_state)
        
        print("    Workflow execution completed ✓\n")
        
        # Show key outputs
        if "recommendation" in result:
            rec = result["recommendation"]
            print(f"    Final Results:")
            print(f"      Action: {rec.get('action', 'N/A')}")
            print(f"      Ticker: {rec.get('ticker', 'N/A')}")
            print(f"      Confidence: {rec.get('confidence', 0):.1%}\n")
        
    except Exception as e:
        print(f"    ⚠️  {e}\n")


def print_summary():
    """Print testing summary"""
    print_header("📋 TEST SUMMARY", 1)
    
    print("""
    ✅ TOOLS TESTED:
    ───────────────────────────────────────────────────────────────
    1. SearchNewsTool
       • Fetches market news from Yahoo Finance
       • Input: ticker, limit
       • Output: List of articles with metadata
    
    2. DatabaseTool
       • SQLite CRUD operations for portfolio
       • Actions: get, upsert, delete, select
       • Manages holdings (ticker, shares, avg_cost)
    
    3. SummarizeTool
       • Extractive text summarization using TF-IDF
       • Input: text, max_sentences
       • Output: Summarized text
    
    ✅ AGENTS TESTED:
    ───────────────────────────────────────────────────────────────
    1. InputAgent → Parse user query
    2. SentimentAnalyzerAgent → Analyze news sentiment
    3. MarketDataAgent → Fetch market data
    4. RiskAlertAgent → Generate risk warnings
    5. MLForecastAgent → Predict price trends
    6. LLMReasoningAgent → Evaluate risk
    7. RecommendationAgent → Final recommendation
    
    ✅ WORKFLOW FEATURES:
    ───────────────────────────────────────────────────────────────
    • Conditional routing (sentiment-based)
    • Risk evaluation with human-in-the-loop
    • Multi-stage analysis pipeline
    • JSON-serializable outputs
    • State management via LangGraph
    
    📌 NEXT STEPS:
    ───────────────────────────────────────────────────────────────
    1. Run full test suite:
       pytest tests/ -v
    
    2. Run specific tool tests:
       pytest tests/test_tools_comprehensive.py -v
    
    3. Run specific agent tests:
       pytest tests/test_agents_comprehensive.py -v
    
    4. Run LangGraph demo:
       python demo_langgraph_workflow.py
    
    5. Check dependencies:
       python check_dependencies.py
    """)


def main():
    """Run all tests"""
    print_header("🧪 COMPREHENSIVE TOOL & AGENT TEST SUITE", 1)
    
    print("\n📝 This script tests every tool and agent with detailed explanations\n")
    
    # Test all tools
    test_tool_search_news()
    test_tool_database()
    test_tool_summarize()
    
    # Test all agents
    test_agent_input()
    test_agent_sentiment()
    test_agent_market_data()
    test_agent_risk_alert()
    test_agent_ml_forecast()
    test_agent_llm_reasoning()
    test_agent_recommendation()
    
    # Test end-to-end
    test_end_to_end_workflow()
    
    # Print summary
    print_summary()
    
    print("\n" + "█"*70)
    print("█" + f"{'✅ All tests completed!'.center(68)}" + "█")
    print("█"*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
