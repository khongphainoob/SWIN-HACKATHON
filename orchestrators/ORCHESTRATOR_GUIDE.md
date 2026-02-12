# Sentiment Advisor Orchestrator - Complete Guide

## 📋 Tổng Quan (Overview)

`SentimentAdvisorOrchestrator` là thành phần chính điều phối toàn bộ quy trình xử lý tin tức (news stream) từ input đến output alerts cho user.

### Nhiệm vụ chính:
1. **Nhận & Sắp xếp ưu tiên tin tức** - Planning Agent prioritize tin
2. **Phân tích cảm xúc thị trường** - Sentiment Agent analyze sentiment & impact  
3. **Xác minh chất lượng** - Monitoring Agent validate recommendations
4. **Tạo alerts thông minh** - Gửi notifications đến user

---

## 🔄 Workflow (Quy Trình Hoạt Động)

```
┌─────────────────────────────────────────────────────────────────┐
│                      NEWS STREAM INPUT                          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 1: PLANNING AGENT                                          │
│ - Ưu tiên hóa tin tức (prioritize)                             │
│ - Tạo execution plan theo portfolio user                        │
│ - Lên lịch tasks xử lý (schedule tasks)                        │
│ Output: scheduled_tasks, priority_order                         │
└──────────────────────────┬──────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    ┌─────────────────────────────────────────────┐
    │ STEP 2: SENTIMENT AGENT (per each task)    │
    │ - Đọc news item                            │
    │ - Phân tích sentiment (pos/neg/neutral)    │
    │ - Tính impact score trên portfolio         │
    │ - Tạo recommendation (Buy/Sell/Hold)       │
    │ Output: sentiment_result                    │
    └──────────────┬──────────────────────────────┘
                   │
                   ▼
    ┌──────────────────────────────────────────────┐
    │ STEP 3: MONITORING AGENT                     │
    │ - Validate chất lượng output từ SentimentAgent│
    │ - Check quality_score                        │
    │ - Đảm bảo recommendation hợp lý             │
    │ Output: is_valid, quality_score              │
    └──────────────┬──────────────────────────────┘
                   │
            ┌──────▼──────┐
            │ Valid?      │
            └──────┬──────┘
                   │
        ┌──────────┴──────────┐
        │                     │
       YES                    NO
        │                     │
        ▼                     ▼
    CREATE ALERT         DROP
    to alerts list
    
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: SUMMARY & REPORT                                        │
│ - Tính toán thống kê (processed count, alerts generated)       │
│ - Tạo quality_report từ MonitoringAgent                        │
│ - Generate summary insights                                    │
│ Output: result dict với tất cả kết quả                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Architecture & Components

### 1. **SentimentAdvisorOrchestrator Class**
Main orchestrator class điều phối tất cả agents và memory.

#### Attributes:
```python
# Agents
self.planning_agent          # Sắp xếp ưu tiên tin
self.sentiment_agent         # Phân tích sentiment
self.monitoring_agent        # Validate output

# Shared Memory
self.vector_memory           # Lưu portfolio, embeddings
self.conversation_memory     # Lưu user profile, context

