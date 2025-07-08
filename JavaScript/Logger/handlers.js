/**
 * Log handlers that determine where log messages are output.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { SimpleFormatter } from './formatters.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Abstract base class for log handlers.
 */
export class Handler {
    constructor() {
        this.formatter = null;
        this.level = null; // Optional level filter
    }

    /**
     * Set the formatter for this handler.
     */
    setFormatter(formatter) {
        this.formatter = formatter;
    }

    /**
     * Set the minimum level for this handler.
     */
    setLevel(level) {
        this.level = level;
    }

    /**
     * Format a record using the handler's formatter.
     */
    format(record) {
        if (this.formatter === null) {
            // Default simple formatter
            this.formatter = new SimpleFormatter();
        }
        return this.formatter.format(record);
    }

    /**
     * Check if the record should be processed by this handler.
     */
    filter(record) {
        if (this.level === null) {
            return true;
        }
        return record.level >= this.level;
    }

    /**
     * Handle a record by filtering, formatting, and emitting it.
     */
    handle(record) {
        if (this.filter(record)) {
            try {
                this.emit(record);
            } catch (error) {
                // Prevent infinite recursion
                console.error(`Handler error: ${error.message}`);
            }
        }
    }

    /**
     * Emit a record. Must be implemented by subclasses.
     */
    emit(record) {
        throw new Error('emit method must be implemented');
    }
}

/**
 * Handler that outputs to console (stdout/stderr).
 */
export class ConsoleHandler extends Handler {
    constructor(stream = null) {
        super();
        this.stream = stream;
    }

    emit(record) {
        if (this.stream === null) {
            // Use stderr for errors and critical, stdout for others
            if (record.level >= 3) { // ERROR or CRITICAL
                this.stream = process.stderr;
            } else {
                this.stream = process.stdout;
            }
        }

        const formatted = this.format(record);
        this.stream.write(formatted + '\n');
    }
}

/**
 * Handler that outputs to a file.
 */
export class FileHandler extends Handler {
    constructor(filename, mode = 'a', encoding = 'utf8') {
        super();
        this.filename = filename;
        this.mode = mode;
        this.encoding = encoding;
        this._file = null;
    }

    _openFile() {
        if (this._file === null) {
            // Create directory if it doesn't exist
            const dir = path.dirname(this.filename);
            if (dir && !fs.existsSync(dir)) {
                fs.mkdirSync(dir, { recursive: true });
            }
            this._file = fs.createWriteStream(this.filename, { 
                flags: this.mode,
                encoding: this.encoding 
            });
        }
    }

    emit(record) {
        this._openFile();
        const formatted = this.format(record);
        this._file.write(formatted + '\n');
    }

    close() {
        if (this._file) {
            this._file.end();
            this._file = null;
        }
    }
}

/**
 * Handler that rotates log files based on size.
 */
export class RotatingFileHandler extends FileHandler {
    constructor(filename, maxBytes = 10 * 1024 * 1024, backupCount = 5, maxFiles = 100, mode = 'a', encoding = 'utf8') {
        super(filename, mode, encoding);
        this.maxBytes = maxBytes;
        this.backupCount = backupCount;
        this.maxFiles = maxFiles;
    }

    emit(record) {
        if (this._file && this._file.bytesWritten >= this.maxBytes) {
            this.rotate();
        }
        super.emit(record);
    }

    rotate() {
        if (this._file) {
            this._file.end();
            this._file = null;
        }

        // Rotate existing backup files
        for (let i = this.backupCount - 1; i > 0; i--) {
            const src = `${this.filename}.${i}`;
            const dst = `${this.filename}.${i + 1}`;
            if (fs.existsSync(src)) {
                if (fs.existsSync(dst)) {
                    fs.unlinkSync(dst);
                }
                fs.renameSync(src, dst);
            }
        }

        // Move current file to .1
        if (fs.existsSync(this.filename)) {
            fs.renameSync(this.filename, `${this.filename}.1`);
        }

        // Clean up old files if we exceed max_files
        this._cleanupOldFiles();
    }

