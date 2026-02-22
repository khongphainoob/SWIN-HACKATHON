"""
agents/recommendation_agent.py
Final Recommendation Generation Agent
"""
from typing import Any, Dict
from services.llm_service import LLMService
from agents.agent_utils import print_agent_banner, print_agent_output, print_agent_summary, _utc_now_iso


class RecommendationAgent:
    """
    Node 8: Final Recommendation
    - Generate actionable recommendation
    - Include confidence and reasoning
    """
    
    @staticmethod
    def run(state: Dict[str, Any]) -> Dict[str, Any]:
        print_agent_banner("RECOMMENDATION AGENT", step_number=8)
        
        ticker = state.get("ticker", "UNKNOWN")
        sentiment_score = state.get("sentiment_score", 0)
        sentiment_label = state.get("sentiment_label", "neutral")
        forecast = state.get("forecast", {})
        risk_alerts = state.get("risk_alerts", [])
        market_data = state.get("market_data", {})
        human_approved = state.get("human_approved", True)
        human_comments = state.get("human_comments", "")
        
        # User context
        user_id = state.get("user_id", "anonymous")
        risk_tolerance = state.get("risk_tolerance", "medium")
        investment_horizon = state.get("investment_horizon", "medium_term")
        investment_amount = state.get("investment_amount", 10000.0)
        portfolio = state.get("portfolio", {})
        
        print(f"📥 Input:")
        print(f"   • Ticker: {ticker}")
        print(f"   • Sentiment: {sentiment_label} ({sentiment_score:.3f})")
        print(f"   • Forecast: {forecast.get('trend', 'N/A')}")
        print(f"   • User: {user_id} | Risk: {risk_tolerance}")
        print(f"   • Amount: ${investment_amount:,.2f}")
        print()
        
        # Điều chỉnh action dựa trên risk tolerance
        if sentiment_score > 0.3 and forecast.get("trend") == "BULLISH":
            action = "BUY"
            urgency = "High" if risk_tolerance == "high" else "Medium"
        elif sentiment_score < -0.3 or len([a for a in risk_alerts if a.get("severity") == "HIGH"]) > 0:
            action = "SELL"
            urgency = "High" if risk_tolerance in ["low", "medium"] else "Medium"
        elif abs(sentiment_score) < 0.2:
            action = "HOLD"
            urgency = "Low"
        else:
            action = "HOLD"
            urgency = "Medium"
        
        # Điều chỉnh recommended amount
        if action == "BUY":
            if risk_tolerance == "high":
                recommended_amount = investment_amount * 0.8
            elif risk_tolerance == "medium":
                recommended_amount = investment_amount * 0.5
            else:
                recommended_amount = investment_amount * 0.3
        else:
            recommended_amount = 0.0
        
        # Build recommendation
        recommendation = {
            "ticker": ticker,
            "action": action,
            "urgency": urgency,
            "confidence": forecast.get("confidence", 0.5),
            "recommended_amount": round(recommended_amount, 2),
            
            "user_context": {
                "user_id": user_id,
                "risk_tolerance": risk_tolerance,
                "investment_horizon": investment_horizon,
                "portfolio_holdings": len(portfolio),
            },
            
            "analysis": {
                "sentiment": {
                    "score": sentiment_score,
                    "label": sentiment_label,
                },
                "forecast": forecast,
                "alerts_count": len(risk_alerts),
                "current_price": market_data.get("current_price"),
            },
            
            "reasoning": [
                f"Sentiment analysis: {sentiment_label} ({sentiment_score:.2f})",
                f"ML forecast: {forecast.get('trend', 'N/A')} with {forecast.get('confidence', 0):.1%} confidence",
                f"Risk alerts: {len(risk_alerts)} detected",
                f"User risk tolerance: {risk_tolerance}",
                f"Investment horizon: {investment_horizon}",
            ],
            
            "human_review": {
                "required": state.get("requires_human_review", False),
                "approved": human_approved,
                "comments": human_comments,
            },
            
            "timestamp": _utc_now_iso(),
        }
        
        llm = LLMService()
        response = llm.call_llm(
            prompt=f"Based on the following analysis, provide a concise investment recommendation for {ticker}:\n"
                   f"Sentiment: {sentiment_label} ({sentiment_score:.2f})\n"
                   f"Forecast: {forecast.get('trend', 'N/A')} with {forecast.get('confidence', 0):.1%} confidence\n"
                   f"Risk Alerts: {len(risk_alerts)} detected\n"
                   f"Market Data: Current Price {market_data.get('current_price')}\n"
                   f"User Profile: Risk Tolerance={risk_tolerance}, Horizon={investment_horizon}, Amount=${investment_amount}\n"
                   f"Human Review: {'Approved' if human_approved else 'Not Approved'} - {human_comments}\n"
                   f"Recommend an action (BUY, SELL, HOLD) with urgency level and brief justification.",
            temperature=0.5,
            max_tokens=200,
        ).strip()
        recommendation["llm_summary"] = response
        
        result = {
            "recommendation": recommendation,
            "current_step": "recommendation_agent",
            "messages": [f"[RecommendationAgent] Final: {action} ({urgency} urgency) - ${recommended_amount:.2f}"],
        }
        
        print_agent_output("Action", action)
        print_agent_output("Urgency", urgency)
        print_agent_output("Confidence", f"{forecast.get('confidence', 0):.1%}")
        print_agent_output("Recommended Amount", f"${recommended_amount:,.2f}")
        print_agent_summary(result["messages"])
        
        return result