# Results
self.processed_alerts        # Danh sách alerts tạo được
```

#### Key Methods:

##### `__init__(config_path: str = None)`
Khởi tạo orchestrator với tất cả agents và memory.

**Những gì xảy ra:**
- Tạo 3 agents (Planning, Sentiment, Monitoring)
- Tạo Vector Memory và Conversation Memory
- Chia sẻ memory cho các agents
- Register agents vào planning agent
- Khởi tạo processed_alerts = []

**Example:**
```python
orchestrator = SentimentAdvisorOrchestrator(config_path="configs/model_config.yaml")
```

---

##### `set_user_portfolio(portfolio_items: List[Any])`
Thiết lập danh sách stock/crypto của user để phân tích impact.

**Parameters:**
- `portfolio_items`: List of `PortfolioItem` objects
  - ticker (str): Mã cổ phiếu (AAPL, MSFT, BTC, etc.)
  - quantity (int): Số lượng sở hữu
  - avg_cost (float): Giá bình quân (cost basis)
  - current_price (float): Giá hiện tại
  - allocation_pct (float): % của tổng portfolio
  - sector (str): Ngành (Technology, Finance, etc.)
  - country (str): Quốc gia (USA, Asia, etc.)

**Example:**
```python
portfolio = [
    PortfolioItem(
        ticker="AAPL",
        quantity=100,
        avg_cost=150.0,
        current_price=180.0,
        allocation_pct=30.0,
        sector="Technology",
        country="USA"
    ),
    PortfolioItem(
        ticker="BTC",
        quantity=0.5,
        avg_cost=45000.0,
        current_price=50000.0,
        allocation_pct=15.0,
        sector="Crypto",
        country="Global"
    )
]
orchestrator.set_user_portfolio(portfolio)
```

---

##### `set_user_profile(user_profile: Any)`
Thiết lập điểm tùy chọn của user.

**UserProfile attributes:**
- `user_id` (str): Định danh user
- `risk_tolerance` (str): Mức độ chấp nhận rủi ro (Low/Moderate/High)
- `notification_threshold` (float): Ngưỡng alert (-1.0 to 1.0)
- `preferred_actions` (List[str]): Hành động ưa thích ([...Buy, Hold, Sell...])

**Example:**
```python
user_profile = UserProfile(
    user_id="user_123",
    risk_tolerance="Moderate",
    notification_threshold=-0.5,  # Alert nếu sentiment < -0.5
    preferred_actions=["Hold", "Sell", "BuyMore"]
)
orchestrator.set_user_profile(user_profile)
```

---

##### `process_news_stream(news_stream: List[Any]) -> Dict[str, Any]`
**Main method** - Xử lý danh sách tin tức theo workflow.

**Parameters:**
- `news_stream`: List of `NewsItem` objects chứa:
  - `news_id` (str): ID tin duy nhất
  - `headline` (str): Tiêu đề tin
  - `content` (str): Nội dung tin
  - `ticker` (str): Mã cổ phiếu liên quan
  - `source` (str): Nguồn tin (Reuters, Bloomberg, etc.)
  - `timestamp` (datetime): Thời gian tin

**Returns:**
```python
{
    'processed_news_count': int,              # Số tin đã xử lý
    'alerts_generated': List[Dict],           # Danh sách alerts
    'quality_report': str,                    # Report từ Monitoring Agent
    'summary': str                            # Summary insights
}
```

**Response structure của mỗi alert:**
```python
{
    'news_id': str,                    # ID của tin
    'headline': str,                   # Tiêu đề tin
    'alert_message': str,              # Pesan alert
    'quality_score': float,            # Điểm chất lượng (0-1)
    'recommendation': {                # Khuyến nghị từ SentimentAgent
        'action': str,                 # Buy/Sell/Hold
        'urgency': str,                # Low/Medium/High
        'reason': str                  # Lý do khuyến nghị
    },
    'impact': {                        # Tác động trên portfolio
        'ticker': str,
        'impact_score': float,         # -1 (very negative) to 1 (very positive)
        'affected_allocation': float   # % portfolio bị ảnh hưởng
    }
}
```

**Usage Example:**
```python
news_items = [
    NewsItem(
        news_id="news_001",
        headline="Apple launches new AI features",
        content="Apple announced...",
        ticker="AAPL",
        source="TechCrunch",
        timestamp=datetime.now()
    ),
    NewsItem(
        news_id="news_002",
        headline="Fed raises interest rates",
        content="Federal Reserve...",
        ticker="MSFT",
        source="Reuters",
        timestamp=datetime.now()
    )
]

result = orchestrator.process_news_stream(news_items)

print(f"Processed: {result['processed_news_count']} news")
print(f"Generated: {len(result['alerts_generated'])} alerts")
print(result['summary'])

for alert in result['alerts_generated']:
    print(f"Alert: {alert['headline']}")
    print(f"Recommendation: {alert['recommendation']['action']}")
    print(f"Quality Score: {alert['quality_score']}")
```

---

##### `get_alerts() -> List[Dict]`
Lấy danh sách tất cả alerts đã tạo.

```python
alerts = orchestrator.get_alerts()
for alert in alerts:
    print(alert['alert_message'])
