"""Simple logging helper.

Detailed documentation
----------------------
Purpose
    Provide a convenient, non-propagating logger factory for tools/services so
    logging works without global configuration.

Behavior
    - Creates a ``StreamHandler`` with a concise formatter.
    - Avoids duplicate handlers by checking existing handlers.
    - Sets desired log level (default INFO) and disables propagation to prevent
      duplicate logs in notebooks or agent runners.

Why this fits LangChain
    - Tools often run inside agent loops; a safe default logger prevents noisy
      propagation while still allowing debug traces when injected.
"""
import logging
from typing import Optional


def get_logger(name: str = "app", level: int = logging.INFO) -> logging.Logger:
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
