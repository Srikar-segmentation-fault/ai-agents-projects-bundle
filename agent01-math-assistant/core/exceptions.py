# ============================================================
# core/exceptions.py
# ============================================================
# Defines custom exception classes for better debugging.
# ============================================================

class LLMInitializationError(Exception):
    """Raised when the chosen LLM fails to initialize."""
    pass

class ToolExecutionError(Exception):
    """Raised when a tool fails unexpectedly."""
    pass

class MissingAPIKeyError(Exception):
    """Raised when a required API key is not found."""
    pass
