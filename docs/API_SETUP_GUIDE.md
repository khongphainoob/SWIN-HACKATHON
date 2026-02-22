# 🔑 API Key Setup Guide

Hướng dẫn chi tiết cách lấy và cấu hình API keys cho SWIN Agentic Project.

---

## 📋 Tổng quan

Hệ thống hỗ trợ **4 LLM providers**:

| Provider | Model | Chi phí | Tốc độ | Khuyến nghị |
|----------|-------|---------|--------|-------------|
| 🤖 **OpenAI** | GPT-4, GPT-3.5 | $$ | Nhanh | Production |
| 🧠 **Gemini** | Gemini Pro | Miễn phí | Nhanh | Development |
| 🎭 **Anthropic** | Claude 3 | $$$ | Trung bình | High quality |
| ⚡ **Groq** | Llama 3, Mixtral | Miễn phí (beta) | Rất nhanh | Testing |

**Lưu ý:** Chỉ cần **1 API key** là đủ để chạy hệ thống. Khuyến nghị dùng **Gemini** (miễn phí) hoặc **Groq** (nhanh) cho development.

---

## 🚀 Quick Start (3 bước)

### 1️⃣ Tạo file .env
```powershell
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

### 2️⃣ Lấy API key (chọn 1 provider)

**Tùy chọn A: Gemini (Khuyến nghị - Miễn phí)**
1. Truy cập: https://makersuite.google.com/app/apikey
2. Đăng nhập Google account
3. Click "Create API Key"
4. Copy key (dạng: `AIzaSy...`)
5. Paste vào `.env`: `GEMINI_API_KEY=AIzaSy...`

**Tùy chọn B: Groq (Nhanh - Miễn phí)**
1. Truy cập: https://console.groq.com/
2. Sign up (free)
3. Vào "API Keys" → "Create API Key"
4. Copy key (dạng: `gsk_...`)
5. Paste vào `.env`: `GROQ_API_KEY=gsk_...`

### 3️⃣ Chạy test
```powershell
python test_streamlit_ready.py
```

Nếu thấy `✅ GEMINI_API_KEY found` hoặc `✅ GROQ_API_KEY found` → **Thành công!**

---

## 📖 Chi tiết từng Provider

### 🤖 OpenAI (GPT-4, GPT-3.5)

**Ưu điểm:**
- Model mạnh nhất (GPT-4)
- Hỗ trợ function calling tốt
- Documentation đầy đủ
- Reliable và stable

**Nhược điểm:**
- Tốn phí ($0.03/1K tokens GPT-4)
- Cần credit card để sử dụng

**Cách lấy API key:**

1. **Đăng ký:**
   - Truy cập: https://platform.openai.com/signup
   - Đăng nhập hoặc tạo account mới
   - Verify email

2. **Thêm payment method:**
   - Vào: https://platform.openai.com/account/billing
   - Add credit card
   - Nạp ít nhất $5 credit

3. **Tạo API key:**
   - Vào: https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Đặt tên (vd: "SWIN Project")
   - Copy key (dạng: `sk-proj-...`)
   - ⚠️ **Lưu ngay! Chỉ hiện 1 lần**

4. **Cấu hình:**
   ```bash
   # .env
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
   ```

5. **Test:**
   ```powershell
   python test_streamlit_ready.py
   ```

**Pricing:**
- GPT-4o: $0.005/1K input tokens, $0.015/1K output tokens
- GPT-3.5-turbo: $0.0015/1K input tokens, $0.002/1K output tokens

**Free tier:** $5 credit khi đăng ký mới (hết hạn sau 3 tháng)

---

### 🧠 Google Gemini (Khuyến nghị)

**Ưu điểm:**
- ✅ **Hoàn toàn miễn phí**
- Model tốt (Gemini 1.5 Pro)
- Tích hợp Google services
- Rate limit cao (60 req/min free)

**Nhược điểm:**
- Chậm hơn GPT-4 một chút
- Function calling phức tạp hơn

**Cách lấy API key (Siêu dễ):**

1. **Đăng nhập Google:**
   - Truy cập: https://makersuite.google.com/app/apikey
   - Hoặc: https://aistudio.google.com/app/apikey
   - Đăng nhập bằng Gmail

2. **Tạo key:**
   - Click "Get API Key" hoặc "Create API Key"
   - Chọn Google Cloud project (hoặc tạo mới)
   - Click "Create API key in existing project"
   - Copy key (dạng: `AIzaSy...`)

3. **Cấu hình:**
   ```bash
   # .env
   GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXX
   ```

4. **Verify:**
   ```powershell
   # Kiểm tra key
   curl "https://generativelanguage.googleapis.com/v1/models?key=YOUR_API_KEY"
   ```

**Rate Limits (Free tier):**
- 60 requests per minute
- 1,500 requests per day
- 1 million tokens per day

**Models available:**
- `gemini-1.5-pro`: Best quality
- `gemini-1.5-flash`: Fast inference
- `gemini-pro`: Legacy (still good)

---

### 🎭 Anthropic (Claude 3)

**Ưu điểm:**
- Claude 3 Opus: Chất lượng cao nhất
- Context window lớn (200K tokens)
- Tốt với phân tích phức tạp
- Ethical AI focus

**Nhược điểm:**
- Đắt nhất ($15/1M input tokens)
- Cần waitlist hoặc invite
- Slower response

**Cách lấy API key:**

1. **Sign up:**
   - Truy cập: https://console.anthropic.com/
   - Create account
   - Verify email

2. **Waitlist (có thể bỏ qua):**
   - Join waitlist nếu không có invite
   - Hoặc dùng direct access (đã mở cho public)

3. **Add payment:**
   - Vào "Settings" → "Billing"
   - Add credit card
   - Buy credits ($5 minimum)

4. **Create key:**
   - Vào "API Keys"
   - Click "Create Key"
   - Copy key (dạng: `sk-ant-...`)

5. **Cấu hình:**
   ```bash
   # .env
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
   ```

**Models:**
- `claude-3-opus`: Best ($15/$75 per 1M tokens)
- `claude-3-sonnet`: Balanced ($3/$15 per 1M tokens)
- `claude-3-haiku`: Fast ($0.25/$1.25 per 1M tokens)

---

### ⚡ Groq (Fast Inference)

**Ưu điểm:**
- ⚡ **Cực kỳ nhanh** (300+ tokens/sec)
- ✅ **Miễn phí trong beta**
- Nhiều open-source models
- Không cần credit card

**Nhược điểm:**
- Beta (có thể thay đổi)
- Rate limit thấp hơn
- Model quality thấp hơn GPT-4

**Cách lấy API key:**

1. **Sign up:**
   - Truy cập: https://console.groq.com/
   - Click "Sign Up"
   - Đăng nhập bằng Google/GitHub

2. **Create key:**
   - Vào dashboard
   - Click "API Keys"
   - Click "Create API Key"
   - Đặt tên
   - Copy key (dạng: `gsk_...`)

3. **Cấu hình:**
   ```bash
   # .env
   GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx
   ```

**Models available:**
- `llama-3.1-70b-versatile`: Best balance
- `mixtral-8x7b-32768`: Fast
- `gemma-7b-it`: Lightweight

**Free tier:**
- 30 requests per minute
- 6,000 requests per day
- Unlimited tokens (beta)

---

## 🔄 Switching Between Providers

Hệ thống cho phép chuyển provider linh hoạt:

### Cách 1: Config file

Edit [configs/model_config.yaml](configs/model_config.yaml):
```yaml
LLM:
  provider: "gemini"  # hoặc "openai", "anthropic", "groq"
  model: "gemini-1.5-pro"
  temperature: 0.3
  max_tokens: 1024
