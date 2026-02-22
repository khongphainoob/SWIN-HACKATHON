"""
orchestrators/langgraph_workflow.py
LangGraph-based Agentic Workflow Implementation

Workflow:
User Input → Planning Agent → Input Agent → News Fetch → Sentiment Analyzer
                    │                                           │
                    │                     ┌─────────────────────┴─────────────────────┐
              (Orchestrate)          sentiment ≥ 0                              sentiment < 0
                    │                     │                                           │
                    │                     ▼                                           ▼
                    │              Market Data Agent                           Risk Alert Agent
                    │                     │                                           │
                    │                     └─────────────┬─────────────────────────────┘
                    │                                   ▼
                    │                          ML Forecast Agent
                    │                                   │
                    └──────(Plan & Monitor)────────────▼
                                             LLM Reasoning Agent
                                                       │
                                         ┌─────────────┴─────────────┐
                                    requires review             autoapprove
                                         │                           │
                                         ▼                           │
                                   Human Review Node                 │
                                         └───────────┬───────────────┘
                                                     ▼
                                          Recommendation Agent → END
"""
from __future__ import annotations

import operator
from typing import Annotated, Any, Dict, List, Literal, Optional, TypedDict, Union
from dataclasses import dataclass, field
from datetime import datetime, timezone

# LangGraph imports
try:
    from langgraph.graph import StateGraph, END
    from langgraph.checkpoint.memory import MemorySaver
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    print("Warning: langgraph not installed. Run: pip install langgraph")

from services.llm_service import LLMService
from services.news_sentiment_service import NewsSentimentRAGService
from agents.planning_agent import PlanningAgent

# Import all agent nodes from agents package
from agents import (
    PlanningAgentNode,
    InputAgent,
    NewsFetchAgent,
    SentimentAnalyzerAgent,
    MarketDataAgent,
    RiskAlertAgent,
    MLForecastAgent,
    LLMReasoningAgent,
    HumanReviewNode,
    RecommendationAgent,
)
from agents.agent_utils import _utc_now_iso

# ============================================================================
# STEP 1: STATE SCHEMA DEFINITION
# ============================================================================

LLM = LLMService()  # Shared LLM service instance LLMService()  # Shared LLM service instance
class WorkflowState(TypedDict, total=False):
    """
    State schema cho toàn bộ workflow.
    Mỗi node sẽ đọc và ghi vào state này.
    """
    # INPUT
    user_query: str                          # Query gốc từ user
    ticker: str                              # Ticker symbol được extract
    
    # USER CONTEXT (NEW)
    user_id: str                             # User identifier
    risk_tolerance: str                      # low/medium/high
    investment_horizon: str                  # short_term/medium_term/long_term
    investment_amount: float                 # Số tiền dự định đầu tư
    portfolio: Dict[str, Any]                # Danh mục hiện tại
    user_preferences: Dict[str, Any]         # Tùy chọn người dùng
    
    # NEWS FETCH
    news_articles: List[Dict[str, Any]]      # Danh sách tin tức
    
    # SENTIMENT ANALYSIS
    sentiment_score: float                   # -1.0 đến 1.0
    sentiment_label: str                     # positive/neutral/negative
    sentiment_details: Dict[str, Any]        # Chi tiết phân tích
    
    # MARKET DATA
    market_data: Dict[str, Any]              # Giá, volume, etc.
    
    # RISK ALERT
    risk_alerts: List[Dict[str, Any]]        # Cảnh báo rủi ro
    
    # ML FORECAST
    forecast: Dict[str, Any]                 # Dự đoán xu hướng
    
    # LLM REASONING
    reasoning: Dict[str, Any]                # Phân tích của LLM
    requires_human_review: bool              # Có cần human review không
    
    # HUMAN REVIEW
    human_approved: bool                     # Kết quả review
    human_comments: str                      # Ghi chú từ human
    
    # RECOMMENDATION
    recommendation: Dict[str, Any]           # Khuyến nghị cuối cùng
    
    # PLANNING (NEW)
    execution_plan: List[Dict[str, Any]]     # Kế hoạch thực thi từ PlanningAgent
    priority_order: List[str]                # Thứ tự ưu tiên
    planned_workflow: Dict[str, Any]         # Thông tin workflow được lập kế hoạch
    
    # METADATA
    messages: Annotated[List[str], operator.add]  # Log messages
    errors: List[str]                        # Errors encountered
    current_step: str                        # Bước hiện tại
    timestamp: str                           # Timestamp


