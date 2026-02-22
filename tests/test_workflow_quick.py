#!/usr/bin/env python
"""
Quick test script for langgraph_workflow.py
Run: python test_workflow_quick.py
"""

import sys
import time
from typing import Dict, Any

def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"🔍 {title}")
    print("=" * 60)

def print_result(label: str, value: Any, success=True):
    """Print formatted result"""
    icon = "✅" if success else "❌"
    print(f"{icon} {label}: {value}")

def print_section(title):
    """Print section separator"""
    print(f"\n📌 {title}")
    print("-" * 40)

# ============================================================================
# TEST 1: IMPORTS
# ============================================================================
def test_imports():
    print_header("TEST 1: Checking Imports")
    
    try:
        from orchestrators.langgraph_workflow import (
            build_workflow_graph,
            create_initial_state,
            InputAgent,
            SentimentAnalyzerAgent,
            MarketDataAgent,
            RiskAlertAgent,
            MLForecastAgent,
            LLMReasoningAgent,
            RecommendationAgent,
            WorkflowState
        )
        print_result("Imports", "All modules loaded", True)
        return True
    except Exception as e:
        print_result("Imports", f"Failed: {e}", False)
        return False

# ============================================================================
# TEST 2: STATE CREATION
# ============================================================================
def test_state_creation():
    print_header("TEST 2: State Creation")
    
    try:
        from orchestrators.langgraph_workflow import create_initial_state
        
        state = create_initial_state("What about Apple stock?")
        
        print_section("State Contents")
        print(f"  user_query: {state.get('user_query')}")
        print(f"  ticker: {state.get('ticker')}")
        print(f"  timestamp: {state.get('timestamp')}")
        print(f"  messages: {len(state.get('messages', []))} items")
        
        print_result("State Creation", "Successful", True)
        return True
    except Exception as e:
        print_result("State Creation", f"Failed: {e}", False)
        return False

# ============================================================================
# TEST 3: GRAPH BUILDING
# ============================================================================
def test_graph_building():
    print_header("TEST 3: Building Workflow Graph")
    
    try:
        from orchestrators.langgraph_workflow import build_workflow_graph
        
        start = time.time()
        graph = build_workflow_graph()
        elapsed = time.time() - start
        
        print_result("Graph Build Time", f"{elapsed:.3f}s", True)
        print_result("Graph Type", str(type(graph).__name__), True)
        
        return True
    except Exception as e:
        print_result("Graph Building", f"Failed: {e}", False)
        return False

# ============================================================================
# TEST 4: SINGLE TICKER ANALYSIS
# ============================================================================
def test_single_ticket():
    print_header("TEST 4: Single Ticker Analysis - AAPL")
    
    try:
        from orchestrators.langgraph_workflow import (
            build_workflow_graph,
            create_initial_state
        )
        
        graph = build_workflow_graph()
        state = create_initial_state("Analyze AAPL")
        
        print_section("Running Analysis")
        start = time.time()
        result = graph.invoke(state)
        elapsed = time.time() - start
        
        print_section("Results")
        print(f"  ⏱️  Time: {elapsed:.2f}s")
        
        # Recommendation
        rec = result.get('recommendation', {})
        print(f"  🎯 Action: {rec.get('action')} ({rec.get('confidence'):.0%} confidence)")
        
        # Sentiment
        sentiment = result.get('sentiment_score', 0)
        sentiment_label = result.get('sentiment_label', 'unknown')
        print(f"  📊 Sentiment: {sentiment:.2f} ({sentiment_label})")
        
        # Current step
        print(f"  👣 Final Step: {result.get('current_step')}")
        
        # Messages count
        print(f"  📝 Messages: {len(result.get('messages', []))} entries")
        
        print_result("Single Ticker Analysis", "Successful", True)
        return True
    except Exception as e:
        print_result("Single Ticker Analysis", f"Failed: {e}", False)
        import traceback
        traceback.print_exc()
        return False

# ============================================================================
# TEST 5: MULTIPLE TICKERS
# ============================================================================
def test_multiple_tickers():
    print_header("TEST 5: Batch Analysis - Multiple Tickers")
    
    try:
        from orchestrators.langgraph_workflow import (
            build_workflow_graph,
            create_initial_state
        )
        
        tickers = ["AAPL", "MSFT", "GOOGL", "NVDA"]
        graph = build_workflow_graph()
        
        print_section("Analyzing Tickers")
        results_summary = {}
        start = time.time()
        
        for i, ticker in enumerate(tickers, 1):
            print(f"  [{i}/{len(tickers)}] {ticker}...", end=" ")
            
            state = create_initial_state(f"Analyze {ticker}")
            result = graph.invoke(state)
            
            action = result['recommendation']['action']
            confidence = result['recommendation']['confidence']
            results_summary[ticker] = action
            
            print(f"→ {action} ({confidence:.0%})")
        
        elapsed = time.time() - start
        
        print_section("Batch Summary")
        buy_count = sum(1 for a in results_summary.values() if a == 'BUY')
        sell_count = sum(1 for a in results_summary.values() if a == 'SELL')
        hold_count = sum(1 for a in results_summary.values() if a == 'HOLD')
        
        print(f"  Total Time: {elapsed:.2f}s ({elapsed/len(tickers):.2f}s per ticker)")
        print(f"  🟢 BUY: {buy_count}")
        print(f"  🔴 SELL: {sell_count}")
        print(f"  🟡 HOLD: {hold_count}")
        
        print_result("Batch Analysis", "Successful", True)
        return True
    except Exception as e:
        print_result("Batch Analysis", f"Failed: {e}", False)
        import traceback
        traceback.print_exc()
        return False

