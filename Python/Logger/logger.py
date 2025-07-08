"""
Core Logger implementation with LogLevel enum and main logging functionality.
"""

import sys
from datetime import datetime
from enum import Enum
from typing import List, Optional, Any, Dict, TYPE_CHECKING
import traceback

if TYPE_CHECKING:
    from .handlers import Handler


class LogLevel(Enum):
    """Log levels in order of severity."""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

    def __str__(self):
        return self.name

    def __lt__(self, other):
        if isinstance(other, LogLevel):
            return self.value < other.value
        return NotImplemented


class Logger:
    """Main Logger class that handles log messages and distributes them to handlers."""
    
    def __init__(self, name: str = "default"):
        self.name = name
        self.level = LogLevel.INFO
        self.handlers: List['Handler'] = []
        self.propagate = True
        self.parent: Optional['Logger'] = None
        self.children: Dict[str, 'Logger'] = {}
        
    def set_level(self, level: LogLevel):
        """Set the minimum log level for this logger."""
        self.level = level
        
    def add_handler(self, handler: 'Handler'):
        """Add a handler to this logger."""
        self.handlers.append(handler)
        
    def remove_handler(self, handler: 'Handler'):
        """Remove a handler from this logger."""
        if handler in self.handlers:
            self.handlers.remove(handler)
            
    def clear_handlers(self):
        """Remove all handlers from this logger."""
        self.handlers.clear()
        
    def get_child(self, name: str) -> 'Logger':
        """Get or create a child logger."""
        if name not in self.children:
            child = Logger(f"{self.name}.{name}")
            child.parent = self
            child.level = self.level
            child.handlers = self.handlers.copy()
            self.children[name] = child
        return self.children[name]
        
    def _log(self, level: LogLevel, message: str, *args, **kwargs):
        """Internal logging method."""
        if level.value < self.level.value:
            return
            
        # Format message with args
        if args:
            message = message % args
            
        # Get the calling script name from the stack trace
        calling_script = self._get_calling_script()
            
        # Create log record
        record = LogRecord(
            name=self.name,
            level=level,
            message=message,
            timestamp=datetime.now(),
            calling_script=calling_script,
            **kwargs
        )
        
        # Send to handlers
        for handler in self.handlers:
            try:
                handler.emit(record)
            except Exception as e:
                # Prevent infinite recursion if handler fails
                sys.stderr.write(f"Handler error: {e}\n")
                
        # Propagate to parent if enabled
        if self.propagate and self.parent:
            self.parent._log(level, message, *args, **kwargs)
            
    def _get_calling_script(self) -> str:
        """Get the name of the script that called the logger, without .py extension."""
        import inspect
        import os
        
        # Get the current stack
        stack = inspect.stack()
        
        # Only skip logger implementation files
        skip_files = [
            'logger.py', 'formatters.py', 'handlers.py', 'registry.py', 'config.py'
        ]
        for frame_info in stack:
            filename = frame_info.filename
            base = os.path.basename(filename)
            if base not in skip_files and '__pycache__' not in filename:
                # Extract just the filename without path and strip .py
                script_name = base
                if script_name.endswith('.py'):
                    script_name = script_name[:-3]
                return script_name
        # Fallback to the logger name if we can't find the calling script
        return self.name
            
    def debug(self, message: str, *args, **kwargs):
        """Log a debug message."""
        self._log(LogLevel.DEBUG, message, *args, **kwargs)
        
    def info(self, message: str, *args, **kwargs):
        """Log an info message."""
        self._log(LogLevel.INFO, message, *args, **kwargs)
        
    def warning(self, message: str, *args, **kwargs):
        """Log a warning message."""
        self._log(LogLevel.WARNING, message, *args, **kwargs)
        
    def error(self, message: str, *args, **kwargs):
        """Log an error message."""
        self._log(LogLevel.ERROR, message, *args, **kwargs)
        
    def critical(self, message: str, *args, **kwargs):
        """Log a critical message."""
        self._log(LogLevel.CRITICAL, message, *args, **kwargs)
        
    def exception(self, message: str, *args, **kwargs):
        """Log an exception with traceback."""
        kwargs['exc_info'] = True
        self._log(LogLevel.ERROR, message, *args, **kwargs)


class LogRecord:
    """Represents a single log record with all relevant information."""
    
    def __init__(self, name: str, level: LogLevel, message: str, timestamp: datetime, **kwargs):
        self.name = name
        self.level = level
        self.message = message
        self.timestamp = timestamp
        self.calling_script = kwargs.get('calling_script', name)
        self.exc_info = kwargs.get('exc_info', False)
        self.extra = {k: v for k, v in kwargs.items() if k not in ['exc_info', 'calling_script']}
        
        # Add exception info if present
        if self.exc_info:
            self.exc_text = ''.join(traceback.format_exc())
        else:
            self.exc_text = None 