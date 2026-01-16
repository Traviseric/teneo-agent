"""
Logging utilities for Teneo Agent.

Provides consistent timestamped logging across all modules.
"""

from datetime import datetime
from typing import Callable, Optional

# Global log callback
_log_callback: Optional[Callable[[str], None]] = None


def set_log_callback(callback: Callable[[str], None]):
    """Set a custom log callback function."""
    global _log_callback
    _log_callback = callback


def log(message: str):
    """
    Print timestamped log message.

    If a callback is set, uses that. Otherwise prints to stdout.
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    formatted = f"[{timestamp}] {message}"

    if _log_callback:
        _log_callback(formatted)
    else:
        print(formatted)
