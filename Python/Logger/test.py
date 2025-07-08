#!/usr/bin/env python3
"""
Comprehensive Example and Test for the Portable Logger Library

This example demonstrates all features of the Logger library and serves as a functional test.
It covers all formatters, handlers, log levels, and advanced usage patterns.
"""

import sys
import os
import time
import traceback
from datetime import datetime

# Test file for the Python Logger library
"""
Comprehensive Example and Test for the Portable Logger Library

This example demonstrates all features of the Logger library and serves as a functional test.
It covers all formatters, handlers, log levels, and advanced usage patterns.
"""

import sys
import os
import time
import traceback
from datetime import datetime

from Logger import (
    LogLevel,
    get_logger,
    close_all_loggers,
    create_logger
)
from Logger.config import (
    setup_development_logger,
    setup_production_logger,
    setup_json_logger,
    setup_rotating_logger,
    setup_multi_handler_logger
)
from Logger.logger import Logger
from Logger.formatters import SimpleFormatter, JSONFormatter, ColoredFormatter, TemplateFormatter
from Logger.handlers import ConsoleHandler, FileHandler, RotatingFileHandler, MemoryHandler

print('🚀 === Python Logger Library - Comprehensive Example & Test ===\n')

# Test counter for validation
test_passed = 0
test_total = 0

def run_test(test_name, test_function):
    """Run a test and track results."""
    global test_passed, test_total
    test_total += 1
    try:
        test_function()
        print(f"✅ {test_name} - PASSED")
        test_passed += 1
    except Exception as error:
        print(f"❌ {test_name} - FAILED: {error}")
        traceback.print_exc()

# Test 1: Basic Logger Creation
def test_basic_logger_creation():
    """Test basic logger creation and functionality."""
    logger = create_logger('basic-test', LogLevel.DEBUG)
    
    logger.debug('Debug message from basic logger')
    logger.info('Info message from basic logger')
    logger.warning('Warning message from basic logger')
    logger.error('Error message from basic logger')
    logger.critical('Critical message from basic logger')
    
    # Test with extra data
    logger.info('User action', extra={'user_id': 123, 'action': 'login', 'timestamp': datetime.now().isoformat()})
    
    # Test exception logging
    try:
        raise ValueError('Test exception for logging')
    except Exception as error:
        logger.exception('Exception occurred during test', extra={'test_phase': 'basic'})

# Test 2: Development Logger
def test_development_logger():
    """Test development logger setup."""
    dev_logger = setup_development_logger('dev-test')
    dev_logger.debug('Development debug message')
    dev_logger.info('Development info message')
    dev_logger.warning('Development warning message')

# Test 3: Production Logger
def test_production_logger():
    """Test production logger setup."""
    prod_logger = setup_production_logger('prod-test', 'production-test.log')
    prod_logger.info('Production info message')
    prod_logger.error('Production error message')
    prod_logger.critical('Production critical message')

# Test 4: JSON Logger
def test_json_logger():
    """Test JSON logger setup."""
    json_logger = setup_json_logger('json-test', 'json-test.log')
    
    # Test structured logging
    json_logger.info('User registration', extra={
        'user_id': 456,
        'email': 'user@example.com',
        'registration_method': 'email',
        'timestamp': datetime.now().isoformat(),
        'metadata': {
            'source': 'web',
            'user_agent': 'Mozilla/5.0...'
        }
    })
    
    json_logger.error('API request failed', extra={
        'endpoint': '/api/users',
        'method': 'POST',
        'status_code': 500,
        'response_time': 1500,
        'error': 'Database connection timeout'
    })

# Test 5: Rotating Logger
def test_rotating_logger():
    """Test rotating logger setup."""
    rotating_logger = setup_rotating_logger('rotating-test', 'rotating-test.log', 1024, 3)
    
    # Log multiple messages to test rotation
    for i in range(50):
        rotating_logger.info(f'Rotating log message {i}', extra={
            'iteration': i,
            'timestamp': datetime.now().isoformat(),
            'data': 'x' * 20  # Add some data to fill the file faster
        })

