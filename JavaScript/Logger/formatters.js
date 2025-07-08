/**
 * Log formatters that convert LogRecord objects into formatted strings.
 */

import { getLogLevelName } from './Logger.js';

/**
 * Abstract base class for log formatters.
 */
export class Formatter {
    format(record) {
        throw new Error('format method must be implemented');
    }
}

/**
 * Simple text formatter with timestamp, level, name, and message.
 */
export class SimpleFormatter extends Formatter {
    constructor(dateFormat = 'YYYY-MM-DD HH:mm:ss') {
        super();
        this.dateFormat = dateFormat;
    }

    format(record) {
        const timestamp = this._formatDate(record.timestamp);
        const level = getLogLevelName(record.level).padEnd(8);
        const name = record.name.padEnd(15);

        let formatted = `[${timestamp}] ${level} ${name}: ${record.message}`;

        // Add exception info if present
        if (record.extra.exc_text) {
            formatted += `\n${record.extra.exc_text}`;
        }

        // Add extra fields if present
        const extraFields = Object.entries(record.extra)
            .filter(([key]) => key !== 'exc_text' && key !== 'exc_info')
            .map(([key, value]) => `${key}=${value}`)
            .join(' ');

        if (extraFields) {
            formatted += ` | ${extraFields}`;
        }

        return formatted;
    }

    _formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');
        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    }
}

/**
 * JSON formatter for structured logging.
 */
export class JSONFormatter extends Formatter {
    constructor(includeTimestamp = true, includeName = true) {
        super();
        this.includeTimestamp = includeTimestamp;
        this.includeName = includeName;
    }

    format(record) {
        const data = {
            level: getLogLevelName(record.level),
            message: record.message
        };

        if (this.includeTimestamp) {
            data.timestamp = record.timestamp.toISOString();
        }

        if (this.includeName) {
            data.logger = record.name;
        }

        if (record.extra.exc_text) {
            data.exception = record.extra.exc_text;
        }

        // Add extra fields
        Object.entries(record.extra)
            .filter(([key]) => key !== 'exc_text' && key !== 'exc_info')
            .forEach(([key, value]) => {
                data[key] = value;
            });

        return JSON.stringify(data);
    }
}

/**
 * Colored console formatter with ANSI color codes.
 */
export class ColoredFormatter extends Formatter {
    constructor(dateFormat = 'YYYY-MM-DD HH:mm:ss', useColors = true) {
        super();
        this.dateFormat = dateFormat;
        this.useColors = useColors;

        // ANSI color codes
        this.COLORS = {
            'DEBUG': '\x1b[36m',    // Cyan
            'INFO': '\x1b[32m',     // Green
            'WARNING': '\x1b[33m',  // Yellow
            'ERROR': '\x1b[31m',    // Red
            'CRITICAL': '\x1b[35m', // Magenta
            'RESET': '\x1b[0m'      // Reset
        };
    }

    format(record) {
        const timestamp = this._formatDate(record.timestamp);
        const level = getLogLevelName(record.level).padEnd(8);
        const name = record.name.padEnd(15);

        let formatted;
        if (this.useColors) {
            const color = this.COLORS[getLogLevelName(record.level)] || '';
            const reset = this.COLORS.RESET;
            formatted = `[${timestamp}] ${color}${level}${reset} ${name}: ${record.message}`;
        } else {
            formatted = `[${timestamp}] ${level} ${name}: ${record.message}`;
        }

        // Add exception info if present
        if (record.extra.exc_text) {
            if (this.useColors) {
                formatted += `\n${this.COLORS.ERROR}${record.extra.exc_text}${this.COLORS.RESET}`;
            } else {
                formatted += `\n${record.extra.exc_text}`;
            }
        }

        // Add extra fields if present
        const extraFields = Object.entries(record.extra)
            .filter(([key]) => key !== 'exc_text' && key !== 'exc_info')
            .map(([key, value]) => `${key}=${value}`)
            .join(' ');

        if (extraFields) {
            if (this.useColors) {
                formatted += ` | ${this.COLORS.DEBUG}${extraFields}${this.COLORS.RESET}`;
            } else {
                formatted += ` | ${extraFields}`;
            }
        }

        return formatted;
    }

    _formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');
        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    }
}

/**
 * Template-based formatter using a custom format string.
 */
export class TemplateFormatter extends Formatter {
    constructor(template = '{timestamp} [{level}] {name}: {message}') {
        super();
        this.template = template;
    }

    format(record) {
        // Create a data object with all available fields
        const data = {
            timestamp: this._formatDate(record.timestamp),
            level: getLogLevelName(record.level),
            name: record.name,
            message: record.message,
            levelname: getLogLevelName(record.level),
            levelno: record.level
        };

        // Add extra fields
        Object.assign(data, record.extra);

        // Format using template
        let formatted = this.template;
        for (const [key, value] of Object.entries(data)) {
            formatted = formatted.replace(new RegExp(`{${key}}`, 'g'), value);
        }

        // Add exception info if present
        if (record.extra.exc_text) {
            formatted += `\n${record.extra.exc_text}`;
        }

        return formatted;
    }

    _formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');
        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    }
} 