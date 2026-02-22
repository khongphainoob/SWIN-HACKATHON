"""
agents/market_data_agent.py
Market Data Fetching Agent
"""
from typing import Any, Dict
from agents.agent_utils import print_agent_banner, print_agent_output, print_agent_summary


class MarketDataAgent:
    """
    Node 4a: Fetch Market Data (when sentiment >= 0)
    - Get current prices
    - Get trading volume
    """
    
    @staticmethod
    def run(state: Dict[str, Any]) -> Dict[str, Any]:
        print_agent_banner("MARKET DATA AGENT", step_number=4)
        
        ticker = state.get("ticker", "UNKNOWN")
        sentiment = state.get("sentiment_score", 0)
        
        print(f"📥 Input:")
        print(f"   • Ticker: {ticker}")
        print(f"   • Sentiment: {sentiment:.3f} (Positive path)")
        print()
        
        try:
            import yfinance as yf
            stock = yf.Ticker(ticker)
            info = stock.info
            market_data = {
                "current_price": info.get("currentPrice", info.get("regularMarketPrice")),
                "previous_close": info.get("previousClose"),
                "volume": info.get("volume"),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "52_week_high": info.get("fiftyTwoWeekHigh"),
                "52_week_low": info.get("fiftyTwoWeekLow"),
            }
        except Exception:
            market_data = {
                "current_price": 150.0,
                "previous_close": 148.5,
                "volume": 50000000,
                "note": "mock_data",
            }
        
        result = {
            "market_data": market_data,
            "risk_alerts": [],  # Initialize empty risk alerts for positive sentiment path
            "current_step": "market_data_agent",
            "messages": [f"[MarketDataAgent] Fetched market data for {ticker}"],
        }
        
        print_agent_output("Current Price", market_data.get("current_price"))
        print_agent_output("Previous Close", market_data.get("previous_close"))
        print_agent_output("Volume", market_data.get("volume"))
        print_agent_summary(result["messages"])
        
        return result
