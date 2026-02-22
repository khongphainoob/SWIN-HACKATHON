# 🚀 Quick Start - Chạy Streamlit App

## ✅ Bước 1: Kiểm tra môi trường

```powershell
# Test xem mọi thứ có sẵn sàng không
python test_streamlit_ready.py
```

**Output mong đợi:**
```
✅ All critical imports successful!
✅ File structure test passed!
✅ At least one API key is configured!
✅ User interface test passed!
✅ Workflow test passed!

🎉 ALL TESTS PASSED! Streamlit app should run fine.
```

---

## ✅ Bước 2: Test nhanh workflow

```powershell
# Test workflow với các profile khác nhau
python quick_test_workflow.py
```

**Output mong đợi:**
```
🧪 QUICK TEST: Simple workflow
✅ TEST PASSED!
Action: BUY
Confidence: 75%
Recommended Amount: $5,000.00

🧪 QUICK TEST: Conservative investor
✅ Logic correct: Low risk suggests ~30%

🧪 QUICK TEST: Aggressive trader  
✅ Logic correct: High risk suggests ~80%

🎉 ALL TESTS PASSED!
```

---

## ✅ Bước 3: Chạy Streamlit

### **Cách 1: Tự động (Khuyến nghị)**
```powershell
.\start_streamlit.ps1
```

Script này sẽ:
1. Chạy pre-flight tests
2. Kill streamlit cũ (nếu đang chạy)
3. Start streamlit mới
4. Mở browser tự động

### **Cách 2: Thủ công**
```powershell
streamlit run streamlit_app.py
```

---

## 🌐 Truy cập App

Mở browser và truy cập:
```
http://localhost:8501
```

---

## 📱 Sử dụng App

### **1. Thiết lập Profile (Sidebar)**

Click **"👤 User Profile"** trong sidebar:

| **Field** | **Options** | **Mô tả** |
|-----------|-------------|-----------|
| User ID | text | ID duy nhất của bạn |
| Risk Tolerance | low / medium / high | Mức chấp nhận rủi ro |
| Investment Horizon | short / medium / long | Thời gian đầu tư |
| Investment Amount | $100 - $1M | Số tiền dự định đầu tư |

**Ví dụ:**
```
User ID: investor_123
Risk: high
Horizon: long_term
Amount: $50,000
```

### **2. Phân tích Stock (Tab 1)**

1. Nhập ticker: `NVDA`
2. Click **"🚀 Analyze"**
3. Xem kết quả:
   - **Recommendation**: BUY/SELL/HOLD
   - **Confidence**: 85%
   - **Sentiment**: 0.65
   - **💰 Suggested Amount**: $40,000 (dựa trên profile)

### **3. Phân tích Portfolio (Tab 2)**

1. Nhập: `AAPL, MSFT, GOOGL, NVDA`
2. Click **"📊 Analyze Portfolio"**
3. Xem bảng kết quả (màu sắc)
4. Download CSV

---

## 🧪 Test Cases

### **Test 1: Conservative Investor**
```
Profile:
- Risk: low
- Amount: $20,000

Ticker: JPM

Expected:
- Action: BUY/HOLD
- Suggested: ~$6,000 (30%)
```

### **Test 2: Aggressive Trader**
```
Profile:
- Risk: high
- Amount: $100,000

Ticker: NVDA

Expected:
- Action: BUY (nếu sentiment positive)
- Suggested: ~$80,000 (80%)
```

### **Test 3: Risk thay đổi**
```
1. Set Risk = low, Amount = $10,000
2. Analyze AAPL → Suggested = ~$3,000

3. Change Risk = high
4. Analyze AAPL → Suggested = ~$8,000
```

---

## 🐛 Troubleshooting

### **Lỗi: Port 8501 already in use**
```powershell
# Cách 1: Kill process
Get-Process -Name streamlit | Stop-Process -Force

# Cách 2: Dùng port khác
streamlit run streamlit_app.py --server.port 8502
```

### **Lỗi: Module not found**
```powershell
pip install -r requirements.txt
```

### **Lỗi: API key not found**
```powershell
# Thêm vào .env
echo OPENAI_API_KEY=sk-your-key > .env
```

### **Lỗi: FinBERT download chậm**
- Lần đầu cần tải model (1-2GB)
- Cần internet
- Lần sau sẽ nhanh (dùng cache)

---

## 📊 Feature Checklist

- [x] User profile (risk, horizon, amount)
- [x] Single stock analysis
- [x] Portfolio analysis
- [x] Suggested investment amount
- [x] RAG sentiment analysis
- [x] FinBERT integration
- [x] News fetching
- [x] Database portfolio
- [x] Admin interface

---

## 📞 Hỗ trợ

| **Tài liệu** | **Link** |
|-------------|----------|
| Streamlit Guide | [RUN_STREAMLIT_GUIDE.md](RUN_STREAMLIT_GUIDE.md) |
| Workflow Guide | [orchestrators/WORKFLOW_USAGE_GUIDE.md](orchestrators/WORKFLOW_USAGE_GUIDE.md) |
| Demo Scripts | [orchestrators/demo_workflow.py](orchestrators/demo_workflow.py) |

---

## ⚡ TL;DR

```powershell
# One-liner quick start
python test_streamlit_ready.py && streamlit run streamlit_app.py
```

**Hoặc:**

```powershell
.\start_streamlit.ps1
```

🎉 Done! App sẽ mở tại http://localhost:8501
