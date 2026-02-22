"""
Demo script for LangGraph Workflow
Quick examples to test the system
"""
from langgraph_workflow import run_workflow

def demo_conservative_investor():
    """Demo: Conservative investor với risk tolerance thấp"""
    print("\n" + "="*80)
    print("DEMO 1: CONSERVATIVE INVESTOR (Low Risk, Long Term)")
    print("="*80)
    
    result = run_workflow(
        query="Nên đầu tư vào cổ phiếu JPM không?",
        user_id="conservative_001",
        risk_tolerance="low",
        investment_horizon="long_term",
        investment_amount=20000.0,
        portfolio={
            "BND": {"shares": 500, "avg_price": 80.0},
            "VTI": {"shares": 100, "avg_price": 220.0}
        },
        user_preferences={
            "preferred_sectors": ["financial", "utilities"],
            "dividend_preference": "income"
        }
    )
    
    print("\n📊 RESULT:")
    print(f"Action: {result['recommendation']['action']}")
    print(f"Urgency: {result['recommendation']['urgency']}")
    print(f"Recommended Amount: ${result['recommendation']['recommended_amount']:,.2f}")
    print(f"Confidence: {result['recommendation']['confidence']:.1%}")


def demo_aggressive_trader():
    """Demo: Aggressive trader với risk tolerance cao"""
    print("\n" + "="*80)
    print("DEMO 2: AGGRESSIVE TRADER (High Risk, Short Term)")
    print("="*80)
    
    result = run_workflow(
        query="NVDA có tiềm năng tăng giá không?",
        user_id="tech_bull_99",
        risk_tolerance="high",
        investment_horizon="short_term",
        investment_amount=100000.0,
        portfolio={
            "NVDA": {"shares": 200, "avg_price": 450.0},
            "AMD": {"shares": 300, "avg_price": 120.0},
            "TSLA": {"shares": 100, "avg_price": 250.0}
        },
        user_preferences={
            "preferred_sectors": ["technology", "AI"],
            "growth_focus": True
        }
    )
    
    print("\n📊 RESULT:")
    print(f"Action: {result['recommendation']['action']}")
    print(f"Urgency: {result['recommendation']['urgency']}")
    print(f"Recommended Amount: ${result['recommendation']['recommended_amount']:,.2f}")
    print(f"Confidence: {result['recommendation']['confidence']:.1%}")


def demo_balanced_portfolio():
    """Demo: Balanced investor"""
    print("\n" + "="*80)
    print("DEMO 3: BALANCED INVESTOR (Medium Risk, Medium Term)")
    print("="*80)
    
    result = run_workflow(
        query="Tôi nên đa dạng hóa với AAPL?",
        user_id="balanced_investor",
        risk_tolerance="medium",
        investment_horizon="medium_term",
        investment_amount=50000.0,
        portfolio={
            "VTI": {"shares": 100, "avg_price": 220.0},
            "AGG": {"shares": 150, "avg_price": 105.0},
            "MSFT": {"shares": 50, "avg_price": 300.0}
        },
        user_preferences={
            "diversification_priority": True,
            "dividend_preference": "balanced",
            "esg_priority": False
        }
    )
    
    print("\n📊 RESULT:")
    print(f"Action: {result['recommendation']['action']}")
    print(f"Urgency: {result['recommendation']['urgency']}")
    print(f"Recommended Amount: ${result['recommendation']['recommended_amount']:,.2f}")
    print(f"Confidence: {result['recommendation']['confidence']:.1%}")


def demo_simple_query():
    """Demo: Simple query không có context"""
    print("\n" + "="*80)
    print("DEMO 4: SIMPLE QUERY (No User Context)")
    print("="*80)
    
    result = run_workflow(
        query="What's the outlook for AAPL stock?"
    )
    
    print("\n📊 RESULT:")
    print(f"Action: {result['recommendation']['action']}")
    print(f"Urgency: {result['recommendation']['urgency']}")
    print(f"Confidence: {result['recommendation']['confidence']:.1%}")


def demo_negative_sentiment():
    """Demo: Test với tin tức tiêu cực"""
    print("\n" + "="*80)
    print("DEMO 5: NEGATIVE SENTIMENT (Risk Alert)")
    print("="*80)
    
    result = run_workflow(
        query="FB có đáng lo ngại không?",
        user_id="cautious_investor",
        risk_tolerance="low",
        investment_horizon="long_term",
        investment_amount=15000.0,
        portfolio={
            "FB": {"shares": 100, "avg_price": 180.0}
        }
    )
    
    print("\n📊 RESULT:")
    print(f"Action: {result['recommendation']['action']}")
    print(f"Urgency: {result['recommendation']['urgency']}")
    print(f"Risk Alerts: {len(result['risk_alerts'])}")


if __name__ == "__main__":
    import sys
    
    demos = {
        "1": demo_conservative_investor,
        "2": demo_aggressive_trader,
        "3": demo_balanced_portfolio,
        "4": demo_simple_query,
        "5": demo_negative_sentiment,
        "all": lambda: [demo() for demo in [
            demo_conservative_investor,
            demo_aggressive_trader,
            demo_balanced_portfolio,
            demo_simple_query,
            demo_negative_sentiment
        ]]
    }
    
    if len(sys.argv) > 1:
        choice = sys.argv[1]
        if choice in demos:
            demos[choice]()
        else:
            print("Invalid choice. Use: 1, 2, 3, 4, 5, or all")
    else:
        print("\n" + "="*80)
        print("LANGGRAPH WORKFLOW DEMO")
        print("="*80)
        print("\nChọn demo:")
        print("1. Conservative Investor (Low Risk)")
        print("2. Aggressive Trader (High Risk)")
        print("3. Balanced Investor (Medium Risk)")
        print("4. Simple Query (No Context)")
        print("5. Negative Sentiment Test")
        print("all. Run all demos")
        print("\nUsage: python demo_workflow.py [1-5|all]")
        print("\nExample: python demo_workflow.py 1")
        print("="*80)
