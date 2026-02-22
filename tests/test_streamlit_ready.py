"""
Test script để kiểm tra Streamlit app có chạy ổn không
Chạy trước khi start Streamlit để đảm bảo no errors
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test tất cả imports cần thiết"""
    print("="*70)
    print("TEST 1: Kiểm tra imports...")
    print("="*70)
    
    try:
        import streamlit as st
        print("✅ streamlit imported successfully")
    except ImportError as e:
        print(f"❌ streamlit import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import plotly.graph_objects as go
        print("✅ plotly imported successfully")
    except ImportError as e:
        print(f"❌ plotly import failed: {e}")
        return False
    
    try:
        from orchestrators.langgraph_workflow import run_workflow, build_workflow_graph
        print("✅ langgraph_workflow imported successfully")
    except ImportError as e:
        print(f"❌ langgraph_workflow import failed: {e}")
        print(f"   Make sure you're in the project root directory")
        return False
    
    try:
        from tools.search_tool import SearchNewsTool
        print("✅ SearchNewsTool imported successfully")
    except ImportError as e:
        print(f"⚠️  SearchNewsTool import failed: {e} (optional)")
    
    try:
        from tools.database_tool import DatabaseTool
        print("✅ DatabaseTool imported successfully")
    except ImportError as e:
        print(f"⚠️  DatabaseTool import failed: {e} (optional)")
    
    print("\n✅ All critical imports successful!\n")
    return True


def test_workflow():
    """Test workflow có chạy được không"""
    print("="*70)
    print("TEST 2: Kiểm tra workflow...")
    print("="*70)
    
    try:
        from orchestrators.langgraph_workflow import run_workflow
        
        print("Chạy test workflow với mock data...")
        result = run_workflow(
            query="Test AAPL stock",
            verbose=False,
            user_id="test_user",
            risk_tolerance="medium",
            investment_horizon="medium_term",
            investment_amount=10000.0
        )
        
        # Check result structure
        assert 'recommendation' in result, "Missing recommendation in result"
        assert 'sentiment_score' in result, "Missing sentiment_score in result"
        
        rec = result['recommendation']
        assert 'action' in rec, "Missing action in recommendation"
        assert 'confidence' in rec, "Missing confidence in recommendation"
        assert 'recommended_amount' in rec, "Missing recommended_amount in recommendation"
        assert 'user_context' in rec, "Missing user_context in recommendation"
        
        print(f"\n✅ Workflow test passed!")
        print(f"   Action: {rec['action']}")
        print(f"   Confidence: {rec['confidence']:.1%}")
        print(f"   Recommended Amount: ${rec['recommended_amount']:,.2f}")
        print(f"   User Risk: {rec['user_context'].get('risk_tolerance', 'N/A')}")
        print()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_user_interface():
    """Test user_interface có load được không"""
    print("="*70)
    print("TEST 3: Kiểm tra user_interface...")
    print("="*70)
    
    try:
        from pages import user_interface
        print("✅ user_interface imported successfully")
        
        # Check if render function exists
        assert hasattr(user_interface, 'render'), "Missing render function"
        print("✅ render function exists")
        
        print("\n✅ User interface test passed!\n")
        return True
        
    except Exception as e:
        print(f"\n❌ User interface test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_file_structure():
    """Test cấu trúc file có đúng không"""
    print("="*70)
    print("TEST 4: Kiểm tra cấu trúc file...")
    print("="*70)
    
    required_files = [
        'streamlit_app.py',
        'pages/user_interface.py',
        'pages/admin_interface.py',
        'orchestrators/langgraph_workflow.py',
        'services/llm_service.py',
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} NOT FOUND")
            all_exist = False
    
    if all_exist:
        print("\n✅ File structure test passed!\n")
    else:
        print("\n⚠️  Some files are missing (may cause issues)\n")
    
    return all_exist


def test_env_variables():
    """Test environment variables"""
    print("="*70)
    print("TEST 5: Kiểm tra environment variables...")
    print("="*70)
    
    openai_key = os.getenv('OPENAI_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if openai_key:
        print(f"✅ OPENAI_API_KEY found (length: {len(openai_key)})")
    else:
        print("⚠️  OPENAI_API_KEY not found")
    
    if gemini_key:
        print(f"✅ GEMINI_API_KEY found (length: {len(gemini_key)})")
    else:
        print("⚠️  GEMINI_API_KEY not found")
    
    if openai_key or gemini_key:
        print("\n✅ At least one API key is configured!\n")
        return True
    else:
        print("\n⚠️  No API keys found (workflow may fail)\n")
        return False


def run_all_tests():
    """Chạy tất cả tests"""
    print("\n" + "="*70)
    print("🧪 STREAMLIT APP PRE-FLIGHT TESTS")
    print("="*70 + "\n")
    
    tests = [
        ("Imports", test_imports),
        ("File Structure", test_file_structure),
        ("Environment", test_env_variables),
        ("User Interface", test_user_interface),
        ("Workflow", test_workflow),
    ]
    
    results = {}
    
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"❌ {name} test crashed: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    for name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{name:20s}: {status}")
    
    print("="*70)
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED! Streamlit app should run fine.")
        print("\n👉 Run: streamlit run streamlit_app.py")
    else:
        failed = [name for name, passed in results.items() if not passed]
        print(f"\n⚠️  Some tests failed: {', '.join(failed)}")
        print("Please fix the issues before running streamlit.")
    
    print()
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