# ============================================================================
# STEP 2: ROUTING FUNCTIONS (Conditional Edges)
# ============================================================================



def route_after_sentiment(state: WorkflowState) -> Literal["market_data", "risk_alert"]:
    """
    Router sau Sentiment Analyzer:
    - sentiment >= 0 → Market Data Agent
    - sentiment < 0 → Risk Alert Agent
    """
    sentiment_score = state.get("sentiment_score", 0)
    
    if sentiment_score >= 0:
        return "market_data"
    else:
        return "risk_alert"


def route_after_reasoning(state: WorkflowState) -> Literal["human_review", "recommendation"]:
    """
    Router sau LLM Reasoning:
    - requires_human_review → Human Review Node
    - autoapprove → Recommendation Agent
    """
    requires_review = state.get("requires_human_review", False)
    
    if requires_review:
        return "human_review"
    else:
        return "recommendation"


# ============================================================================
# STEP 4: BUILD THE GRAPH
# ============================================================================

def build_workflow_graph() -> Optional["StateGraph"]:
    """
    Build the complete LangGraph workflow.
    
    Returns:
        Compiled StateGraph or None if langgraph not available
    """
    if not LANGGRAPH_AVAILABLE:
        print("Error: langgraph not installed")
        return None
    
    # Initialize graph with state schema
    workflow = StateGraph(WorkflowState)
    
    # ---- ADD NODES ----
    # Add Planning Agent as first node
    workflow.add_node("planning_agent", PlanningAgentNode.run)
    workflow.add_node("input_agent", InputAgent.run)
    workflow.add_node("news_fetch_agent", NewsFetchAgent.run)
    workflow.add_node("sentiment_analyzer_agent", SentimentAnalyzerAgent.run)
    workflow.add_node("market_data_agent", MarketDataAgent.run)
    workflow.add_node("risk_alert_agent", RiskAlertAgent.run)
    workflow.add_node("ml_forecast_agent", MLForecastAgent.run)
    workflow.add_node("llm_reasoning_agent", LLMReasoningAgent.run)
    workflow.add_node("human_review_agent", HumanReviewNode.run)
    workflow.add_node("recommendation_agent", RecommendationAgent.run)
    
    # ---- ADD EDGES ----
    # Add planning edge at the beginning
    workflow.add_edge("planning_agent", "input_agent")
    
    # Linear flow: input → news → sentiment
    workflow.add_edge("input_agent", "news_fetch_agent")
    workflow.add_edge("news_fetch_agent", "sentiment_analyzer_agent")
    
    # Conditional: sentiment → market_data OR risk_alert
    workflow.add_conditional_edges(
        "sentiment_analyzer_agent",
        route_after_sentiment,
        {
            "market_data": "market_data_agent",
            "risk_alert": "risk_alert_agent",
        }
    )
    
    # Both paths converge to ml_forecast
    workflow.add_edge("market_data_agent", "ml_forecast_agent")
    workflow.add_edge("risk_alert_agent", "ml_forecast_agent")
    
    # Continue: ml_forecast → llm_reasoning
    workflow.add_edge("ml_forecast_agent", "llm_reasoning_agent")
    
    # Conditional: llm_reasoning → human_review OR recommendation
    workflow.add_conditional_edges(
        "llm_reasoning_agent",
        route_after_reasoning,
        {
            "human_review": "human_review_agent",
            "recommendation": "recommendation_agent",
        }
    )
    
    # Human review → recommendation
    workflow.add_edge("human_review_agent", "recommendation_agent")
    
    # Final edge to END
    workflow.add_edge("recommendation_agent", END)
    
    # ---- SET ENTRY POINT ----
    # Set Planning Agent as the new entry point
    workflow.set_entry_point("planning_agent")
    
    # ---- COMPILE ----
    # Optional: Add memory saver for checkpointing
    # memory = MemorySaver()
    # compiled = workflow.compile(checkpointer=memory)
    
    compiled = workflow.compile()
    
    return compiled


