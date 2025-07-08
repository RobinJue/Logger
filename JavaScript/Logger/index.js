/**
 * Portable Logger Library for Node.js
 * 
 * A self-contained, portable logging library that can be easily copied into projects.
 * Provides comprehensive logging functionality with multiple formatters and handlers.
 * 
 * @author Robin Jüngerich
 * @license MIT
 */

// Core exports
export { LogLevel } from './Logger.js';

// Public API functions
export { getLogger, closeAllLoggers } from './registry.js';

// Configuration helpers
export { 
    setupBasicLogger,
    setupDevelopmentLogger,
    setupProductionLogger,
    setupJsonLogger,
    setupRotatingLogger,
    setupMultiHandlerLogger,
    quickLogger
} from './config.js';

// Internal classes (for advanced usage)
export { Logger, LogRecord, getLogLevelName } from './Logger.js';
export { 
    Formatter, 
    SimpleFormatter, 
    JSONFormatter, 
    ColoredFormatter, 
    TemplateFormatter 
} from './formatters.js';
export { 
    Handler, 
    ConsoleHandler, 
    FileHandler, 
    RotatingFileHandler, 
    TimedRotatingFileHandler, 
    NullHandler, 
    MemoryHandler 
} from './handlers.js';

// Import functions needed for createLogger
import { getLogger } from './registry.js';
import { LogLevel } from './Logger.js';
import { 
    setupBasicLogger,
    setupJsonLogger,
    setupRotatingLogger
} from './config.js';

/**
 * Create a logger with the given name and configuration.
 * This is the main entry point for most users.
 * 
 * @param {string} name - Logger name
 * @param {Object} options - Configuration options
 * @param {string} options.level - Log level ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
 * @param {boolean} options.console - Whether to output to console (default: true)
 * @param {string} options.file - Optional file path for file output
 * @param {boolean} options.colored - Whether to use colored output (default: true)
 * @param {boolean} options.json - Whether to use JSON format (default: false)
 * @param {boolean} options.rotating - Whether to use rotating file handler (default: false)
 * @param {number} options.maxBytes - Max bytes for rotating handler (default: 10MB)
 * @param {number} options.backupCount - Number of backup files (default: 5)
 * @returns {Logger} Configured logger instance
 */
export function createLogger(name = "default", options = {}) {
    const {
        level = "INFO",
        console = true,
        file = null,
        colored = true,
        json = false,
        rotating = false,
        maxBytes = 10 * 1024 * 1024,
        backupCount = 5
    } = options;

    // Check if logger already exists
    const existingLogger = getLogger(name);
    if (existingLogger) {
        return existingLogger;
    }

    // Convert string level to numeric LogLevel
    const levelMap = {
        "DEBUG": LogLevel.DEBUG,
        "INFO": LogLevel.INFO,
        "WARNING": LogLevel.WARNING,
        "ERROR": LogLevel.ERROR,
        "CRITICAL": LogLevel.CRITICAL
    };
    
    const numericLevel = levelMap[level.toUpperCase()] || LogLevel.INFO;

    // Create logger based on options
    if (json) {
        return setupJsonLogger(name, file);
    } else if (rotating) {
        return setupRotatingLogger(name, file, maxBytes, backupCount);
    } else {
        return setupBasicLogger(name, numericLevel, console, file, colored);
    }
} 