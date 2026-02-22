# Multi-Asset Support Guide

## 🎯 Tổng quan

Hệ thống đã được nâng cấp từ chỉ phân tích **cổ phiếu (stocks)** sang hỗ trợ **đa loại tài sản**:

- 📈 **Stocks** (Cổ phiếu): AAPL, MSFT, GOOGL...
- ₿ **Crypto** (Tiền ảo): BTC-USD, ETH-USD, SOL-USD...
- 🥇 **Commodities** (Hàng hóa): GC=F (vàng), CL=F (dầu)...
- 💱 **Forex** (Ngoại hối): EURUSD=X, GBPUSD=X...

---

## 🆕 Tính năng mới

### 1. Asset Type Selector (Chọn loại tài sản)
Thay vì chỉ nhập ticker, bây giờ bạn chọn loại tài sản trước:

```
Asset Type: [📈 Stock | ₿ Crypto | 🥇 Commodity | 💱 Forex]
```

### 2. Company Name Search (Tìm theo tên công ty)
Không cần nhớ ticker nữa! Chỉ cần gõ tên công ty:

**Hỗ trợ 70+ công ty:**
- **Tech Giants**: Apple, Microsoft, Google, NVIDIA, Tesla, Meta, Amazon...
- **Finance**: JP Morgan, Bank of America, Goldman Sachs, Wells Fargo...
- **Healthcare**: Pfizer, Johnson & Johnson, Moderna...
- **Consumer**: Nike, Starbucks, McDonald's, Coca-Cola, Pepsi...
- **Vietnamese**: Vietcombank (VCB), Vingroup (VIC), FPT...

**Ví dụ:**
```
Input: "Apple"        → Detected: AAPL
Input: "JP Morgan"    → Detected: JPM
Input: "coca cola"    → Detected: KO
Input: "vietcombank"  → Detected: VCB
```

### 3. Curated Asset Lists (Danh sách tài sản phổ biến)

#### 🪙 Crypto (10 options)
- Bitcoin (BTC-USD)
- Ethereum (ETH-USD)
- Binance Coin (BNB-USD)
- Cardano (ADA-USD)
- Solana (SOL-USD)
- Polkadot (DOT-USD)
- Dogecoin (DOGE-USD)
- Ripple (XRP-USD)
- Polygon (MATIC-USD)
- Avalanche (AVAX-USD)

#### 🥇 Commodities (8 options)
- Gold (GC=F)
- Silver (SI=F)
- Crude Oil (CL=F)
- Natural Gas (NG=F)
- Copper (HG=F)
- Corn (ZC=F)
- Wheat (ZW=F)
- Coffee (KC=F)

#### 💱 Forex (6 options)
- Euro/USD (EURUSD=X)
- Pound/USD (GBPUSD=X)
- Yen/USD (JPYUSD=X)
- AUD/USD (AUDUSD=X)
- USD/CAD (USDCAD=X)
- USD/CHF (USDCHF=X)

---

## 📖 Cách sử dụng

### Phân tích cổ phiếu (2 cách)

**Cách 1: Nhập ticker**
```
1. Chọn: 📈 Stock
2. Input method: "Ticker Symbol"
3. Nhập: AAPL
4. Click "🚀 Analyze"
```

**Cách 2: Tìm theo tên công ty**
```
1. Chọn: 📈 Stock
2. Input method: "Company Name"
3. Nhập: Apple (hoặc apple, APPLE)
4. Hệ thống tự detect → AAPL
5. Click "🚀 Analyze"
```

### Phân tích Crypto
```
1. Chọn: ₿ Crypto
2. Chọn từ dropdown: BTC-USD (Bitcoin ₿)
3. Click "🚀 Analyze"
```

### Phân tích Hàng hóa
```
1. Chọn: 🥇 Commodity
2. Chọn: GC=F (Gold 🥇)
3. Click "🚀 Analyze"
```

### Phân tích Forex
```
1. Chọn: 💱 Forex
2. Chọn: EURUSD=X (Euro/USD €/$)
3. Click "🚀 Analyze"
```

---

## 🛠️ Technical Details

### Ticker Format Cheat Sheet

| Asset Type | Format         | Example       | Explanation                     |
|------------|----------------|---------------|---------------------------------|
| Stock      | `SYMBOL`       | `AAPL`        | 1-5 chữ cái                     |
| Crypto     | `SYMBOL-USD`   | `BTC-USD`     | Crypto ticker + "-USD"          |
| Commodity  | `SYMBOL=F`     | `GC=F`        | Future contract symbol + "=F"   |
| Forex      | `PAIR=X`       | `EURUSD=X`    | Currency pair + "=X"            |