```

---

##### `clear_alerts()`
Xóa danh sách alerts (sau khi user đã xem/xử lý).

```python
orchestrator.clear_alerts()
```

---

## 🔗 Integration Points

### 1. **Planning Agent Input**
Orchestrator gửi message cho Planning Agent:
```python
planning_result = self.planning_agent.execute(
    task={
        'news_stream': news_stream,
        'action': 'plan_and_orchestrate'
    },
    context={
        'user_profile': self.conversation_memory.user_profile,
        'portfolio': self.vector_memory.get_portfolio()
    }
)
```

**Expected Output từ Planning Agent:**
```python
{
    'scheduled_tasks': [
        {'news_id': 'news_001', 'priority': 1, 'status': 'scheduled'},
        {'news_id': 'news_002', 'priority': 2, 'status': 'scheduled'},
        ...
    ],
    'priority_order': ['AAPL', 'MSFT', 'JPM', ...],
    'reasoning': 'Tin về AAPL quan trọng nhất vì...'
}
```

### 2. **Sentiment Agent Input**
Orchestrator gửi từng news item cho Sentiment Agent:
```python
sentiment_result = self.sentiment_agent.execute(
    task={
        'news': news_item,
        'action': 'analyze'
    },
    context={
        'user_profile': self.conversation_memory.user_profile,
        'portfolio': self.vector_memory.get_portfolio()
    }
)
```

**Expected Output từ Sentiment Agent:**
```python
{
    'news_id': str,
    'headline': str,
    'sentiment': float,           # -1 to 1
    'sentiment_label': str,       # 'Positive', 'Negative', 'Neutral'
    'impact': {
        'ticker': str,
        'impact_score': float,
        'affected_allocation': float
    },
    'recommendation': {
        'action': str,            # Buy/Sell/Hold
        'urgency': str,           # Low/Medium/High
        'reason': str
    },
    'should_alert': bool,         # Có nên tạo alert?
    'alert_message': str,
    'confidence': float           # 0-1
}
```

### 3. **Monitoring Agent Input**
Orchestrator gửi Sentiment output cho Monitoring Agent để validate:
```python
monitoring_result = self.monitoring_agent.execute(
    task={
        'agent_output': sentiment_result,
        'action': 'validate'
    },
    context={
        'user_profile': self.conversation_memory.user_profile,
        'portfolio': self.vector_memory.get_portfolio()
    }
)
```

**Expected Output từ Monitoring Agent:**
```python
{
    'is_valid': bool,
    'quality_score': float,       # 0-1
    'issues': [],                 # Danh sách vấn đề (nếu có)
    'suggestions': str            # Gợi ý cải thiện
}
```

---

## 📊 Alert Generation Rules

Alert chỉ được tạo khi **CẢ HAI điều kiện sau** được thỏa mãn:

1. **SentimentAgent says `should_alert = True`**
   - Sentiment score > 0.6 (Positive Signal)
   - Hoặc Sentiment score < -0.6 (Negative Signal)
   - Hoặc Impact Score > user's notification_threshold

2. **MonitoringAgent says `is_valid = True`**
   - Quality Score > threshold (thường 0.5)
   - Không có issues nghiêm trọng
   - Recommendation hợp lý

**Code:**
```python
if sentiment_result.get('should_alert') and monitoring_result.get('is_valid'):
    # Create alert
    alert = {
        'news_id': sentiment_result.get('news_id'),
        'headline': sentiment_result.get('headline'),
        'alert_message': sentiment_result.get('alert_message'),
        'quality_score': monitoring_result.get('quality_score'),
        'recommendation': sentiment_result.get('recommendation'),
        'impact': sentiment_result.get('impact')
    }
    self.processed_alerts.append(alert)
```

---

## 🛠️ Extending the Orchestrator

### Scenario 1: Thêm Agent Mới

```python
from agents.custom.my_agent import MyCustomAgent

class ExtendedOrchestrator(SentimentAdvisorOrchestrator):
    def __init__(self, config_path=None):
        super().__init__(config_path)
        
        # Thêm agent mới
        self.my_agent = MyCustomAgent(config_path)
        self.my_agent.set_vector_memory(self.vector_memory)
        self.my_agent.set_conversation_memory(self.conversation_memory)
        
        # Register vào planning agent
        self.planning_agent.register_agent('MyAgent', self.my_agent)
    
    def process_news_stream(self, news_stream):
        # Gọi parent method
        result = super().process_news_stream(news_stream)
        
        # Thêm logic mới
        # result['my_agent_output'] = ...
        
        return result
```

### Scenario 2: Thay đổi Alert Logic

```python
class FilteredOrchestrator(SentimentAdvisorOrchestrator):
    def process_news_stream(self, news_stream):
        # Gọi parent method
        result = super().process_news_stream(news_stream)
        
        # Filter alerts với threshold cao hơn
        filtered_alerts = [
            alert for alert in result['alerts_generated']
            if alert['quality_score'] > 0.8 and alert['recommendation']['urgency'] == 'High'
        ]
        
        result['alerts_generated'] = filtered_alerts
        return result
```

### Scenario 3: Thêm Processing Step

```python
class AsyncOrchestrator(SentimentAdvisorOrchestrator):
    async def process_news_stream_async(self, news_stream):
        # Parallel processing
        tasks = [
            self.sentiment_agent.execute(...)
            for task in scheduling_result['scheduled_tasks']
        ]
        
        sentiment_results = await asyncio.gather(*tasks)
        # ... rest of logic
