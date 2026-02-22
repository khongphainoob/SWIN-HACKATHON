"""
Test LLM Service with Real API Calls
Verify that all providers work correctly with their APIs
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.llm_service import LLMService

def test_provider(provider_name: str, test_prompt: str = "What is 2+2?"):
    """Test a specific LLM provider."""
    print(f"\n{'='*70}")
    print(f"🧪 Testing {provider_name.upper()}")
    print(f"{'='*70}")
    
    # Create service for this provider
    llm = LLMService(provider=provider_name)
    
    # Check API key
    has_key = llm.validate_api_key(provider_name)
    print(f"📋 API Key: {'✅ Found' if has_key else '❌ Not found'}")
    
    if not has_key:
        print(f"⚠️  Skipping test - No API key for {provider_name}")
        print(f"💡 Set {provider_name.upper()}_API_KEY in your .env file")
        return False
    
    # Test API call
    try:
        print(f"📤 Sending: '{test_prompt}'")
        response = llm.call_llm(
            prompt=test_prompt,
            temperature=0.3,
            max_tokens=100
        )
        
        print(f"📥 Response: {response[:150]}...")
        
        # Check if it's a mock response
        if "[MOCK" in response:
            print("⚠️  Received mock response - API call may have failed")
            return False
        else:
            print(f"✅ {provider_name.upper()} API call successful!")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_all_providers():
    """Test all available LLM providers."""
    print("\n" + "="*70)
    print("🚀 LLM SERVICE API TEST")
    print("="*70)
    print("\nTesting real API calls for all providers...")
    
    providers = ["gemini", "openai", "anthropic", "groq"]
    results = {}
    
    for provider in providers:
        results[provider] = test_provider(provider)
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    for provider, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED/SKIPPED"
        print(f"  {provider.upper():<12} {status}")
    
    total_tested = sum(1 for v in results.values() if v)
    print(f"\nTotal providers tested: {total_tested}/{len(providers)}")
    
    if total_tested == 0:
        print("\n⚠️  WARNING: No providers were successfully tested!")
        print("💡 Make sure to:")
        print("   1. Install provider packages: pip install google-generativeai openai anthropic groq")
        print("   2. Set API keys in .env file")
        print("   3. Run: python setup_api_keys.py")
    
    print()


def test_ticker_extraction():
    """Test ticker extraction functionality."""
    print("\n" + "="*70)
    print("🧪 Testing Ticker Extraction")
    print("="*70)
    
    test_queries = [
        "Should I buy NVDA stock?",
        "What's the outlook for AAPL?",
        "Analyze MSFT for me",
    ]
    
    llm = LLMService()
    
    for query in test_queries:
        prompt = f"Extract the stock ticker symbol from the following query: '{query}'. If no ticker is found, respond with 'UNKNOWN'."
        
        try:
            result = llm.call_llm(prompt, temperature=0.0, max_tokens=10)
            print(f"  Query: {query}")
            print(f"  → Ticker: {result}")
        except Exception as e:
            print(f"  Query: {query}")
            print(f"  → Error: {e}")
    
    print()


def test_model_selection():
    """Test different models for each provider."""
    print("\n" + "="*70)
    print("🧪 Testing Model Selection")
    print("="*70)
    
    test_configs = [
        ("gemini", "gemini-1.5-pro"),
        ("gemini", "gemini-1.5-flash"),
        ("openai", "gpt-3.5-turbo"),
        ("openai", "gpt-4"),
        ("anthropic", "claude-3-sonnet-20240229"),
        ("groq", "llama-3.1-70b-versatile"),
    ]
    
    prompt = "Say 'OK' if you receive this."
    
    for provider, model in test_configs:
        llm = LLMService(provider=provider)
        
        if not llm.validate_api_key(provider):
            print(f"  ⏭️  {provider}/{model}: Skipped (no API key)")
            continue
        
        try:
            response = llm.call_llm(prompt, model=model, max_tokens=50)
            status = "✅" if response and not "[MOCK" in response else "⚠️"
            print(f"  {status} {provider}/{model}: {response[:40]}...")
        except Exception as e:
            print(f"  ❌ {provider}/{model}: {str(e)[:50]}...")
    
    print()


def main():
    """Run all tests."""
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("⚠️  python-dotenv not installed, using system environment variables")
    
    # Run tests
    test_all_providers()
    test_ticker_extraction()
    test_model_selection()
    
    print("="*70)
    print("🎉 Testing complete!")
    print("="*70)
    print("\n💡 Next steps:")
    print("   • If all tests passed: You're ready to use the LLM service!")
    print("   • If some failed: Check API keys and package installations")
    print("   • Run workflow: python orchestrators/langgraph_workflow.py")
    print()


if __name__ == "__main__":
    main()
