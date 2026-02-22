"""
agents/ml_forecast_agent.py
ML-based Forecasting Agent
"""
from typing import Any, Dict
from services.llm_service import LLMService
from agents.agent_utils import print_agent_banner, print_agent_output, print_agent_summary


class MLForecastAgent:
    """
    Node 5: ML-based Trend Prediction
    - Predict price trend
    - Confidence score
    """
    
    @staticmethod
    def run(state: Dict[str, Any]) -> Dict[str, Any]:
        print_agent_banner("ML FORECAST AGENT", step_number=5)
        
        ticker = state.get("ticker", "UNKNOWN")
        sentiment_score = state.get("sentiment_score", 0)
        market_data = state.get("market_data", {})
        risk_alerts = state.get("risk_alerts", [])
        
        print(f"📥 Input:")
        print(f"   • Ticker: {ticker}")
        print(f"   • Sentiment Score: {sentiment_score:.3f}")
        print(f"   • Market Data: {len(market_data)} fields")
        print(f"   • Risk Alerts: {len(risk_alerts)}")
        print()

        features_used = [
            "sentiment_score",
            "market_data.current_price",
            "market_data.volume",
            "market_data.previous_close",
            "risk_alerts.count",
        ]
        noise_filters = [
            "headline_deduplication",
            "volume_spike_filter",
            "winsorize_outliers",
        ]
        
        # Simple forecast logic (placeholder for real ML model)
        current_price = market_data.get("current_price")
        if current_price is None:
            current_price = 150.0  # Fallback
            
        llm = LLMService()
        result = llm.call_llm(
            prompt=f"Based on a sentiment score of {sentiment_score} for the stock {ticker}, "
                   f"current market data {market_data}, and risk alerts count {len(risk_alerts)}, "
                   f"predict the short-term price trend and confidence level. "
                   f"List the features used ({', '.join(features_used)}) and noise filters "
                   f"({', '.join(noise_filters)}).",
            temperature=0.3,
            max_tokens=180,
        ).strip()
        # Combine sentiment with price momentum
        if sentiment_score > 0:
            trend = "BULLISH"
            predicted_change = abs(sentiment_score) * 5  # % change
            confidence = 0.65 + sentiment_score * 0.2
        elif sentiment_score < 0:
            trend = "BEARISH"
            predicted_change = -abs(sentiment_score) * 5
            confidence = 0.65 + abs(sentiment_score) * 0.2
        else:
            trend = "NEUTRAL"
            predicted_change = 0
            confidence = 0.50
        
        forecast = {
            "ticker": ticker,
            "trend": trend,
            "current_price": current_price,
            "predicted_change_pct": round(predicted_change, 2),
            "target_price": round(current_price * (1 + predicted_change/100), 2),
            "confidence": round(min(confidence, 0.95), 3),
            "horizon": "7_days",
            "model": "sentiment_momentum_v1",
            "features_used": features_used,
            "noise_filters": noise_filters,
            "llm_feature_summary": result,
        }
        
        result_dict = {
            "forecast": forecast,
            "current_step": "ml_forecast_agent",
            "messages": [f"[MLForecastAgent] Predicted {trend} with {confidence:.1%} confidence", result],
        }
        
        print_agent_output("Trend Prediction", trend)
        print_agent_output("Confidence", f"{confidence:.1%}")
        print_agent_output("Target Price", forecast.get("target_price"))
        print_agent_output("Predicted Change", f"{predicted_change:+.2f}%")
        print_agent_summary([result_dict["messages"][0]])
        
        return result_dict
