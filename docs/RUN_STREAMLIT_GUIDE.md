# 🚀 Hướng dẫn chạy Streamlit App

## 📋 Yêu cầu cài đặt

### 1. Cài đặt dependencies
```powershell
pip install streamlit pandas plotly langgraph langchain-core transformers torch yfinance
```

### 2. Cài đặt môi trường (nếu chưa có)
```powershell
# Tạo .env file
echo OPENAI_API_KEY=your_openai_key > .env
echo GEMINI_API_KEY=your_gemini_key >> .env
```

---

## 🎯 Cách chạy Streamlit App

### Phương pháp 1: Chạy từ terminal
```powershell
# Di chuyển vào thư mục project
cd "d:\AI Agentic Project\SWIN"

# Chạy streamlit
streamlit run streamlit_app.py
```

### Phương pháp 2: Chạy với port cụ thể
```powershell
streamlit run streamlit_app.py --server.port 8501
```

### Phương pháp 3: Chạy với cấu hình
```powershell
streamlit run streamlit_app.py --server.headless true --server.port 8501
```

---

## 🌐 Truy cập ứng dụng

Sau khi chạy, mở trình duyệt và truy cập:
```
http://localhost:8501
```

---

## 📱 Giao diện User

### **Bước 1: Thiết lập User Profile (Sidebar)**

Click vào **"👤 User Profile"** trong sidebar để mở cấu hình:

1. **User ID**: ID duy nhất của bạn (vd: "user_001")
2. **Risk Tolerance**: 
   - 🟢 **Low**: Ít rủi ro, bảo toàn vốn
   - 🟡 **Medium**: Cân bằng rủi ro/lợi nhuận
   - 🔴 **High**: Chấp nhận rủi ro cao
3. **Investment Horizon**:
   - **Short Term**: < 1 năm
   - **Medium Term**: 1-5 năm
   - **Long Term**: > 5 năm
4. **Investment Amount**: Số tiền dự định đầu tư ($)

### **Bước 2: Sử dụng các Tab**

#### **Tab 1: 🔍 Single Stock Analysis**
1. Nhập ticker (vd: AAPL, MSFT, NVDA)
2. Click **"🚀 Analyze"**
3. Xem kết quả:
   - **Recommendation**: BUY/SELL/HOLD
   - **Confidence**: Độ tin cậy
   - **Sentiment**: Điểm cảm xúc
   - **💰 Suggested Amount**: Số tiền nên đầu tư (dựa trên profile)

#### **Tab 2: 📈 Portfolio Analysis**
1. Nhập nhiều ticker phân cách bằng dấu phẩy
   - Vd: `AAPL, MSFT, GOOGL, NVDA, TSLA`
2. Click **"📊 Analyze Portfolio"**
3. Xem bảng kết quả với màu sắc:
   - 🟢 **Green**: BUY
   - 🔴 **Red**: SELL
   - 🟡 **Yellow**: HOLD
4. Download kết quả CSV

#### **Tab 3: 📰 News & Sentiment**
1. Nhập ticker
2. Chọn số lượng bài viết
3. Click **"📰 Fetch News"**
4. Đọc tin tức và tóm tắt

#### **Tab 4: 💼 My Portfolio**
1. Nhập User ID
2. Add holdings (Ticker, Shares, Avg Cost)
3. View portfolio
4. Analyze all holdings

---

## ⚙️ Admin Interface

### Truy cập Admin:
1. Click **"⚙️ Admin Interface"** trong sidebar
2. Nhập password (default: `admin123`)
3. Quản lý:
   - System config
   - API keys
   - Database
   - Logs

---

## 🧪 Test nhanh

### Test 1: Phân tích đơn giản
```
1. Mở app: http://localhost:8501
2. Sidebar → User Profile:
   - User ID: test_user
   - Risk: medium
   - Horizon: medium_term
   - Amount: $10,000
3. Tab 1 → Nhập: NVDA
4. Click "Analyze"
5. Kiểm tra: Action, Confidence, Suggested Amount
```

### Test 2: Portfolio
```
1. Tab 2 → Nhập: AAPL, MSFT, GOOGL
2. Click "Analyze Portfolio"
3. Kiểm tra bảng kết quả
4. Download CSV
```

### Test 3: User Profile thay đổi
```
1. Sidebar → Đổi Risk = high
2. Sidebar → Đổi Amount = $50,000
3. Tab 1 → Analyze lại NVDA
4. So sánh Suggested Amount (phải tăng)
```

---

## 🐛 Khắc phục lỗi

### Lỗi: Port already in use
```powershell
# Đổi port
streamlit run streamlit_app.py --server.port 8502
```

### Lỗi: Module not found
```powershell
# Cài lại dependencies
pip install -r requirements.txt
```

### Lỗi: API Key not found
```powershell
# Thêm API key vào .env
echo OPENAI_API_KEY=sk-xxx > .env
```

### Lỗi: FinBERT chậm lần đầu
- Model tải từ Hugging Face, cần internet
- Lần sau sẽ nhanh hơn (dùng cache)

### Lỗi: Database not found
```powershell
# Tự động tạo khi add holding đầu tiên
# Hoặc tạo thủ công:
mkdir data
```

---

## 📊 Ví dụ đầy đủ

### Ví dụ 1: Conservative Investor
```
Profile:
- User ID: conservative_001
- Risk: low
- Horizon: long_term
- Amount: $20,000

Query: "Should I invest in JPM?"

Expected Output:
- Action: BUY/HOLD (tùy sentiment)
- Suggested Amount: ~$6,000 (30% of $20,000 for low risk)
```

### Ví dụ 2: Aggressive Trader
```
Profile:
- User ID: trader_999
- Risk: high
- Horizon: short_term
- Amount: $100,000

Query: "NVDA looks promising?"

Expected Output:
- Action: BUY (nếu sentiment positive)
- Suggested Amount: ~$80,000 (80% of $100,000 for high risk)
```

### Ví dụ 3: Balanced Investor
```
Profile:
- User ID: balanced_user
- Risk: medium
- Horizon: medium_term
- Amount: $50,000

Query: "Diversify with AAPL?"

Expected Output:
- Action: BUY/HOLD
- Suggested Amount: ~$25,000 (50% of $50,000 for medium risk)
```

---

## 🎨 Tùy chỉnh

### Thay đổi theme
Tạo file `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

### Thay đổi admin password
Edit `streamlit_app.py`:
```python
admin_password = "your_secure_password"
```

---

## 📞 Hỗ trợ

- **Docs**: [WORKFLOW_USAGE_GUIDE.md](orchestrators/WORKFLOW_USAGE_GUIDE.md)
- **Demo**: [demo_workflow.py](orchestrators/demo_workflow.py)
- **Issues**: Check logs trong terminal

---

## ✅ Checklist trước khi chạy

- [ ] Đã cài đặt Python 3.8+
- [ ] Đã cài đặt tất cả dependencies
- [ ] Đã có API keys (OPENAI hoặc GEMINI)
- [ ] Đã ở đúng thư mục project
- [ ] Port 8501 không bị chiếm
- [ ] Internet kết nối (cho FinBERT lần đầu)

---

## 🚀 Quick Start Command

```powershell
cd "d:\AI Agentic Project\SWIN" && streamlit run streamlit_app.py
```

Enjoy! 🎉