# ============================================================================
# TEST 6: OUTPUT STRUCTURE VALIDATION
# ============================================================================
def test_output_structure():
    print_header("TEST 6: Output Structure Validation")
    
    try:
        from orchestrators.langgraph_workflow import (
            build_workflow_graph,
            create_initial_state
        )
        
        graph = build_workflow_graph()
        state = create_initial_state("Analyze MSFT")
        result = graph.invoke(state)
        
        print_section("Checking Required Fields")
        
        required_fields = {
            'recommendation': dict,
            'sentiment_score': float,
            'sentiment_label': str,
            'current_step': str,
            'timestamp': str,
            'messages': list
        }
        
        all_valid = True
        for field, expected_type in required_fields.items():
            value = result.get(field)
            if value is None:
                print_result(f"Field: {field}", "MISSING", False)
                all_valid = False
            elif not isinstance(value, expected_type):
                print_result(f"Field: {field}", f"Wrong type (got {type(value).__name__})", False)
                all_valid = False
            else:
                print_result(f"Field: {field}", f"{type(value).__name__} ✓", True)
        
        print_section("Recommendation Structure")
        rec = result.get('recommendation', {})
        rec_fields = ['action', 'confidence', 'reasoning', 'urgency']
        
        for field in rec_fields:
            if field in rec:
                print_result(f"  {field}", str(rec[field])[:50], True)
            else:
                print_result(f"  {field}", "MISSING", False)
                all_valid = False
        
        print_result("Output Structure", "Valid" if all_valid else "Invalid", all_valid)
        return all_valid
    except Exception as e:
        print_result("Output Structure", f"Failed: {e}", False)
        return False

# ============================================================================
# TEST 7: PERFORMANCE CHECK
# ============================================================================
def test_performance():
    print_header("TEST 7: Performance Check")
    
    try:
        from orchestrators.langgraph_workflow import (
            build_workflow_graph,
            create_initial_state
        )
        
        graph = build_workflow_graph()
        
        print_section("Timing Single Analysis")
        state = create_initial_state("Analyze TSLA")
        
        times = []
        for i in range(3):
            start = time.time()
            result = graph.invoke(state)
            elapsed = time.time() - start
            times.append(elapsed)
            print(f"  Run {i+1}: {elapsed:.2f}s")
        
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print_section("Performance Metrics")
        print(f"  Average: {avg_time:.2f}s")
        print(f"  Min: {min_time:.2f}s")
        print(f"  Max: {max_time:.2f}s")
        
        # Performance criteria
        if avg_time < 5:
            status = "Excellent 🚀"
        elif avg_time < 10:
            status = "Good ✅"
        elif avg_time < 20:
            status = "Acceptable ⚠️"
        else:
            status = "Slow 🐢"
        
        print(f"  Status: {status}")
        
        print_result("Performance", f"Avg {avg_time:.2f}s", avg_time < 10)
        return True
    except Exception as e:
        print_result("Performance", f"Failed: {e}", False)
        return False

# ============================================================================
# MAIN TEST RUNNER
# ============================================================================
def main():
    print("\n" + "🧪 WORKFLOW QUICK TEST SUITE 🧪".center(60, "="))
    
    tests = [
        ("Import Check", test_imports),
        ("State Creation", test_state_creation),
        ("Graph Building", test_graph_building),
        ("Single Ticker", test_single_ticket),
        ("Multiple Tickers", test_multiple_tickers),
        ("Output Structure", test_output_structure),
        ("Performance", test_performance),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print_header(f"ERROR in {name}")
            print_result(name, f"Crashed: {e}", False)
            results.append((name, False))
    
    # FINAL SUMMARY
    print_header("📊 TEST SUMMARY")
    
    print_section("Results")
    for name, result in results:
        icon = "✅" if result else "❌"
        status = "PASS" if result else "FAIL"
        print(f"  {icon} {name}: {status}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print_section("Statistics")
    print(f"  Passed: {passed}/{total} ({percentage:.0f}%)")
    
    if passed == total:
        print("\n" + "🎉 ALL TESTS PASSED! 🎉".center(60, "="))
        return 0
    else:
        print("\n" + f"⚠️  {total - passed} TEST(S) FAILED".center(60, "="))
        return 1

if __name__ == "__main__":
    sys.exit(main())