    _cleanupOldFiles() {
        const pattern = `${this.filename}.*`;
        const files = this._getMatchingFiles(pattern);
        
        // Sort files by modification time (oldest first)
        files.sort((a, b) => fs.statSync(a).mtime.getTime() - fs.statSync(b).mtime.getTime());
        
        // If we have more files than max_files, remove the oldest ones
        if (files.length > this.maxFiles) {
            const filesToRemove = files.slice(0, files.length - this.maxFiles);
            for (const oldFile of filesToRemove) {
                try {
                    fs.unlinkSync(oldFile);
                } catch (error) {
                    // Ignore errors
                }
            }
        }
    }

    _getMatchingFiles(pattern) {
        const dir = path.dirname(this.filename);
        const base = path.basename(this.filename);
        const files = [];
        
        if (fs.existsSync(dir)) {
            const dirFiles = fs.readdirSync(dir);
            for (const file of dirFiles) {
                if (file.startsWith(base + '.')) {
                    files.push(path.join(dir, file));
                }
            }
        }
        
        return files;
    }
}

/**
 * Handler that rotates log files based on time intervals.
 */
export class TimedRotatingFileHandler extends FileHandler {
    constructor(filename, when = 'midnight', interval = 1, backupCount = 5, maxFiles = 100, mode = 'a', encoding = 'utf8') {
        super(filename, mode, encoding);
        this.when = when;
        this.interval = interval;
        this.backupCount = backupCount;
        this.maxFiles = maxFiles;
        this.lastRotation = new Date();
    }

    emit(record) {
        if (this.shouldRotate(record.timestamp)) {
            this.rotate();
        }
        super.emit(record);
    }

    shouldRotate(timestamp) {
        if (this.when === 'midnight') {
            return timestamp.toDateString() !== this.lastRotation.toDateString();
        } else if (this.when === 'hour') {
            return (timestamp - this.lastRotation) >= 3600 * 1000 * this.interval;
        } else if (this.when === 'minute') {
            return (timestamp - this.lastRotation) >= 60 * 1000 * this.interval;
        }
        return false;
    }

    rotate() {
        if (this._file) {
            this._file.end();
            this._file = null;
        }

        // Create backup filename with timestamp
        const timestamp = this._formatTimestamp(this.lastRotation);
        const backupName = `${this.filename}.${timestamp}`;

        if (fs.existsSync(this.filename)) {
            fs.renameSync(this.filename, backupName);
        }

        // Remove old backups
        this._removeOldBackups();
        this.lastRotation = new Date();
    }

    _formatTimestamp(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');
        return `${year}${month}${day}_${hours}${minutes}${seconds}`;
    }

    _removeOldBackups() {
        const pattern = `${this.filename}.*`;
        const files = this._getMatchingFiles(pattern);
        
        // Sort files by modification time (oldest first)
        files.sort((a, b) => fs.statSync(a).mtime.getTime() - fs.statSync(b).mtime.getTime());
        
        // Keep only the most recent files, respecting both backup_count and max_files
        const maxToKeep = Math.min(this.backupCount, this.maxFiles);
        if (files.length > maxToKeep) {
            const filesToRemove = files.slice(0, files.length - maxToKeep);
            for (const oldFile of filesToRemove) {
                try {
                    fs.unlinkSync(oldFile);
                } catch (error) {
                    // Ignore errors
                }
            }
        }
    }

    _getMatchingFiles(pattern) {
        const dir = path.dirname(this.filename);
        const base = path.basename(this.filename);
        const files = [];
        
        if (fs.existsSync(dir)) {
            const dirFiles = fs.readdirSync(dir);
            for (const file of dirFiles) {
                if (file.startsWith(base + '.')) {
                    files.push(path.join(dir, file));
                }
            }
        }
        
        return files;
    }
}

/**
 * Handler that does nothing (useful for testing).
 */
export class NullHandler extends Handler {
    emit(record) {
        // Do nothing
    }
}

/**
 * Handler that stores records in memory.
 */
export class MemoryHandler extends Handler {
    constructor(capacity = 1000) {
        super();
        this.capacity = capacity;
        this.buffer = [];
    }

    emit(record) {
        this.buffer.push(record);
        if (this.buffer.length > this.capacity) {
            this.buffer.shift();
        }
    }

    getRecords() {
        return [...this.buffer];
    }

    clear() {
        this.buffer = [];
    }
} 