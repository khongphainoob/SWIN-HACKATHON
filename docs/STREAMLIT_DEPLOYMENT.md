# SWIN Streamlit - Deployment Guide

## 📋 Overview

This guide covers deploying the SWIN Streamlit application to various platforms.

---

## 🖥️ Local Development

### Windows

#### Using Batch File (Easiest)
```bash
# Double-click: run.bat
# Select option 1
```

#### Using PowerShell
```pwsh
python -m streamlit run streamlit_app.py
```

#### Using Python Menu
```bash
python run.py
# Select option 1
```

### macOS/Linux

#### Using Bash
```bash
python -m streamlit run streamlit_app.py
```

#### Using Python Menu
```bash
python run.py
# Select option 1
```

---

## ☁️ Cloud Deployment

### Option 1: Streamlit Cloud (Recommended)

**Advantages:**
- Free tier available
- No server management
- Auto-deploys from GitHub
- Built-in secrets management

**Steps:**

1. **Push to GitHub**
```bash
git add .
git commit -m "Add Streamlit app"
git push origin main
```

2. **Create Streamlit Account**
- Go to https://streamlit.io/cloud
- Sign in with GitHub

3. **Deploy Application**
- Click "New app"
- Select your repository
- Set these options:
  - **Main file path:** `streamlit_app.py`
  - **Python version:** 3.10

4. **Add Secrets**
- In app settings → "Secrets"
- Add your `.streamlit/secrets.toml` content:
```toml
openai_api_key = "your-key-here"
admin_password = "your-password"
yfinance_api_key = "optional"
newsapi_key = "optional"
```

5. **Deploy!**
Click "Deploy"

**Access:**
```
https://[username]-swin.streamlit.app
```

---

### Option 2: Heroku

**Advantages:**
- Pay-as-you-go pricing
- More control
- Custom domain support

**Setup:**

1. **Install Heroku CLI**
```bash
# Windows
choco install heroku-cli

# macOS
brew tap heroku/brew && brew install heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Create Procfile**
```bash
echo "web: streamlit run streamlit_app.py --logger.level=debug --client.toolbarMode=viewer" > Procfile
```

3. **Create runtime.txt**
```bash
echo "python-3.10.13" > runtime.txt
```

4. **Create .gitignore**
```bash
# Ensure these are ignored
echo ".streamlit/secrets.toml" >> .gitignore
echo "__pycache__/" >> .gitignore
echo ".pytest_cache/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "venv/" >> .gitignore
```

5. **Login to Heroku**
```bash
heroku login
```

6. **Create Heroku App**
```bash
heroku create your-swin-app
```

7. **Add Secrets**
```bash
heroku config:set OPENAI_API_KEY="your-key"
heroku config:set ADMIN_PASSWORD="your-password"
```

8. **Deploy**
```bash
git push heroku main
```

9. **View Logs**
```bash
heroku logs --tail
```

**Access:**
```
https://your-swin-app.herokuapp.com
```

---

### Option 3: AWS (with Docker + EC2)

**Advantages:**
- Full control
- Enterprise features
- Custom configurations

**Setup:**

1. **Create Docker Image**

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create streamlit config
RUN mkdir -p ~/.streamlit && \
    echo "[server]" > ~/.streamlit/config.toml && \
    echo "port = 8501" >> ~/.streamlit/config.toml && \
    echo "headless = true" >> ~/.streamlit/config.toml

# Expose port
EXPOSE 8501

# Run app
CMD ["streamlit", "run", "streamlit_app.py"]
```

2. **Build Docker Image**
```bash
docker build -t swin-app:latest .
```

3. **Test Locally**
```bash
docker run -p 8501:8501 \
  -e OPENAI_API_KEY="your-key" \
  -e ADMIN_PASSWORD="your-password" \
  swin-app:latest
```

4. **Push to AWS ECR**
```bash
# Create ECR repo
aws ecr create-repository --repository-name swin-app

# Login
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  your-account.dkr.ecr.us-east-1.amazonaws.com

# Tag image
docker tag swin-app:latest \
  your-account.dkr.ecr.us-east-1.amazonaws.com/swin-app:latest

# Push
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/swin-app:latest
```

5. **Deploy to EC2 or ECS**
See AWS documentation for EC2/ECS deployment

---

### Option 4: DigitalOcean (App Platform)

**Advantages:**
- Simple deployment
- Good pricing
- Great documentation

**Steps:**

1. **Create DigitalOcean Account**
- Go to https://www.digitalocean.com

2. **Connect GitHub Repository**
- In DigitalOcean dashboard
- Click "Apps" → "Create App"
- Select GitHub repository

3. **Configure App**
```yaml
name: swin-app
services:
  - name: web
    github:
      repo: your-username/swin
      branch: main
    build_command: pip install -r requirements.txt
    run_command: streamlit run streamlit_app.py --server.port=8080
    http_port: 8080
    health_check:
      http_path: /_stcore/health
envs:
  - key: OPENAI_API_KEY
    value: your-key
    type: SECRET
  - key: ADMIN_PASSWORD
    value: your-password
    type: SECRET
```

