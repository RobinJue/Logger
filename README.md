# Portable Logger Library

A comprehensive, portable logging library available in both Python and JavaScript with consistent APIs and features.

## Overview

This library provides a robust logging solution with:
- **Multiple log levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Various formatters**: Simple, JSON, Colored, Template
- **Flexible handlers**: Console, File, Rotating, TimedRotating, Memory
- **Configuration helpers**: Quick setup for development, production, and specialized use cases
- **Singleton registry**: Manage multiple loggers across your application

## Languages

### Python
- **Location**: `Python/Logger/`
- **Requirements**: Python 3.6+
- **Installation**: Copy the `Logger` folder to your project
- **Usage**: See `Python/USAGE.md` for detailed examples

### JavaScript
- **Location**: `JavaScript/Logger/`
- **Requirements**: Node.js 14+
- **Installation**: Copy the `Logger` folder to your project
- **Usage**: See `JavaScript/USAGE.md` for detailed examples

## Quick Start

### Python
```python
from Logger import create_logger, LogLevel

# Create a logger
logger = create_logger('myapp', level='INFO', console=True, file='app.log')

# Use it
logger.info('Application started')
logger.error('An error occurred', extra={'user_id': 123})
```

### JavaScript
```javascript
import { createLogger, LogLevel } from './Logger/index.js';

// Create a logger
const logger = create_logger('myapp', {
    level: 'INFO',
    console: true,
    file: 'app.log'
});

// Use it
logger.info('Application started');
logger.error('An error occurred', { userId: 123 });
```

## Features

### Core Features
- ✅ **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- ✅ **Formatters**: Simple, JSON, Colored, Template
- ✅ **Handlers**: Console, File, Rotating, TimedRotating, Memory
- ✅ **Configuration**: Development, Production, JSON, Rotating setups
- ✅ **Registry**: Singleton pattern for managing multiple loggers
- ✅ **Child Loggers**: Hierarchical logging with inheritance
- ✅ **Exception Handling**: Automatic stack trace logging
- ✅ **Extra Data**: Structured logging with additional context

### Advanced Features
- ✅ **File Rotation**: Size-based and time-based rotation
- ✅ **Colored Output**: ANSI color codes for console output
- ✅ **JSON Formatting**: Structured logging for machine processing
- ✅ **Template Formatting**: Customizable log message templates
- ✅ **Memory Buffering**: In-memory log storage with flush capabilities

## Project Structure

```
Logger/
├── Python/
│   ├── Logger/           # Python library
│   ├── example.py        # Basic usage example
│   └── USAGE.md         # Detailed usage guide
├── JavaScript/
│   ├── Logger/          # JavaScript library
│   ├── example.js       # Basic usage example
│   └── USAGE.md         # Detailed usage guide
├── LICENSE              # MIT License
└── README.md           # This file
```

## Installation

### For Python Projects
1. Copy the `Python/Logger/` folder to your project
2. Import and use as shown in the examples

### For JavaScript Projects
1. Copy the `JavaScript/Logger/` folder to your project
2. Import and use as shown in the examples

## Testing

Both versions include comprehensive test suites:

### Python
```bash
cd Python
python Logger/test.py
```

### JavaScript
```bash
cd JavaScript
node Logger/test.js
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

This is a portable library designed to be easily integrated into any project. Feel free to:
- Copy and modify for your specific needs
- Extend with additional formatters or handlers
- Adapt for other programming languages

## Examples

See the `example.py` and `example.js` files in each language directory for basic usage examples, and the `test.py` and `test.js` files for comprehensive feature demonstrations. 