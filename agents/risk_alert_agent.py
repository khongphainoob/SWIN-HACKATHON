"""
agents/risk_alert_agent.py
Risk Alert Generation Agent
"""
from typing import Any, Dict
from agents.agent_utils import print_agent_banner, print_agent_output, print_agent_summary


class RiskAlertAgent:
    """
    Node 4b: Risk Alert (when sentiment < 0)
    - Generate risk warnings
    - Assess severity
    """
    
    @staticmethod
    def run(state: Dict[str, Any]) -> Dict[str, Any]:
        print_agent_banner("RISK ALERT AGENT", step_number=4)
        
        ticker = state.get("ticker", "UNKNOWN")
        sentiment_score = state.get("sentiment_score", 0)
        articles = state.get("news_articles", [])
        
        print(f"📥 Input:")
        print(f"   • Ticker: {ticker}")
        print(f"   • Sentiment: {sentiment_score:.3f} (Negative path)")
        print(f"   • Articles: {len(articles)}")
        print()
        
        # Generate alerts based on severity
        alerts = []
        
        if sentiment_score < -0.5:
            severity = "HIGH"
            alerts.append({
                "type": "SEVERE_NEGATIVE_SENTIMENT",
                "severity": severity,
                "message": f"⚠️ CRITICAL: {ticker} showing severe negative sentiment ({sentiment_score:.2f})",
                "action": "Consider immediate review of position",
            })
        elif sentiment_score < -0.2:
            severity = "MEDIUM"
            alerts.append({
                "type": "NEGATIVE_SENTIMENT",
                "severity": severity,
                "message": f"⚠️ WARNING: {ticker} showing negative sentiment ({sentiment_score:.2f})",
                "action": "Monitor closely",
            })
        else:
            severity = "LOW"
            alerts.append({
                "type": "CAUTION",
                "severity": severity,
                "message": f"ℹ️ NOTICE: {ticker} sentiment slightly negative ({sentiment_score:.2f})",
                "action": "Continue monitoring",
            })
        
        # Add source-based alerts
        for article in articles[:3]:
            if any(kw in str(article.get("title", "")).lower() 
                   for kw in ["crash", "fraud", "bankruptcy"]):
                alerts.append({
                    "type": "NEWS_ALERT",
                    "severity": "HIGH",
                    "message": f"Critical news detected: {article.get('title', '')[:50]}...",
                    "source": article.get("source", "Unknown"),
                })
        
        result = {
            "risk_alerts": alerts,
            "current_step": "risk_alert_agent",
            "messages": [f"[RiskAlertAgent] Generated {len(alerts)} alerts for {ticker}"],
        }
        
        print_agent_output("Risk Alerts Generated", len(alerts))
        for alert in alerts:
            severity = alert.get("severity", "UNKNOWN")
            msg = alert.get("message", "N/A")[:60]
            print(f"   • [{severity}] {msg}...")
        print_agent_summary(result["messages"])
        
        return result
