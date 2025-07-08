#!/usr/bin/env python3
"""
Example demonstrating singleton logger pattern across multiple modules.
All modules use the same logger instance, creating one log file per program run.
Demonstrates all log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL.
"""

import sys
import os
import atexit
import time

# Add the Logger directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Logger'))

from Logger import create_logger, get_logger, close_all_loggers, LogLevel

# Add import for the new worker module
import worker_module

# Module 1: Database operations
def database_operations():
    """Simulate database operations."""
    logger = get_logger("example")  # Get the same logger instance
    logger.debug("[DB] Debug: Preparing to connect to database...")
    logger.info("[DB] Info: Starting database operations")
    logger.warning("[DB] Warning: Using default credentials (not recommended)")
    
    try:
        logger.debug("[DB] Debug: Connecting to database...")
        time.sleep(0.1)  # Simulate work
        logger.info("[DB] Info: Database connection established")
        
        logger.debug("[DB] Debug: Executing query...")
        time.sleep(0.1)  # Simulate work
        logger.info("[DB] Info: Query executed successfully")
        
        # Simulate a warning condition
        logger.warning("[DB] Warning: Query took longer than expected")
        
        # Simulate a critical error
        if True:
            raise RuntimeError("[DB] Critical: Database corruption detected!")
        
    except Exception as e:
        logger.error(f"[DB] Error: Database operation failed: {e}")
        logger.critical("[DB] Critical: Shutting down database operations due to error!")
        # Don't re-raise to allow program to continue

# Module 2: File operations
def file_operations():
    """Simulate file operations."""
    logger = get_logger("example")  # Get the same logger instance
    logger.debug("[File] Debug: Preparing to open file...")
    logger.info("[File] Info: Starting file operations")
    
    try:
        logger.debug("[File] Debug: Opening file...")
        time.sleep(0.1)  # Simulate work
        logger.info("[File] Info: File opened successfully")
        
        logger.debug("[File] Debug: Processing file content...")
        time.sleep(0.1)  # Simulate work
        logger.info("[File] Info: File processing completed")
        
        # Simulate a warning
        logger.warning("[File] Warning: File is larger than expected")
        
        # Simulate an error
        if True:
            raise IOError("[File] Error: Failed to write to file!")
        
    except Exception as e:
        logger.error(f"[File] Error: File operation failed: {e}")
        logger.critical("[File] Critical: File system may be corrupted!")
        # Don't re-raise to allow program to continue

# Module 3: Network operations
def network_operations():
    """Simulate network operations."""
    logger = get_logger("example")  # Get the same logger instance
    logger.debug("[Net] Debug: Preparing to establish network connection...")
    logger.info("[Net] Info: Starting network operations")
    
    try:
        logger.debug("[Net] Debug: Establishing network connection...")
        time.sleep(0.1)  # Simulate work
        logger.info("[Net] Info: Network connection established")
        
        logger.debug("[Net] Debug: Sending data...")
        time.sleep(0.1)  # Simulate work
        logger.info("[Net] Info: Data sent successfully")
        
        # Simulate a warning
        logger.warning("[Net] Warning: Network latency is high")
        
        # Simulate an error
        if True:
            raise TimeoutError("[Net] Error: Network timeout occurred!")
        
    except Exception as e:
        logger.error(f"[Net] Error: Network operation failed: {e}")
        logger.critical("[Net] Critical: Network is down!")
        # Don't re-raise to allow program to continue

def main():
    """Main program that coordinates all operations."""
    # Initialize the logger once at the start of the program
    logger = create_logger("example", level=LogLevel.DEBUG)
    
    logger.info("=== Starting Multi-Module Application ===")
    
    # Run operations from different modules
    database_operations()
    file_operations()
    network_operations()
    
    # Call the new worker module to demonstrate logging from another file
    worker_module.do_work()
    
    logger.info("All operations completed (with some simulated errors)")
    logger.info("=== Multi-Module Application Finished ===")

def cleanup():
    """Cleanup function to close all loggers."""
    print("Closing all loggers...")
    close_all_loggers()

if __name__ == "__main__":
    # Register cleanup function to run at exit
    atexit.register(cleanup)
    
    main() 