# ============================================================================
# STEP 5: HELPER FUNCTIONS
# ============================================================================

def create_initial_state(
    user_query: str,
    user_id: str = "anonymous",
    risk_tolerance: str = "medium",
    investment_horizon: str = "medium_term",
    investment_amount: float = 10000.0,
    portfolio: Optional[Dict[str, Any]] = None,
    user_preferences: Optional[Dict[str, Any]] = None,
) -> WorkflowState:
    """Create initial state for workflow execution with user context.
    
    Args:
        user_query: User's investment question
        user_id: Unique user identifier
        risk_tolerance: low/medium/high
        investment_horizon: short_term (< 1yr) / medium_term (1-5yr) / long_term (> 5yr)
        investment_amount: Amount user plans to invest
        portfolio: Current holdings {ticker: {shares, avg_price, ...}}
        user_preferences: Additional preferences {preferred_sectors, avoid_sectors, ...}
    """
    return {
        "user_query": user_query,
        "messages": [],
        "errors": [],
        "timestamp": _utc_now_iso(),
        # User context
        "user_id": user_id,
        "risk_tolerance": risk_tolerance,
        "investment_horizon": investment_horizon,
        "investment_amount": investment_amount,
        "portfolio": portfolio or {},
        "user_preferences": user_preferences or {},
        # Initialize all optional fields to prevent None errors
        "news_articles": [],
        "sentiment_score": 0.0,
        "sentiment_label": "neutral",
        "sentiment_details": {},
        "market_data": {},
        "risk_alerts": [],
        "forecast": {},
        "reasoning": {},
        "requires_human_review": False,
        "human_approved": False,
        "human_comments": "",
        "recommendation": {},
        # Planning fields
        "execution_plan": [],
        "priority_order": [],
        "planned_workflow": {},
    }

def visualize_workflow_graph(graph: StateGraph, output_path: str = "workflow_graph.png") -> None:
    """Visualize the workflow graph and save to file."""
    try:
        # Get PNG data from Mermaid graph
        png_data = graph.get_graph().draw_mermaid_png()
        
        # Save to file
        with open(output_path, "wb") as f:
            f.write(png_data)
        
        print(f"✅ Workflow graph saved to: {output_path}")
        
    except Exception as e:
        print(f"⚠️ Could not visualize graph: {e}")
        print("Tip: Install group 'pygraphviz' or use Mermaid live editor with the following markup:")
        try:
            print("\n" + graph.get_graph().draw_mermaid())
        except:
            pass

def format_recommendation_output(result: WorkflowState) -> str:
    """Format final recommendation as human-readable string."""
    rec = result.get("recommendation", {})
    planned = result.get("planned_workflow", {})
    user_ctx = rec.get("user_context", {})
    confidence_val = rec.get('confidence', 0)
    confidence_str = f"{confidence_val:.1%}"
    recommended_amt = rec.get('recommended_amount', 0)
    
    output = f"""
╔══════════════════════════════════════════════════════════════╗
║                    📊 INVESTMENT RECOMMENDATION               ║
╠══════════════════════════════════════════════════════════════╣
║  Ticker: {rec.get('ticker', 'N/A'):<52} ║
║  Action: {rec.get('action', 'N/A'):<52} ║
║  Urgency: {rec.get('urgency', 'N/A'):<51} ║
║  Confidence: {confidence_str:<48} ║
║  Recommended Amount: ${recommended_amt:,.2f}{' '*(35-len(f'{recommended_amt:,.2f}'))} ║
╠══════════════════════════════════════════════════════════════╣
║  USER PROFILE                                                ║
╠══════════════════════════════════════════════════════════════╣
║  User ID: {user_ctx.get('user_id', 'N/A'):<50} ║
║  Risk Tolerance: {user_ctx.get('risk_tolerance', 'N/A'):<45} ║
║  Investment Horizon: {user_ctx.get('investment_horizon', 'N/A'):<42} ║
║  Portfolio Holdings: {user_ctx.get('portfolio_holdings', 0):<42} ║
╠══════════════════════════════════════════════════════════════╣
║  PLANNING INFORMATION                                        ║
╠══════════════════════════════════════════════════════════════╣
║  Total Tasks: {planned.get('total_tasks', 0):<47} ║
║  Strategy: {planned.get('workflow_strategy', 'N/A'):<50} ║
╠══════════════════════════════════════════════════════════════╣
║  ANALYSIS SUMMARY                                            ║
╠══════════════════════════════════════════════════════════════╣"""
    
    for reason in rec.get("reasoning", []):
        output += f"\n║  • {reason:<56} ║"
    
    output += f"""
╠══════════════════════════════════════════════════════════════╣
║  Human Review: {'Yes' if rec.get('human_review', {}).get('required') else 'No':<46} ║
║  Approved: {'Yes' if rec.get('human_review', {}).get('approved') else 'No':<50} ║
╚══════════════════════════════════════════════════════════════╝
"""
    return output


