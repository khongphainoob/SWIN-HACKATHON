"""
orchestrators/base_orchestrator.py
Orchestrator: Điều phối toàn bộ agentic workflow - từ news input đến user alert.
"""
from typing import List, Dict, Any, Optional
from agents.base_agent import Agent
from agents.planning_agent import PlanningAgent
from agents.custom.sentiment_agent import SentimentAgent
from agents.monitoring_agent import MonitoringAgent
from memory.vector_memory import VectorMemory, NewsItem
from memory.conversation_memory import ConversationMemory

class SentimentAdvisorOrchestrator:
    """
    Orchestrator chính: Quản lý tất cả agents, điều phối workflow.
    
    Flow:
    1. [INPUT] Nhận news stream
    2. [PlanningAgent] Ưu tiên hóa tin, tạo execution plan
    3. [SentimentAgent] Phân tích sentiment, tính impact, tạo recommendations
    4. [MonitoringAgent] Validate quality của recommendations
    5. [OUTPUT] Gửi smart alerts tới user
    """
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path
        
        # Initialize agents
        self.planning_agent = PlanningAgent(config_path)
        self.sentiment_agent = SentimentAgent(config_path)
        self.monitoring_agent = MonitoringAgent(config_path)
        
        # Initialize shared memory
        self.vector_memory = VectorMemory()
        self.conversation_memory = ConversationMemory()
        
        # Share memory across agents
        self._share_memory_across_agents()
        
        # Register agents to planning agent
        self.planning_agent.register_agent('SentimentAgent', self.sentiment_agent)
        self.planning_agent.register_agent('MonitoringAgent', self.monitoring_agent)
        
        # Store results
        self.processed_alerts: List[Dict] = []
    
    def _share_memory_across_agents(self):
        """Chia sẻ vector memory và conversation memory giữa các agents."""
        for agent in [self.sentiment_agent, self.monitoring_agent]:
            agent.set_vector_memory(self.vector_memory)
            agent.set_conversation_memory(self.conversation_memory)
    
    def set_user_portfolio(self, portfolio_items: List[Any]):
        """Thiết lập danh mục đầu tư của user."""
        self.vector_memory.set_portfolio(portfolio_items)
    
    def set_user_profile(self, user_profile: Any):
        """Thiết lập user profile."""
        self.conversation_memory.user_profile = user_profile
    
    def process_news_stream(self, news_stream: List[Any]) -> Dict[str, Any]:
        """
        Main orchestration loop.
        
        Args:
            news_stream: Danh sách tin tức mới nhất
        
        Returns:
            {
                'processed_news_count': int,
                'alerts_generated': List[Dict],
                'quality_report': str,
                'summary': str
            }
        """
        # STEP 1: Planning - Ưu tiên hóa và tạo execution plan
        planning_result = self.planning_agent.execute(
            task={'news_stream': news_stream, 'action': 'plan_and_orchestrate'},
            context={
                'user_profile': self.conversation_memory.user_profile,
                'portfolio': self.vector_memory.get_portfolio()
            }
        )
        
        scheduled_tasks = planning_result['scheduled_tasks']
        priority_order = planning_result['priority_order']
        
        # STEP 2: Process each news item through SentimentAgent
        sentiment_results = []
        for task in scheduled_tasks:
            if task['status'] != 'scheduled':
                continue
            
            # Find corresponding news item
            news_item = self._find_news_by_id(news_stream, task['news_id'])
            if not news_item:
                continue
            
            # Execute sentiment analysis
            sentiment_result = self.sentiment_agent.execute(
                task={'news': news_item, 'action': 'analyze'},
                context={
                    'user_profile': self.conversation_memory.user_profile,
                    'portfolio': self.vector_memory.get_portfolio()
                }
            )
            sentiment_results.append(sentiment_result)
            
            # STEP 3: Validate output with MonitoringAgent
            monitoring_result = self.monitoring_agent.execute(
                task={'agent_output': sentiment_result, 'action': 'validate'},
                context={
                    'user_profile': self.conversation_memory.user_profile,
                    'portfolio': self.vector_memory.get_portfolio()
                }
            )
            
            # Only generate alert if:
            # 1. SentimentAgent says should_alert = True
            # 2. MonitoringAgent validates is_valid = True
            if sentiment_result.get('should_alert') and monitoring_result.get('is_valid'):
                alert = {
                    'news_id': sentiment_result.get('news_id'),
                    'headline': sentiment_result.get('headline'),
                    'alert_message': sentiment_result.get('alert_message'),
                    'quality_score': monitoring_result.get('quality_score'),
                    'recommendation': sentiment_result.get('recommendation'),
                    'impact': sentiment_result.get('impact')
                }
                self.processed_alerts.append(alert)
        
        # STEP 4: Generate summary report
        summary = self._generate_summary(sentiment_results, planning_result)
        
        return {
            'processed_news_count': len(sentiment_results),
            'alerts_generated': self.processed_alerts,
            'quality_report': self.monitoring_agent.get_quality_report(),
            'summary': summary
        }
    
    def _find_news_by_id(self, news_stream: List[Any], news_id: str) -> Optional[Any]:
        """Tìm news item theo ID."""
        for news in news_stream:
            if getattr(news, 'news_id', None) == news_id:
                return news
        return None
    
    def _generate_summary(self, sentiment_results: List[Dict], planning_result: Dict) -> str:
        """Tạo summary report."""
        total_analyzed = len(sentiment_results)
        total_alerts = len(self.processed_alerts)
        
        summary = f"""
        === SENTIMENT ADVISOR SUMMARY ===
        
        📊 Processing Status:
        - News items processed: {total_analyzed}
        - Alerts generated: {total_alerts}
        - Processing priority: {', '.join(planning_result.get('priority_order', [])[:3])}...
        
        💡 Key Insights:
        """
        
        if self.processed_alerts:
            high_urgency = sum(1 for a in self.processed_alerts if a['recommendation'].get('urgency') == 'High')
            summary += f"\n- High urgency alerts: {high_urgency}"
            
            actions = {}
            for alert in self.processed_alerts:
                action = alert['recommendation'].get('action', 'Hold')
                actions[action] = actions.get(action, 0) + 1
            
            summary += "\n- Recommended actions: " + ", ".join([f"{k}: {v}" for k, v in actions.items()])
        
        summary += "\n\n📋 Next steps: Check alerts for detailed recommendations."
        
        return summary
    
    def get_alerts(self) -> List[Dict]:
        """Lấy danh sách alerts đã tạo."""
        return self.processed_alerts
    
    def clear_alerts(self):
        """Xóa alerts (sau khi user đã xem)."""
        self.processed_alerts = []
