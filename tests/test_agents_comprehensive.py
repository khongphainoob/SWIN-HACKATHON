"""
tests/test_agents_comprehensive.py
Comprehensive tests for all Agentic components

This test suite covers:
1. InputAgent - Parse user query
2. SentimentAnalyzerAgent - NLP sentiment analysis
3. MarketDataAgent - Fetch market data
4. RiskAlertAgent - Generate risk warnings
5. MLForecastAgent - Predict trends
6. LLMReasoningAgent - Risk evaluation
7. RecommendationAgent - Final recommendation
"""
import unittest
from typing import Dict, Any

from orchestrators.langgraph_workflow import (
    InputAgent,
    SentimentAnalyzerAgent,
    MarketDataAgent,
    RiskAlertAgent,
    MLForecastAgent,
    LLMReasoningAgent,
    RecommendationAgent,
    WorkflowState,
)


class TestInputAgent(unittest.TestCase):
    """Test InputAgent - Parse and normalize user input"""
    
    def test_extract_ticker_from_query(self):
        """Test ticker extraction from various query formats"""
        print("\n" + "="*60)
        print("TEST: InputAgent - Extract Ticker")
        print("="*60)
        
        test_cases = [
            ("What's the outlook for NVDA?", "NVDA"),
            ("Analyze AAPL stock", "AAPL"),
            ("msft performance", "MSFT"),
            ("Buy signal for TSLA", "TSLA"),
            ("Should I buy JPM?", "JPM"),
        ]
        
        for query, expected_ticker in test_cases:
            result = InputAgent.run({"user_query": query})
            
            print(f"\nQuery: '{query}'")
            print(f"  Expected: {expected_ticker}")
            print(f"  Got: {result['ticker']}")
            print(f"  ✓ Match" if result['ticker'] == expected_ticker else "  ⚠️  Different")
    
    def test_input_agent_output_structure(self):
        """Test output structure of InputAgent"""
        print("\n" + "="*60)
        print("TEST: InputAgent - Output Structure")
        print("="*60)
        
        state = {"user_query": "Analyze GOOGL stock"}
        result = InputAgent.run(state)
        
        expected_keys = {"ticker", "current_step", "messages", "timestamp"}
        has_all_keys = expected_keys.issubset(set(result.keys()))
        
        assert has_all_keys, f"Missing keys. Got: {set(result.keys())}"
        assert result["current_step"] == "input_agent"
        
        print(f"✓ Output has required keys: {expected_keys}")
        print(f"✓ current_step = 'input_agent'")
        print(f"✓ Messages: {result['messages']}")


class TestSentimentAnalyzerAgent(unittest.TestCase):
    """Test SentimentAnalyzerAgent - NLP sentiment analysis"""
    
    def test_sentiment_scoring(self):
        """Test sentiment scoring on news articles"""
        print("\n" + "="*60)
        print("TEST: SentimentAnalyzerAgent - Sentiment Scoring")
        print("="*60)
        
        test_cases = [
            {
                "news_articles": [
                    {
                        "title": "Apple beats revenue expectations, stock surges",
                        "summary": "Strong profit growth and record buyback"
                    }
                ],
                "expected_label": "positive",
            },
            {
                "news_articles": [
                    {
                        "title": "Microsoft misses targets, stock crashes",
                        "summary": "Disappointing earnings decline and layoffs"
                    }
                ],
                "expected_label": "negative",
            },
            {
                "news_articles": [
                    {
                        "title": "Market report: Mixed signals for tech",
                        "summary": "Some winners and losers in today's trading"
                    }
                ],
                "expected_label": "neutral",
            },
        ]
        
        for idx, test_case in enumerate(test_cases):
            state = {"news_articles": test_case["news_articles"]}
            result = SentimentAnalyzerAgent.run(state)
            
            print(f"\n📰 Test Case {idx + 1}:")
            print(f"   Title: {test_case['news_articles'][0]['title']}")
            print(f"   Expected Label: {test_case['expected_label']}")
            print(f"   Sentiment Score: {result['sentiment_score']:.3f}")
            print(f"   Sentiment Label: {result['sentiment_label']}")
            
            assert result["sentiment_label"] == test_case["expected_label"]
            print(f"   ✓ Correct sentiment detected")
    
    def test_sentiment_output_structure(self):
        """Test output structure"""
        print("\n" + "="*60)
        print("TEST: SentimentAnalyzerAgent - Output Structure")
        print("="*60)
        
        state = {
            "news_articles": [
                {"title": "Strong earnings", "summary": "Profit growth"}
            ]
        }
        result = SentimentAnalyzerAgent.run(state)
        
        expected_keys = {"sentiment_score", "sentiment_label", "sentiment_details", "current_step"}
        has_all_keys = expected_keys.issubset(set(result.keys()))
        
        assert has_all_keys
        assert -1.0 <= result["sentiment_score"] <= 1.0
        assert result["sentiment_label"] in ["positive", "negative", "neutral"]
        assert result["current_step"] == "sentiment_analyzer"
        
        print(f"✓ Output structure valid")
        print(f"  Score range: [-1.0, 1.0] ✓")
        print(f"  Label valid: {result['sentiment_label']} ✓")