def print_execution_log(result: WorkflowState) -> None:
    """Print execution log from state messages."""
    print("\n📋 EXECUTION LOG:")
    print("-" * 40)
    for msg in result.get("messages", []):
        print(f"  {msg}")
    print("-" * 40)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def run_workflow(
    query: str,
    verbose: bool = True,
    user_id: str = "anonymous",
    risk_tolerance: str = "medium",
    investment_horizon: str = "medium_term",
    investment_amount: float = 10000.0,
    portfolio: Optional[Dict[str, Any]] = None,
    user_preferences: Optional[Dict[str, Any]] = None,
) -> WorkflowState:
    """
    Run the complete workflow for a given query.
    
    Args:
        query: User query (e.g., "Analyze NVDA stock")
        verbose: Print execution details
        user_id: Unique user identifier
        risk_tolerance: low/medium/high
        investment_horizon: short_term/medium_term/long_term
        investment_amount: Amount to invest
        portfolio: Current holdings
        user_preferences: User preferences
    
    Returns:
        Final workflow state with recommendation
    """
    if verbose:
        print(f"\n🚀 Starting workflow for: '{query}'")
        print(f"📊 User: {user_id} | Risk: {risk_tolerance} | Horizon: {investment_horizon}")
        print("=" * 60)
    
    # Build graph
    graph = build_workflow_graph()
    if graph is None:
        return {"errors": ["LangGraph not available"]}
    
    # Create initial state
    initial_state = create_initial_state(
        query,
        user_id=user_id,
        risk_tolerance=risk_tolerance,
        investment_horizon=investment_horizon,
        investment_amount=investment_amount,
        portfolio=portfolio,
        user_preferences=user_preferences,
    )
    
    # Execute workflow
    result = graph.invoke(initial_state)
    
    if verbose:
        print_execution_log(result)
        print(format_recommendation_output(result))
    
    return result


if __name__ == "__main__":
    # Demo execution với full context
    print("\n" + "="*70)
    print("DEMO 1: Simple Query")
    print("="*70)
    
    result = run_workflow(
        query="What's the outlook for NVDA stock?",
        user_id="user_123",
        risk_tolerance="high",
        investment_horizon="long_term",
        investment_amount=50000.0,
        portfolio={
            "AAPL": {"shares": 100, "avg_price": 150.0},
            "MSFT": {"shares": 50, "avg_price": 300.0}
        },
        user_preferences={
            "preferred_sectors": ["technology", "AI"],
            "avoid_sectors": ["tobacco", "gambling"]
        }
    )
    
    print("\n" + "="*70)
    print("DEMO 2: Test Sentiment Analyzer")
    print("="*70)
    
    sentiment = SentimentAnalyzerAgent.run({
        "news_articles": [  
            {"title": "NVDA stock surges after earnings beat", "summary": "NVIDIA reported strong quarterly results, beating analyst expectations and raising guidance for the next quarter."},
            {"title": "NVIDIA faces lawsuit over alleged GPU defects", "summary": "A class-action lawsuit has been filed against NVIDIA, alleging that certain GPU models have manufacturing defects causing overheating and performance issues."}
        ]
    })
    print(f"Sentiment Score: {sentiment['sentiment_score']}, Label: {sentiment['sentiment_label']}")
    print(f"Method: {sentiment['sentiment_details'].get('method')}")
    print(f"Features: {sentiment['sentiment_details'].get('features_used')}")

