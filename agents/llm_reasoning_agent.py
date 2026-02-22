"""
agents/llm_reasoning_agent.py
LLM-based Reasoning Agent
"""
from typing import Any, Dict
from services.llm_service import LLMService
from agents.agent_utils import print_agent_banner, print_agent_output, print_agent_summary


class LLMReasoningAgent:
    """
    Node 6: LLM-based Risk Evaluation
    - Synthesize all information
    - Determine if human review needed
    """
    
    @staticmethod
    def run(state: Dict[str, Any]) -> Dict[str, Any]:
        print_agent_banner("LLM REASONING AGENT", step_number=6)
        
        ticker = state.get("ticker", "UNKNOWN")
        sentiment_score = state.get("sentiment_score", 0)
        forecast = state.get("forecast", {})
        risk_alerts = state.get("risk_alerts", [])
        
        print(f"📥 Input:")
        print(f"   • Ticker: {ticker}")
        print(f"   • Sentiment: {sentiment_score:.3f}")
        print(f"   • Forecast Trend: {forecast.get('trend', 'N/A')}")
        print(f"   • Risk Alerts: {len(risk_alerts)}")
        print()
        
        # Determine if human review is required
        requires_review = False
        review_reasons = []
        
        # Rule 1: High severity alerts
        high_alerts = [a for a in risk_alerts if a.get("severity") == "HIGH"]
        if high_alerts:
            requires_review = True
            review_reasons.append("High severity alerts detected")
        
        # Rule 2: Low confidence forecast
        if forecast.get("confidence", 1) < 0.6:
            requires_review = True
            review_reasons.append("Low forecast confidence")
        
        # Rule 3: Conflicting signals
        if (sentiment_score > 0 and forecast.get("trend") == "BEARISH") or \
           (sentiment_score < 0 and forecast.get("trend") == "BULLISH"):
            requires_review = True
            review_reasons.append("Conflicting sentiment and forecast signals")
        
        # Rule 4: Extreme values
        if abs(sentiment_score) > 0.8:
            requires_review = True
            review_reasons.append("Extreme sentiment value detected")
        
        llm = LLMService()
        Results = llm.call_llm(
            prompt=f"Given the sentiment score of {sentiment_score}, "
                   f"forecast trend '{forecast.get('trend', 'N/A')}' with confidence {forecast.get('confidence', 0):.1%}, "
                   f"and {len(risk_alerts)} risk alerts, determine if human review is necessary. "
                   f"Provide a brief reasoning.",
            temperature=0.3,
            max_tokens=150,
        ).strip()
        
        # Generate reasoning summary
        reasoning = {
            "ticker": ticker,
            "summary": f"Analysis complete for {ticker}",
            "key_factors": [
                f"Sentiment: {sentiment_score:.2f}",
                f"Forecast: {forecast.get('trend', 'N/A')}",
                f"Alerts: {len(risk_alerts)}",
            ],
            "risk_level": "HIGH" if requires_review else "MODERATE",
            "review_reasons": review_reasons,
            "recommendation_ready": not requires_review,
        }
        
        result = {
            "reasoning": reasoning,
            "requires_human_review": requires_review,
            "current_step": "llm_reasoning_agent",
            "messages": [f"[LLMReasoningAgent] Review required: {requires_review}"],
        }
        
        print_agent_output("Risk Level", reasoning.get("risk_level"))
        print_agent_output("Requires Review", requires_review)
        if review_reasons:
            print("   Review Reasons:")
            for reason in review_reasons:
                print(f"     • {reason}")
        print_agent_summary(result["messages"])
        
        return result
