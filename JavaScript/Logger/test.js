/**
 * Comprehensive Example and Test for the Portable Logger Library
 * 
 * This example demonstrates all features of the Logger library and serves as a functional test.
 * It covers all formatters, handlers, log levels, and advanced usage patterns.
 */

import { 
    createLogger, 
    getLogger, 
    closeAllLoggers, 
    LogLevel,
    setupDevelopmentLogger,
    setupProductionLogger,
    setupJsonLogger,
    setupRotatingLogger,
    setupMultiHandlerLogger,
    Logger,
    SimpleFormatter,
    JSONFormatter,
    ColoredFormatter,
    TemplateFormatter,
    ConsoleHandler,
    FileHandler,
    RotatingFileHandler,
    TimedRotatingFileHandler,
    MemoryHandler
} from './index.js';

console.log('🚀 === JavaScript Logger Library - Comprehensive Example & Test ===\n');

// Test counter for validation
let testPassed = 0;
let testTotal = 0;

function runTest(testName, testFunction) {
    testTotal++;
    try {
        testFunction();
        console.log(`✅ ${testName} - PASSED`);
        testPassed++;
    } catch (error) {
        console.log(`❌ ${testName} - FAILED: ${error.message}`);
    }
}

// Test 1: Basic Logger Creation
runTest('Basic Logger Creation', () => {
    const logger = createLogger('basic-test', {
        level: 'DEBUG',
        console: true,
        file: 'basic-test.log',
        colored: true
    });
    
    logger.debug('Debug message from basic logger');
    logger.info('Info message from basic logger');
    logger.warning('Warning message from basic logger');
    logger.error('Error message from basic logger');
    logger.critical('Critical message from basic logger');
    
    // Test with extra data
    logger.info('User action', { userId: 123, action: 'login', timestamp: new Date().toISOString() });
    
    // Test exception logging
    try {
        throw new Error('Test exception for logging');
    } catch (error) {
        logger.exception('Exception occurred during test', error, { testPhase: 'basic' });
    }
});

// Test 2: Development Logger
runTest('Development Logger Setup', () => {
    const devLogger = setupDevelopmentLogger('dev-test');
    devLogger.debug('Development debug message');
    devLogger.info('Development info message');
    devLogger.warning('Development warning message');
});

// Test 3: Production Logger
runTest('Production Logger Setup', () => {
    const prodLogger = setupProductionLogger('prod-test', 'production-test.log');
    prodLogger.info('Production info message');
    prodLogger.error('Production error message');
    prodLogger.critical('Production critical message');
});

// Test 4: JSON Logger
runTest('JSON Logger Setup', () => {
    const jsonLogger = setupJsonLogger('json-test', 'json-test.log');
    
    // Test structured logging
    jsonLogger.info('User registration', {
        userId: 456,
        email: 'user@example.com',
        registrationMethod: 'email',
        timestamp: new Date().toISOString(),
        metadata: {
            source: 'web',
            userAgent: 'Mozilla/5.0...'
        }
    });
    
    jsonLogger.error('API request failed', {
        endpoint: '/api/users',
        method: 'POST',
        statusCode: 500,
        responseTime: 1500,
        error: 'Database connection timeout'
    });
});

// Test 5: Rotating Logger
runTest('Rotating Logger Setup', () => {
    const rotatingLogger = setupRotatingLogger('rotating-test', 'rotating-test.log', 1024, 3);
    
    // Log multiple messages to test rotation
    for (let i = 0; i < 50; i++) {
        rotatingLogger.info(`Rotating log message ${i}`, { 
            iteration: i,
            timestamp: new Date().toISOString(),
            data: 'x'.repeat(20) // Add some data to fill the file faster
        });
    }
});

// Test 6: Multi-Handler Logger
runTest('Multi-Handler Logger Setup', () => {
    const multiLogger = setupMultiHandlerLogger('multi-test', true, 'multi-test.log', 'multi-test-errors.log');
    
    multiLogger.debug('Debug message to console and file');
    multiLogger.info('Info message to console and file');
    multiLogger.warning('Warning message to console and file');
    multiLogger.error('Error message to console, main file, and error file');
    multiLogger.critical('Critical message to console, main file, and error file');
});

// Test 7: Logger Registry and Singleton Pattern
runTest('Logger Registry and Singleton Pattern', () => {
    // Create a logger
    const logger1 = createLogger('registry-test');
    logger1.info('First logger instance');
    
    // Try to get the same logger
    const logger2 = getLogger('registry-test');
    logger2.info('Second logger instance (should be the same)');
    
    // Verify they are the same instance
    if (logger1 !== logger2) {
        throw new Error('Logger registry singleton pattern failed');
    }
    
    // Test non-existent logger
    const nonExistent = getLogger('non-existent');
    if (nonExistent !== null) {
        throw new Error('Non-existent logger should return null');
    }
});

// Test 8: Child Loggers
runTest('Child Logger Hierarchy', () => {
    const parentLogger = createLogger('parent-test', { file: 'parent-test.log' });
    
    const child1 = parentLogger.getChild('child1');
    const child2 = parentLogger.getChild('child2');
    const grandchild = child1.getChild('grandchild');
    
    parentLogger.info('Parent logger message');
    child1.info('Child 1 logger message');
    child2.info('Child 2 logger message');
    grandchild.info('Grandchild logger message');
    
    // Test that child loggers are cached
    const child1Again = parentLogger.getChild('child1');
    if (child1 !== child1Again) {
        throw new Error('Child logger caching failed');
    }
});

