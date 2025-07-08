/**
 * Configuration utilities for easy logger setup.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { Logger, LogLevel } from './Logger.js';
import { SimpleFormatter, JSONFormatter, ColoredFormatter } from './formatters.js';
import { ConsoleHandler, FileHandler, RotatingFileHandler } from './handlers.js';
import { registerLogger } from './registry.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Get the absolute path to the Logger/logs directory
const _LOGGER_DIR = path.dirname(__filename);
const _LOGS_DIR = path.join(_LOGGER_DIR, 'logs');

// Ensure logs directory exists
if (!fs.existsSync(_LOGS_DIR)) {
    fs.mkdirSync(_LOGS_DIR, { recursive: true });
}

/**
 * Get timestamp for log file naming.
 */
function _timestamp() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day}_${hours}-${minutes}-${seconds}`;
}

/**
 * Get absolute log path.
 */
function _absLogPath(filename, name = null) {
    // If filename is null, use timestamp-name.log
    if (filename === null && name !== null) {
        filename = `${_timestamp()}-${name}.log`;
    } else if (filename !== null && name !== null && !filename.endsWith('.log')) {
        filename = `${_timestamp()}-${filename}.log`;
    } else if (filename !== null && name !== null && filename === name) {
        filename = `${_timestamp()}-${name}.log`;
    } else if (filename !== null && !path.isAbsolute(filename) && !filename.startsWith(_LOGS_DIR)) {
        // If not absolute and not already in logs dir, add timestamp
        const base = path.basename(filename);
        filename = `${_timestamp()}-${base}`;
    }
    
    if (filename !== null && !path.isAbsolute(filename)) {
        filename = path.join(_LOGS_DIR, filename);
    }
    
    return filename;
}

/**
 * Setup a basic logger with common configuration.
 * 
 * @param {string} name - Logger name
 * @param {number} level - Minimum log level
 * @param {boolean} console - Whether to output to console
 * @param {string} file - Optional file path for file output (defaults to logs/{timestamp}-{name}.log)
 * @param {boolean} colored - Whether to use colored output (console only)
 */
export function setupBasicLogger(name = "default", level = LogLevel.INFO, console = true, file = null, colored = true) {
    const logger = new Logger(name);
    logger.setLevel(level);

    // Console handler
    if (console) {
        const consoleHandler = new ConsoleHandler();
        if (colored) {
            consoleHandler.setFormatter(new ColoredFormatter());
        } else {
            consoleHandler.setFormatter(new SimpleFormatter());
        }
        logger.addHandler(consoleHandler);
    }

    // File handler
    file = _absLogPath(file, name);
    if (file) {
        const fileHandler = new FileHandler(file);
        fileHandler.setFormatter(new SimpleFormatter());
        logger.addHandler(fileHandler);
    }

    // Register the logger
    registerLogger(name, logger);

    return logger;
}

/**
 * Setup a logger suitable for development with colored console output.
 */
export function setupDevelopmentLogger(name = "default") {
    return setupBasicLogger(
        name,
        LogLevel.DEBUG,
        true,
        null,
        true
    );
}

/**
 * Setup a logger suitable for production with file output.
 */
export function setupProductionLogger(name = "default", logFile = "app.log") {
    return setupBasicLogger(
        name,
        LogLevel.INFO,
        false,
        logFile,
        false
    );
}

/**
 * Setup a logger that outputs JSON format (useful for log aggregation).
 */
export function setupJsonLogger(name = "default", logFile = "app.json.log") {
    const logger = new Logger(name);
    logger.setLevel(LogLevel.INFO);
    
    logFile = _absLogPath(logFile, name);
    const fileHandler = new FileHandler(logFile);
    fileHandler.setFormatter(new JSONFormatter());
    logger.addHandler(fileHandler);

    // Register the logger
    registerLogger(name, logger);

    return logger;
}

/**
 * Setup a logger with rotating file output.
 */
export function setupRotatingLogger(name = "default", logFile = "app.log", maxBytes = 10 * 1024 * 1024, backupCount = 5, maxFiles = 100) {
    const logger = new Logger(name);
    logger.setLevel(LogLevel.INFO);
    
    logFile = _absLogPath(logFile, name);
    const rotatingHandler = new RotatingFileHandler(
        logFile,
        maxBytes,
        backupCount,
        maxFiles
    );
    rotatingHandler.setFormatter(new SimpleFormatter());
    logger.addHandler(rotatingHandler);

    // Register the logger
    registerLogger(name, logger);

    return logger;
}

/**
 * Setup a logger with multiple handlers for different purposes.
 */
export function setupMultiHandlerLogger(name = "default", console = true, logFile = "app.log", errorFile = "error.log") {
    const logger = new Logger(name);
    logger.setLevel(LogLevel.DEBUG);

    if (console) {
        const consoleHandler = new ConsoleHandler();
        consoleHandler.setFormatter(new ColoredFormatter());
        logger.addHandler(consoleHandler);
    }

    if (logFile) {
        logFile = _absLogPath(logFile, name);
        const fileHandler = new FileHandler(logFile);
        fileHandler.setFormatter(new SimpleFormatter());
        logger.addHandler(fileHandler);
    }

    if (errorFile) {
        errorFile = _absLogPath(errorFile, name);
        const errorHandler = new FileHandler(errorFile);
        errorHandler.setFormatter(new SimpleFormatter());
        errorHandler.setLevel(LogLevel.ERROR);
        logger.addHandler(errorHandler);
    }

    // Register the logger
    registerLogger(name, logger);

    return logger;
}

/**
 * Quick setup for a basic logger.
 * 
 * @param {string} name - Logger name
 * @param {string} level - Log level as string ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
 */
export function quickLogger(name = "default", level = "INFO") {
    const levelMap = {
        "DEBUG": LogLevel.DEBUG,
        "INFO": LogLevel.INFO,
        "WARNING": LogLevel.WARNING,
        "ERROR": LogLevel.ERROR,
        "CRITICAL": LogLevel.CRITICAL
    };

    const logLevel = levelMap[level.toUpperCase()] || LogLevel.INFO;
    return setupBasicLogger(name, logLevel);
} 