```

---

## 📝 Memory Sharing

Orchestrator chia sẻ memory giữa các agents:

### VectorMemory
- **Lưu trữ:** Portfolio, Embeddings, Vector Store
- **Sử dụng bởi:** SentimentAgent, MonitoringAgent
- **Methods:**
  - `set_portfolio(items)` - Set user portfolio
  - `get_portfolio()` - Lấy portfolio
  - `add_news_to_store(news_item)` - Lưu embedding

```python
self.vector_memory.set_portfolio(portfolio_items)
portfolio = self.vector_memory.get_portfolio()
```

### ConversationMemory
- **Lưu trữ:** User Profile, Conversation History
- **Sử dụng bởi:** Tất cả agents
- **Attributes:**
  - `user_profile` - UserProfile object

```python
self.conversation_memory.user_profile = user_profile
```

---

## 🔍 Data Flow Diagram

```
┌────────────────┐
│  News Stream   │
└───────┬────────┘
        │
        ▼
┌───────────────────────────────────────────┐
│  SentimentAdvisorOrchestrator              │
│  ┌─────────────────────────────────────┐  │
│  │ 1. Call PlanningAgent.execute()     │  │
│  │    └─> scheduled_tasks,             │  │
│  │        priority_order               │  │
│  └─────────────────────────────────────┘  │
│           │                                 │
│           ▼                                 │
│  ┌─────────────────────────────────────┐  │
│  │ 2. For each task:                   │  │
│  │    a) Call SentimentAgent.execute() │  │
│  │       └─> sentiment_result          │  │
│  │    b) Call MonitoringAgent.execute()│  │
│  │       └─> monitoring_result         │  │
│  │    c) If both valid => add to       │  │
│  │       processed_alerts              │  │
│  └─────────────────────────────────────┘  │
│           │                                 │
│           ▼                                 │
│  ┌─────────────────────────────────────┐  │
│  │ 3. Generate Summary & Report        │  │
│  │    └─> Return result dict           │  │
│  └─────────────────────────────────────┘  │
│                                            │
│  Shared Memory (across agents):            │
│  ┌─────────────────────────────────────┐  │
│  │ VectorMemory: portfolio, embeddings │  │
│  │ ConversationMemory: user_profile    │  │
│  └─────────────────────────────────────┘  │
└───────────────────────────────────────────┘
        │
        ▼
┌────────────────────┐
│  Result Dict:      │
│  - alerts          │
│  - summary         │
│  - quality_report  │
└────────────────────┘
```

---

## 🧪 Complete Usage Example

```python
from datetime import datetime
from memory.vector_memory import PortfolioItem, NewsItem
from memory.conversation_memory import UserProfile
from orchestrators.base_orchestrator import SentimentAdvisorOrchestrator

# 1. Initialize Orchestrator
orchestrator = SentimentAdvisorOrchestrator()

# 2. Set User Profile
user_profile = UserProfile(
    user_id="investor_001",
    risk_tolerance="Moderate",
    notification_threshold=-0.4,
    preferred_actions=["Buy", "Hold", "Sell"]
)
orchestrator.set_user_profile(user_profile)

# 3. Set Portfolio
portfolio = [
    PortfolioItem(
        ticker="AAPL",
        quantity=100,
        avg_cost=150.0,
        current_price=180.0,
        allocation_pct=35.0,
        sector="Technology",
        country="USA"
    ),
    PortfolioItem(
        ticker="MSFT",
        quantity=50,
        avg_cost=300.0,
        current_price=350.0,
        allocation_pct=25.0,
        sector="Technology",
        country="USA"
    ),
    PortfolioItem(
        ticker="JPM",
        quantity=30,
        avg_cost=140.0,
        current_price=160.0,
        allocation_pct=20.0,
        sector="Finance",
        country="USA"
    ),
    PortfolioItem(
        ticker="TSLA",
        quantity=20,
        avg_cost=200.0,
        current_price=250.0,
        allocation_pct=20.0,
        sector="Automotive",
        country="USA"
    )
]
orchestrator.set_user_portfolio(portfolio)