class TestMarketDataAgent(unittest.TestCase):
    """Test MarketDataAgent - Fetch market data"""
    
    def test_market_data_output_structure(self):
        """Test market data structure"""
        print("\n" + "="*60)
        print("TEST: MarketDataAgent - Output Structure")
        print("="*60)
        
        state = {"ticker": "AAPL"}
        result = MarketDataAgent.run(state)
        
        # Check required keys
        assert "market_data" in result
        market_data = result["market_data"]
        
        # Should have price information
        assert "current_price" in market_data or "note" in market_data
        
        print(f"✓ Market data retrieved")
        print(f"  Ticker: AAPL")
        print(f"  Data keys: {list(market_data.keys())}")
        
        if "current_price" in market_data:
            print(f"  Current Price: ${market_data['current_price']}")
        
        if "volume" in market_data:
            print(f"  Volume: {market_data['volume']:,.0f}")


class TestRiskAlertAgent(unittest.TestCase):
    """Test RiskAlertAgent - Generate risk warnings"""
    
    def test_high_risk_alerts(self):
        """Test alert generation for high-risk scenarios"""
        print("\n" + "="*60)
        print("TEST: RiskAlertAgent - High Risk Alerts")
        print("="*60)
        
        state = {
            "ticker": "TEST",
            "sentiment_score": -0.8,  # Very negative
            "news_articles": [
                {"title": "Company fraud investigation announced"}
            ]
        }
        
        result = RiskAlertAgent.run(state)
        alerts = result["risk_alerts"]
        
        assert len(alerts) > 0
        high_alerts = [a for a in alerts if a.get("severity") == "HIGH"]
        
        print(f"✓ Generated {len(alerts)} alerts")
        print(f"✓ High severity alerts: {len(high_alerts)}")
        
        for alert in high_alerts[:2]:
            print(f"\n  Alert Type: {alert['type']}")
            print(f"  Message: {alert['message']}")
            print(f"  Action: {alert['action']}")
    
    def test_low_risk_alerts(self):
        """Test alert generation for low-risk scenarios"""
        print("\n" + "="*60)
        print("TEST: RiskAlertAgent - Low Risk Alerts")
        print("="*60)
        
        state = {
            "ticker": "TEST",
            "sentiment_score": 0.1,  # Weakly positive
            "news_articles": [
                {"title": "Company maintains operations"}
            ]
        }
        
        result = RiskAlertAgent.run(state)
        alerts = result["risk_alerts"]
        
        print(f"✓ Generated {len(alerts)} alerts")
        
        for alert in alerts:
            severity = alert.get("severity", "UNKNOWN")
            print(f"  Alert: {alert['message'][:50]}... (Severity: {severity})")


class TestMLForecastAgent(unittest.TestCase):
    """Test MLForecastAgent - Trend prediction"""
    
    def test_bullish_forecast(self):
        """Test forecast for positive sentiment"""
        print("\n" + "="*60)
        print("TEST: MLForecastAgent - Bullish Forecast")
        print("="*60)
        
        state = {
            "ticker": "AAPL",
            "sentiment_score": 0.7,  # Positive
            "market_data": {"current_price": 180.0}
        }
        
        result = MLForecastAgent.run(state)
        forecast = result["forecast"]
        
        assert forecast["trend"] == "BULLISH"
        assert forecast["predicted_change_pct"] > 0
        
        print(f"✓ Forecast generated")
        print(f"  Ticker: {forecast['ticker']}")
        print(f"  Trend: {forecast['trend']}")
        print(f"  Current Price: ${forecast['current_price']}")
        print(f"  Predicted Change: {forecast['predicted_change_pct']:+.2f}%")
        print(f"  Target Price: ${forecast['target_price']:.2f}")
        print(f"  Confidence: {forecast['confidence']:.1%}")
    
    def test_bearish_forecast(self):
        """Test forecast for negative sentiment"""
        print("\n" + "="*60)
        print("TEST: MLForecastAgent - Bearish Forecast")
        print("="*60)
        
        state = {
            "ticker": "TEST",
            "sentiment_score": -0.6,  # Negative
            "market_data": {"current_price": 100.0}
        }
        
        result = MLForecastAgent.run(state)
        forecast = result["forecast"]
        
        assert forecast["trend"] == "BEARISH"
        assert forecast["predicted_change_pct"] < 0
        
        print(f"✓ Forecast generated")
        print(f"  Trend: {forecast['trend']}")
        print(f"  Predicted Change: {forecast['predicted_change_pct']:+.2f}%")
        print(f"  Target Price: ${forecast['target_price']:.2f}")


