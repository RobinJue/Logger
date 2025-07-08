/**
 * Core Logger implementation with LogLevel enum and main logging functionality.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Log levels in order of severity.
 */
export const LogLevel = {
    DEBUG: 0,
    INFO: 1,
    WARNING: 2,
    ERROR: 3,
    CRITICAL: 4
};

/**
 * Get the string representation of a log level.
 */
export function getLogLevelName(level) {
    return Object.keys(LogLevel).find(key => LogLevel[key] === level) || 'UNKNOWN';
}

/**
 * Represents a single log record with all relevant information.
 */
export class LogRecord {
    constructor(name, level, message, timestamp, extra = {}) {
        this.name = name;
        this.level = level;
        this.message = message;
        this.timestamp = timestamp;
        this.extra = extra;
    }
}

/**
 * Main Logger class that handles log messages and distributes them to handlers.
 */
export class Logger {
    constructor(name = "default") {
        this.name = name;
        this.level = LogLevel.INFO;
        this.handlers = [];
        this.propagate = true;
        this.parent = null;
        this.children = new Map();
    }

    /**
     * Set the minimum log level for this logger.
     */
    setLevel(level) {
        this.level = level;
    }

    /**
     * Add a handler to this logger.
     */
    addHandler(handler) {
        this.handlers.push(handler);
    }

    /**
     * Remove a handler from this logger.
     */
    removeHandler(handler) {
        const index = this.handlers.indexOf(handler);
        if (index > -1) {
            this.handlers.splice(index, 1);
        }
    }

    /**
     * Remove all handlers from this logger.
     */
    clearHandlers() {
        this.handlers = [];
    }

    /**
     * Get or create a child logger.
     */
    getChild(name) {
        if (!this.children.has(name)) {
            const child = new Logger(`${this.name}.${name}`);
            child.parent = this;
            child.level = this.level;
            child.handlers = [...this.handlers];
            this.children.set(name, child);
        }
        return this.children.get(name);
    }

    /**
     * Internal logging method.
     */
    _log(level, message, ...args) {
        if (level < this.level) {
            return;
        }

        // Format message with args
        let formattedMessage = message;
        if (args.length > 0) {
            formattedMessage = message.replace(/%s/g, () => args.shift());
        }

        // Create log record
        const record = new LogRecord(
            this.name,
            level,
            formattedMessage,
            new Date(),
            args.length > 0 ? args[0] : {}
        );

        // Send to handlers
        for (const handler of this.handlers) {
            try {
                handler.emit(record);
            } catch (error) {
                // Prevent infinite recursion if handler fails
                console.error(`Handler error: ${error.message}`);
            }
        }

        // Propagate to parent if enabled
        if (this.propagate && this.parent) {
            this.parent._log(level, message, ...args);
        }
    }

    /**
     * Log a debug message.
     */
    debug(message, ...args) {
        this._log(LogLevel.DEBUG, message, ...args);
    }

    /**
     * Log an info message.
     */
    info(message, ...args) {
        this._log(LogLevel.INFO, message, ...args);
    }

    /**
     * Log a warning message.
     */
    warning(message, ...args) {
        this._log(LogLevel.WARNING, message, ...args);
    }

    /**
     * Log an error message.
     */
    error(message, ...args) {
        this._log(LogLevel.ERROR, message, ...args);
    }

    /**
     * Log a critical message.
     */
    critical(message, ...args) {
        this._log(LogLevel.CRITICAL, message, ...args);
    }

    /**
     * Log an exception with traceback.
     */
    exception(message, error, ...args) {
        const extra = args.length > 0 ? args[0] : {};
        extra.exc_info = true;
        extra.exc_text = error ? error.stack : new Error().stack;
        this._log(LogLevel.ERROR, message, extra);
    }
} 