# 4. Create News Stream
news_stream = [
    NewsItem(
        news_id="news_20260210_001",
        headline="Apple Reports Record Q1 Earnings, Beats Expectations",
        content="Apple announced quarterly earnings today, exceeding analyst expectations...",
        ticker="AAPL",
        source="Reuters",
        timestamp=datetime.now()
    ),
    NewsItem(
        news_id="news_20260210_002",
        headline="Microsoft Azure Expands to New Regions",
        content="Microsoft announced expansion of Azure cloud services...",
        ticker="MSFT",
        source="TechCrunch",
        timestamp=datetime.now()
    ),
    NewsItem(
        news_id="news_20260210_003",
        headline="JPMorgan Faces Regulatory Scrutiny",
        content="JPMorgan Chase is under investigation for compliance issues...",
        ticker="JPM",
        source="Bloomberg",
        timestamp=datetime.now()
    ),
    NewsItem(
        news_id="news_20260210_004",
        headline="Tesla Announces New Gigafactory in Mexico",
        content="Tesla confirmed plans to build new manufacturing facility...",
        ticker="TSLA",
        source="CNBC",
        timestamp=datetime.now()
    )
]

# 5. Process News Stream
print("Starting sentiment advisor processing...\n")
result = orchestrator.process_news_stream(news_stream)

# 6. Display Results
print(f"✅ Processed {result['processed_news_count']} news items")
print(f"🚨 Generated {len(result['alerts_generated'])} alerts\n")

print("=" * 70)
print("ALERTS GENERATED:")
print("=" * 70)

for i, alert in enumerate(result['alerts_generated'], 1):
    print(f"\n{i}. {alert['headline']}")
    print(f"   Quality Score: {alert['quality_score']:.2f}")
    print(f"   Action: {alert['recommendation']['action']} "
          f"(Urgency: {alert['recommendation']['urgency']})")
    print(f"   Message: {alert['alert_message']}")
    print(f"   Impact: {alert['impact']}")

print("\n" + "=" * 70)
print("SUMMARY:")
print("=" * 70)
print(result['summary'])

print("\n" + "=" * 70)
print("QUALITY REPORT:")
print("=" * 70)
print(result['quality_report'])

# 7. Get All Alerts (stored in orchestrator)
all_alerts = orchestrator.get_alerts()
print(f"\nTotal alerts in orchestrator memory: {len(all_alerts)}")

# 8. Clear alerts after processing
orchestrator.clear_alerts()
print("Alerts cleared.")
```

---

## ❓ Troubleshooting

### Issue: Alerts not being generated
- **Cause:** SentimentAgent returns `should_alert=False` hoặc MonitoringAgent returns `is_valid=False`
- **Solution:** Check sentiment scores và quality scores; adjust thresholds

### Issue: Memory not shared between agents
- **Cause:** `_share_memory_across_agents()` không được gọi
- **Solution:** Ensure orchestrator __init__ gọi method này

### Issue: Performance slow with large news streams
- **Cause:** Sequential processing của từng news item
- **Solution:** Implement async/parallel processing (extend orchestrator class)

### Issue: News items not found
- **Cause:** `news_id` không match hoặc News không có `news_id` attribute
- **Solution:** Validate NewsItem structure; check ID format

---

## 📚 Related Files

- **[agents/base_agent.py](../agents/base_agent.py)** - Base Agent class
- **[agents/planning_agent.py](../agents/planning_agent.py)** - Planning Agent implementation
- **[agents/custom/sentiment_agent.py](../agents/custom/sentiment_agent.py)** - Sentiment Agent implementation
- **[agents/monitoring_agent.py](../agents/monitoring_agent.py)** - Monitoring Agent implementation
- **[memory/vector_memory.py](../memory/vector_memory.py)** - Vector Memory & PortfolioItem, NewsItem definitions
- **[memory/conversation_memory.py](../memory/conversation_memory.py)** - Conversation Memory & UserProfile definitions
- **[demo_sentiment_advisor.py](../demo_sentiment_advisor.py)** - Complete demo script

---

## 🎯 Next Steps for Developers

1. **Implement Agent Methods** - Complete the `execute()` method in each agent
2. **Add Config Loading** - Load model configs from `configs/model_config.yaml`
3. **Implement Memory Persistence** - Save/load alerts và portfolio from database
4. **Add Async Support** - Implement async versions for parallel processing
5. **Add Error Handling** - Robust error handling & fallback mechanisms
6. **Add Logging** - Comprehensive logging for debugging
7. **Add Tests** - Unit tests cho orchestrator và agents

---

## 📞 Contact & Support

Nếu có câu hỏi hoặc muốn extend orchestrator, vui lòng:
1. Kiểm tra file này trước
2. Xem source code trong `base_orchestrator.py`
3. Tham khảo agent implementations
4. Tạo issue hoặc contact team
