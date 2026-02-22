"""
Asset mapping utilities
Map company names to tickers and provide asset information
"""

# Comprehensive company name to ticker mapping
COMPANY_TO_TICKER = {
    # Tech Giants
    "apple": "AAPL",
    "microsoft": "MSFT",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "nvidia": "NVDA",
    "tesla": "TSLA",
    "meta": "META",
    "facebook": "META",
    "amazon": "AMZN",
    "netflix": "NFLX",
    "intel": "INTC",
    "amd": "AMD",
    "ibm": "IBM",
    "oracle": "ORCL",
    "salesforce": "CRM",
    "adobe": "ADBE",
    "cisco": "CSCO",
    
    # Finance
    "jp morgan": "JPM",
    "jpmorgan": "JPM",
    "bank of america": "BAC",
    "wells fargo": "WFC",
    "goldman sachs": "GS",
    "morgan stanley": "MS",
    "citigroup": "C",
    "visa": "V",
    "mastercard": "MA",
    "paypal": "PYPL",
    "american express": "AXP",
    
    # Healthcare
    "johnson & johnson": "JNJ",
    "johnson and johnson": "JNJ",
    "pfizer": "PFE",
    "moderna": "MRNA",
    "abbvie": "ABBV",
    "merck": "MRK",
    "eli lilly": "LLY",
    "bristol myers": "BMY",
    
    # Consumer
    "coca cola": "KO",
    "coca-cola": "KO",
    "pepsi": "PEP",
    "pepsico": "PEP",
    "procter & gamble": "PG",
    "pg": "PG",
    "walmart": "WMT",
    "target": "TGT",
    "costco": "COST",
    "nike": "NKE",
    "starbucks": "SBUX",
    "mcdonald": "MCD",
    "mcdonalds": "MCD",
    
    # Energy
    "exxon": "XOM",
    "exxonmobil": "XOM",
    "chevron": "CVX",
    "shell": "SHEL",
    "bp": "BP",
    "conocophillips": "COP",
    
    # Industrial
    "boeing": "BA",
    "caterpillar": "CAT",
    "3m": "MMM",
    "general electric": "GE",
    "ge": "GE",
    "general motors": "GM",
    "gm": "GM",
    "ford": "F",
    
    # Vietnamese stocks
    "vietcombank": "VCB",
    "vingroup": "VIC",
    "vinhomes": "VHM",
    "hoabank": "HDB",
    "techcombank": "TCB",
    "fpt": "FPT",
    "mobile world": "MWG",
    "vinamilk": "VNM",
}

# Asset type information
ASSET_TYPES = {
    "stock": {
        "name": "Stock",
        "icon": "📈",
        "description": "Company shares",
        "examples": ["AAPL", "MSFT", "GOOGL"],
        "suffix": "",
    },
    "crypto": {
        "name": "Cryptocurrency",
        "icon": "₿",
        "description": "Digital currencies",
        "examples": ["BTC-USD", "ETH-USD", "BNB-USD"],
        "suffix": "-USD",
    },
    "commodity": {
        "name": "Commodity",
        "icon": "🥇",
        "description": "Raw materials",
        "examples": ["GC=F", "SI=F", "CL=F"],
        "suffix": "=F",
    },
    "forex": {
        "name": "Forex",
        "icon": "💱",
        "description": "Currency pairs",
        "examples": ["EURUSD=X", "GBPUSD=X"],
        "suffix": "=X",
    }
}

# Popular assets by type
POPULAR_ASSETS = {
    "crypto": [
        ("BTC-USD", "Bitcoin", "₿"),
        ("ETH-USD", "Ethereum", "Ξ"),
        ("BNB-USD", "Binance Coin", "BNB"),
        ("ADA-USD", "Cardano", "ADA"),
        ("SOL-USD", "Solana", "SOL"),
        ("DOT-USD", "Polkadot", "DOT"),
        ("DOGE-USD", "Dogecoin", "DOGE"),
        ("XRP-USD", "Ripple", "XRP"),
        ("MATIC-USD", "Polygon", "MATIC"),
        ("AVAX-USD", "Avalanche", "AVAX"),
    ],
    "commodity": [
        ("GC=F", "Gold", "🥇"),
        ("SI=F", "Silver", "🥈"),
        ("CL=F", "Crude Oil", "🛢️"),
        ("NG=F", "Natural Gas", "🔥"),
        ("HG=F", "Copper", "🔶"),
        ("ZC=F", "Corn", "🌽"),
        ("ZW=F", "Wheat", "🌾"),
        ("KC=F", "Coffee", "☕"),
    ],
    "forex": [
        ("EURUSD=X", "Euro/USD", "€/$"),
        ("GBPUSD=X", "Pound/USD", "£/$"),
        ("JPYUSD=X", "Yen/USD", "¥/$"),
        ("AUDUSD=X", "AUD/USD", "A$/$"),
        ("USDCAD=X", "USD/CAD", "$/C$"),
        ("USDCHF=X", "USD/CHF", "$/CHF"),
    ]
}


def search_company(query: str) -> str:
    """
    Search company name and return ticker.
    
    Args:
        query: Company name or partial name
    
    Returns:
        Ticker symbol or original query if not found
    """
    query_lower = query.lower().strip()
    
    # Exact match
    if query_lower in COMPANY_TO_TICKER:
        return COMPANY_TO_TICKER[query_lower]
    
    # Partial match
    for company, ticker in COMPANY_TO_TICKER.items():
        if query_lower in company or company in query_lower:
            return ticker
    
    # No match - return original (uppercase)
    return query.upper().strip()


def get_asset_info(ticker: str) -> dict:
    """
    Get asset type and info from ticker format.
    
    Args:
        ticker: Ticker symbol
    
    Returns:
        Dict with asset type and info
    """
    ticker_upper = ticker.upper()
    
    if "-USD" in ticker_upper:
        return {
            "type": "crypto",
            "symbol": ticker_upper.replace("-USD", ""),
            **ASSET_TYPES["crypto"]
        }
    elif "=F" in ticker_upper:
        return {
            "type": "commodity",
            "symbol": ticker_upper.replace("=F", ""),
            **ASSET_TYPES["commodity"]
        }
    elif "=X" in ticker_upper:
        return {
            "type": "forex",
            "symbol": ticker_upper.replace("=X", ""),
            **ASSET_TYPES["forex"]
        }
    else:
        return {
            "type": "stock",
            "symbol": ticker_upper,
            **ASSET_TYPES["stock"]
        }


def format_asset_name(ticker: str) -> str:
    """
    Format asset name for display.
    
    Args:
        ticker: Ticker symbol
    
    Returns:
        Formatted display name
    """
    info = get_asset_info(ticker)
    icon = info["icon"]
    symbol = info["symbol"]
    asset_type = info["name"]
    
    return f"{icon} {symbol} ({asset_type})"


if __name__ == "__main__":
    # Test
    print("Testing company search:")
    print(f"Apple → {search_company('Apple')}")
    print(f"microsoft → {search_company('microsoft')}")
    print(f"JP Morgan → {search_company('JP Morgan')}")
    print(f"coca cola → {search_company('coca cola')}")
    
    print("\nTesting asset info:")
    print(f"AAPL → {get_asset_info('AAPL')}")
    print(f"BTC-USD → {get_asset_info('BTC-USD')}")
    print(f"GC=F → {get_asset_info('GC=F')}")
    print(f"EURUSD=X → {get_asset_info('EURUSD=X')}")
    
    print("\nTesting format:")
    print(f"AAPL → {format_asset_name('AAPL')}")
    print(f"BTC-USD → {format_asset_name('BTC-USD')}")
