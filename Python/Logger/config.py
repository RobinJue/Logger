"""
Configuration utilities for easy logger setup.
"""

import os
from datetime import datetime
from .logger import Logger, LogLevel
from .formatters import SimpleFormatter, JSONFormatter, ColoredFormatter
from .handlers import ConsoleHandler, FileHandler, RotatingFileHandler
from .registry import register_logger

# Get the absolute path to the Logger/logs directory
_LOGGER_DIR = os.path.dirname(os.path.abspath(__file__))
_LOGS_DIR = os.path.join(_LOGGER_DIR, "logs")
os.makedirs(_LOGS_DIR, exist_ok=True)

def _timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def _abs_log_path(filename, name=None):
    # If filename is None, use timestamp-name.log
    if filename is None and name is not None:
        filename = f"{_timestamp()}-{name}.log"
    elif filename is not None and name is not None and not filename.endswith('.log'):
        filename = f"{_timestamp()}-{filename}.log"
    elif filename is not None and name is not None and filename == name:
        filename = f"{_timestamp()}-{name}.log"
    elif filename is not None and not os.path.isabs(filename) and not filename.startswith(_LOGS_DIR):
        # If not absolute and not already in logs dir, add timestamp
        base = os.path.basename(filename)
        filename = f"{_timestamp()}-{base}"
    if filename is not None and not os.path.isabs(filename):
        filename = os.path.join(_LOGS_DIR, filename)
    return filename

def setup_basic_logger(name="default", level=LogLevel.INFO, 
                      console=True, file=None, colored=True):
    """
    Setup a basic logger with common configuration.
    
    Args:
        name: Logger name
        level: Minimum log level
        console: Whether to output to console
        file: Optional file path for file output (defaults to logs/{timestamp}-{name}.log)
        colored: Whether to use colored output (console only)
    """
    logger = Logger(name)
    logger.set_level(level)
    
    # Console handler
    if console:
        console_handler = ConsoleHandler()
        if colored:
            console_handler.set_formatter(ColoredFormatter())
        else:
            console_handler.set_formatter(SimpleFormatter())
        logger.add_handler(console_handler)
    
    # File handler
    file = _abs_log_path(file, name)
    if file:
        file_handler = FileHandler(file)
        file_handler.set_formatter(SimpleFormatter())
        logger.add_handler(file_handler)
    
    # Register the logger
    register_logger(name, logger)
    
    return logger


def setup_development_logger(name="default"):
    """
    Setup a logger suitable for development with colored console output.
    """
    return setup_basic_logger(
        name=name,
        level=LogLevel.DEBUG,
        console=True,
        colored=True
    )


def setup_production_logger(name="default", log_file="app.log"):
    """
    Setup a logger suitable for production with file output.
    """
    return setup_basic_logger(
        name=name,
        level=LogLevel.INFO,
        console=False,
        file=log_file,
        colored=False
    )


def setup_json_logger(name="default", log_file="app.json.log"):
    """
    Setup a logger that outputs JSON format (useful for log aggregation).
    """
    logger = Logger(name)
    logger.set_level(LogLevel.INFO)
    log_file = _abs_log_path(log_file, name)
    file_handler = FileHandler(log_file)
    file_handler.set_formatter(JSONFormatter())
    logger.add_handler(file_handler)
    
    # Register the logger
    register_logger(name, logger)
    
    return logger


def setup_rotating_logger(name="default", log_file="app.log", 
                         max_bytes=10*1024*1024, backup_count=5, max_files=100):
    """
    Setup a logger with rotating file output.
    """
    logger = Logger(name)
    logger.set_level(LogLevel.INFO)
    log_file = _abs_log_path(log_file, name)
    rotating_handler = RotatingFileHandler(
        log_file, 
        max_bytes=max_bytes, 
        backup_count=backup_count,
        max_files=max_files
    )
    rotating_handler.set_formatter(SimpleFormatter())
    logger.add_handler(rotating_handler)
    
    # Register the logger
    register_logger(name, logger)
    
    return logger


def setup_multi_handler_logger(name="default", console=True, 
                              log_file="app.log", error_file="error.log"):
    """
    Setup a logger with multiple handlers for different purposes.
    """
    logger = Logger(name)
    logger.set_level(LogLevel.DEBUG)
    if console:
        console_handler = ConsoleHandler()
        console_handler.set_formatter(ColoredFormatter())
        logger.add_handler(console_handler)
    if log_file:
        log_file = _abs_log_path(log_file, name)
        file_handler = FileHandler(log_file)
        file_handler.set_formatter(SimpleFormatter())
        logger.add_handler(file_handler)
    if error_file:
        error_file = _abs_log_path(error_file, name)
        error_handler = FileHandler(error_file)
        error_handler.set_formatter(SimpleFormatter())
        error_handler.set_level(LogLevel.ERROR)
        logger.add_handler(error_handler)
    
    # Register the logger
    register_logger(name, logger)
    
    return logger


# Convenience function for quick setup
def quick_logger(name="default", level="INFO"):
    """
    Quick setup for a basic logger.
    
    Args:
        name: Logger name
        level: Log level as string ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
    """
    level_map = {
        "DEBUG": LogLevel.DEBUG,
        "INFO": LogLevel.INFO,
        "WARNING": LogLevel.WARNING,
        "ERROR": LogLevel.ERROR,
        "CRITICAL": LogLevel.CRITICAL
    }
    
    log_level = level_map.get(level.upper(), LogLevel.INFO)
    return setup_basic_logger(name=name, level=log_level) 