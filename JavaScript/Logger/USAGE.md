# Logger Library Usage Guide

This guide provides practical examples and usage patterns for the Portable Logger Library.

## Basic Usage Patterns

### 1. Simple Application Logging

```javascript
import { createLogger } from './Logger/index.js';

// Create a basic logger
const logger = createLogger('myapp');

// Use throughout your application
logger.info('Application started');
logger.debug('Debug information');
logger.warning('Warning message');
logger.error('Error occurred');
```

### 2. Development vs Production

```javascript
import { setupDevelopmentLogger, setupProductionLogger } from './Logger/index.js';

// In development
const devLogger = setupDevelopmentLogger('dev');
devLogger.debug('Detailed debug info');

// In production
const prodLogger = setupProductionLogger('prod', 'production.log');
prodLogger.info('Production log message');
```

### 3. Multi-Module Application

```javascript
// main.js
import { createLogger } from './Logger/index.js';

const appLogger = createLogger('app', { file: 'app.log' });

// module1.js
import { getLogger } from './Logger/index.js';

const logger = getLogger('app').getChild('module1');
logger.info('Module 1 initialized');

// module2.js
import { getLogger } from './Logger/index.js';

const logger = getLogger('app').getChild('module2');
logger.info('Module 2 initialized');
```

## Advanced Usage Patterns

### 1. Structured Logging with JSON

```javascript
import { setupJsonLogger } from './Logger/index.js';

const logger = setupJsonLogger('api', 'api.json.log');

// Log structured data
logger.info('User login attempt', {
    userId: 123,
    ip: '192.168.1.1',
    userAgent: 'Mozilla/5.0...',
    timestamp: new Date().toISOString()
});

logger.error('Database connection failed', {
    error: 'Connection timeout',
    retryCount: 3,
    database: 'users_db'
});
```

### 2. Error Handling and Exceptions

```javascript
import { createLogger } from './Logger/index.js';

const logger = createLogger('error-handler');

// Log exceptions with stack traces
try {
    // Some risky operation
    throw new Error('Database connection failed');
} catch (error) {
    logger.exception('Failed to connect to database', error, {
        database: 'users_db',
        retryAttempt: 1
    });
}

// Log errors with context
logger.error('API request failed', {
    endpoint: '/api/users',
    statusCode: 500,
    responseTime: 1500,
    userId: 123
});
```

### 3. Performance Monitoring

```javascript
import { createLogger } from './Logger/index.js';

const logger = createLogger('performance');

function measurePerformance(operation, fn) {
    const start = Date.now();
    try {
        const result = fn();
        const duration = Date.now() - start;
        
        if (duration > 1000) {
            logger.warning('Slow operation detected', {
                operation,
                duration,
                threshold: 1000
            });
        } else {
            logger.debug('Operation completed', {
                operation,
                duration
            });
        }
        
        return result;
    } catch (error) {
        const duration = Date.now() - start;
        logger.error('Operation failed', {
            operation,
            duration,
            error: error.message
        });
        throw error;
    }
}

// Usage
measurePerformance('database-query', () => {
    // Your database query here
    return db.query('SELECT * FROM users');
});
```

### 4. Request/Response Logging

```javascript
import { createLogger } from './Logger/index.js';

const logger = createLogger('http', { file: 'http.log' });

// Express.js middleware example
function requestLogger(req, res, next) {
    const start = Date.now();
    
    // Log request
    logger.info('HTTP Request', {
        method: req.method,
        url: req.url,
        ip: req.ip,
        userAgent: req.get('User-Agent'),
        userId: req.user?.id
    });
    
    // Override res.end to log response
    const originalEnd = res.end;
    res.end = function(chunk, encoding) {
        const duration = Date.now() - start;
        
        logger.info('HTTP Response', {
            method: req.method,
            url: req.url,
            statusCode: res.statusCode,
            duration,
            contentLength: res.get('Content-Length')
        });
        
        originalEnd.call(this, chunk, encoding);
    };
    
    next();
}
```

### 5. Rotating Log Files

```javascript
import { setupRotatingLogger } from './Logger/index.js';

// Create rotating logger (1MB max, 5 backups)
const logger = setupRotatingLogger('app', 'app.log', 1024 * 1024, 5);

// Log many messages to trigger rotation
for (let i = 0; i < 10000; i++) {
    logger.info(`Log message ${i}`, { 
        iteration: i,
        timestamp: new Date().toISOString()
    });
}
```

### 6. Custom Formatters

```javascript
import { Logger } from './Logger/index.js';
import { TemplateFormatter } from './Logger/index.js';
import { ConsoleHandler } from './Logger/index.js';

const logger = new Logger('custom');

// Custom template formatter
const formatter = new TemplateFormatter(
    '{timestamp} | {level} | {name} | {message} | {extra}'
);

const handler = new ConsoleHandler();
handler.setFormatter(formatter);
logger.addHandler(handler);

logger.info('Custom formatted message', { userId: 123 });
```

### 7. Memory Handler for Testing

```javascript
import { Logger } from './Logger/index.js';
import { MemoryHandler } from './Logger/index.js';

const logger = new Logger('test');
const memoryHandler = new MemoryHandler(100); // Store last 100 records
logger.addHandler(memoryHandler);

// Log some messages
logger.info('Test message 1');
logger.error('Test message 2');

// Retrieve logged records
const records = memoryHandler.getRecords();
console.log('Logged records:', records.length);

// Clear memory
memoryHandler.clear();
```

## Configuration Examples

### 1. Environment-Based Configuration