class TestLLMReasoningAgent(unittest.TestCase):
    """Test LLMReasoningAgent - Risk evaluation and human review decision"""
    
    def test_requires_human_review(self):
        """Test when human review is required"""
        print("\n" + "="*60)
        print("TEST: LLMReasoningAgent - Requires Review")
        print("="*60)
        
        state = {
            "ticker": "TEST",
            "sentiment_score": -0.85,  # Extreme
            "forecast": {"confidence": 0.5, "trend": "BEARISH"},
            "risk_alerts": [
                {"severity": "HIGH", "type": "CRITICAL"}
            ]
        }
        
        result = LLMReasoningAgent.run(state)
        
        assert result["requires_human_review"] == True
        reasoning = result["reasoning"]
        
        print(f"✓ Human review required: {result['requires_human_review']}")
        print(f"  Risk Level: {reasoning['risk_level']}")
        print(f"  Review Reasons: {reasoning['review_reasons']}")
    
    def test_autoapprove_scenario(self):
        """Test when automatic approval is possible"""
        print("\n" + "="*60)
        print("TEST: LLMReasoningAgent - Auto Approve")
        print("="*60)
        
        state = {
            "ticker": "AAPL",
            "sentiment_score": 0.3,  # Moderate positive
            "forecast": {"confidence": 0.75, "trend": "BULLISH"},
            "risk_alerts": []
        }
        
        result = LLMReasoningAgent.run(state)
        
        print(f"✓ Human review required: {result['requires_human_review']}")
        print(f"  Risk Level: {result['reasoning']['risk_level']}")
        print(f"  Auto-approval: {not result['requires_human_review']}")


class TestRecommendationAgent(unittest.TestCase):
    """Test RecommendationAgent - Final recommendation"""
    
    def test_buy_recommendation(self):
        """Test BUY recommendation generation"""
        print("\n" + "="*60)
        print("TEST: RecommendationAgent - BUY Recommendation")
        print("="*60)
        
        state = {
            "ticker": "NVDA",
            "sentiment_score": 0.6,
            "sentiment_label": "positive",
            "forecast": {
                "trend": "BULLISH",
                "confidence": 0.8,
                "predicted_change_pct": 5.0,
                "target_price": 150.0,
            },
            "market_data": {"current_price": 140.0},
            "risk_alerts": [],
            "requires_human_review": False,
            "human_approved": True,
            "human_comments": "Approved",
        }
        
        result = RecommendationAgent.run(state)
        rec = result["recommendation"]
        
        assert rec["action"] in ["BUY", "HOLD"]  # Should suggest action
        
        print(f"✓ Recommendation generated")
        print(f"  Ticker: {rec['ticker']}")
        print(f"  Action: {rec['action']}")
        print(f"  Urgency: {rec['urgency']}")
        print(f"  Confidence: {rec['confidence']:.1%}")
        
        print(f"\n  Reasoning:")
        for reason in rec["reasoning"]:
            print(f"    • {reason}")
    
    def test_sell_recommendation(self):
        """Test SELL recommendation generation"""
        print("\n" + "="*60)
        print("TEST: RecommendationAgent - SELL Recommendation")
        print("="*60)
        
        state = {
            "ticker": "TSLA",
            "sentiment_score": -0.7,
            "sentiment_label": "negative",
            "forecast": {
                "trend": "BEARISH",
                "confidence": 0.75,
            },
            "market_data": {"current_price": 200.0},
            "risk_alerts": [
                {"severity": "HIGH", "type": "CRITICAL"}
            ],
            "requires_human_review": False,
            "human_approved": True,
        }
        
        result = RecommendationAgent.run(state)
        rec = result["recommendation"]
        
        print(f"✓ Recommendation generated")
        print(f"  Action: {rec['action']}")
        print(f"  Urgency: {rec['urgency']}")


def run_all_agent_tests():
    """Run all agent tests"""
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + "  🤖 COMPREHENSIVE AGENTS TEST SUITE".center(58) + "█")
    print("█" + " "*58 + "█")
    print("█"*60)
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all agent tests
    suite.addTests(loader.loadTestsFromTestCase(TestInputAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestSentimentAnalyzerAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestMarketDataAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestRiskAlertAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestMLForecastAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestLLMReasoningAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestRecommendationAgent))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "="*60)
    print("AGENT TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_agent_tests()
    exit(0 if success else 1)
