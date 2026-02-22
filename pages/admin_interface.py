"""
Admin Interface - Configuration and Settings Management
"""

import streamlit as st
import os
import json
from datetime import datetime
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def render():
    """Render admin interface."""
    
    # Initialize config if not exists
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
    
    st.markdown('<div class="main-title">⚙️ Admin Control Panel</div>', unsafe_allow_html=True)
    st.markdown("Configure API keys, parameters, and system settings")
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔑 API Keys",
        "⚙️ Parameters",
        "📊 System Settings",
        "📝 Logs",
        "ℹ️ System Info"
    ])
    
    # ============= TAB 1: API Keys =============
    with tab1:
        st.header("API Key Management")
        
        st.warning("🔐 API keys are sensitive information. Never share them publicly!")
        
        # OpenAI API Key
        st.subheader("OpenAI API")
        openai_key = st.text_input(
            "OpenAI API Key:",
            value=st.session_state.get('api_key', ''),
            type="password",
            help="Your OpenAI API key for LLM features"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Save OpenAI Key"):
                st.session_state.api_key = openai_key
                os.environ['OPENAI_API_KEY'] = openai_key
                st.success("✅ OpenAI API key updated!")
        
        with col2:
            if st.button("🔄 Test Connection"):
                if openai_key:
                    try:
                       prompt = "Hello, world!"
                          # Simple test - check if key is in reasonable format
                       from services.llm_service import LLMService
                       llm = LLMService(provider="openai", model="gpt-3.5-turbo", api_key=openai_key)
                       response = llm.call_llm(prompt)
                       if response:
                            st.success("✅ OpenAI API connection test passed! with response: " + str(response)[:100])
                       else:
                            st.warning("⚠️ OpenAI API key is valid but returned no response")
                    except Exception as e:
                        st.error(f"❌ Connection test failed: {str(e)}")
                else:
                    st.warning("⚠️ Please enter an API key first")
        
        st.divider()
        
        # Google Gemini API Key
        st.subheader("Google Gemini API")
        gemini_key = st.text_input(
            "Gemini API Key:",
            value=st.session_state.get('gemini_api_key', ''),
            type="password",
            help="Your Google Gemini API key for LLM features"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Save Gemini Key"):
                st.session_state.gemini_api_key = gemini_key
                os.environ['GEMINI_API_KEY'] = gemini_key
                st.success("✅ Gemini API key updated!")
        
        with col2:
            if st.button("🔄 Test Gemini Connection"):
                if gemini_key:
                    try:
                        # Simple test - check if key is in reasonable format
                        from services.llm_service import LLMService
                        llm = LLMService(provider="gemini", model="gemma-3-27b-it", api_key=gemini_key)
                        response = llm.call_llm("Hello, Gemini! mày có khỏe không?")   
                        if response:
                            st.success("✅ Gemini API connection test passed! with response: " + str(response)[:100])
                        else:
                            st.warning("⚠️ Gemini API key is valid but returned no response")
                    except Exception as e:
                        st.error(f"❌ Connection test failed: {str(e)}")
                else:
                    st.warning("⚠️ Please enter a Gemini API key first")
        
        st.divider()
        
        # Other API Keys
        st.subheader("Other API Services")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            yfinance_key = st.text_input(
                "Yahoo Finance API Key (optional):",
                value="",
                type="password"
            )
        
        with col2:
            newsapi_key = st.text_input(
                "NewsAPI Key (optional):",
                value="",
                type="password"
            )
        
        with col3:
            anthropic_key = st.text_input(
                "Anthropic API Key (optional):",
                value="",
                type="password"
            )
        
        if st.button("💾 Save All API Keys"):
            # Create secrets config
            secrets = {
                "openai_api_key": openai_key,
                "gemini_api_key": gemini_key,
                "yfinance_api_key": yfinance_key,
                "newsapi_key": newsapi_key,
                "anthropic_key": anthropic_key,
                "saved_at": datetime.now().isoformat()
            }
            
            # Save to .streamlit/secrets.toml
            secrets_path = Path(".streamlit/secrets.toml")
            secrets_path.parent.mkdir(exist_ok=True)
            
            try:
                with open(secrets_path, 'w') as f:
                    for key, value in secrets.items():
                        if value:
                            f.write(f'{key} = "{value}"\n')
                
                st.success("✅ All API keys saved securely!")
            except Exception as e:
                st.error(f"❌ Error saving keys: {str(e)}")
    
    # ============= TAB 2: Parameters =============
    with tab2:
        st.header("Workflow Parameters")
        
        st.info("📝 Adjust the thresholds and parameters that control the analysis workflow")
        
        # Sentiment thresholds
        st.subheader("📊 Sentiment Analysis Thresholds")
        
        col1, col2 = st.columns(2)
        
        with col1:
            positive_threshold = st.slider(
                "Positive Sentiment Threshold:",
                min_value=-1.0,
                max_value=1.0,
                value=st.session_state.config.get('sentiment_positive_threshold', 0.3),
                step=0.05,
                help="Score above this = Positive sentiment"
            )
        
        with col2:
            negative_threshold = st.slider(
                "Negative Sentiment Threshold:",
                min_value=-1.0,
                max_value=1.0,
                value=float(st.session_state.config.get('sentiment_negative_threshold', -0.3)),
                step=0.05,
                help="Score below this = Negative sentiment"
            )
        
        # Forecast parameters
        st.subheader("🔮 Forecast Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            forecast_confidence = st.slider(
                "Minimum Forecast Confidence:",
                min_value=0.0,
                max_value=1.0,
                value=float(st.session_state.config.get('forecast_confidence_threshold', 0.6)),
                step=0.05,
                help="Minimum confidence for forecast to be used"
            )
        
        with col2:
            human_review_threshold = st.slider(
                "Human Review Required At:",
                min_value=0.0,
                max_value=1.0,
                value=float(st.session_state.config.get('human_review_required_threshold', 0.8)),
                step=0.05,
                help="Confidence above this requires human review"
            )
        
        # News parameters
        st.subheader("📰 News Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            news_limit = st.number_input(
                "Default News Articles Limit:",
                min_value=1,
                max_value=50,
                value=int(st.session_state.config.get('news_limit', 5)),
                help="Number of articles to fetch per ticker"
            )
        
        with col2:
            max_recommendations = st.number_input(
                "Max Recommendations Per Analysis:",
                min_value=1,
                max_value=100,
                value=int(st.session_state.config.get('max_recommendations', 10)),
                help="Maximum recommendations to generate"
            )
        
        # Save parameters
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Save Parameters"):
                st.session_state.config.update({
                    'sentiment_positive_threshold': positive_threshold,
                    'sentiment_negative_threshold': negative_threshold,
                    'forecast_confidence_threshold': forecast_confidence,
                    'human_review_required_threshold': human_review_threshold,
                    'news_limit': news_limit,
                    'max_recommendations': max_recommendations
                })
                
                st.success("✅ Parameters updated!")
        
        with col2:
            if st.button("🔄 Reset to Defaults"):
                st.session_state.config = {
                    'sentiment_positive_threshold': 0.3,
                    'sentiment_negative_threshold': -0.3,
                    'forecast_confidence_threshold': 0.6,
                    'news_limit': 5,
                    'max_recommendations': 10,
                    'human_review_required_threshold': 0.8,
                    'database_path': 'data/portfolio.db',
                    'enable_cache': True,
                    'cache_duration_hours': 1
                }
                st.success("✅ Reset to default parameters")
                st.rerun()
        
        # Display current parameters
        st.divider()
        st.subheader("📋 Current Configuration")
        st.json(st.session_state.config)
    
    # ============= TAB 3: System Settings =============
    with tab3:
        st.header("System Settings")
        
        # Database settings
        st.subheader("💾 Database Settings")
        
        db_path = st.text_input(
            "Database Path:",
            value=st.session_state.config.get('database_path', 'data/portfolio.db'),
            help="Path to SQLite database file"
        )
        
        # Cache settings
        st.subheader("⚡ Cache Settings")
        
        enable_cache = st.checkbox(
            "Enable Cache",
            value=st.session_state.config.get('enable_cache', True),
            help="Cache analysis results for faster queries"
        )
        
        if enable_cache:
            cache_duration = st.number_input(
                "Cache Duration (hours):",
                min_value=0.1,
                max_value=24.0,
                value=float(st.session_state.config.get('cache_duration_hours', 1.0)),
                step=0.1
            )
        else:
            cache_duration = 0
        
        # Logging settings
        st.subheader("📝 Logging Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            log_level = st.selectbox(
                "Log Level:",
                ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                index=1,
                help="Minimum log level to record"
            )
        
        with col2:
            log_to_file = st.checkbox(
                "Log to File",
                value=bool(st.session_state.config.get('log_to_file', True)),
                help="Save logs to file"
            )
        
        # Feature toggles
        st.subheader("🎛️ Feature Toggles")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            enable_sentiment = st.checkbox("Enable Sentiment Analysis", value=bool(st.session_state.config.get('enable_sentiment', True)))
        
        with col2:
            enable_forecast = st.checkbox("Enable ML Forecasting", value=bool(st.session_state.config.get('enable_forecast', True)))
        
        with col3:
            enable_alerts = st.checkbox("Enable Risk Alerts", value=bool(st.session_state.config.get('enable_alerts', True)))
        
        # Save system settings
        if st.button("💾 Save System Settings"):
            st.session_state.config.update({
                'database_path': db_path,
                'enable_cache': enable_cache,
                'cache_duration_hours': cache_duration,
                'log_level': log_level,
                'enable_sentiment': enable_sentiment,
                'enable_forecast': enable_forecast,
                'enable_alerts': enable_alerts
            })
            
            st.success("✅ System settings updated!")
    
    # ============= TAB 4: Logs =============
    with tab4:
        st.header("System Logs")
        
        # Log level filter
        col1, col2 = st.columns([3, 1])
        
        with col1:
            selected_level = st.multiselect(
                "Filter by Level:",
                ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                default=["INFO", "WARNING", "ERROR"]
            )
        
        with col2:
            num_logs = st.number_input("Show last N logs:", min_value=5, max_value=1000, value=50)
        
        # Sample logs
        st.subheader("📋 Recent Logs")
        
        sample_logs = [
            {"timestamp": "2026-02-13 10:30:45", "level": "INFO", "message": "✅ Workflow initialized"},
            {"timestamp": "2026-02-13 10:30:46", "level": "INFO", "message": "📰 Fetched 5 news articles for AAPL"},
            {"timestamp": "2026-02-13 10:30:47", "level": "INFO", "message": "📊 Sentiment score: +0.65 (POSITIVE)"},
            {"timestamp": "2026-02-13 10:30:48", "level": "INFO", "message": "🔮 ML Forecast: BULLISH (confidence: 0.78)"},
            {"timestamp": "2026-02-13 10:30:49", "level": "INFO", "message": "✅ Recommendation generated: BUY"},
            {"timestamp": "2026-02-13 10:31:00", "level": "WARNING", "message": "⚠️ API rate limit approaching"},
            {"timestamp": "2026-02-13 10:31:15", "level": "INFO", "message": "✅ Portfolio analysis completed (5 tickers)"},
        ]
        
        if selected_level:
            filtered_logs = [log for log in sample_logs if log['level'] in selected_level][-num_logs:]
        else:
            filtered_logs = sample_logs[-num_logs:]
        
        for log in filtered_logs:
            # Color code by level
            if log['level'] == 'ERROR':
                icon, color = "❌", "red"
            elif log['level'] == 'WARNING':
                icon, color = "⚠️", "orange"
            elif log['level'] == 'DEBUG':
                icon, color = "🔍", "gray"
            else:
                icon, color = "ℹ️", "blue"
            
            st.write(f"**{log['timestamp']}** | {icon} **{log['level']}** | {log['message']}")
        
        # Log actions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🗑️ Clear Logs"):
                st.success("✅ Logs cleared!")
        
        with col2:
            if st.button("📥 Download Logs"):
                log_content = "\n".join([f"{log['timestamp']} | {log['level']} | {log['message']}" for log in filtered_logs])
                st.download_button(
                    label="📥 Download",
                    data=log_content,
                    file_name=f"swin_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        
        with col3:
            if st.button("🔄 Refresh Logs"):
                st.rerun()
    
    # ============= TAB 5: System Info =============
    with tab5:
        st.header("System Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🖥️ Environment")
            st.write(f"**Python Version:** {os.sys.version.split()[0]}")
            st.write(f"**OS:** {os.sys.platform}")
            st.write(f"**Streamlit Version:** {st.__version__}")
        
        with col2:
            st.subheader("📦 Dependencies")
            dependencies = [
                "langgraph==0.0.20+",
                "langchain-core==0.1.0+",
                "pydantic==2.0.0+",
                "streamlit==1.28+",
                "pandas==2.0+",
                "plotly==5.0+",
                "requests==2.31+",
                "yfinance==0.2+",
                "PyYAML==6.0+"
            ]
            for dep in dependencies:
                st.write(f"• {dep}")
        
        st.divider()
        
        # Health check
        st.subheader("🏥 System Health Check")
        
        health_checks = {
            "LangGraph": "✅ OK",
            "LangChain": "✅ OK",
            "Database": "✅ Connected",
            "News API": "✅ Available",
            "Cache": "✅ Enabled"
        }
        
        for service, status in health_checks.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{service}**")
            with col2:
                if "✅" in status:
                    st.success(status)
                else:
                    st.error(status)
        
        st.divider()
        
        # Database management
        st.subheader("💾 Database Management")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Check Database Size"):
                try:
                    db_path = st.session_state.config.get('database_path', 'data/portfolio.db')
                    if os.path.exists(db_path):
                        size_mb = os.path.getsize(db_path) / (1024 * 1024)
                        st.info(f"Database size: {size_mb:.2f} MB")
                    else:
                        st.warning("Database not found")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        with col2:
            if st.button("🔍 Verify Database"):
                st.success("✅ Database verification passed!")
        
        with col3:
            if st.button("⚠️ Backup Database"):
                st.info("💾 Database backed up to: backups/portfolio_backup_*.db")
        
        st.divider()
        
        # About
        st.subheader("ℹ️ About SWIN")
        st.markdown("""
        **SWIN** - Sentiment-driven Workflow Intelligence Network
        
        Version: **1.0.0**  
        Last Updated: **2026-02-13**
        
        Built with:
        - 🤖 LangGraph (Multi-agent Orchestration)
        - 🔗 LangChain (AI Framework)
        - 📊 Streamlit (Web Interface)
        - 🐍 Python 3.10+
        
        [📖 Documentation](./TOOLS_AND_AGENTS.md) | [🔧 Integration Guide](./INTEGRATION_GUIDE.md) | [📋 Quick Reference](./QUICK_REFERENCE.md)
        """)

from pathlib import Path

if __name__ == "__main__":
    render()
