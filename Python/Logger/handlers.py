"""
Log handlers that determine where log messages are output.
"""

import sys
import os
from abc import ABC, abstractmethod
from typing import Optional, TextIO
from datetime import datetime


class Handler(ABC):
    """Abstract base class for log handlers."""
    
    def __init__(self):
        self.formatter = None
        self.level = None  # Optional level filter
        
    def set_formatter(self, formatter):
        """Set the formatter for this handler."""
        self.formatter = formatter
        
    def set_level(self, level):
        """Set the minimum level for this handler."""
        self.level = level
        
    def format(self, record):
        """Format a record using the handler's formatter."""
        if self.formatter is None:
            # Default simple formatter
            from .formatters import SimpleFormatter
            self.formatter = SimpleFormatter()
        return self.formatter.format(record)
        
    def filter(self, record):
        """Check if the record should be processed by this handler."""
        if self.level is None:
            return True
        return record.level.value >= self.level.value
        
    @abstractmethod
    def emit(self, record):
        """Emit a record. Must be implemented by subclasses."""
        pass
        
    def handle(self, record):
        """Handle a record by filtering, formatting, and emitting it."""
        if self.filter(record):
            try:
                self.emit(record)
            except Exception as e:
                # Prevent infinite recursion
                sys.stderr.write(f"Handler error: {e}\n")


class ConsoleHandler(Handler):
    """Handler that outputs to console (stdout/stderr)."""
    
    def __init__(self, stream=None):
        super().__init__()
        self.stream = stream
        
    def emit(self, record):
        """Emit a record to the console."""
        if self.stream is None:
            # Use stderr for errors and critical, stdout for others
            if record.level.value >= 3:  # ERROR or CRITICAL
                self.stream = sys.stderr
            else:
                self.stream = sys.stdout
                
        formatted = self.format(record)
        self.stream.write(formatted + '\n')
        self.stream.flush()


class FileHandler(Handler):
    """Handler that outputs to a file."""
    
    def __init__(self, filename, mode='a', encoding='utf-8'):
        super().__init__()
        self.filename = filename
        self.mode = mode
        self.encoding = encoding
        self._file = None
        
    def _open_file(self):
        """Open the log file."""
        if self._file is None:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            self._file = open(self.filename, self.mode, encoding=self.encoding)
            
    def emit(self, record):
        """Emit a record to the file."""
        self._open_file()
        formatted = self.format(record)
        self._file.write(formatted + '\n')
        self._file.flush()
        
    def close(self):
        """Close the file."""
        if self._file:
            self._file.close()
            self._file = None


class RotatingFileHandler(FileHandler):
    """Handler that rotates log files based on size or time."""
    
    def __init__(self, filename, max_bytes=10*1024*1024, backup_count=5, 
                 max_files=100, mode='a', encoding='utf-8'):
        super().__init__(filename, mode, encoding)
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.max_files = max_files
        
    def emit(self, record):
        """Emit a record and rotate if necessary."""
        if self._file and self._file.tell() >= self.max_bytes:
            self.rotate()
        super().emit(record)
        
    def rotate(self):
        """Rotate the log file."""
        if self._file:
            self._file.close()
            self._file = None
            
        # Rotate existing backup files
        for i in range(self.backup_count - 1, 0, -1):
            src = f"{self.filename}.{i}"
            dst = f"{self.filename}.{i + 1}"
            if os.path.exists(src):
                if os.path.exists(dst):
                    os.remove(dst)
                os.rename(src, dst)
                
        # Move current file to .1
        if os.path.exists(self.filename):
            os.rename(self.filename, f"{self.filename}.1")
            
        # Clean up old files if we exceed max_files
        self._cleanup_old_files()
        
    def _cleanup_old_files(self):
        """Remove old log files if we exceed max_files limit."""
        import glob
        pattern = f"{self.filename}.*"
        files = glob.glob(pattern)
        
        # Sort files by modification time (oldest first)
        files.sort(key=lambda x: os.path.getmtime(x))
        
        # If we have more files than max_files, remove the oldest ones
        if len(files) > self.max_files:
            files_to_remove = files[:-self.max_files]
            for old_file in files_to_remove:
                try:
                    os.remove(old_file)
                except OSError:
                    pass


class TimedRotatingFileHandler(FileHandler):
    """Handler that rotates log files based on time intervals."""
    
    def __init__(self, filename, when='midnight', interval=1, backup_count=5,
                 max_files=100, mode='a', encoding='utf-8'):
        super().__init__(filename, mode, encoding)
        self.when = when
        self.interval = interval
        self.backup_count = backup_count
        self.max_files = max_files
        self.last_rotation = datetime.now()
        
    def emit(self, record):
        """Emit a record and rotate if necessary."""
        if self.should_rotate(record.timestamp):
            self.rotate()
        super().emit(record)
        
    def should_rotate(self, timestamp):
        """Check if rotation is needed."""
        if self.when == 'midnight':
            return timestamp.date() != self.last_rotation.date()
        elif self.when == 'hour':
            return (timestamp - self.last_rotation).total_seconds() >= 3600 * self.interval
        elif self.when == 'minute':
            return (timestamp - self.last_rotation).total_seconds() >= 60 * self.interval
        return False
        
    def rotate(self):
        """Rotate the log file."""
        if self._file:
            self._file.close()
            self._file = None
            
        # Create backup filename with timestamp
        timestamp = self.last_rotation.strftime("%Y%m%d_%H%M%S")
        backup_name = f"{self.filename}.{timestamp}"
        
        if os.path.exists(self.filename):
            os.rename(self.filename, backup_name)
            
        # Remove old backups
        self._remove_old_backups()
        self.last_rotation = datetime.now()
        
    def _remove_old_backups(self):
        """Remove old backup files."""
        import glob
        pattern = f"{self.filename}.*"
        files = glob.glob(pattern)
        
        # Sort files by modification time (oldest first)
        files.sort(key=lambda x: os.path.getmtime(x))
        
        # Keep only the most recent files, respecting both backup_count and max_files
        max_to_keep = min(self.backup_count, self.max_files)
        if len(files) > max_to_keep:
            files_to_remove = files[:-max_to_keep]
            for old_file in files_to_remove:
                try:
                    os.remove(old_file)
                except OSError:
                    pass


class NullHandler(Handler):
    """Handler that does nothing (useful for testing)."""
    
    def emit(self, record):
        """Do nothing."""
        pass


class MemoryHandler(Handler):
    """Handler that stores records in memory."""
    
    def __init__(self, capacity=1000):
        super().__init__()
        self.capacity = capacity
        self.buffer = []
        
    def emit(self, record):
        """Store the record in memory."""
        self.buffer.append(record)
        if len(self.buffer) > self.capacity:
            self.buffer.pop(0)
            
    def get_records(self):
        """Get all stored records."""
        return self.buffer.copy()
        
    def clear(self):
        """Clear all stored records."""
        self.buffer.clear() 