4. **Deploy**
- Click "Deploy"

5. **Access**
```
https://your-app.ondigitalocean.app
```

---

### Option 5: Google Cloud (Cloud Run)

**Setup:**

1. **Install Google Cloud SDK**
```bash
curl https://sdk.cloud.google.com | bash
gcloud init
```

2. **Create `cloudbuild.yaml`**
```yaml
steps:
  - name: "gcr.io/cloud-builders/docker"
    args:
      - "build"
      - "-t"
      - "gcr.io/$PROJECT_ID/swin:latest"
      - "."
  - name: "gcr.io/cloud-builders/docker"
    args:
      - "push"
      - "gcr.io/$PROJECT_ID/swin:latest"
  - name: "gcr.io/cloud-builders/gke-deploy"
    args:
      - "run"
      - "--filename=k8s/"
      - "--image=gcr.io/$PROJECT_ID/swin:latest"
      - "--location=us-central1"
      - "--cluster=swin-cluster"
images:
  - "gcr.io/$PROJECT_ID/swin:latest"
```

3. **Deploy**
```bash
gcloud builds submit --config cloudbuild.yaml
```

---

## 🔒 Security Considerations

### Secrets Management

**DO NOT:**
```
❌ Commit .streamlit/secrets.toml to Git
❌ Push API keys to GitHub
❌ Share passwords in code
❌ Use default passwords in production
```

**DO:**
```
✅ Use environment variables
✅ Use cloud provider secrets management
✅ Rotate API keys regularly
✅ Use strong, unique passwords
✅ Enable HTTPS
✅ Use IP whitelisting if available
```

### Environment Variables

**Set in deployment:**
```bash
# Streamlit Cloud secrets
OPENAI_API_KEY
ADMIN_PASSWORD
DATABASE_PATH

# Optional
YFINANCE_API_KEY
NEWSAPI_KEY
LOG_LEVEL
CACHE_DURATION_HOURS
```

### Production Checklist

- [ ] All secrets in environment variables
- [ ] HTTPS enabled
- [ ] Admin password changed from default
- [ ] API keys rotated
- [ ] Logging configured
- [ ] Database backed up
- [ ] Rate limiting enabled
- [ ] Error monitoring set up
- [ ] Performance monitoring enabled
- [ ] Documentation updated

---

## 📊 Monitoring

### Streamlit Cloud
- View logs: App settings → Logs
- Monitor performance: Dashboard
- Set alerts: In app settings

### Self-Hosted
```bash
# Check container health
docker ps

# View logs
docker logs container-id

# Monitor resources
docker stats

# Check endpoints
curl http://localhost:8501/_stcore/health
```

### Application Monitoring
```python
# Add to app for monitoring
import streamlit as st
from datetime import datetime

# Log page visits
st.write(f"Last updated: {datetime.now()}")

# Monitor usage
with st.spinner("Loading..."):
    # Your code
    pass
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.10
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
      
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Streamlit Cloud
        run: |
          # Deploy using Streamlit CLI
          # Requires STREAMLIT_TOKEN secret
```

---

## 📈 Performance Optimization

### Caching
```python
@st.cache_data
def load_data():
    # This runs only once
    return expensive_operation()

@st.cache_resource
def init_model():
    # Initialize expensive resource once
    return Model()
```

### Session State
```python
if 'analysis_cache' not in st.session_state:
    st.session_state.analysis_cache = {}
```

### Resource Management
```
- Set reasonable timeouts
- Limit API call frequency
- Cache external API responses
- Use async functions where possible
```

---

## 🆘 Troubleshooting Deployment

### "Port already in use"
```bash
# Find process using port 8501
lsof -i :8501

# Kill process
kill -9 <PID>
```

### "Module not found"
```bash
# Ensure requirements.txt is complete
pip freeze > requirements.txt

# Rebuild container
docker build --no-cache -t swin-app:latest .
```

### "Out of memory"
- Reduce cache settings
- Optimize data loading
- Use pagination for large datasets
- Close unused resources

### "Slow performance"
- Enable caching
- Use async operations
- Optimize queries
- Use CDN for static assets

---

## 📚 Deployment Checklists

### Pre-Deployment
- [ ] All tests pass: `pytest tests/ -v`
- [ ] No hardcoded secrets
- [ ] Requirements.txt updated
- [ ] Documentation current
- [ ] Error handling in place
- [ ] Logging configured

### Post-Deployment
- [ ] Health check passes
- [ ] All features tested
- [ ] Performance acceptable
- [ ] Monitoring active
- [ ] Backup configured
- [ ] Team notified

---

## 📞 Support

**Quick Links:**
- Streamlit Docs: https://docs.streamlit.io
- Deployment Guide: https://docs.streamlit.io/deploy
- Docker Docs: https://docs.docker.com
- AWS Docs: https://docs.aws.amazon.com

**For Issues:**
1. Check logs
2. Review error messages
3. Test locally first
4. Check platform documentation
5. Review our troubleshooting guide

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-13