// Test 9: Log Levels
runTest('Log Level Filtering', () => {
    const levelLogger = createLogger('level-test', { level: 'WARNING' });
    
    // These should not appear
    levelLogger.debug('This debug message should not appear');
    levelLogger.info('This info message should not appear');
    
    // These should appear
    levelLogger.warning('This warning message should appear');
    levelLogger.error('This error message should appear');
    levelLogger.critical('This critical message should appear');
});

// Test 10: Custom Configuration
runTest('Custom Logger Configuration', () => {
    const customLogger = new Logger('custom-test');
    customLogger.setLevel(LogLevel.DEBUG);
    
    // Console handler with colored output
    const consoleHandler = new ConsoleHandler();
    consoleHandler.setFormatter(new ColoredFormatter());
    customLogger.addHandler(consoleHandler);
    
    // File handler with JSON format
    const fileHandler = new FileHandler('custom-test.json.log');
    fileHandler.setFormatter(new JSONFormatter());
    customLogger.addHandler(fileHandler);
    
    // Memory handler for testing
    const memoryHandler = new MemoryHandler(10);
    customLogger.addHandler(memoryHandler);
    
    customLogger.info('Custom configured logger message');
    customLogger.debug('Debug message with custom setup');
    customLogger.error('Error message with custom setup');
    
    // Test memory handler
    const records = memoryHandler.getRecords();
    if (records.length !== 3) {
        throw new Error(`Memory handler should have 3 records, got ${records.length}`);
    }
    
    // Test record structure
    const firstRecord = records[0];
    if (!firstRecord.name || !firstRecord.message || !firstRecord.timestamp) {
        throw new Error('Log record structure is invalid');
    }
});

// Test 11: Template Formatter
runTest('Template Formatter', () => {
    const templateLogger = new Logger('template-test');
    
    const templateFormatter = new TemplateFormatter(
        'CUSTOM | {timestamp} | {level} | {name} | {message} | {extra}'
    );
    
    const handler = new ConsoleHandler();
    handler.setFormatter(templateFormatter);
    templateLogger.addHandler(handler);
    
    templateLogger.info('Template formatted message', { userId: 789, action: 'test' });
});

// Test 12: Performance Test
runTest('Performance Test', () => {
    const perfLogger = createLogger('perf-test', { level: 'INFO' });
    
    const start = Date.now();
    const iterations = 1000;
    
    for (let i = 0; i < iterations; i++) {
        perfLogger.info(`Performance test message ${i}`);
    }
    
    const duration = Date.now() - start;
    const rate = Math.round(iterations / (duration / 1000));
    
    console.log(`   Performance: ${iterations} messages in ${duration}ms (${rate} msg/sec)`);
    
    if (rate < 100) {
        throw new Error(`Performance too slow: ${rate} msg/sec`);
    }
});

// Test 13: Error Handling
runTest('Error Handling', () => {
    const errorLogger = createLogger('error-test');
    
    // Test handler error handling
    const badHandler = {
        emit: () => {
            throw new Error('Handler error');
        }
    };
    
    errorLogger.addHandler(badHandler);
    
    // This should not crash the application
    errorLogger.info('Message with bad handler');
    
    // Remove the bad handler
    errorLogger.removeHandler(badHandler);
    errorLogger.info('Message after removing bad handler');
});

// Test 14: File Handler Operations
runTest('File Handler Operations', () => {
    const fileLogger = new Logger('file-test');
    
    const fileHandler = new FileHandler('file-test.log');
    fileHandler.setFormatter(new SimpleFormatter());
    fileLogger.addHandler(fileHandler);
    
    fileLogger.info('File handler test message');
    fileLogger.error('File handler error message');
    
    // Test handler close
    fileHandler.close();
    
    // This should not cause an error
    fileLogger.info('Message after handler close');
});

// Test 15: Integration Test
runTest('Integration Test - Complete Workflow', () => {
    // Simulate a complete application workflow
    const appLogger = createLogger('integration-test', {
        level: 'DEBUG',
        console: true,
        file: 'integration-test.log',
        colored: true
    });
    
    // Application startup
    appLogger.info('Application starting up', { version: '1.0.0', environment: 'test' });
    
    // Database connection
    const dbLogger = appLogger.getChild('database');
    dbLogger.info('Connecting to database', { host: 'localhost', port: 5432 });
    
    try {
        // Simulate database operation
        dbLogger.debug('Executing query: SELECT * FROM users');
        // Simulate error
        throw new Error('Connection timeout');
    } catch (error) {
        dbLogger.exception('Database connection failed', error, { retryAttempt: 1 });
    }
    
    // API request
    const apiLogger = appLogger.getChild('api');
    apiLogger.info('Processing API request', { 
        method: 'POST', 
        endpoint: '/api/users',
        userId: 123 
    });
    
    // Application shutdown
    appLogger.info('Application shutting down', { reason: 'test completion' });
});

console.log('\n📊 === Test Results ===');
console.log(`Tests Passed: ${testPassed}/${testTotal}`);
console.log(`Success Rate: ${Math.round((testPassed / testTotal) * 100)}%`);

if (testPassed === testTotal) {
    console.log('🎉 All tests passed! The Logger library is working correctly.');
} else {
    console.log('⚠️  Some tests failed. Please check the implementation.');
}

console.log('\n📁 Check the Logger/logs/ directory for generated log files:');
console.log('- basic-test.log');
console.log('- production-test.log');
console.log('- json-test.log');
console.log('- rotating-test.log');
console.log('- multi-test.log');
console.log('- multi-test-errors.log');
console.log('- parent-test.log');
console.log('- custom-test.json.log');
console.log('- file-test.log');
console.log('- integration-test.log');

// Clean up
setTimeout(() => {
    console.log('\n🧹 Closing all loggers...');
    closeAllLoggers();
    console.log('✅ All loggers closed successfully.');
    console.log('\n✨ Example and test completed!');
}, 1000); 