# Test 6: Multi-Handler Logger
def test_multi_handler_logger():
    """Test multi-handler logger setup."""
    multi_logger = setup_multi_handler_logger('multi-test', True, 'multi-test.log', 'multi-test-errors.log')
    
    multi_logger.debug('Debug message to console and file')
    multi_logger.info('Info message to console and file')
    multi_logger.warning('Warning message to console and file')
    multi_logger.error('Error message to console, main file, and error file')
    multi_logger.critical('Critical message to console, main file, and error file')

# Test 7: Logger Registry and Singleton Pattern
def test_logger_registry():
    """Test logger registry and singleton pattern."""
    # Create a logger
    logger1 = create_logger('registry-test')
    logger1.info('First logger instance')
    
    # Try to get the same logger
    logger2 = get_logger('registry-test')
    logger2.info('Second logger instance (should be the same)')
    
    # Verify they are the same instance
    if logger1 is not logger2:
        raise ValueError('Logger registry singleton pattern failed')
    
    # Test non-existent logger
    non_existent = get_logger('non-existent')
    if non_existent is not None:
        raise ValueError('Non-existent logger should return None')

# Test 8: Child Loggers
def test_child_loggers():
    """Test child logger hierarchy."""
    parent_logger = create_logger('parent-test')
    
    child1 = parent_logger.get_child('child1')
    child2 = parent_logger.get_child('child2')
    grandchild = child1.get_child('grandchild')
    
    parent_logger.info('Parent logger message')
    child1.info('Child 1 logger message')
    child2.info('Child 2 logger message')
    grandchild.info('Grandchild logger message')
    
    # Test that child loggers are cached
    child1_again = parent_logger.get_child('child1')
    if child1 is not child1_again:
        raise ValueError('Child logger caching failed')

# Test 9: Log Levels
def test_log_levels():
    """Test log level filtering."""
    level_logger = create_logger('level-test', LogLevel.WARNING)
    
    # These should not appear
    level_logger.debug('This debug message should not appear')
    level_logger.info('This info message should not appear')
    
    # These should appear
    level_logger.warning('This warning message should appear')
    level_logger.error('This error message should appear')
    level_logger.critical('This critical message should appear')

# Test 10: Custom Configuration
def test_custom_configuration():
    """Test custom logger configuration."""
    custom_logger = Logger('custom-test')
    custom_logger.set_level(LogLevel.DEBUG)
    
    # Console handler with colored output
    console_handler = ConsoleHandler()
    console_handler.set_formatter(ColoredFormatter())
    custom_logger.add_handler(console_handler)
    
    # File handler with JSON format
    file_handler = FileHandler('custom-test.json.log')
    file_handler.set_formatter(JSONFormatter())
    custom_logger.add_handler(file_handler)
    
    # Memory handler for testing
    memory_handler = MemoryHandler(10)
    custom_logger.add_handler(memory_handler)
    
    custom_logger.info('Custom configured logger message')
    custom_logger.debug('Debug message with custom setup')
    custom_logger.error('Error message with custom setup')
    
    # Test memory handler
    records = memory_handler.get_records()
    if len(records) != 3:
        raise ValueError(f'Memory handler should have 3 records, got {len(records)}')
    
    # Test record structure
    first_record = records[0]
    if not hasattr(first_record, 'name') or not hasattr(first_record, 'message') or not hasattr(first_record, 'timestamp'):
        raise ValueError('Log record structure is invalid')

# Test 11: Template Formatter
def test_template_formatter():
    """Test template formatter."""
    template_logger = Logger('template-test')
    
    template_formatter = TemplateFormatter(
        'CUSTOM | {timestamp} | {level} | {name} | {message} | {extra}'
    )
    
    handler = ConsoleHandler()
    handler.set_formatter(template_formatter)
    template_logger.add_handler(handler)
    
    template_logger.info('Template formatted message', extra={'user_id': 789, 'action': 'test'})

