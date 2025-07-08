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
    
    def __init__(self, date_format: str = "%Y-%m-%d %H:%M:%S", enable_links: bool = None):
        self.date_format = date_format
        # Auto-detect if we should enable links based on terminal support
        if enable_links is None:
            self.enable_links = self._detect_link_support()
        else:
            self.enable_links = enable_links
            
    def _detect_link_support(self) -> bool:
        """Detect if the terminal supports hyperlinks."""
        import os
        # Check if we're in a terminal that likely supports hyperlinks
        term = os.environ.get('TERM', '')
        term_program = os.environ.get('TERM_PROGRAM', '')
        
        # Common terminals that support hyperlinks
        supported_terms = ['xterm-256color', 'screen-256color', 'tmux-256color']
        supported_programs = ['iTerm.app', 'Apple_Terminal', 'vscode']
        
        return (term in supported_terms or 
                term_program in supported_programs or
                'ITERM' in os.environ.get('TERM_PROGRAM', ''))
        
    def _create_link(self, text: str, file_path: str) -> str:
        """Create a clickable terminal link."""
        if not self.enable_links or not file_path:
            return text.ljust(15)
        
        try:
            # ANSI escape sequence for clickable link
            # Format: \033]8;;file://path\033\\text\033]8;;\033\\
            link_start = f"\033]8;;file://{file_path}\033\\"
            link_end = "\033]8;;\033\\"
            linked_text = f"{link_start}{text}{link_end}"
            return linked_text.ljust(15)
        except:
            # Fallback if something goes wrong
            return text.ljust(15)
        
    def format(self, record) -> str:
        """Format record as: [timestamp] LEVEL calling_script: message"""
        timestamp = record.timestamp.strftime(self.date_format)
        level = str(record.level).ljust(8)
        
        # Get script name and create clickable link if path is available
        script_name = getattr(record, 'calling_script', record.name)
        file_path = getattr(record, 'calling_path', "")
        script_display = self._create_link(script_name, file_path)
        
        formatted = f"[{timestamp}] {level} {script_display}: {record.message}"
        
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
            data["calling_path"] = getattr(record, 'calling_path', "")
            
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
    
    def __init__(self, date_format: str = "%Y-%m-%d %H:%M:%S", use_colors: bool = True, enable_links: bool = None):
        self.date_format = date_format
        self.use_colors = use_colors
        # Auto-detect if we should enable links based on terminal support
        if enable_links is None:
            self.enable_links = self._detect_link_support()
        else:
            self.enable_links = enable_links
            
    def _detect_link_support(self) -> bool:
        """Detect if the terminal supports hyperlinks."""
        import os
        # Check if we're in a terminal that likely supports hyperlinks
        term = os.environ.get('TERM', '')
        term_program = os.environ.get('TERM_PROGRAM', '')
        
        # Common terminals that support hyperlinks
        supported_terms = ['xterm-256color', 'screen-256color', 'tmux-256color']
        supported_programs = ['iTerm.app', 'Apple_Terminal', 'vscode']
        
        return (term in supported_terms or 
                term_program in supported_programs or
                'ITERM' in os.environ.get('TERM_PROGRAM', ''))
        
    def _create_link(self, text: str, file_path: str) -> str:
        """Create a clickable terminal link."""
        if not self.enable_links or not file_path:
            return text.ljust(15)
        
        try:
            # ANSI escape sequence for clickable link
            # Format: \033]8;;file://path\033\\text\033]8;;\033\\
            link_start = f"\033]8;;file://{file_path}\033\\"
            link_end = "\033]8;;\033\\"
            linked_text = f"{link_start}{text}{link_end}"
            return linked_text.ljust(15)
        except:
            # Fallback if something goes wrong
            return text.ljust(15)
        
    def format(self, record) -> str:
        """Format record with colors."""
        timestamp = record.timestamp.strftime(self.date_format)
        level = str(record.level).ljust(8)
        
        # Get script name and create clickable link if path is available
        script_name = getattr(record, 'calling_script', record.name)
        file_path = getattr(record, 'calling_path', "")
        script_display = self._create_link(script_name, file_path)
        
        if self.use_colors:
            color = self.COLORS.get(record.level.name, '')
            reset = self.COLORS['RESET']
            formatted = f"[{timestamp}] {color}{level}{reset} {script_display}: {record.message}"
        else:
            formatted = f"[{timestamp}] {level} {script_display}: {record.message}"
        
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
            'calling_path': getattr(record, 'calling_path', ""),
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