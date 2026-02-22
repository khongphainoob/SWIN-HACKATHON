"""
demo_langgraph_workflow.py
Demo script to test the LangGraph-based Agentic Workflow

Usage:
    python demo_langgraph_workflow.py
"""
import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from orchestrators.langgraph_workflow import (
    run_workflow,
    build_workflow_graph,
    InputAgent,
    SentimentAnalyzerAgent,
    format_recommendation_output,
    LANGGRAPH_AVAILABLE,
)


def demo_basic():
    """Demo cơ bản - chạy workflow với một query."""
    print("\n" + "="*70)
    print("🎯 DEMO 1: Basic Workflow Execution")
    print("="*70)
    
    query = "What is the outlook for NVDA stock?"
    result = run_workflow(query, verbose=True)
    
    return result


def demo_negative_sentiment():
    """Demo với tin tức tiêu cực - sẽ trigger Risk Alert path."""
    print("\n" + "="*70)
    print("🎯 DEMO 2: Negative Sentiment Path (Risk Alert)")
    print("="*70)
    
    # Chạy với state có sentiment âm để test Risk Alert path
    if not LANGGRAPH_AVAILABLE:
        print("❌ LangGraph not installed. Run: pip install langgraph")
        return None
    
    from orchestrators.langgraph_workflow import (
        WorkflowState,
        create_initial_state,
    )
    
    graph = build_workflow_graph()
    
    # Tạo state với news articles có sentiment âm
    initial_state = create_initial_state("Analyze TSLA stock crash news")
    
    # Execute
    result = graph.invoke(initial_state)
    
    print(format_recommendation_output(result))
    
    return result


def demo_step_by_step():
    """Demo từng bước - chạy và hiển thị intermediate states."""
    print("\n" + "="*70)
    print("🎯 DEMO 3: Step-by-Step Execution with Stream")
    print("="*70)
    
    if not LANGGRAPH_AVAILABLE:
        print("❌ LangGraph not installed. Run: pip install langgraph")
        return None
    
    from orchestrators.langgraph_workflow import create_initial_state
    
    graph = build_workflow_graph()
    initial_state = create_initial_state("Analyze AAPL performance")
    
    print("\n📍 Streaming through nodes...\n")
    
    step = 1
    for state in graph.stream(initial_state):
        node_name = list(state.keys())[0]
        node_output = state[node_name]
        
        print(f"┌─ Step {step}: {node_name}")
        
        # Show key outputs for each node
        if "ticker" in node_output:
            print(f"│  Ticker extracted: {node_output.get('ticker')}")
        if "news_articles" in node_output:
            print(f"│  Articles fetched: {len(node_output.get('news_articles', []))}")
        if "sentiment_score" in node_output:
            print(f"│  Sentiment: {node_output.get('sentiment_score')} ({node_output.get('sentiment_label')})")
        if "market_data" in node_output:
            print(f"│  Current price: {node_output.get('market_data', {}).get('current_price')}")
        if "risk_alerts" in node_output:
            print(f"│  Risk alerts: {len(node_output.get('risk_alerts', []))}")
        if "forecast" in node_output:
            f = node_output.get('forecast', {})
            print(f"│  Forecast: {f.get('trend')} ({f.get('confidence', 0):.1%})")
        if "requires_human_review" in node_output:
            print(f"│  Human review required: {node_output.get('requires_human_review')}")
        if "recommendation" in node_output:
            rec = node_output.get('recommendation', {})
            print(f"│  ★ RECOMMENDATION: {rec.get('action')} ({rec.get('urgency')})")
        
        print(f"└─ Messages: {node_output.get('messages', [])}")
        print()
        
        step += 1
    
    print("✅ Workflow completed!")


