# ============================================================
# core/logger.py
# ============================================================
# Handles all logging configuration for the agent.
# Provides colored output for clarity during tool execution.
# ============================================================

import logging

def setup_logger(name: str = "agent_logger", level: int = logging.INFO):
    """Create and configure a named logger."""
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S"
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers if logger already exists
    if not logger.handlers:
        logger.addHandler(handler)

    return logger


# Example:
# logger = setup_logger()
# logger.info("Agent initialized successfully.")
