"""Retry decorator with exponential backoff.

Detailed documentation
----------------------
Purpose
    Wrap fragile functions (network/file I/O) with bounded retries and
    exponential backoff to improve robustness of tools/services.

Parameters
    - ``exceptions``: Tuple of exception types to catch (default ``Exception``).
    - ``tries``: Total attempts including first call.
    - ``delay``: Initial backoff delay in seconds.
    - ``backoff``: Multiplier applied after each failure.
    - ``max_delay``: Upper bound for backoff.

Why this fits LangChain
    - Tools inside agents may hit transient API errors; this decorator gives a
      lightweight resilience layer without adding new dependencies.
"""
from __future__ import annotations

import functools
import time
from typing import Any, Callable, Iterable, Tuple


def retry(
    exceptions: Iterable[type[BaseException]] = (Exception,),
    tries: int = 3,
    delay: float = 0.5,
    backoff: float = 2.0,
    max_delay: float = 10.0,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Retry a function when specified exceptions are raised.

    Args:
        exceptions: Iterable of exception classes to catch.
        tries: Total attempts (first call counts as an attempt).
        delay: Initial delay between attempts in seconds.
        backoff: Multiplier applied to delay after each failure.
        max_delay: Ceiling for delay between retries.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _tries, _delay = tries, delay
            while _tries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    time.sleep(_delay)
                    _delay = min(_delay * backoff, max_delay)
                    _tries -= 1
            return func(*args, **kwargs)

        return wrapper

    return decorator
