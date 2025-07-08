/**
 * Example usage of the Portable Logger Library (JavaScript)
 *
 * This example demonstrates basic usage: creating a logger, logging at all levels, and logging extra data and exceptions.
 */

import { createLogger, LogLevel } from './Logger/index.js';

// Create a logger with console and file output
const logger = createLogger('example', {
    level: 'DEBUG',
    console: true,
    file: 'example.log',
    colored: true
});

logger.debug('Debug message');
logger.info('Info message');
logger.warning('Warning message');
logger.error('Error message');
logger.critical('Critical message');

// Log with extra data
logger.info('User logged in', { userId: 123, ip: '192.168.1.1' });

// Log an exception
try {
    throw new Error('Something went wrong');
} catch (error) {
    logger.exception('An exception occurred', error);
}

console.log('\nCheck the Logger/logs/ directory for generated log files.'); 