### File Structure
```
utils/
  └── asset_mapping.py          # Asset utilities
      ├── search_company()      # Tìm ticker từ tên công ty
      ├── get_asset_info()      # Phát hiện loại tài sản
      ├── format_asset_name()   # Format hiển thị
      ├── COMPANY_TO_TICKER     # 71 công ty mapping
      └── POPULAR_ASSETS        # Lists for UI dropdowns
```

---

## ✅ Testing

Chạy test suite:
```powershell
python test_asset_mapping.py
```

**Output:**
```
✓ Company search: 71 companies
✓ Asset detection: 4 types
✓ Formatting: Icons + names
✓ Popular lists: 24 assets
✓ Integration: End-to-end
```

---

## 🚀 Running the App

### Quick Start
```powershell
# Windows PowerShell
.\start_streamlit.ps1

# Or directly
streamlit run streamlit_app.py
```

### Test Workflow
```powershell
# Test with different assets
python test_workflow_quick.py
```

---

## 📝 Examples

### Stock Analysis (Company Name)
```
Input: "nvidia"
→ Detected: NVDA
→ Analysis: News fetch → Sentiment → Forecast → Recommendation
→ Output: "BUY $4,500 (Risk: Medium)"
```

### Crypto Analysis
```
Input: BTC-USD
→ Analysis: Bitcoin price trends → Sentiment → Volatility forecast
→ Output: "HOLD (High volatility, wait for dip)"
```

### Commodity Analysis
```
Input: GC=F (Gold)
→ Analysis: Gold market news → Safe-haven sentiment → Price forecast
→ Output: "BUY $2,000 (Hedge against inflation)"
```

### Forex Analysis
```
Input: EURUSD=X
→ Analysis: Currency pair trends → Economic sentiment → Rate forecast
→ Output: "SELL (USD strengthening)"
```

---

## 🔄 Workflow Integration

Multi-asset support hoạt động với toàn bộ pipeline:

```
User Input (Any Asset Type)
    ↓
Planning Agent (Task prioritization)
    ↓
Search Tool (News relevant to asset)
    ↓
Sentiment Analysis (RAG + FinBERT)
    ↓
ML Forecast Agent (Price/trend prediction)
    ↓
Recommendation Agent (BUY/SELL/HOLD + Amount)
    ↓
Output (Personalized based on risk profile)
```

**Lưu ý:** Các agent không cần biết asset type, chúng xử lý tất cả tài sản như nhau thông qua ticker symbol.

---

## 🎨 UI Updates

### Page Title
**Before:** `📊 Stock Intelligence Analyzer`  
**After:** `📊 Multi-Asset Intelligence Analyzer`

### Description
**Before:** "Analyze stock sentiment..."  
**After:** "Analyze stocks, crypto, commodities & forex..."

### Tab 1
**Before:** "🔍 Single Stock Analysis"  
**After:** "🔍 Asset Analysis"

---

## 📚 Tài liệu liên quan

- [WORKFLOW_USAGE_GUIDE.md](./WORKFLOW_USAGE_GUIDE.md) - Chi tiết workflow
- [RUN_STREAMLIT_GUIDE.md](./RUN_STREAMLIT_GUIDE.md) - Hướng dẫn chạy
- [STREAMLIT_QUICKSTART.md](./STREAMLIT_QUICKSTART.md) - Quick start

---

## ❓ FAQ

**Q: Ticker "AAPL" vs "BTC-USD" khác nhau thế nào?**  
A: Chỉ khác format. AAPL là stock, BTC-USD là crypto. Cả 2 đều là "ticker" (mã giao dịch).

**Q: Tôi có thể thêm công ty mới vào search không?**  
A: Có! Mở `utils/asset_mapping.py` → Thêm vào `COMPANY_TO_TICKER` dictionary.

**Q: Crypto/commodity có chính xác như stock không?**  
A: Workflow giống nhau, nhưng:
- Crypto: volatility cao hơn
- Commodity: bị ảnh hưởng supply/demand
- Forex: phụ thuộc lãi suất, chính sách

**Q: Tôi muốn thêm stock Việt Nam?**  
A: Thêm vào `COMPANY_TO_TICKER`:
```python
"mwg": "MWG",
"mobile world": "MWG",
"the gioi di dong": "MWG",
```

---

## 🎯 Next Steps

1. **Test assets:** Thử phân tích BTC, Gold, EUR/USD
2. **Add companies:** Thêm công ty Việt vào mapping
3. **Customize:** Điều chỉnh risk tolerance và investment parameters
4. **Explore:** So sánh sentiment giữa stocks vs crypto

---

**🚀 Ready to analyze! Open Streamlit and try different asset types.**
