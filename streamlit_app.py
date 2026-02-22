"""
SWIN Streamilit Application
Main entry point with User and Admin interfaces
"""

import streamlit as st
import os
from pathlib import Path
from streamlit.errors import StreamlitSecretNotFoundError

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file if exists
except ImportError:
    pass  # python-dotenv not installed, skip

# Configure page
st.set_page_config(
    page_title="SWIN - Stock Intelligence Network",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .admin-panel {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #ff6b6b;
    }
    .user-panel {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        color: #155724;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
        color: #721c24;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        color: #856404;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'interface_mode' not in st.session_state:
    st.session_state.interface_mode = 'user'

if 'api_key' not in st.session_state:
    st.session_state.api_key = os.getenv('OPENAI_API_KEY', '')

if 'gemini_api_key' not in st.session_state:
    st.session_state.gemini_api_key = os.getenv('GEMINI_API_KEY', '')

# User profile defaults
if 'user_id' not in st.session_state:
    st.session_state.user_id = 'user_001'
if 'risk_tolerance' not in st.session_state:
    st.session_state.risk_tolerance = 'medium'
if 'investment_horizon' not in st.session_state:
    st.session_state.investment_horizon = 'medium_term'
if 'investment_amount' not in st.session_state:
    st.session_state.investment_amount = 10000.0

# Configuration defaults
if 'config' not in st.session_state:
    st.session_state.config = {
        'sentiment_positive_threshold': 0.3,
        'sentiment_negative_threshold': -0.3,
        'forecast_confidence_threshold': 0.6,
        'news_limit': 5,
        'max_recommendations': 10,
        'human_review_required_threshold': 0.8,
        'database_path': 'data/portfolio.db',
        'enable_cache': True,
        'cache_duration_hours': 1.0,
        'log_to_file': True,
        'enable_sentiment': True,
        'enable_forecast': True,
        'enable_alerts': True
    }

# Sidebar navigation
st.sidebar.markdown("## 🎯 SWIN Navigation")

# Authentication check for admin
try:
    admin_password = st.secrets.get("admin_password", "admin123")
except StreamlitSecretNotFoundError:
    admin_password = "admin123"
mode = st.sidebar.radio(
    "Select Interface:",
    ["👤 User Interface", "⚙️ Admin Interface"],
    index=0 if st.session_state.interface_mode == 'user' else 1
)

if "User" in mode:
    st.session_state.interface_mode = 'user'
else:
    # Ask for password for admin
    password_input = st.sidebar.text_input("Admin Password:", type="password")
    if password_input:
        if password_input == admin_password:
            st.session_state.interface_mode = 'admin'
            st.sidebar.success("✅ Admin access granted")
        else:
            st.sidebar.error("❌ Wrong password")
            st.session_state.interface_mode = 'user'
    else:
        st.session_state.interface_mode = 'user'

# Load appropriate interface
if st.session_state.interface_mode == 'user':
    from pages import user_interface
    user_interface.render()
else:
    from pages import admin_interface
    admin_interface.render()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
**SWIN v1.0.0**
Sentiment-driven Workflow Intelligence Network

[GitHub](https://github.com) | [Docs](./TOOLS_AND_AGENTS.md) | [API](./INTEGRATION_GUIDE.md)
""")
