"""
Log formatters that convert LogRecord objects into formatted strings.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict
import json


class Formatter(ABC):
    """Abstract base class for log formatters."""
    
    @abstractmethod
    def format(self, record) -> str:
        """Format a log record into a string."""
        pass


class SimpleFormatter(Formatter):
    """Simple text formatter with timestamp, level, calling_script, and message."""
    
    def __init__(self, date_format: str = "%Y-%m-%d %H:%M:%S"):
        self.date_format = date_format
        
    def format(self, record) -> str:
        """Format record as: [timestamp] LEVEL calling_script: message"""
        timestamp = record.timestamp.strftime(self.date_format)
        level = str(record.level).ljust(8)
        script_name = getattr(record, 'calling_script', record.name).ljust(15)
        
        formatted = f"[{timestamp}] {level} {script_name}: {record.message}"
        
        # Add exception info if present
        if record.exc_text:
            formatted += f"\n{record.exc_text}"
            
        # Add extra fields if present
        if record.extra:
            extra_str = " ".join(f"{k}={v}" for k, v in record.extra.items())
            formatted += f" | {extra_str}"
            
        return formatted


class JSONFormatter(Formatter):
    """JSON formatter for structured logging."""
    
    def __init__(self, include_timestamp: bool = True, include_name: bool = True):
        self.include_timestamp = include_timestamp
        self.include_name = include_name
        
    def format(self, record) -> str:
        """Format record as JSON."""
        data = {
            "level": record.level.name,
            "message": record.message
        }
        
        if self.include_timestamp:
            data["timestamp"] = record.timestamp.isoformat()
            
        if self.include_name:
            data["logger"] = record.name
            data["calling_script"] = getattr(record, 'calling_script', record.name)
            
        if record.exc_text:
            data["exception"] = record.exc_text
            
        if record.extra:
            data.update(record.extra)
            
        return json.dumps(data, ensure_ascii=False)


class ColoredFormatter(Formatter):
    """Colored console formatter with ANSI color codes."""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def __init__(self, date_format: str = "%Y-%m-%d %H:%M:%S", use_colors: bool = True):
        self.date_format = date_format
        self.use_colors = use_colors
        
    def format(self, record) -> str:
        """Format record with colors."""
        timestamp = record.timestamp.strftime(self.date_format)
        level = str(record.level).ljust(8)
        script_name = getattr(record, 'calling_script', record.name).ljust(15)
        
        if self.use_colors:
            color = self.COLORS.get(record.level.name, '')
            reset = self.COLORS['RESET']
            formatted = f"[{timestamp}] {color}{level}{reset} {script_name}: {record.message}"
        else:
            formatted = f"[{timestamp}] {level} {script_name}: {record.message}"
        
        # Add exception info if present
        if record.exc_text:
            if self.use_colors:
                formatted += f"\n{self.COLORS['ERROR']}{record.exc_text}{self.COLORS['RESET']}"
            else:
                formatted += f"\n{record.exc_text}"
                
        # Add extra fields if present
        if record.extra:
            extra_str = " ".join(f"{k}={v}" for k, v in record.extra.items())
            if self.use_colors:
                formatted += f" | {self.COLORS['DEBUG']}{extra_str}{self.COLORS['RESET']}"
            else:
                formatted += f" | {extra_str}"
                
        return formatted


class TemplateFormatter(Formatter):
    """Template-based formatter using a custom format string."""
    
    def __init__(self, template: str = "{timestamp} [{level}] {name}: {message}"):
        self.template = template
        
    def format(self, record) -> str:
        """Format record using the template."""
        # Create a dict with all available fields
        data = {
            'timestamp': record.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'level': str(record.level),
            'name': record.name,
            'calling_script': getattr(record, 'calling_script', record.name),
            'message': record.message,
            'levelname': record.level.name,
            'levelno': record.level.value
        }
        
        # Add extra fields
        data.update(record.extra)
        
        # Format using template
        try:
            formatted = self.template.format(**data)
        except KeyError as e:
            # If template has unknown fields, fall back to simple format
            formatted = f"[{data['timestamp']}] {data['level']} {data['name']}: {data['message']}"
            
        # Add exception info if present
        if record.exc_text:
            formatted += f"\n{record.exc_text}"
            
        return formatted 