```

### Cách 2: Code

```python
from services.llm_service import LLMService

# Gemini
llm = LLMService(provider="gemini", model="gemini-1.5-pro")

# OpenAI
llm = LLMService(provider="openai", model="gpt-4")

# Anthropic
llm = LLMService(provider="anthropic", model="claude-3-sonnet")

# Groq
llm = LLMService(provider="groq", model="llama-3.1-70b-versatile")
```

### Cách 3: Runtime override

```python
llm = LLMService(provider="gemini")

# Single call với OpenAI
response = llm.call_llm(
    prompt="Analyze this...",
    provider="openai",
    model="gpt-4"
)
```

### Cách 4: Streamlit Admin (Đã implement)

1. Chạy `streamlit run streamlit_app.py`
2. Vào tab "⚙️ Settings"
3. Nhập API key
4. Click "Test Connection"
5. Save

---

## 🛠️ Troubleshooting

### Lỗi: "API key not found"

**Giải pháp:**
```powershell
# 1. Kiểm tra file .env tồn tại
Get-ChildItem .env

# 2. Kiểm tra nội dung
Get-Content .env | Select-String "API_KEY"

# 3. Load lại environment
$env:GEMINI_API_KEY = "AIzaSy..."

# 4. Test
python test_streamlit_ready.py
```

### Lỗi: "Invalid API key"

**Nguyên nhân:**
- Key sai format
- Key đã expire hoặc revoke
- Key không có quyền

**Giải pháp:**
1. Tạo key mới
2. Check billing/payment
3. Verify permissions

### Lỗi: "Rate limit exceeded"

**Giải pháp:**
- Đợi 1 phút
- Nâng cấp plan
- Hoặc switch sang provider khác

### Lỗi: "Model not found"

**Giải pháp:**
- Check model name đúng format
- Xem docs của provider
- Update [configs/model_config.yaml](configs/model_config.yaml)

---

## 📊 Cost Comparison

### Ví dụ: Phân tích 1 stock (workflow hoàn chỉnh)

**Estimate tokens:**
- Planning Agent: ~500 tokens
- Sentiment Analysis: ~1,000 tokens
- ML Forecast: ~800 tokens
- Recommendation: ~700 tokens
- **Total: ~3,000 tokens per analysis**

**Chi phí (100 analyses/day):**

| Provider | Model | Input Cost | Output Cost | Total/Day |
|----------|-------|-----------|-------------|-----------|
| Gemini | Gemini Pro | $0 | $0 | **$0** ✅ |
| Groq | Llama 3 70B | $0 | $0 | **$0** ✅ |
| OpenAI | GPT-3.5 | $0.45 | $0.60 | **$1.05** |
| OpenAI | GPT-4o | $1.50 | $4.50 | **$6.00** |
| Anthropic | Claude 3 | $0.90 | $2.25 | **$3.15** |

**Khuyến nghị:**
- **Development:** Gemini (miễn phí)
- **Testing:** Groq (nhanh + miễn phí)
- **Production:** GPT-3.5 (cân bằng giá/chất lượng)
- **High-end:** GPT-4o hoặc Claude 3 (chất lượng cao)

---

## ✅ Verification Checklist

Sau khi setup xong, check:

- [ ] File `.env` tồn tại trong project root
- [ ] Ít nhất 1 API key đã được điền
- [ ] Key không có space/newline thừa
- [ ] Chạy `python test_streamlit_ready.py` → PASS
- [ ] Streamlit app chạy được
- [ ] Tab "Asset Analysis" hoạt động
- [ ] Nhận được response từ LLM

---

## 🔐 Security Best Practices

### ✅ DO (Nên làm)
- Store keys trong `.env` file
- Add `.env` vào `.gitignore`
- Rotate keys định kỳ (3-6 tháng)
- Sử dụng key riêng cho dev/prod
- Set rate limits
- Monitor usage

### ❌ DON'T (Không làm)
- ❌ Commit `.env` vào Git
- ❌ Hardcode keys trong code
- ❌ Share keys qua email/chat
- ❌ Sử dụng 1 key cho nhiều projects
- ❌ Expose keys trong logs/errors

### .gitignore check
```bash
# Đảm bảo .env đã ignore
cat .gitignore | grep ".env"
# Output: .env
```

---

## 📚 Tài liệu Provider

- **OpenAI:** https://platform.openai.com/docs
- **Gemini:** https://ai.google.dev/docs
- **Anthropic:** https://docs.anthropic.com/
- **Groq:** https://console.groq.com/docs

---

## 🆘 Support

**Gặp vấn đề?**

1. Check [Troubleshooting](#troubleshooting)
2. Xem logs: `logs/app.log`
3. Test workflow: `python test_workflow_quick.py`
4. GitHub Issues: [Create issue](https://github.com/your-repo/issues)

---

## 🎯 Next Steps

Sau khi setup API keys:

1. ✅ **Test workflow:**
   ```powershell
   python test_workflow_quick.py
   ```

2. ✅ **Chạy Streamlit:**
   ```powershell
   .\start_streamlit.ps1
   ```

3. ✅ **Phân tích stock đầu tiên:**
   - Chọn asset type
   - Nhập ticker hoặc company name
   - Click "🚀 Analyze"

4. ✅ **Optimize config:**
   - Edit [configs/model_config.yaml](configs/model_config.yaml)
   - Điều chỉnh temperature, max_tokens
   - Test với nhiều providers

---

**🚀 Ready to build! Your API keys are configured.**
