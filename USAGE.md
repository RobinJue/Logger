# Logger Library Usage Guide

## Overview

This is a **portable, self-contained logging library** that you can copy into any Python project. No external dependencies required!

## Quick Start

### 1. Copy the Logger folder to your project

```bash
cp -r Logger /path/to/your/project/
```

### 2. Use it in your code

```python
# Simple usage
from Logger import get_logger

logger = get_logger("myapp")
logger.info("Hello, world!")
```

## File Structure

```
Logger/
├── __init__.py          # Main exports and convenience functions
├── logger.py           # Core Logger class and LogLevel enum
├── formatters.py       # Log formatters (Simple, JSON, Colored, etc.)
├── handlers.py         # Log handlers (Console, File, Rotating, etc.)
├── config.py           # Configuration helper functions
├── registry.py         # Logger registry for singleton pattern
├── setup.py            # Optional setup script
├── requirements.txt    # Dependencies (none required)
├── LICENSE             # MIT License
├── .gitignore          # Git ignore rules
├── logs/               # Log files directory
│   └── .gitkeep       # Ensures directory is included in version control
└── README.md          # Detailed documentation
```

## Basic Usage Examples

### Simple Logger
```python
from Logger import create_logger, get_logger, LogLevel

# Initialize once
logger = create_logger("myapp", level=LogLevel.DEBUG)

# Use throughout your program
logger.info("Application started")
logger.warning("This is a warning")
logger.error("Something went wrong")
```

### Custom Logger
```python
from Logger import Logger, LogLevel, ConsoleHandler, ColoredFormatter

logger = Logger("myapp")
logger.set_level(LogLevel.DEBUG)

handler = ConsoleHandler()
handler.set_formatter(ColoredFormatter())
logger.add_handler(handler)

logger.debug("Debug message")
logger.info("Info message")
```

### File Logging
```python
from Logger import Logger, FileHandler, SimpleFormatter

logger = Logger("myapp")
handler = FileHandler("app.log")
handler.set_formatter(SimpleFormatter())
logger.add_handler(handler)

logger.info("This will be written to app.log")
```

## Configuration Helpers

### Development Logger
```python
from Logger.config import setup_development_logger

logger = setup_development_logger("myapp")
# Colored console output, DEBUG level
```

### Production Logger
```python
from Logger.config import setup_production_logger

logger = setup_production_logger("myapp", "app.log")
# File output, INFO level
```

### JSON Logger
```python
from Logger.config import setup_json_logger

logger = setup_json_logger("myapp", "app.json.log")
# JSON format for log aggregation
```

### Rotating Logger
```python
from Logger.config import setup_rotating_logger

logger = setup_rotating_logger("myapp", "app.log", max_files=100)
# Automatically rotates log files
```

## Log Levels

- `DEBUG`: Detailed debugging information
- `INFO`: General information
- `WARNING`: Warning messages
- `ERROR`: Error messages
- `CRITICAL`: Critical errors

## Formatters

- `SimpleFormatter`: Basic text format
- `ColoredFormatter`: Colored console output
- `JSONFormatter`: JSON structured logging
- `TemplateFormatter`: Custom format strings

## Handlers

- `ConsoleHandler`: Output to console
- `FileHandler`: Output to file
- `RotatingFileHandler`: Rotate files by size
- `TimedRotatingFileHandler`: Rotate files by time
- `MemoryHandler`: Store in memory (for testing)

## Advanced Features

### Extra Fields
```python
logger.info("User login", extra={
    "user_id": 12345,
    "ip_address": "192.168.1.100"
})
```

### Exception Logging
```python
try:
    result = 1 / 0
except Exception:
    logger.exception("An error occurred")
    # Automatically includes traceback
```

### Child Loggers
```python
parent = get_logger("parent")
child = parent.get_child("child")
child.info("Child message")
```

## Testing

Run the test suite to see all features in action:

```bash
python3 test.py
```

## Migration from Standard Library

If you're using Python's built-in logging:

```python
# Old way
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("myapp")

# New way
from Logger import get_logger
logger = get_logger("myapp")
```

## Best Practices

1. **Use meaningful logger names** (module/class names)
2. **Set appropriate log levels** (DEBUG for dev, INFO for prod)
3. **Include context** with extra fields
4. **Use structured logging** for production systems
5. **Handle exceptions properly** with `logger.exception()`

## No Dependencies Required!

This library uses only Python standard library modules:
- `datetime`
- `enum`
- `json`
- `os`
- `sys`
- `traceback`
- `typing`

## Portability

The entire library is contained in the `Logger` folder. To use it in a new project:

1. Copy the `Logger` folder
2. Import and use immediately
3. No installation or dependencies needed

That's it! Your logging library is ready to use. 