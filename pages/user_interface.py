"""
User Interface - Stock Analysis and Recommendations
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import sys
import os
from typing import List, Dict, Any, Optional, Union

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrators.langgraph_workflow import LLM, build_workflow_graph, create_initial_state,run_workflow
from tools.search_tool import SearchNewsTool
from tools.database_tool import DatabaseTool
from tools.function_tools.summarize_tool import SummarizeTool
from utils.asset_mapping import search_company, get_asset_info, format_asset_name, POPULAR_ASSETS

def render():
    """Render user interface."""
    
    # Initialize session state variables if not exists
    if 'user_id' not in st.session_state:
        st.session_state.user_id = 'user_001'
    if 'risk_tolerance' not in st.session_state:
        st.session_state.risk_tolerance = 'medium'
    if 'investment_horizon' not in st.session_state:
        st.session_state.investment_horizon = 'medium_term'
    if 'investment_amount' not in st.session_state:
        st.session_state.investment_amount = 10000.0
    
    st.markdown('<div class="main-title">📊 Multi-Asset Intelligence Analyzer</div>', unsafe_allow_html=True)
    st.markdown("Analyze stocks, crypto, commodities & forex with AI-powered recommendations")
    
    # User Profile Sidebar
    with st.sidebar.expander("👤 User Profile", expanded=False):
        st.subheader("Investment Profile")
        
        user_id = st.text_input(
            "User ID:",
            value=st.session_state.get('user_id', 'user_001'),
            help="Unique identifier for your profile"
        )
        st.session_state.user_id = user_id
        
        risk_tolerance = st.select_slider(
            "Risk Tolerance:",
            options=["low", "medium", "high"],
            value=st.session_state.get('risk_tolerance', 'medium'),
            help="Low: Conservative, Medium: Balanced, High: Aggressive"
        )
        st.session_state.risk_tolerance = risk_tolerance
        
        investment_horizon = st.selectbox(
            "Investment Horizon:",
            options=["short_term", "medium_term", "long_term"],
            index=["short_term", "medium_term", "long_term"].index(st.session_state.get('investment_horizon', 'medium_term')),
            help="Short: < 1 year, Medium: 1-5 years, Long: > 5 years"
        )
        st.session_state.investment_horizon = investment_horizon
        
        investment_amount = st.number_input(
            "Investment Amount ($):",
            min_value=100.0,
            max_value=1000000.0,
            value=st.session_state.get('investment_amount', 10000.0),
            step=1000.0,
            help="Amount you plan to invest"
        )
        st.session_state.investment_amount = investment_amount
        
        # Display summary
        st.markdown("---")
        st.markdown("**Profile Summary:**")
        risk_emoji = "🟢" if risk_tolerance == "low" else "🟡" if risk_tolerance == "medium" else "🔴"
        st.markdown(f"**Risk:** {risk_emoji} {risk_tolerance.upper()}")
        st.markdown(f"**Horizon:** {investment_horizon.replace('_', ' ').title()}")
        st.markdown(f"**Amount:** ${investment_amount:,.2f}")
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Asset Analysis",
        "📈 Portfolio Analysis",
        "📰 News & Sentiment",
        "💼 My Portfolio"
    ])
    
    # ============= TAB 1: Single Stock Analysis =============
    with tab1:
        st.header("Investment Analysis")
        
        # Asset Type Selector
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            asset_type = st.selectbox(
                "Asset Type:",
                options=[
                    "📈 Stock (Cổ phiếu)",
                    "₿ Crypto (Tiền ảo)",
                    "🥇 Commodity (Hàng hóa)",
                    "💱 Forex (Ngoại hối)"
                ],
                help="Chọn loại tài sản muốn phân tích"
            )
            
            # Extract asset type code
            asset_code = asset_type.split()[0].replace("📈", "stock").replace("₿", "crypto").replace("🥇", "commodity").replace("💱", "forex")
        
        with col2:
            # Input method based on asset type
            if "Stock" in asset_type:
                input_method = st.radio(
                    "Input method:",
                    options=["Ticker Symbol", "Company Name"],
                    horizontal=True,
                    help="Chọn cách nhập"
                )
            else:
                input_method = "Ticker Symbol"
        
        # Input field
        if "Stock" in asset_type and input_method == "Company Name":
            company_name = st.text_input(
                "Enter Company Name:",
                value="Apple",
                placeholder="e.g., Apple, Microsoft, NVIDIA, JP Morgan",
                help="Nhập tên công ty - hỗ trợ 50+ công ty lớn"
            )
            
            # Convert company name to ticker using utility
            ticker = search_company(company_name)
            
            # Show detected ticker with icon
            asset_info = get_asset_info(ticker)
            st.caption(f"🔍 Detected: **{ticker}** ({asset_info['name']})")
            
        elif "Crypto" in asset_type:
            # Build options from POPULAR_ASSETS
            crypto_options = [f"{t} ({n} {i})" for t, n, i in POPULAR_ASSETS["crypto"]]
            selected_crypto = st.selectbox(
                "Select Cryptocurrency:",
                options=crypto_options,
                help="Chọn crypto muốn phân tích"
            )
            ticker = selected_crypto.split()[0]  # Get ticker part only
            
        elif "Commodity" in asset_type:
            commodity_options = [f"{t} ({n} {i})" for t, n, i in POPULAR_ASSETS["commodity"]]
            selected_commodity = st.selectbox(
                "Select Commodity:",
                options=commodity_options,
                help="Chọn hàng hóa muốn phân tích"
            )
            ticker = selected_commodity.split()[0]
            
        elif "Forex" in asset_type:
            forex_options = [f"{t} ({n} {i})" for t, n, i in POPULAR_ASSETS["forex"]]
            selected_forex = st.selectbox(
                "Select Currency Pair:",
                options=forex_options,
                help="Chọn cặp tiền tệ"
            )
            ticker = selected_forex.split()[0]
            
        else:
            ticker = st.text_input(
                "Enter Ticker Symbol:",
                value="AAPL",
                placeholder="e.g., AAPL, MSFT, NVDA",
                help="Nhập mã ticker (1-5 chữ cái)"
            ).upper()
        
        with col3:
            st.write("")  # Spacing
            st.write("")  # Spacing
            analyze_button = st.button("🚀 Analyze", use_container_width=True)
        
        if analyze_button and ticker:
            print(f"Analyzing {ticker}...")
            with st.spinner(f"🔄 Analyzing {ticker}..."):
                try:
                    # Get user context from session
                    user_id = st.session_state.get('user_id', 'anonymous')
                    risk_tolerance = st.session_state.get('risk_tolerance', 'medium')
                    investment_horizon = st.session_state.get('investment_horizon', 'medium_term')
                    investment_amount = st.session_state.get('investment_amount', 10000.0)
                    
                    # Build graph and analyze
                    print("Running workflow...")
                    result = run_workflow(
                        query=f"Analyze {ticker} stock performance and provide investment recommendation.",
                        verbose=False,
                        user_id=user_id,
                        risk_tolerance=risk_tolerance,
                        investment_horizon=investment_horizon,
                        investment_amount=investment_amount
                    )
                    
                    # Extract recommendation
                    rec = result['recommendation']
                    sentiment = result.get('sentiment_score', 0)
                    
                    # Display recommendation card
                    col1, col2, col3, col4 = st.columns(4)
                    
                    # Color coding for action
                    action_color = "🟢" if rec['action'] == 'BUY' else "🔴" if rec['action'] == 'SELL' else "🟡"
                    
                    with col1:
                        st.metric(
                            "Recommendation",
                            f"{action_color} {rec['action']}",
                            help=f"Action: {rec['action']}"
                        )
                    
                    with col2:
                        confidence_pct = f"{rec['confidence']:.0%}"
                        st.metric(
                            "Confidence",
                            confidence_pct,
                            help=f"Model confidence: {confidence_pct}"
                        )
                    
                    with col3:
                        sentiment_label = "Positive" if sentiment > 0.2 else "Negative" if sentiment < -0.2 else "Neutral"
                        st.metric(
                            "Sentiment",
                            f"{sentiment:.2f}",
                            delta=sentiment_label,
                            help=f"Sentiment score: {sentiment:.2f}"
                        )
                    
                    with col4:
                        recommended_amt = rec.get('recommended_amount', 0)
                        st.metric(
                            "💰 Suggested Amount",
                            f"${recommended_amt:,.0f}",
                            help=f"Based on your profile and risk tolerance"
                        )
                    
                    # Detailed analysis
                    st.divider()
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.subheader("📋 Analysis Details")
                        
                        analysis_data = rec.get('analysis', {})
                        user_ctx = rec.get('user_context', {})
                        
                        analysis_col1, analysis_col2 = st.columns(2)
                        
                        with analysis_col1:
                            st.write(f"**Current Price:** ${analysis_data.get('current_price', 'N/A')}")
                            st.write(f"**Forecast:** {analysis_data.get('forecast', {}).get('trend', 'N/A')}")
                            st.write(f"**Your Risk:** {user_ctx.get('risk_tolerance', 'N/A').upper()}")
                        
                        with analysis_col2:
                            st.write(f"**Alerts:** {analysis_data.get('alerts_count', 0)}")
                            st.write(f"**Your Horizon:** {user_ctx.get('investment_horizon', 'N/A').replace('_', ' ').title()}")
                            st.write(f"**Holdings:** {user_ctx.get('portfolio_holdings', 0)} stocks")
                    
                    with col2:
                        st.subheader("🎯 Urgency")
                        urgency_color = "🔴" if rec.get('urgency') == 'High' else "🟡" if rec.get('urgency') == 'Medium' else "🟢"
                        st.write(f"{urgency_color} **{rec.get('urgency', 'Unknown')}**")
                    
                    # Reasoning
                    st.subheader("💡 Reasoning")
                    for i, reason in enumerate(rec.get('reasoning', []), 1):
                        st.write(f"{i}. {reason}")
                    
                    # Store recommendation in session
                    st.session_state.last_analysis = {
                        'ticker': ticker,
                        'recommendation': rec,
                        'sentiment': sentiment,
                        'timestamp': datetime.now()
                    }
                    
                    # Success message
                    st.markdown(
                        f'<div class="success-box">✅ Analysis completed successfully!</div>',
                        unsafe_allow_html=True
                    )
                
                except Exception as e:
                    st.error(f"❌ Error analyzing {ticker}: {str(e)}")
    # ============= TAB 2: Portfolio Analysis =============
    with tab2:
        st.header("Portfolio Analysis")
        
        # Input tickers
        tickers_input = st.text_area(
            "Enter Stock Tickers (comma-separated):",
            value="AAPL, MSFT, GOOGL, NVDA, TSLA",
            help="Enter ticker symbols separated by commas"
        )
        
        col1, col2 = st.columns([4, 1])
        
        with col2:
            analyze_portfolio_button = st.button("📊 Analyze Portfolio", use_container_width=True)
        
        if analyze_portfolio_button and tickers_input:
            tickers = [t.strip().upper() for t in tickers_input.split(',') if t.strip()]
            
            with st.spinner(f"🔄 Analyzing {len(tickers)} stocks..."):
                try:
        
                    results = []
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for i, ticker in enumerate(tickers):
                        status_text.text(f"Analyzing {ticker}... ({i+1}/{len(tickers)})")
                        
                        try:
                            # Get user context
                            user_id = st.session_state.get('user_id', 'anonymous')
                            risk_tolerance = st.session_state.get('risk_tolerance', 'medium')
                            investment_horizon = st.session_state.get('investment_horizon', 'medium_term')
                            investment_amount = st.session_state.get('investment_amount', 10000.0)
                            
                            result = run_workflow(
                                query=f"Analyze {ticker} stock performance and provide investment recommendation.",
                                verbose=False,
                                user_id=user_id,
                                risk_tolerance=risk_tolerance,
                                investment_horizon=investment_horizon,
                                investment_amount=investment_amount
                            )
                            rec = result['recommendation']
                            
                            results.append({
                                'Ticker': ticker,
                                'Action': rec['action'],
                                'Confidence': f"{rec['confidence']:.0%}",
                                'Urgency': rec.get('urgency', 'Unknown'),
                                'Sentiment': f"{result.get('sentiment_score', 0):.2f}"
                            })
                        except Exception as e:
                            results.append({
                                'Ticker': ticker,
                                'Action': 'ERROR',
                                'Confidence': '0%',
                                'Urgency': 'N/A',
                                'Sentiment': 'N/A'
                            })
                        
                        progress_bar.progress((i + 1) / len(tickers))
                    
                    status_text.empty()
                    
                    # Display results
                    df = pd.DataFrame(results)
                    
                    # Color code actions
                    def highlight_action(row):
                        if row['Action'] == 'BUY':
                            return ['background-color: lightgreen'] * len(row)
                        elif row['Action'] == 'SELL':
                            return ['background-color: lightcoral'] * len(row)
                        elif row['Action'] == 'HOLD':
                            return ['background-color: lightyellow'] * len(row)
                        else:
                            return ['background-color: lightgray'] * len(row)
                    
                    styled_df = df.style.apply(highlight_action, axis=1)
                    st.dataframe(styled_df, use_container_width=True)
                    
                    # Summary statistics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    buy_count = len(df[df['Action'] == 'BUY'])
                    sell_count = len(df[df['Action'] == 'SELL'])
                    hold_count = len(df[df['Action'] == 'HOLD'])
                    error_count = len(df[df['Action'] == 'ERROR'])
                    
                    with col1:
                        st.metric("🟢 Buy", buy_count)
                    with col2:
                        st.metric("🔴 Sell", sell_count)
                    with col3:
                        st.metric("🟡 Hold", hold_count)
                    with col4:
                        st.metric("⚠️ Errors", error_count)
                    
                    # Download results
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results",
                        data=csv,
                        file_name=f"portfolio_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                except Exception as e:
                    st.error(f"❌ Error analyzing portfolio: {str(e)}")
    
    # ============= TAB 3: News & Sentiment =============
    with tab3:
        st.header("News & Sentiment Analysis")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            news_ticker = st.text_input(
                "Stock Ticker:",
                value="AAPL",
                placeholder="Enter ticker symbol"
            ).upper()
        
        with col2:
            news_limit = st.number_input("Number of Articles:", min_value=1, max_value=20, value=5)
        
        with col3:
            fetch_news_button = st.button("📰 Fetch News", use_container_width=True)
        
        if fetch_news_button:
            with st.spinner(f"🔄 Fetching news for {news_ticker}..."):
                try:
                    search_tool = SearchNewsTool()
                    articles = search_tool.invoke({
                        "query": news_ticker,
                        "limit": news_limit
                    })
                    
                    if articles:
                        for i, article in enumerate(articles, 1):
                            with st.expander(f"📄 Article {i}: {article.get('title', 'No title')}", expanded=False):
                                col1, col2 = st.columns([3, 1])
                                
                                with col1:
                                    st.write(f"**Publisher:** {article.get('publisher', 'Unknown')}")
                                    st.write(f"**Date:** {article.get('published', 'Unknown')}")
                                
                                with col2:
                                    if article.get('link'):
                                        st.markdown(f"[🔗 Read Full Article]({article['link']})")
                                
                                # Try to get and summarize content
                                if article.get('content'):
                                    st.write("**Summary:**")
                                    try:
                                        summarize_tool = SummarizeTool()
                                        summary = summarize_tool.invoke({
                                            "text": article['content'],
                                            "max_sentences": 3
                                        })
                                        st.write(summary)
                                    except:
                                        st.write(article.get('content', 'Content not available')[:500] + "...")
                    else:
                        st.info(f"No articles found for {news_ticker}")
                
                except Exception as e:
                    st.error(f"❌ Error fetching news: {str(e)}")
    
    # ============= TAB 4: My Portfolio =============
    with tab4:
        st.header("💼 My Portfolio")
        
        # User ID
        user_id = st.text_input(
            "Your User ID:",
            value="user123",
            help="Unique identifier for your portfolio"
        )
        
        col1, col2, col3 = st.columns(3)
        
        # Add holding
        with col1:
            with st.form("add_holding_form"):
                st.subheader("➕ Add Holding")
                add_ticker = st.text_input("Ticker:", key="add_ticker").upper()
                add_shares = st.number_input("Shares:", min_value=0.01, step=0.01, key="add_shares")
                add_cost = st.number_input("Avg Cost ($):", min_value=0.01, step=0.01, key="add_cost")
                
                if st.form_submit_button("✅ Add"):
                    if add_ticker and add_shares > 0 and add_cost > 0:
                        try:
                            db = DatabaseTool()
                            db.invoke({
                                "action": "upsert",
                                "user_id": user_id,
                                "symbol": add_ticker,
                                "shares": add_shares,
                                "avg_cost": add_cost
                            })
                            st.success(f"✅ Added {add_shares} shares of {add_ticker}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
        
        # View portfolio
        with col2:
            if st.button("👁️ View Portfolio", use_container_width=True):
                try:
                    db = DatabaseTool()
                    holdings = db.invoke({
                        "action": "get",
                        "user_id": user_id
                    })
                    
                    if holdings:
                        st.session_state.portfolio_data = holdings
                        st.success(f"✅ Loaded {len(holdings)} holdings")
                    else:
                        st.info("📭 Portfolio is empty")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        with col3:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()
        
        st.divider()
        
        # Display portfolio
        if 'portfolio_data' in st.session_state and st.session_state.portfolio_data:
            df_portfolio = pd.DataFrame(st.session_state.portfolio_data)
            st.subheader("📊 Holdings")
            st.dataframe(df_portfolio, use_container_width=True)
            
            # Calculate totals
            total_invested = (df_portfolio['shares'] * df_portfolio['avg_cost']).sum()
            st.metric("Total Invested", f"${total_invested:,.2f}")
            
            # Analyze portfolio
            if st.button("📈 Analyze All Holdings"):
                tickers = df_portfolio['symbol'].tolist()
                tickers_str = ", ".join(tickers)
                with st.spinner(f"🔄 Analyzing portfolio...")  :    
                    st.session_state.tickers_to_analyze = tickers_str
                    result = run_workflow(f"Analyze the following stocks: {tickers_str} and provide investment recommendations.", verbose=False)    
                    st.subheader("📋 Portfolio Analysis Result")
                    st.text(result.get('summary', 'No summary available'))
                    st.markdown("---")
                    st.text("Detailed Alerts:")
                    for alert in result.get('alerts_generated', []):
                        st.write(alert)
                    st.text(f'Quality Report: {result.get("quality_report", {})}')
                    st.rerun()
        
        else:
            st.info("👆 Click 'View Portfolio' to see your holdings")
        

if __name__ == "__main__":
    render()
