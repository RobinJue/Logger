/**
 * Logger registry for managing singleton logger instances.
 */

import { Logger } from './Logger.js';

/**
 * Registry for managing singleton logger instances.
 */
class LoggerRegistry {
    constructor() {
        this._loggers = new Map();
    }

    /**
     * Get an existing logger by name.
     */
    getLogger(name) {
        return this._loggers.get(name) || null;
    }

    /**
     * Register a logger instance.
     */
    registerLogger(name, logger) {
        this._loggers.set(name, logger);
    }

    /**
     * Close all handlers for a logger and remove it from registry.
     */
    closeLogger(name) {
        if (this._loggers.has(name)) {
            const logger = this._loggers.get(name);
            // Close all handlers
            for (const handler of logger.handlers) {
                if (typeof handler.close === 'function') {
                    handler.close();
                }
            }
            // Remove from registry
            this._loggers.delete(name);
            return true;
        }
        return false;
    }

    /**
     * Close all registered loggers.
     */
    closeAll() {
        for (const name of this._loggers.keys()) {
            this.closeLogger(name);
        }
    }

    /**
     * Get all registered loggers.
     */
    getAllLoggers() {
        return new Map(this._loggers);
    }
}

// Global registry instance
const _registry = new LoggerRegistry();

/**
 * Get a logger instance by name from the registry.
 */
export function getLogger(name) {
    return _registry.getLogger(name);
}

/**
 * Register a logger instance in the registry.
 */
export function registerLogger(name, logger) {
    _registry.registerLogger(name, logger);
}

/**
 * Close a logger and remove it from the registry.
 */
export function closeLogger(name) {
    return _registry.closeLogger(name);
}

/**
 * Close all registered loggers.
 */
export function closeAllLoggers() {
    _registry.closeAll();
}

/**
 * Get all registered loggers.
 */
export function getAllLoggers() {
    return _registry.getAllLoggers();
} 