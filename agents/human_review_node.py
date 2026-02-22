"""
agents/human_review_node.py
Human Review Node
"""
from typing import Any, Dict
from agents.agent_utils import print_agent_banner, print_agent_output, print_agent_summary


class HumanReviewNode:
    """
    Node 7: Human Review (conditional)
    - Present analysis for human verification
    - Collect approval/rejection
    """
    
    @staticmethod
    def run(state: Dict[str, Any]) -> Dict[str, Any]:
        print_agent_banner("HUMAN REVIEW NODE", step_number=7)
        
        ticker = state.get("ticker", "UNKNOWN")
        reasoning = state.get("reasoning", {})
        
        print(f"📥 Input:")
        print(f"   • Ticker: {ticker}")
        print(f"   • Risk Level: {reasoning.get('risk_level', 'N/A')}")
        print()
        
        # In production, this would pause and wait for human input
        # For demo, we auto-approve with simulation
        print("\n" + "="*60)
        print("🔍 HUMAN REVIEW REQUIRED")
        print("="*60)
        print(f"Ticker: {ticker}")
        print(f"Risk Level: {reasoning.get('risk_level', 'N/A')}")
        print(f"Review Reasons: {reasoning.get('review_reasons', [])}")
        print("="*60)
        
        # Simulate human approval (in real system, this would be interactive)
        human_approved = True
        human_comments = "Reviewed and approved. Proceed with caution."
        
        result = {
            "human_approved": human_approved,
            "human_comments": human_comments,
            "current_step": "human_review_node",
            "messages": [f"[HumanReview] Approved: {human_approved}"],
        }
        
        print_agent_output("Approved", human_approved)
        print_agent_output("Comments", human_comments)
        print_agent_summary(result["messages"])
        
        return result