# Test 12: Performance Test
def test_performance():
    """Test logger performance."""
    perf_logger = create_logger('perf-test', LogLevel.INFO)
    
    start_time = time.time()
    iterations = 1000
    
    for i in range(iterations):
        perf_logger.info(f'Performance test message {i}')
    
    duration = time.time() - start_time
    rate = int(iterations / duration)
    
    print(f"   Performance: {iterations} messages in {duration:.3f}s ({rate} msg/sec)")
    
    if rate < 100:
        raise ValueError(f'Performance too slow: {rate} msg/sec')

# Test 13: Error Handling
def test_error_handling():
    """Test error handling in handlers."""
    error_logger = create_logger('error-test')
    
    # Test handler error handling
    class BadHandler:
        def emit(self, record):
            raise RuntimeError('Handler error')
    
    bad_handler = BadHandler()
    error_logger.add_handler(bad_handler)
    
    # This should not crash the application
    error_logger.info('Message with bad handler')
    
    # Remove the bad handler
    error_logger.remove_handler(bad_handler)
    error_logger.info('Message after removing bad handler')

# Test 14: File Handler Operations
def test_file_handler_operations():
    """Test file handler operations."""
    file_logger = Logger('file-test')
    
    file_handler = FileHandler('file-test.log')
    file_handler.set_formatter(SimpleFormatter())
    file_logger.add_handler(file_handler)
    
    file_logger.info('File handler test message')
    file_logger.error('File handler error message')
    
    # Test handler close
    file_handler.close()
    
    # This should not cause an error
    file_logger.info('Message after handler close')

# Test 15: Integration Test
def test_integration():
    """Test complete application workflow."""
    # Simulate a complete application workflow
    app_logger = create_logger('integration-test', LogLevel.DEBUG)
    
    # Application startup
    app_logger.info('Application starting up', extra={'version': '1.0.0', 'environment': 'test'})
    
    # Database connection
    db_logger = app_logger.get_child('database')
    db_logger.info('Connecting to database', extra={'host': 'localhost', 'port': 5432})
    
    try:
        # Simulate database operation
        db_logger.debug('Executing query: SELECT * FROM users')
        # Simulate error
        raise ConnectionError('Connection timeout')
    except Exception as error:
        db_logger.exception('Database connection failed', extra={'retry_attempt': 1})
    
    # API request
    api_logger = app_logger.get_child('api')
    api_logger.info('Processing API request', extra={
        'method': 'POST',
        'endpoint': '/api/users',
        'user_id': 123
    })
    
    # Application shutdown
    app_logger.info('Application shutting down', extra={'reason': 'test completion'})

# Run all tests
run_test('Basic Logger Creation', test_basic_logger_creation)
run_test('Development Logger Setup', test_development_logger)
run_test('Production Logger Setup', test_production_logger)
run_test('JSON Logger Setup', test_json_logger)
run_test('Rotating Logger Setup', test_rotating_logger)
run_test('Multi-Handler Logger Setup', test_multi_handler_logger)
run_test('Logger Registry and Singleton Pattern', test_logger_registry)
run_test('Child Logger Hierarchy', test_child_loggers)
run_test('Log Level Filtering', test_log_levels)
run_test('Custom Logger Configuration', test_custom_configuration)
run_test('Template Formatter', test_template_formatter)
run_test('Performance Test', test_performance)
run_test('Error Handling', test_error_handling)
run_test('File Handler Operations', test_file_handler_operations)
run_test('Integration Test - Complete Workflow', test_integration)

print('\n📊 === Test Results ===')
print(f'Tests Passed: {test_passed}/{test_total}')
print(f'Success Rate: {int((test_passed / test_total) * 100)}%')

if test_passed == test_total:
    print('🎉 All tests passed! The Logger library is working correctly.')
else:
    print('⚠️  Some tests failed. Please check the implementation.')

print('\n📁 Check the Logger/logs/ directory for generated log files:')
print('- basic-test.log')
print('- production-test.log')
print('- json-test.log')
print('- rotating-test.log')
print('- multi-test.log')
print('- multi-test-errors.log')
print('- custom-test.json.log')
print('- file-test.log')
print('- integration-test.log')

# Clean up
print('\n🧹 Closing all loggers...')
close_all_loggers()
print('✅ All loggers closed successfully.')
print('\n✨ Example and test completed!') 