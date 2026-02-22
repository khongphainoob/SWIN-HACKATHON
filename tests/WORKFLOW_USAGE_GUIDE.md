# 📘 LangGraph Workflow Usage Guide

## 🚀 Cách chạy file

### 1. Cài đặt dependencies
```powershell
pip install langgraph langchain-core transformers torch yfinance
```

### 2. Chạy trực tiếp
```powershell
# Từ thư mục gốc
cd "d:\AI Agentic Project\SWIN"
python orchestrators/langgraph_workflow.py
```

### 3. Import và sử dụng
```python
from orchestrators.langgraph_workflow import run_workflow

# Cách 1: Basic query
result = run_workflow("What's the outlook for NVDA stock?")

# Cách 2: Full context với user profile
result = run_workflow(
    query="Should I buy AAPL?",
    user_id="user_123",
    risk_tolerance="high",           # low/medium/high
    investment_horizon="long_term",  # short_term/medium_term/long_term
    investment_amount=50000.0,
    portfolio={
        "MSFT": {"shares": 100, "avg_price": 300.0},
        "GOOGL": {"shares": 50, "avg_price": 120.0}
    },
    user_preferences={
        "preferred_sectors": ["technology", "healthcare"],
        "avoid_sectors": ["tobacco", "gambling"]
    }
)
```

---

## 📊 Input Fields (WorkflowState)

### **Bắt buộc:**
- `user_query` (str): Câu hỏi của người dùng

### **User Context (Tùy chọn):**
- `user_id` (str): ID người dùng (default: "anonymous")
- `risk_tolerance` (str): Mức chấp nhận rủi ro
  - `"low"`: Ít rủi ro, tập trung vào bảo toàn vốn
  - `"medium"`: Cân bằng giữa rủi ro và lợi nhuận
  - `"high"`: Chấp nhận rủi ro cao để tăng lợi nhuận
- `investment_horizon` (str): Thời gian đầu tư
  - `"short_term"`: < 1 năm
  - `"medium_term"`: 1-5 năm
  - `"long_term"`: > 5 năm
- `investment_amount` (float): Số tiền dự định đầu tư (USD)
- `portfolio` (dict): Danh mục hiện tại
  ```python
  {
      "TICKER": {
          "shares": 100,
          "avg_price": 150.0,
          "purchase_date": "2024-01-01"
      }
  }
  ```
- `user_preferences` (dict): Tùy chọn cá nhân
  ```python
  {
      "preferred_sectors": ["technology", "healthcare"],
      "avoid_sectors": ["tobacco", "weapons"],
      "esg_priority": True,
      "dividend_preference": "growth"
  }
  ```

---

## 📤 Output Structure

### **Recommendation Object:**
```python
{
    "ticker": "NVDA",
    "action": "BUY",              # BUY / SELL / HOLD
    "urgency": "High",            # Low / Medium / High
    "confidence": 0.85,           # 0.0 - 1.0
    "recommended_amount": 40000.0,
    
    "user_context": {
        "user_id": "user_123",
        "risk_tolerance": "high",
        "investment_horizon": "long_term",
        "portfolio_holdings": 2
    },
    
    "analysis": {
        "sentiment": {
            "score": 0.65,
            "label": "positive"
        },
        "forecast": {
            "trend": "BULLISH",
            "target_price": 575.0,
            "confidence": 0.85
        },
        "alerts_count": 0,
        "current_price": 550.0
    },
    
    "reasoning": [
        "Sentiment analysis: positive (0.65)",
        "ML forecast: BULLISH with 85% confidence",
        "Risk alerts: 0 detected",
        "User risk tolerance: high",
        "Investment horizon: long_term"
    ],
    
    "human_review": {
        "required": False,
        "approved": True,
        "comments": "Auto-approved"
    }
}
```

---

## 🎯 Ví dụ sử dụng

### Ví dụ 1: Conservative Investor
```python
result = run_workflow(
    query="Analyze JPM stock",
    user_id="conservative_001",
    risk_tolerance="low",
    investment_horizon="long_term",
    investment_amount=20000.0,
    portfolio={"BND": {"shares": 500, "avg_price": 80.0}},
    user_preferences={"preferred_sectors": ["financial", "utilities"]}
)
```

### Ví dụ 2: Aggressive Tech Investor
```python
result = run_workflow(
    query="Should I buy more NVDA?",
    user_id="tech_bull_99",
    risk_tolerance="high",
    investment_horizon="short_term",
    investment_amount=100000.0,
    portfolio={
        "NVDA": {"shares": 200, "avg_price": 450.0},
        "AMD": {"shares": 300, "avg_price": 120.0}
    },
    user_preferences={
        "preferred_sectors": ["technology", "AI"],
        "growth_focus": True
    }
)
```

### Ví dụ 3: Balanced Portfolio
```python
result = run_workflow(
    query="Diversify with AAPL?",
    user_id="balanced_investor",
    risk_tolerance="medium",
    investment_horizon="medium_term",
    investment_amount=30000.0,
    portfolio={
        "VTI": {"shares": 100, "avg_price": 220.0},
        "AGG": {"shares": 150, "avg_price": 105.0}
    },
    user_preferences={
        "diversification_priority": True,
        "dividend_preference": "balanced"
    }
)
```

---

## 🔍 Workflow Steps

1. **PlanningAgent**: Lập kế hoạch & ưu tiên
2. **InputAgent**: Trích xuất ticker từ query
3. **NewsFetchAgent**: Thu thập tin tức
4. **SentimentAnalyzerAgent**: Phân tích sentiment (RAG + FinBERT)
5. **MarketDataAgent** hoặc **RiskAlertAgent**: Dữ liệu thị trường hoặc cảnh báo
6. **MLForecastAgent**: Dự báo xu hướng
7. **LLMReasoningAgent**: Tổng hợp & quyết định review
8. **HumanReviewNode** (nếu cần): Xác nhận người
9. **RecommendationAgent**: Khuyến nghị cuối cùng

---

## 🎨 Tùy chỉnh

### Thay đổi risk tolerance logic:
Edit `RecommendationAgent.run()` trong [langgraph_workflow.py](langgraph_workflow.py)

### Thêm field mới:
1. Cập nhật `WorkflowState` (TypedDict)
2. Cập nhật `create_initial_state()`
3. Sử dụng field trong các agent nodes

---

## 🐛 Troubleshooting

### Lỗi: `transformers` not found
```powershell
pip install transformers torch
```

### Lỗi: `langgraph` not found
```powershell
pip install langgraph langchain-core
```

### Lỗi: `yfinance` not found
```powershell
pip install yfinance
```

### FinBERT chậm lần đầu
- Model tải từ Hugging Face, cần internet
- Lần sau sẽ dùng cache
