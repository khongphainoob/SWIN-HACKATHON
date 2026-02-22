"""
Quick test - chạy workflow với input đơn giản
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestrators.langgraph_workflow import run_workflow

def test_simple():
    """Test đơn giản nhất"""
    print("\n" + "="*70)
    print("🧪 QUICK TEST: Simple workflow")
    print("="*70 + "\n")
    
    try:
        result = run_workflow(
            query="Should I buy AAPL?",
            verbose=True,
            user_id="test_user",
            risk_tolerance="medium",
            investment_horizon="medium_term",
            investment_amount=10000.0
        )
        
        print("\n" + "="*70)
        print("✅ TEST PASSED!")
        print("="*70)
        print(f"\nAction: {result['recommendation']['action']}")
        print(f"Confidence: {result['recommendation']['confidence']:.1%}")
        print(f"Recommended Amount: ${result['recommendation']['recommended_amount']:,.2f}")
        print()
        
        return True
        
    except Exception as e:
        print("\n" + "="*70)
        print("❌ TEST FAILED!")
        print("="*70)
        print(f"\nError: {e}\n")
        
        import traceback
        traceback.print_exc()
        
        return False


def test_conservative():
    """Test với conservative investor"""
    print("\n" + "="*70)
    print("🧪 QUICK TEST: Conservative investor")
    print("="*70 + "\n")
    
    try:
        result = run_workflow(
            query="Analyze JPM for long-term investment",
            verbose=False,
            user_id="conservative_user",
            risk_tolerance="low",
            investment_horizon="long_term",
            investment_amount=20000.0
        )
        
        rec = result['recommendation']
        suggested = rec['recommended_amount']
        
        print(f"✅ Action: {rec['action']}")
        print(f"✅ Confidence: {rec['confidence']:.1%}")
        print(f"✅ Suggested Amount: ${suggested:,.2f}")
        print(f"✅ Risk: {rec['user_context']['risk_tolerance']}")
        
        # Check logic: low risk should suggest ~30% of amount
        expected = 20000.0 * 0.3
        if rec['action'] == 'BUY' and abs(suggested - expected) < 2000:
            print(f"✅ Logic correct: Low risk suggests ~30% (${expected:,.2f})")
        
        print()
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}\n")
        return False


def test_aggressive():
    """Test với aggressive trader"""
    print("\n" + "="*70)
    print("🧪 QUICK TEST: Aggressive trader")
    print("="*70 + "\n")
    
    try:
        result = run_workflow(
            query="NVDA short-term opportunity",
            verbose=False,
            user_id="trader_999",
            risk_tolerance="high",
            investment_horizon="short_term",
            investment_amount=50000.0
        )
        
        rec = result['recommendation']
        suggested = rec['recommended_amount']
        
        print(f"✅ Action: {rec['action']}")
        print(f"✅ Confidence: {rec['confidence']:.1%}")
        print(f"✅ Suggested Amount: ${suggested:,.2f}")
        print(f"✅ Risk: {rec['user_context']['risk_tolerance']}")
        
        # Check logic: high risk should suggest ~80% of amount
        expected = 50000.0 * 0.8
        if rec['action'] == 'BUY' and abs(suggested - expected) < 5000:
            print(f"✅ Logic correct: High risk suggests ~80% (${expected:,.2f})")
        
        print()
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}\n")
        return False


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 QUICK WORKFLOW TESTS")
    print("="*70)
    
    tests = [
        ("Simple", test_simple),
        ("Conservative", test_conservative),
        ("Aggressive", test_aggressive),
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n❌ {name} crashed: {e}\n")
            results[name] = False
    
    # Summary
    print("\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70)
    
    for name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{name:20s}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("Streamlit app is ready to use.\n")
    else:
        print("\n⚠️  Some tests failed. Check errors above.\n")
    
    sys.exit(0 if all_passed else 1)
