"""
agents/planning_agent.py
PlanningAgent: Lập kế hoạch task, phân chia công việc cho các agent khác, orchestrate workflow.
"""
from typing import Optional, Dict, Any, List
from agents.base_agent import Agent

class PlanningAgent(Agent):
    """
    Agent quản lý workflow tổng thể.
    
    Trách nhiệm:
    1. Nhận news stream
    2. Routing: Quyết định task nào đi tới agent nào
    3. Prioritization: Tin tức nào cần xử lý trước
    4. Orchestration: Điều phối các agent khác
    """
    
    def __init__(self, config_path: str = None):
        super().__init__(
            name="PlanningAgent",
            description="Lập kế hoạch workflow, phân chia task cho các agent khác.",
            config_path=config_path
        )
        self.task_queue: List[Dict[str, Any]] = []
        self.agent_registry: Dict[str, Agent] = {}
    
    def register_agent(self, agent_name: str, agent: Agent):
        """Đăng ký một agent để có thể routing task."""
        self.agent_registry[agent_name] = agent
    
    def execute(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Lập kế hoạch và orchestrate workflow.
        
        Args:
            task: {'news_stream': List[NewsEvent], 'action': 'plan_and_orchestrate'}
            context: {'user_profile': UserProfile, 'portfolio': Dict}
        
        Returns:
            {
                'plan': List[Dict],
                'scheduled_tasks': List[Dict],
                'priority_order': List[str]
            }
        """
        news_stream = task.get('news_stream', [])
        
        # STEP 1: Prioritize news by sentiment importance
        prioritized_news = self._prioritize_news(news_stream)
        
        # STEP 2: Create execution plan
        execution_plan = self._create_execution_plan(prioritized_news)
        
        # STEP 3: Route to appropriate agents
        scheduled_tasks = self._route_tasks(execution_plan, context)
        
        result = {
            'plan': execution_plan,
            'scheduled_tasks': scheduled_tasks,
            'priority_order': [item['news_id'] for item in prioritized_news],
            'total_tasks': len(scheduled_tasks)
        }
        
        self.log_execution(task, result, "success")
        return result
    
    def _prioritize_news(self, news_stream: List[Any]) -> List[Any]:
        """
        Ưu tiên hóa tin tức theo các tiêu chí:
        1. Sentiment score (tin xấu trước)
        2. Portfolio relevance (ảnh hưởng trực tiếp)
        3. Verification status (verified tin trước)
        """
        # Giả lập: sắp xếp theo sentiment score (thấp nhất trước = tin xấu nhất)
        prioritized = sorted(
            news_stream,
            key=lambda n: (
                getattr(n, 'sentiment_score', 0.0),  # Ascending
                -len(getattr(n, 'tickers_mentioned', []))  # More relevant first
            )
        )
        return prioritized
    
    def _create_execution_plan(self, news_stream: List[Any]) -> List[Dict[str, Any]]:
        """
        Tạo plan chi tiết về các task sẽ thực hiện.
        
        Returns:
            [
                {
                    'task_id': str,
                    'news_id': str,
                    'target_agent': str,
                    'action': str,
                    'priority': int
                }
            ]
        """
        plan = []
        for idx, news in enumerate(news_stream):
            task = {
                'task_id': f"task_{idx}",
                'news_id': getattr(news, 'news_id', f'news_{idx}'),
                'target_agent': 'SentimentAgent',  # Mặc định route đến SentimentAgent
                'action': 'analyze_and_recommend',
                'priority': idx
            }
            plan.append(task)
        return plan
    
    def _route_tasks(self, execution_plan: List[Dict], context: Optional[Dict]) -> List[Dict[str, Any]]:
        """
        Route tasks đến các agent tương ứng.
        
        Returns: Danh sách tasks đã được schedule với status
        """
        scheduled_tasks = []
        
        for task_plan in execution_plan:
            target_agent_name = task_plan['target_agent']
            
            if target_agent_name not in self.agent_registry:
                # Nếu agent chưa register, log warning
                scheduled_tasks.append({
                    'task_id': task_plan['task_id'],
                    'status': 'pending',
                    'reason': f"Agent {target_agent_name} not registered"
                })
                continue
            
            # Đánh dấu task là scheduled
            scheduled_tasks.append({
                'task_id': task_plan['task_id'],
                'news_id': task_plan['news_id'],
                'target_agent': target_agent_name,
                'priority': task_plan['priority'],
                'status': 'scheduled'
            })
        
        return scheduled_tasks
    
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate output."""
        required_keys = ['plan', 'scheduled_tasks', 'priority_order']
        return all(key in output for key in required_keys)
