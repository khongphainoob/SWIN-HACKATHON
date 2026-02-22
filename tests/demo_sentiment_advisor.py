"""
demo_sentiment_advisor.py
Demo script: Test end-to-end sentiment advisor workflow.
"""
from memory.vector_memory import PortfolioItem, NewsItem, VectorMemory
from memory.conversation_memory import UserProfile, ConversationMemory
from orchestrators.base_orchestrator import SentimentAdvisorOrchestrator

def demo():
    """Demo sentiment advisor system."""
    
    # STEP 1: Khởi tạo Orchestrator
    print("=" * 60)
    print("SENTIMENT ADVISOR - DEMO")
    print("=" * 60)
    
    orchestrator = SentimentAdvisorOrchestrator()
    
    # STEP 2: Set up user profile
    user_profile = UserProfile(
        user_id="user_123",
        risk_tolerance="Moderate",
        notification_threshold=-0.5,
        preferred_actions=["Hold", "Sell", "BuyMore"]
    )
    orchestrator.set_user_profile(user_profile)
    
    # STEP 3: Set up user portfolio
    portfolio = [
        PortfolioItem(
            ticker="AAPL",
            quantity=100,
            avg_cost=150.0,
            current_price=180.0,
            allocation_pct=30.0,
            sector="Technology",
            country="USA"
        ),
        PortfolioItem(
            ticker="MSFT",
            quantity=50,
            avg_cost=300.0,
            current_price=350.0,
            allocation_pct=20.0,
            sector="Technology",
            country="USA"
        ),
        PortfolioItem(
            ticker="JPM",
            quantity=30,
            avg_cost=120.0,
            current_price=145.0,
            allocation_pct=15.0,
            sector="Finance",
            country="USA"
        ),
        PortfolioItem(
            ticker="GLD",
            quantity=50,
            avg_cost=180.0,
            current_price=185.0,
            allocation_pct=10.0,
            sector="Commodity",
            country="USA"
        ),
    ]
    orchestrator.set_user_portfolio(portfolio)
    
    print(f"\n✅ User Profile Setup:")
    print(f"  - Risk Tolerance: {user_profile.risk_tolerance}")
    print(f"  - Portfolio Size: {len(portfolio)} tickers")
    print(f"  - Portfolio Allocation: {sum(p.allocation_pct for p in portfolio):.0f}%")
    
    # STEP 4: Create sample news stream
    news_stream = [
        NewsItem(
            news_id="news_001",
            headline="Apple Q4 earnings miss expectations, stock tumbles",
            content="Apple reported Q4 earnings significantly below analyst expectations...",
            source="Bloomberg",
            timestamp="2026-02-07T10:30:00Z",
            tickers_mentioned=["AAPL", "QQQ"],
            sentiment_score=-0.75
        ),
        NewsItem(
            news_id="news_002",
            headline="Microsoft beats revenue targets, stock rallies",
            content="Microsoft exceeded Q4 revenue targets by 12%...",
            source="Reuters",
            timestamp="2026-02-07T11:00:00Z",
            tickers_mentioned=["MSFT"],
            sentiment_score=0.65
        ),
        NewsItem(
            news_id="news_003",
            headline="Fed signals possible rate cut in March meeting",
            content="Federal Reserve chairman hints at interest rate reduction...",
            source="CNBC",
            timestamp="2026-02-07T11:15:00Z",
            tickers_mentioned=["JPM", "GLD"],
            sentiment_score=0.45
        ),
        NewsItem(
            news_id="news_004",
            headline="Bitcoin crashes after regulatory crackdown rumors",
            content="Unconfirmed reports of new crypto regulations spark selloff...",
            source="Twitter",
            timestamp="2026-02-07T11:30:00Z",
            tickers_mentioned=["BTC"],
            sentiment_score=-0.85
        ),
    ]
    
    print(f"\n📰 News Stream ({len(news_stream)} items):")
    for news in news_stream:
        print(f"  - {news.headline} (Sentiment: {news.sentiment_score:.2f})")
    
    # STEP 5: Process news stream through orchestrator
    print(f"\n⚙️  Processing news stream...")
    result = orchestrator.process_news_stream(news_stream)
    
    # STEP 6: Display results
    print(f"\n{'='*60}")
    print("RESULTS:")
    print(f"{'='*60}")
    
    print(f"\n📊 Processing Summary:")
    print(f"  - News items analyzed: {result['processed_news_count']}")
    print(f"  - Alerts generated: {len(result['alerts_generated'])}")
    
    print(f"\n{'='*60}")
    print("🚨 GENERATED ALERTS:")
    print(f"{'='*60}")
    
    if result['alerts_generated']:
        for idx, alert in enumerate(result['alerts_generated'], 1):
            print(f"\n📌 Alert #{idx}")
            print(f"  Headline: {alert['headline']}")
            print(f"  Message: {alert['alert_message']}")
            print(f"  Recommendation: {alert['recommendation']['action']}")
            print(f"  Urgency: {alert['recommendation'].get('urgency', 'Unknown')}")
            print(f"  Quality Score: {alert['quality_score']:.0%}")
    else:
        print("\nℹ️  No alerts generated (all news below threshold or unverified)")
    
    print(f"\n{'='*60}")
    print("📈 Quality Report:")
    print(f"{'='*60}")
    print(result['quality_report'])
    
    print(f"\n{'='*60}")
    print(result['summary'])
    print(f"{'='*60}")

if __name__ == "__main__":
    demo()