def demo_graph_visualization():
    """Demo hiển thị cấu trúc graph."""
    print("\n" + "="*70)
    print("🎯 DEMO 4: Graph Structure Visualization")
    print("="*70)
    
    if not LANGGRAPH_AVAILABLE:
        print("❌ LangGraph not installed")
        return
    
    graph = build_workflow_graph()
    
    print("""
    Graph Structure:
    ================
    
    ┌───────────────┐
    │  input_agent  │  ← Entry Point
    └───────┬───────┘
            │
            ▼
    ┌───────────────┐
    │  news_fetch   │
    └───────┬───────┘
            │
            ▼
    ┌───────────────────────┐
    │  sentiment_analyzer   │
    └───────────┬───────────┘
                │
        ┌───────┴───────┐
        │               │
   sentiment ≥ 0   sentiment < 0
        │               │
        ▼               ▼
    ┌─────────┐   ┌───────────┐
    │ market_ │   │ risk_     │
    │ data    │   │ alert     │
    └────┬────┘   └─────┬─────┘
         │              │
         └──────┬───────┘
                │
                ▼
        ┌───────────────┐
        │  ml_forecast  │
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │ llm_reasoning │
        └───────┬───────┘
                │
        ┌───────┴───────┐
        │               │
    requires        autoapprove
    review              │
        │               │
        ▼               │
    ┌─────────────┐     │
    │human_review │     │
    └──────┬──────┘     │
           │            │
           └──────┬─────┘
                  │
                  ▼
        ┌─────────────────┐
        │ recommendation  │
        └────────┬────────┘
                 │
                 ▼
            ┌─────────┐
            │   END   │
            └─────────┘
    """)
    
    # Try to get graph structure
    try:
        # Get nodes
        print("\n📊 Graph Nodes:")
        for node in ["input_agent", "news_fetch", "sentiment_analyzer", 
                     "market_data", "risk_alert", "ml_forecast",
                     "llm_reasoning", "human_review", "recommendation"]:
            print(f"  • {node}")
        
        print("\n🔗 Conditional Edges:")
        print("  • sentiment_analyzer → market_data (if sentiment ≥ 0)")
        print("  • sentiment_analyzer → risk_alert (if sentiment < 0)")
        print("  • llm_reasoning → human_review (if requires review)")
        print("  • llm_reasoning → recommendation (if autoapprove)")
        
    except Exception as e:
        print(f"Could not inspect graph: {e}")


def demo_multiple_tickers():
    """Demo với nhiều tickers khác nhau."""
    print("\n" + "="*70)
    print("🎯 DEMO 5: Multiple Tickers Analysis")
    print("="*70)
    
    tickers = ["AAPL", "MSFT", "NVDA"]
    
    for ticker in tickers:
        print(f"\n{'─'*50}")
        print(f"📈 Analyzing {ticker}...")
        print(f"{'─'*50}")
        
        result = run_workflow(f"What's the outlook for {ticker}?", verbose=False)
        
        rec = result.get("recommendation", {})
        print(f"  Ticker: {rec.get('ticker')}")
        print(f"  Action: {rec.get('action')}")
        print(f"  Urgency: {rec.get('urgency')}")
        print(f"  Confidence: {rec.get('confidence', 0):.1%}")
        
        sentiment = rec.get("analysis", {}).get("sentiment", {})
        print(f"  Sentiment: {sentiment.get('label')} ({sentiment.get('score', 0):.3f})")


def main():
    """Run all demos."""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  🚀 LANGGRAPH AGENTIC WORKFLOW DEMO".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    if not LANGGRAPH_AVAILABLE:
        print("\n❌ ERROR: langgraph not installed!")
        print("Please install with: pip install langgraph")
        print("\nAlternatively, you can still view the code structure.")
        demo_graph_visualization()
        return
    
    # Run demos
    try:
        demo_graph_visualization()
        demo_step_by_step()
        demo_basic()
        # demo_negative_sentiment()  # Uncomment to test risk alert path
        # demo_multiple_tickers()    # Uncomment for multi-ticker analysis
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*70)
    print("✅ Demo completed!")
    print("="*70)


if __name__ == "__main__":
    main()
