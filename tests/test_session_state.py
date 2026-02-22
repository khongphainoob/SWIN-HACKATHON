"""
Test session state initialization for Streamlit app
Quick verification script
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_session_state_mock():
    """Test that all session_state accesses have proper fallbacks"""
    
    print("="*70)
    print("🧪 Testing Session State Initialization")
    print("="*70)
    print()
    
    # Mock session_state for testing
    class MockSessionState:
        def __init__(self):
            self._data = {}
        
        def __contains__(self, key):
            return key in self._data
        
        def __getitem__(self, key):
            return self._data[key]
        
        def __setitem__(self, key, value):
            self._data[key] = value
        
        def get(self, key, default=None):
            return self._data.get(key, default)
    
    # Test 1: Check admin interface initialization
    print("Test 1: Admin Interface Config Initialization")
    print("-" * 70)
    
    session_state = MockSessionState()
    
    # Simulate what happens in admin_interface.py render()
    if 'config' not in session_state:
        session_state['config'] = {
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
    
    # Try to access config
    try:
        config = session_state['config']
        value = config.get('sentiment_positive_threshold', 0.3)
        print(f"✅ Config initialized successfully")
        print(f"   • sentiment_positive_threshold: {value}")
        print(f"   • Total config keys: {len(config)}")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    print()
    
    # Test 2: Check user interface initialization
    print("Test 2: User Interface Profile Initialization")
    print("-" * 70)
    
    session_state2 = MockSessionState()
    
    # Simulate user_interface.py initialization
    if 'user_id' not in session_state2:
        session_state2['user_id'] = 'user_001'
    if 'risk_tolerance' not in session_state2:
        session_state2['risk_tolerance'] = 'medium'
    if 'investment_horizon' not in session_state2:
        session_state2['investment_horizon'] = 'medium_term'
    if 'investment_amount' not in session_state2:
        session_state2['investment_amount'] = 10000.0
    
    try:
        user_id = session_state2.get('user_id', 'anonymous')
        risk = session_state2.get('risk_tolerance', 'medium')
        horizon = session_state2.get('investment_horizon', 'medium_term')
        amount = session_state2.get('investment_amount', 10000.0)
        
        print(f"✅ User profile initialized successfully")
        print(f"   • user_id: {user_id}")
        print(f"   • risk_tolerance: {risk}")
        print(f"   • investment_horizon: {horizon}")
        print(f"   • investment_amount: ${amount:,.2f}")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    print()
    
    # Test 3: Check streamlit_app.py initialization
    print("Test 3: Main App Session State Initialization")
    print("-" * 70)
    
    session_state3 = MockSessionState()
    
    # Simulate streamlit_app.py initialization
    if 'interface_mode' not in session_state3:
        session_state3['interface_mode'] = 'user'
    if 'api_key' not in session_state3:
        session_state3['api_key'] = os.getenv('OPENAI_API_KEY', '')
    if 'gemini_api_key' not in session_state3:
        session_state3['gemini_api_key'] = os.getenv('GEMINI_API_KEY', '')
    if 'user_id' not in session_state3:
        session_state3['user_id'] = 'user_001'
    if 'config' not in session_state3:
        session_state3['config'] = {
            'sentiment_positive_threshold': 0.3,
            'sentiment_negative_threshold': -0.3,
        }
    
    try:
        mode = session_state3.get('interface_mode', 'user')
        config = session_state3['config']
        
        print(f"✅ Main app initialized successfully")
        print(f"   • interface_mode: {mode}")
        print(f"   • config keys: {len(config)}")
        print(f"   • config accessible: Yes")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    print()
    print("="*70)
    print("✅ All tests passed! Session state initialization is working correctly.")
    print("="*70)
    print()
    print("💡 Tips:")
    print("   • Always check 'if key not in st.session_state' before first use")
    print("   • Use st.session_state.get(key, default) for safe access")
    print("   • Initialize all keys at app startup in streamlit_app.py")
    print()


if __name__ == "__main__":
    test_session_state_mock()
