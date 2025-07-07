# Portable Logger Library

A self-contained, portable logging library that can be easily copied into any Python project. No external dependencies required!

## Features

- **Portable**: Just copy the `Logger` folder into your project
- **No Dependencies**: Uses only Python standard library
- **Multiple Output Formats**: Console, file, JSON, colored output
- **Configurable**: Multiple log levels, formatters, and handlers
- **Production Ready**: File rotation, error handling, structured logging

## Quick Start

### Basic Usage

```python
from Logger import create_logger, get_logger, close_all_loggers, LogLevel

# Initialize the logger once at the start of your program
logger = create_logger("myapp", level=LogLevel.DEBUG)

# Use it throughout your program
logger.info("Application started")
logger.warning("This is a warning")
logger.error("Something went wrong")

# Close all loggers at the end (optional, happens automatically)
close_all_loggers()
```

### Advanced Setup

For advanced usage, you can import the internal classes directly:

```python
from Logger.logger import Logger, LogLevel
from Logger.handlers import ConsoleHandler, FileHandler
from Logger.formatters import ColoredFormatter

# Create custom logger
logger = Logger("myapp")
logger.set_level(LogLevel.DEBUG)

# Add console handler with colors
console_handler = ConsoleHandler()
console_handler.set_formatter(ColoredFormatter())
logger.add_handler(console_handler)

# Add file handler
file_handler = FileHandler("logs/app.log")
logger.add_handler(file_handler)

# Use it
logger.debug("Debug message")
logger.info("Info message")
```

## Configuration Helpers

For advanced configuration, you can import the setup functions directly:

```python
from Logger.config import (
    setup_development_logger,
    setup_production_logger,
    setup_json_logger,
    setup_rotating_logger
)

# Development logger (colored console output)
dev_logger = setup_development_logger("myapp")

# Production logger (file output)
prod_logger = setup_production_logger("myapp", "app.log")

# JSON logger (for log aggregation)
json_logger = setup_json_logger("myapp", "app.json.log")

# Rotating file logger (keeps max 100 files)
rotating_logger = setup_rotating_logger("myapp", "app.log", max_files=100)
```

## Log Levels

- `DEBUG`: Detailed information for debugging
- `INFO`: General information about program execution
- `WARNING`: Indicate a potential problem
- `ERROR`: A more serious problem
- `CRITICAL`: A critical problem that may prevent the program from running

## Formatters

### SimpleFormatter
Default text format: `[timestamp] LEVEL name: message`

### ColoredFormatter
Same as SimpleFormatter but with ANSI colors for different log levels.

### JSONFormatter
Structured JSON output for log aggregation systems.

### TemplateFormatter
Custom format using template strings.

## Handlers

### ConsoleHandler
Outputs to console (stdout/stderr).

### FileHandler
Outputs to a file.

### RotatingFileHandler
Rotates log files based on size. Automatically deletes oldest files when exceeding the maximum file limit.

### TimedRotatingFileHandler
Rotates log files based on time intervals. Automatically deletes oldest files when exceeding the maximum file limit.

### MemoryHandler
Stores logs in memory (useful for testing).

## Examples

### Basic Application

```python
from Logger import create_logger, get_logger, close_all_loggers
import atexit

# Initialize logger once at program start
logger = create_logger("myapp")

def main():
    logger.info("Starting application")
    
    try:
        # Your application code here
        result = process_data()
        logger.info("Processing completed successfully")
        return result
    except Exception as e:
        logger.exception("Processing failed")
        raise

def cleanup():
    """Cleanup function to close all loggers."""
    close_all_loggers()

if __name__ == "__main__":
    # Register cleanup to run at exit
    atexit.register(cleanup)
    main()
```

### Web Application

```python
from Logger.config import setup_multi_handler_logger

# Setup logger with console and file output
logger = setup_multi_handler_logger(
    name="webapp",
    console=True,
    log_file="app.log",  # Will be created in logs/app.log
    error_file="error.log"  # Will be created in logs/error.log
)
```

def handle_request(request):
    logger.info("Processing request", extra={
        "method": request.method,
        "path": request.path,
        "ip": request.ip
    })
    
    try:
        # Process request
        response = process_request(request)
        logger.info("Request processed successfully")
        return response
    except Exception as e:
        logger.exception("Request processing failed")
        return error_response()
```

### API Service

```python
from Logger.config import setup_json_logger

# JSON logger for API services
logger = setup_json_logger("api", "api.json.log")  # Will be created in logs/api.json.log

def api_endpoint(data):
    logger.info("API call received", extra={
        "endpoint": "/api/data",
        "user_id": data.get("user_id"),
        "request_size": len(str(data))
    })
    
    # Process API call
    result = process_api_call(data)
    
    logger.info("API call completed", extra={
        "endpoint": "/api/data",
        "response_time": result.response_time,
        "status": "success"
    })
    
    return result
```

## Installation

Simply copy the `Logger` folder into your project:

```bash
cp -r Logger /path/to/your/project/
```

Then import it:

```python
from Logger import create_logger, get_logger, close_all_loggers, LogLevel
```

## File Structure

```
Logger/
├── __init__.py          # Main module exports
├── logger.py           # Core Logger and LogLevel classes
├── formatters.py       # Log formatters
├── handlers.py         # Log handlers
├── config.py           # Configuration helpers
├── registry.py         # Logger registry for singleton pattern
├── setup.py            # Optional setup script
├── requirements.txt    # Dependencies (none required)
├── LICENSE             # MIT License
├── .gitignore          # Git ignore rules
├── logs/               # Log files directory
│   └── .gitkeep       # Ensures directory is included in version control
└── README.md          # This file
```

## Best Practices

1. **Use meaningful logger names**: Use module or class names as logger names
2. **Set appropriate log levels**: Use DEBUG for development, INFO for production
3. **Include context**: Use the `extra` parameter to add relevant information
4. **Handle exceptions properly**: Use `logger.exception()` for automatic traceback
5. **Use structured logging**: Consider JSON format for production systems

## Migration from Standard Library

If you're currently using Python's built-in `logging` module, this library provides a similar API:

```python
# Standard library
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("myapp")

# This library
from Logger import get_logger
logger = get_logger("myapp")
```

## Contributing

This is a self-contained library designed for portability. If you need additional features, you can extend the classes or create your own formatters and handlers.

## License

This library is provided as-is for use in any project. 