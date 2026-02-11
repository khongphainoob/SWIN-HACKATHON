"""Project logging utilities.

Exposes a small logger factory with consistent formatting and safe defaults for
local tool/service execution.
"""
import logging
from typing import Optional


def get_logger(name: str = "app", level: int = logging.INFO) -> logging.Logger:
    """Create or reuse a logger with one stream handler and fixed formatting."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    return logger
