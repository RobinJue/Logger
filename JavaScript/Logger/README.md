# Portable Logger Library for Node.js

A self-contained, portable logging library for Node.js that can be easily copied into projects. Provides comprehensive logging functionality with multiple formatters and handlers.

## Features

- **Portable**: Single directory that can be copied into any project
- **Multiple Formatters**: Simple, JSON, Colored, and Template formatters
- **Multiple Handlers**: Console, File, Rotating File, Timed Rotating, Memory, and Null handlers
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Logger Registry**: Singleton pattern ensures one logger instance per name
- **Child Loggers**: Hierarchical logger structure
- **Exception Logging**: Built-in exception handling with stack traces
- **Configuration Helpers**: Pre-configured setups for common use cases
- **No Dependencies**: Pure Node.js with no external dependencies

## Quick Start

```javascript
import { createLogger } from './Logger/index.js';

// Create a basic logger
const logger = createLogger('myapp', {
    level: 'INFO',
    console: true,
    file: 'app.log',
    colored: true
});

// Use the logger
logger.info('Application started');
logger.error('An error occurred', { userId: 123 });
```

## Installation

Simply copy the `Logger` folder into your project:

```bash
cp -r Logger /path/to/your/project/
```

Then import it in your code:

```javascript
import { createLogger, LogLevel } from './Logger/index.js';
```

## API Reference

### Main Functions

#### `createLogger(name, options)`

Creates a new logger with the specified configuration.

**Parameters:**
- `name` (string): Logger name (default: "default")
- `options` (object): Configuration options
  - `level` (string): Log level ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
  - `console` (boolean): Whether to output to console (default: true)
  - `file` (string): Optional file path for file output
  - `colored` (boolean): Whether to use colored output (default: true)
  - `json` (boolean): Whether to use JSON format (default: false)
  - `rotating` (boolean): Whether to use rotating file handler (default: false)
  - `maxBytes` (number): Max bytes for rotating handler (default: 10MB)
  - `backupCount` (number): Number of backup files (default: 5)

**Returns:** Logger instance

#### `getLogger(name)`

Retrieves an existing logger by name.

**Parameters:**
- `name` (string): Logger name

**Returns:** Logger instance or null

#### `closeAllLoggers()`

Closes all registered loggers and their handlers.

### Log Levels

```javascript
import { LogLevel } from './Logger/index.js';

LogLevel.DEBUG    // 0
LogLevel.INFO     // 1
LogLevel.WARNING  // 2
LogLevel.ERROR    // 3
LogLevel.CRITICAL // 4
```

### Logger Methods

```javascript
const logger = createLogger('example');

// Basic logging
logger.debug('Debug message');
logger.info('Info message');
logger.warning('Warning message');
logger.error('Error message');
logger.critical('Critical message');

// Exception logging
try {
    throw new Error('Something went wrong');
} catch (error) {
    logger.exception('An exception occurred', error);
}

// Logging with extra data
logger.info('User action', { userId: 123, action: 'login' });

// Child loggers
const childLogger = logger.getChild('module');
childLogger.info('Message from child logger');
```

## Configuration Helpers

### Development Logger

```javascript
import { setupDevelopmentLogger } from './Logger/index.js';

const logger = setupDevelopmentLogger('dev');
// Creates logger with DEBUG level, colored console output
```

### Production Logger

```javascript
import { setupProductionLogger } from './Logger/index.js';

const logger = setupProductionLogger('prod', 'app.log');
// Creates logger with INFO level, file output only
```

### JSON Logger

```javascript
import { setupJsonLogger } from './Logger/index.js';

const logger = setupJsonLogger('json', 'app.json.log');
// Creates logger that outputs JSON format
```

### Rotating Logger

```javascript
import { setupRotatingLogger } from './Logger/index.js';

const logger = setupRotatingLogger('rotating', 'app.log', 1024 * 1024, 5);
// Creates logger with rotating file handler (1MB max, 5 backups)
```

## Formatters

### Simple Formatter

```javascript
import { SimpleFormatter } from './Logger/index.js';

const formatter = new SimpleFormatter();
// Output: [2024-01-01 12:00:00] INFO     example        : Message
```

### JSON Formatter

```javascript
import { JSONFormatter } from './Logger/index.js';

const formatter = new JSONFormatter();
// Output: {"level":"INFO","message":"Message","timestamp":"2024-01-01T12:00:00.000Z"}
```

### Colored Formatter

```javascript
import { ColoredFormatter } from './Logger/index.js';

const formatter = new ColoredFormatter();
// Output: Colored text with ANSI color codes
```

### Template Formatter

```javascript
import { TemplateFormatter } from './Logger/index.js';

const formatter = new TemplateFormatter('{timestamp} [{level}] {name}: {message}');
// Custom format using template variables
```

## Handlers

### Console Handler

```javascript
import { ConsoleHandler } from './Logger/index.js';

const handler = new ConsoleHandler();
// Outputs to stdout/stderr
```

### File Handler

```javascript
import { FileHandler } from './Logger/index.js';

const handler = new FileHandler('app.log');
// Outputs to file
```

### Rotating File Handler

```javascript
import { RotatingFileHandler } from './Logger/index.js';

const handler = new RotatingFileHandler('app.log', 1024 * 1024, 5);
// Rotates files when they reach 1MB, keeps 5 backups
```

### Timed Rotating File Handler

```javascript
import { TimedRotatingFileHandler } from './Logger/index.js';

const handler = new TimedRotatingFileHandler('app.log', 'midnight', 1, 5);
// Rotates files at midnight, keeps 5 backups
```

## Advanced Usage

### Custom Configuration

```javascript
import { Logger } from './Logger/index.js';
import { ColoredFormatter, JSONFormatter } from './Logger/index.js';
import { ConsoleHandler, FileHandler } from './Logger/index.js';

const logger = new Logger('custom');
logger.setLevel(LogLevel.DEBUG);

// Console handler with colored output
const consoleHandler = new ConsoleHandler();
consoleHandler.setFormatter(new ColoredFormatter());
logger.addHandler(consoleHandler);

// File handler with JSON format
const fileHandler = new FileHandler('custom.json.log');
fileHandler.setFormatter(new JSONFormatter());
logger.addHandler(fileHandler);
```

### Multi-Module Usage

```javascript
// In main.js
import { createLogger } from './Logger/index.js';

const logger = createLogger('app', { file: 'app.log' });

// In module1.js
import { getLogger } from './Logger/index.js';

const logger = getLogger('app').getChild('module1');
logger.info('Module 1 message');

// In module2.js
import { getLogger } from './Logger/index.js';

const logger = getLogger('app').getChild('module2');
logger.info('Module 2 message');
```

## File Structure

```
Logger/
├── index.js          # Main entry point and public API
├── Logger.js         # Core Logger class and LogLevel
├── formatters.js     # Log formatters
├── handlers.js       # Log handlers
├── config.js         # Configuration helpers
├── registry.js       # Logger registry
├── package.json      # Package metadata
├── example.js        # Usage examples
├── README.md         # This file
└── logs/             # Generated log files (created automatically)
    └── .gitignore    # Ignores log files in git
```

## Log Files

Log files are automatically created in the `logs/` directory with timestamps:

- `2024-01-01_12-00-00-example.log`
- `2024-01-01_12-00-00-app.json.log`
- etc.

## Requirements

- Node.js 14.0.0 or higher
- ES modules support (use `"type": "module"` in package.json)

## License

MIT License - see LICENSE file for details.

## Author

Robin Jüngerich

## Contributing

This is a portable library designed to be copied into projects. For improvements, please create a new version or fork the repository. 