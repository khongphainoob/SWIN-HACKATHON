# SWIN Streamlit Web Interface

## Overview

The SWIN Streamlit application provides an intuitive web interface for stock sentiment analysis and investment recommendations. It includes:

- **👤 User Interface**: For analyzing stocks, viewing recommendations, and managing portfolio
- **⚙️ Admin Interface**: For configuring API keys, parameters, and system settings

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Streamlit and other dependencies
pip install -r requirements.txt
```

### 2. Configure Secrets

Copy and customize the secrets template:

```bash
# Copy the example secrets file
copy .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml` and add your API keys:

```toml
openai_api_key = "your-openai-key"
admin_password = "your-admin-password"
```

### 3. Run the Application

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📋 Features Overview

### User Interface

#### 🔍 Single Stock Analysis
- Enter a ticker symbol (e.g., AAPL, MSFT)
- Get sentiment analysis and ML-powered recommendation
- View detailed reasoning and analysis

**Features:**
- Real-time news sentiment analysis
- Confidence scoring
- Urgency levels (High/Medium/Low)
- Detailed recommendation reasoning

#### 📈 Portfolio Analysis
- Analyze multiple stocks at once
- View recommendations for all holdings
- Download results as CSV
- Summary statistics (BUY/SELL/HOLD counts)

**Example:**
```
Enter: AAPL, MSFT, GOOGL, NVDA, TSLA
Get: Individual recommendations for each
```

#### 📰 News & Sentiment
- Fetch latest news for any ticker
- Automated text summarization
- View full articles
- Track sentiment trends

#### 💼 My Portfolio
- Add/update stock holdings
- Track cost basis
- View portfolio summary
- Analyze all holdings at once
- Calculate total investment

### Admin Interface

#### 🔑 API Keys Management
- OpenAI API key configuration
- Optional Yahoo Finance API key
- Optional NewsAPI key
- Secure key testing

#### ⚙️ Workflow Parameters
- **Sentiment thresholds**: Adjust positive/negative detection
- **Forecast confidence**: Minimum confidence for recommendations
- **Human review threshold**: When to require manual review
- **News limit**: How many articles to fetch
- **Max recommendations**: Limit outputs

#### 📊 System Settings
- Database configuration
- Cache settings (enable/duration)
- Logging configuration
- Feature toggles
- Database management

#### 📝 System Logs
- View recent activity
- Filter by log level
- Download logs
- Clear logs

#### ℹ️ System Info
- Environment details
- Dependency versions
- Health checks
- Database management
- System about information

---

## 🔑 Configuration Guide

### API Keys

#### OpenAI API
1. Get key from https://platform.openai.com/api-keys
2. Go to Admin Interface → API Keys
3. Paste key and click "Save OpenAI Key"

#### Google Gemini API
1. Get key from https://makersuite.google.com/app/apikey
2. Go to Admin Interface → API Keys
3. Paste key and click "Save Gemini Key"

#### Yahoo Finance (Optional)
- Automatically uses free tier
- No API key required

#### NewsAPI (Optional)
- Get key from https://newsapi.org
- Optional for enhanced news features

### Parameters

**Sentiment Thresholds:**
- Positive threshold (default 0.3): Score >= this = Bullish
- Negative threshold (default -0.3): Score <= this = Bearish
- Between = Neutral

**Forecast Settings:**
- Confidence threshold: Minimum confidence for recommendations
- Human review threshold: When manual approval is needed

**News Settings:**
- Limit: Number of articles to fetch (1-20)
- Max recommendations: Maximum outputs per analysis

---

## 🔐 Security

### Password Protection
Admin interface requires password (default: `admin123`)

To change:
1. Edit `.streamlit/secrets.toml`
2. Update `admin_password` value
3. Click Admin Interface and enter new password

### API Key Safety
- Keys stored in `.streamlit/secrets.toml`
- **Never commit this file to Git**
- Displayed as password fields in UI
- Added to `.gitignore`

---

## 📊 Usage Examples

### Example 1: Analyze Single Stock
```
1. Go to "🔍 Single Stock Analysis"
2. Enter "AAPL"
3. Click "🚀 Analyze"
4. See recommendation with reasoning
```

### Example 2: Portfolio Batch Analysis
```
1. Go to "📈 Portfolio Analysis"
2. Enter "AAPL, MSFT, GOOGL, NVDA"
3. Click "📊 Analyze Portfolio"
4. View colored table with recommendations
5. Download as CSV
```

### Example 3: Adjust Sentiment Threshold
```
1. Go to "⚙️ Admin Interface"
2. Enter admin password
3. Go to "⚙️ Parameters"
4. Adjust "Positive Sentiment Threshold" to 0.4
5. Click "💾 Save Parameters"
6. New analyses use updated threshold
```

### Example 4: Add Portfolio Holding
```
1. Go to "💼 My Portfolio"
2. Enter User ID: "myuser123"
3. Fill in ticker (AAPL), shares (100), cost ($150)
4. Click "✅ Add"
5. Click "👁️ View Portfolio" to see holding
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:**
```bash
pip install streamlit==1.28.0
```

### Issue: "Connection refused at localhost:8501"
**Solution:**
1. App might already be running
2. Try different port: `streamlit run streamlit_app.py --server.port 8502`
3. Check if port 8501 is blocked by firewall

### Issue: "Admin password incorrect"
**Solution:**
1. Edit `.streamlit/secrets.toml`
2. Check `admin_password` value
3. Restart Streamlit: Press Ctrl+C and run again

### Issue: "API key not found"
**Solution:**
1. Go to Admin Interface → API Keys
2. Enter and save your OpenAI or Gemini API key
3. Click "Test Connection"

### Issue: "No articles found"
**Solution:**
- Yahoo Finance might be rate-limited
- Wait 1-2 minutes and try again
- Or use a different ticker

---

## 📱 Browser Support

**Recommended:**
- Chrome/Chromium (v100+)
- Firefox (v100+)
- Safari (v15+)
- Edge (v100+)

**Minimum Resolution:** 1024x768

---

## 🎨 Customization

### Change Color Theme
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#1f77b4"        # Change this
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

### Add Custom Pages
Create new file in `pages/` directory:
```python
# pages/my_feature.py
def render():
    st.header("My Feature")
    # Your code here

if __name__ == "__main__":
    render()
```

Import in `streamlit_app.py`:
```python
from pages import my_feature
```

---

## 🚀 Deployment

### Deploy to Streamlit Cloud
1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app" and select repository
4. Set main file to `streamlit_app.py`
5. Add secrets in dashboard

### Deploy to Docker
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

Run:
```bash
docker build -t swin .
docker run -p 8501:8501 swin
```

---

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [SWIN Tools & Agents Guide](./TOOLS_AND_AGENTS.md)
- [Integration Guide](./INTEGRATION_GUIDE.md)
- [Quick Reference](./QUICK_REFERENCE.md)

---

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Read [TOOLS_AND_AGENTS.md](./TOOLS_AND_AGENTS.md)
3. Review [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md)
4. Check test files for usage examples

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-13  
**Python:** 3.10+
