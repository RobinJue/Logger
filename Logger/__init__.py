"""
Portable Logger Library

A self-contained logging library that can be easily copied into any project.
Provides configurable logging with multiple output formats and levels.
"""

from .logger import LogLevel
from .registry import get_logger, close_all_loggers

__version__ = "1.0.0"
__author__ = "Robin Jüngerich"

# Public API - only these should be used from outside the Logger folder
__all__ = [
    'LogLevel',
    'get_logger',
    'close_all_loggers',
    'create_logger'
]

# Convenience function to create a default logger
def create_logger(name="default", level=LogLevel.INFO):
    """Create a default logger with console output."""
    from .config import setup_basic_logger
    logger = setup_basic_logger(name, level)
    return logger 