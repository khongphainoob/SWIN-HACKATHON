"""Retry helpers with exponential backoff.

Provides a lightweight decorator for retrying transiently failing operations.
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
        """Decorate ``func`` with retry-on-exception behavior."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Execute function with bounded retry and backoff."""
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
