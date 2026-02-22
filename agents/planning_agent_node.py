"""
agents/planning_agent_node.py
Planning & Orchestration Agent
"""
from typing import Any, Dict
from agents.planning_agent import PlanningAgent
from agents.agent_utils import print_agent_banner, print_agent_output, print_agent_summary, _utc_now_iso


class PlanningAgentNode:
    """
    Node 0: Planning & Orchestration
    - Analyze user query and context
    - Create execution plan
    - Prioritize tasks
    - Determine workflow routing
    """
    
    _planning_agent = None
    
    @classmethod
    def get_agent(cls) -> PlanningAgent:
        """Singleton pattern for PlanningAgent instance."""
        if cls._planning_agent is None:
            cls._planning_agent = PlanningAgent()
        return cls._planning_agent
    
    @staticmethod
    def run(state: Dict[str, Any]) -> Dict[str, Any]:
        # Display agent start
        print_agent_banner("PLANNING AGENT", step_number=0)
        
        user_query = state.get("user_query", "")
        ticker = state.get("ticker", "UNKNOWN")
        
        print(f"📥 Input:")
        print(f"   • User Query: {user_query}")
        print(f"   • Ticker: {ticker}")
        print()
        
        # Create a task representation for the planning agent
        planning_task = {
            'user_query': user_query,
            'ticker': ticker,
            'action': 'plan_workflow',
            'news_stream': []  # Will be populated after news fetch
        }
        
        # Execute planning
        try:
            planning_agent = PlanningAgentNode.get_agent()
            plan_result = planning_agent.execute(planning_task)
            
            execution_plan = plan_result.get('plan', [])
            priority_order = plan_result.get('priority_order', [])
            
            result = {
                "execution_plan": execution_plan,
                "priority_order": priority_order,
                "planned_workflow": {
                    "total_tasks": plan_result.get('total_tasks', 0),
                    "planning_timestamp": _utc_now_iso(),
                    "workflow_strategy": "sentiment_driven_analysis"
                },
                "current_step": "planning_agent",
                "messages": [
                    f"[PlanningAgent] Created execution plan with {len(execution_plan)} tasks",
                    f"[PlanningAgent] Priority order: {priority_order[:3]}..."
                ],
            }
            
            # Display output
            print_agent_output("Execution Plan", execution_plan)
            print_agent_output("Priority Order", priority_order)
            print_agent_output("Total Tasks", plan_result.get('total_tasks', 0))
            print_agent_summary(result["messages"])
            
            return result
        except Exception as e:
            result = {
                "execution_plan": [],
                "priority_order": [],
                "planned_workflow": {},
                "current_step": "planning_agent",
                "messages": [f"[PlanningAgent] Warning: {str(e)} - Proceeding with default workflow"],
                "errors": [f"Planning agent error: {str(e)}"],
            }
            print(f"❌ Error: {str(e)}")
            print_agent_summary(result["messages"])
            return result
