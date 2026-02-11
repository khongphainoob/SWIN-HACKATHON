"""Shared helper utilities used across tools and services.

Includes formatting helpers, safe dictionary access, whitespace normalization,
date parsing, and cosine similarity math.
"""
from __future__ import annotations

import datetime as _dt
import math
import re
from typing import Any, Dict, Iterable, List, Optional


def format_currency(value: float, currency: str = "USD", decimals: int = 2) -> str:
    """Format a numeric value as a human-readable currency string."""
    formatted = f"{value:,.{decimals}f}"
    return f"{currency} {formatted}"


def format_percent(value: float, decimals: int = 2) -> str:
    """Format a numeric value as a percent string."""
    return f"{value:.{decimals}f}%"


def safe_get(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """Safely retrieve a nested key using dot notation."""
    current: Any = data
    for part in path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return default
    return current


def normalize_whitespace(text: str) -> str:
    """Collapse repeated whitespace and trim."""
    return " ".join(text.split())


def parse_date(date_str: str, formats: Optional[Iterable[str]] = None) -> Optional[_dt.datetime]:
    """Parse a date string using a list of potential formats."""
    fmts = formats or ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%Y-%m-%dT%H:%M:%SZ")
    for fmt in fmts:
        try:
            return _dt.datetime.strptime(date_str, fmt)
        except (ValueError, TypeError):
            continue
    return None


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity for two same-length numeric vectors."""
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must be the same length")
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
