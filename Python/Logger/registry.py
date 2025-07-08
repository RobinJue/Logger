"""
Logger registry for managing singleton logger instances.
"""

from typing import Dict, Optional
from .logger import Logger


class LoggerRegistry:
    """Registry for managing singleton logger instances."""
    
    def __init__(self):
        self._loggers: Dict[str, Logger] = {}
    
    def get_logger(self, name: str) -> Optional[Logger]:
        """Get an existing logger by name."""
        return self._loggers.get(name)
    
    def register_logger(self, name: str, logger: Logger) -> None:
        """Register a logger instance."""
        self._loggers[name] = logger
    
    def close_logger(self, name: str) -> bool:
        """Close all handlers for a logger and remove it from registry."""
        if name in self._loggers:
            logger = self._loggers[name]
            # Close all handlers
            for handler in logger.handlers:
                if hasattr(handler, 'close'):
                    handler.close()
            # Remove from registry
            del self._loggers[name]
            return True
        return False
    
    def close_all(self) -> None:
        """Close all registered loggers."""
        for name in list(self._loggers.keys()):
            self.close_logger(name)
    
    def get_all_loggers(self) -> Dict[str, Logger]:
        """Get all registered loggers."""
        return self._loggers.copy()


# Global registry instance
_registry = LoggerRegistry()


def get_logger(name: str) -> Optional[Logger]:
    """Get a logger instance by name from the registry."""
    return _registry.get_logger(name)


def register_logger(name: str, logger: Logger) -> None:
    """Register a logger instance in the registry."""
    _registry.register_logger(name, logger)


def close_logger(name: str) -> bool:
    """Close a logger and remove it from the registry."""
    return _registry.close_logger(name)


def close_all_loggers() -> None:
    """Close all registered loggers."""
    _registry.close_all()


def get_all_loggers() -> Dict[str, Logger]:
    """Get all registered loggers."""
    return _registry.get_all_loggers() 