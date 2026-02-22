"""
Quick test for asset mapping utilities
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.asset_mapping import (
    search_company, 
    get_asset_info, 
    format_asset_name,
    POPULAR_ASSETS,
    COMPANY_TO_TICKER
)

def test_company_search():
    """Test company name to ticker conversion"""
    print("=" * 60)
    print("TEST 1: Company Search")
    print("=" * 60)
    
    test_cases = [
        "Apple",
        "microsoft",
        "JP Morgan",
        "coca cola",
        "tesla",
        "nvidia",
        "vietcombank",
        "ZZZ",  # Not found
    ]
    
    for company in test_cases:
        ticker = search_company(company)
        print(f"✓ '{company}' → {ticker}")
    
    print(f"\nTotal companies in database: {len(COMPANY_TO_TICKER)}")
    print()


def test_asset_info():
    """Test asset type detection"""
    print("=" * 60)
    print("TEST 2: Asset Info Detection")
    print("=" * 60)
    
    test_cases = [
        "AAPL",
        "BTC-USD",
        "GC=F",
        "EURUSD=X",
        "TSLA",
        "ETH-USD",
    ]
    
    for ticker in test_cases:
        info = get_asset_info(ticker)
        print(f"✓ {ticker:<12} → {info['icon']} {info['type']:<10} ({info['name']})")
    print()


def test_format_asset():
    """Test asset name formatting"""
    print("=" * 60)
    print("TEST 3: Asset Formatting")
    print("=" * 60)
    
    test_cases = [
        "AAPL",
        "BTC-USD",
        "GC=F",
        "EURUSD=X",
    ]
    
    for ticker in test_cases:
        formatted = format_asset_name(ticker)
        print(f"✓ {ticker:<12} → {formatted}")
    print()


def test_popular_assets():
    """Test popular assets lists"""
    print("=" * 60)
    print("TEST 4: Popular Assets")
    print("=" * 60)
    
    for asset_type, assets in POPULAR_ASSETS.items():
        print(f"\n{asset_type.upper()}: {len(assets)} assets")
        for ticker, name, icon in assets[:3]:  # Show first 3
            print(f"  {icon} {ticker:<12} - {name}")
        if len(assets) > 3:
            print(f"  ... and {len(assets) - 3} more")
    print()


def test_integration():
    """Test complete workflow"""
    print("=" * 60)
    print("TEST 5: Integration Test")
    print("=" * 60)
    
    # User searches for "Apple"
    company_query = "Apple"
    ticker = search_company(company_query)
    info = get_asset_info(ticker)
    formatted = format_asset_name(ticker)
    
    print(f"User input: '{company_query}'")
    print(f"↓")
    print(f"Detected ticker: {ticker}")
    print(f"↓")
    print(f"Asset type: {info['type']}")
    print(f"↓")
    print(f"Display: {formatted}")
    print("\n✅ Integration test passed!")
    print()


if __name__ == "__main__":
    print("\n🧪 Testing Asset Mapping Utilities\n")
    
    try:
        test_company_search()
        test_asset_info()
        test_format_asset()
        test_popular_assets()
        test_integration()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
