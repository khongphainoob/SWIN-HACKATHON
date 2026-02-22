"""
agents/input_agent.py
Input Parsing Agent
"""
from typing import Any, Dict
from services.llm_service import LLMService
from agents.agent_utils import print_agent_banner, print_agent_output, print_agent_summary, _utc_now_iso


class InputAgent:
    """
    Node 1: Parse user input
    - Extract ticker symbol
    - Validate query
    """
    
    @staticmethod
    def run(state: Dict[str, Any]) -> Dict[str, Any]:
        print_agent_banner("INPUT AGENT", step_number=1)
        
        user_query = state.get("user_query", "")
        
        print(f"📥 Input:")
        print(f"   • User Query: {user_query}")
        print()
        
        # Extract ticker (simple heuristic)
        llm = LLMService()
        llm_response = llm.call_llm(
            prompt=f"Extract the stock ticker symbol from the following query: '{user_query}'. "
                   f"If no ticker is found, respond with 'UNKNOWN'.",
            temperature=0.0,
            max_tokens=10,
        ).strip().upper()
        
        result = {
            "ticker": llm_response,
            "current_step": "input_agent",
            "messages": [f"[InputAgent] Parsed query: '{user_query}' → ticker: {llm_response}"],
            "timestamp": _utc_now_iso(),
        }
        
        print_agent_output("Ticker Extracted", llm_response)
        print_agent_summary(result["messages"])
        
        return result
    
    @staticmethod
    def _extract_ticker(query: str) -> str:
        """Extract ticker symbol from query."""
        import re
        # Match uppercase 1-5 letter words (typical ticker format)
        matches = re.findall(r'\b[A-Z]{1,5}\b', query.upper())
        
        # Common stock tickers
        known_tickers = {"AAPL", "MSFT", "GOOGL", "NVDA", "TSLA", "META", "AMZN", "JPM", "GLD"}
        
        for match in matches:
            if match in known_tickers:
                return match
        
        return matches[0] if matches else "UNKNOWN"