```javascript
import { createLogger } from './Logger/index.js';

const isDevelopment = process.env.NODE_ENV === 'development';
const isProduction = process.env.NODE_ENV === 'production';

let logger;

if (isDevelopment) {
    logger = createLogger('app', {
        level: 'DEBUG',
        console: true,
        colored: true
    });
} else if (isProduction) {
    logger = createLogger('app', {
        level: 'INFO',
        console: false,
        file: 'app.log',
        rotating: true,
        maxBytes: 10 * 1024 * 1024, // 10MB
        backupCount: 10
    });
} else {
    logger = createLogger('app', {
        level: 'WARNING',
        console: true,
        colored: false
    });
}
```

### 2. Multiple Handlers for Different Purposes

```javascript
import { Logger } from './Logger/index.js';
import { ConsoleHandler, FileHandler } from './Logger/index.js';
import { ColoredFormatter, JSONFormatter } from './Logger/index.js';

const logger = new Logger('multi-handler');

// Console handler for all levels with colors
const consoleHandler = new ConsoleHandler();
consoleHandler.setFormatter(new ColoredFormatter());
logger.addHandler(consoleHandler);

// File handler for errors only
const errorHandler = new FileHandler('errors.log');
errorHandler.setFormatter(new JSONFormatter());
errorHandler.setLevel(LogLevel.ERROR);
logger.addHandler(errorHandler);

// File handler for all levels in JSON format
const jsonHandler = new FileHandler('all.json.log');
jsonHandler.setFormatter(new JSONFormatter());
logger.addHandler(jsonHandler);
```

### 3. Child Logger Hierarchy

```javascript
import { createLogger } from './Logger/index.js';

// Main application logger
const appLogger = createLogger('app', { file: 'app.log' });

// Module-specific loggers
const dbLogger = appLogger.getChild('database');
const apiLogger = appLogger.getChild('api');
const authLogger = appLogger.getChild('auth');

// Usage in different modules
dbLogger.info('Database connection established');
apiLogger.info('API endpoint called', { endpoint: '/users' });
authLogger.warning('Failed login attempt', { ip: '192.168.1.1' });

// Output will show hierarchy: app.database, app.api, app.auth
```

## Best Practices

### 1. Logger Naming

```javascript
// Good: Descriptive names
const logger = createLogger('user-service');
const logger = createLogger('payment-processor');
const logger = createLogger('email-sender');

// Avoid: Generic names
const logger = createLogger('logger');
const logger = createLogger('log');
```

### 2. Log Levels

```javascript
// DEBUG: Detailed information for debugging
logger.debug('SQL query executed', { query: 'SELECT * FROM users', duration: 45 });

// INFO: General information about application flow
logger.info('User registered successfully', { userId: 123, email: 'user@example.com' });

// WARNING: Something unexpected happened but the application can continue
logger.warning('Database connection slow', { responseTime: 2000, threshold: 1000 });

// ERROR: An error occurred that prevented a specific operation
logger.error('Failed to send email', { userId: 123, error: 'SMTP connection failed' });

// CRITICAL: A critical error that may cause the application to fail
logger.critical('Database connection lost', { database: 'users_db', error: 'Connection timeout' });
```

### 3. Structured Data

```javascript
// Good: Structured data with context
logger.info('Order processed', {
    orderId: 456,
    userId: 123,
    amount: 99.99,
    paymentMethod: 'credit_card',
    status: 'completed'
});

// Avoid: Unstructured messages
logger.info('Order 456 processed for user 123 with amount 99.99');
```

### 4. Exception Handling

```javascript
// Good: Log exceptions with context
try {
    const result = await riskyOperation();
    logger.info('Operation completed successfully', { result });
} catch (error) {
    logger.exception('Operation failed', error, {
        operation: 'riskyOperation',
        userId: 123,
        retryAttempt: 1
    });
    throw error; // Re-throw if needed
}
```

### 5. Performance Considerations

```javascript
// Good: Use appropriate log levels
logger.debug('Detailed debug info'); // Only in development
logger.info('Important business event'); // Always log

// Avoid: Logging too much in production
logger.debug('Every single step'); // This will impact performance
```

## Integration Examples

### 1. Express.js Integration

```javascript
import express from 'express';
import { createLogger } from './Logger/index.js';

const app = express();
const logger = createLogger('express-app', { file: 'express.log' });

// Request logging middleware
app.use((req, res, next) => {
    const start = Date.now();
    
    res.on('finish', () => {
        const duration = Date.now() - start;
        logger.info('HTTP Request', {
            method: req.method,
            url: req.url,
            statusCode: res.statusCode,
            duration,
            ip: req.ip
        });
    });
    
    next();
});

app.get('/users', (req, res) => {
    logger.info('Fetching users', { userId: req.user?.id });
    res.json({ users: [] });
});
```

### 2. Database Integration

```javascript
import { createLogger } from './Logger/index.js';

const logger = createLogger('database', { file: 'database.log' });

class Database {
    async query(sql, params) {
        const start = Date.now();
        
        try {
            logger.debug('Executing query', { sql, params });
            const result = await this.executeQuery(sql, params);
            const duration = Date.now() - start;
            
            logger.debug('Query completed', { 
                sql, 
                duration, 
                rowCount: result.length 
            });
            
            return result;
        } catch (error) {
            const duration = Date.now() - start;
            logger.error('Query failed', { 
                sql, 
                params, 
                duration, 
                error: error.message 
            });
            throw error;
        }
    }
}
```

This usage guide covers the most common patterns and best practices for using the Portable Logger Library effectively in your Node.js applications. 