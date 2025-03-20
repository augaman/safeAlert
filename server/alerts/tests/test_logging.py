"""Test module for logging configuration."""
import pytest
import logging
import json
from src.app import create_app


def test_logging_configuration(app):
    """Test logging configuration."""
    # Verify logger exists
    logger = logging.getLogger('alerts')
    assert logger is not None
    
    # Verify log level
    assert logger.level == logging.INFO
    
    # Verify handlers
    assert len(logger.handlers) > 0
    
    # Verify JSON formatter
    for handler in logger.handlers:
        if isinstance(handler.formatter, logging.Formatter):
            assert isinstance(handler.formatter, logging.Formatter)


def test_logging_output(client, caplog):
    """Test logging output format and content."""
    # Set log level to INFO
    caplog.set_level(logging.INFO)
    
    # Make a request to trigger logging
    data = {
        'type': 'EMERGENCY',
        'description': 'Test alert',
        'location': 'Test location'
    }
    response = client.post('/alerts', json=data)
    
    # Verify log entries
    assert len(caplog.records) > 0
    
    # Check log format
    for record in caplog.records:
        # Verify JSON format
        try:
            log_data = json.loads(record.message)
            assert 'timestamp' in log_data
            assert 'level' in log_data
            assert 'message' in log_data
        except json.JSONDecodeError:
            pytest.fail('Log message is not in JSON format')


def test_logging_levels(client, caplog):
    """Test different logging levels."""
    # Set log level to DEBUG
    caplog.set_level(logging.DEBUG)
    
    # Make requests to trigger different log levels
    data = {
        'type': 'EMERGENCY',
        'description': 'Test alert',
        'location': 'Test location'
    }
    
    # Test INFO level
    client.post('/alerts', json=data)
    assert any(record.levelno == logging.INFO for record in caplog.records)
    
    # Test ERROR level
    with pytest.MonkeyPatch.context() as m:
        def mock_commit(*args, **kwargs):
            raise Exception('Database error')
        
        m.setattr(client.application.extensions['sqlalchemy'].db.session, 'commit', mock_commit)
        client.post('/alerts', json=data)
        assert any(record.levelno == logging.ERROR for record in caplog.records)


def test_logging_context(client, caplog):
    """Test logging context information."""
    caplog.set_level(logging.INFO)
    
    # Make a request with context
    data = {
        'type': 'EMERGENCY',
        'description': 'Test alert',
        'location': 'Test location'
    }
    response = client.post('/alerts', json=data)
    
    # Verify context information in logs
    for record in caplog.records:
        try:
            log_data = json.loads(record.message)
            assert 'request_id' in log_data
            assert 'endpoint' in log_data
            assert 'method' in log_data
        except json.JSONDecodeError:
            pytest.fail('Log message is not in JSON format')


def test_logging_performance(client, caplog):
    """Test logging performance impact."""
    import time
    
    caplog.set_level(logging.INFO)
    
    # Measure time without logging
    start_time = time.time()
    for _ in range(100):
        data = {
            'type': 'EMERGENCY',
            'description': 'Test alert',
            'location': 'Test location'
        }
        client.post('/alerts', json=data)
    end_time = time.time()
    logging_time = end_time - start_time
    
    # Verify logging doesn't significantly impact performance
    assert logging_time < 5.0  # Should complete within 5 seconds


def test_logging_rotation(app):
    """Test log file rotation."""
    import os
    from logging.handlers import RotatingFileHandler
    
    # Find the rotating file handler
    rotating_handler = None
    for handler in app.logger.handlers:
        if isinstance(handler, RotatingFileHandler):
            rotating_handler = handler
            break
    
    assert rotating_handler is not None
    
    # Verify rotation settings
    assert rotating_handler.maxBytes > 0
    assert rotating_handler.backupCount > 0


def test_logging_error_handling(client, caplog):
    """Test logging error handling."""
    caplog.set_level(logging.ERROR)
    
    # Test database error logging
    with pytest.MonkeyPatch.context() as m:
        def mock_commit(*args, **kwargs):
            raise Exception('Database error')
        
        m.setattr(client.application.extensions['sqlalchemy'].db.session, 'commit', mock_commit)
        
        data = {
            'type': 'EMERGENCY',
            'description': 'Test alert',
            'location': 'Test location'
        }
        response = client.post('/alerts', json=data)
        
        # Verify error logging
        assert any(
            record.levelno == logging.ERROR and
            'Database error' in record.message
            for record in caplog.records
        ) 