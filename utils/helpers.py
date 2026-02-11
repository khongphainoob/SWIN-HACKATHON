"""Generic helper utilities.

Detailed documentation
----------------------
Purpose
    Centralize lightweight helper functions for formatting, safe access,
    vector math, whitespace normalization, and date parsing.

Functions
    - ``format_currency`` / ``format_percent``: Presentation helpers.
    - ``safe_get``: Dot-path lookup in nested dicts.
    - ``normalize_whitespace``: Collapses repeated whitespace.
    - ``parse_date``: Attempts multiple date formats.
    - ``cosine_similarity``: Vector similarity for TF-IDF store.

Why this fits LangChain
    - Provides small, dependency-free utilities used by tools and vector
      store; keeps outputs serializable and predictable for agent flows.
"""
from __future__ import annotations

import datetime as _dt
import math
import re
from typing import Any, Dict, Iterable, List, Optional


def format_currency(value: float, currency: str = "USD", decimals: int = 2) -> str:
    formatted = f"{value:,.{decimals}f}"
    return f"{currency} {formatted}"


def format_percent(value: float, decimals: int = 2) -> str:
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
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must be the same length")
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
