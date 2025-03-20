"""Test module for configuration management."""
import pytest
import os
from src.app import create_app


def test_config_loading():
    """Test configuration loading."""
    app = create_app()
    
    # Test default configuration
    assert app.config['TESTING'] is False
    assert app.config['DEBUG'] is False
    assert 'SQLALCHEMY_DATABASE_URI' in app.config
    assert 'SQLALCHEMY_TRACK_MODIFICATIONS' in app.config
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False


def test_config_environment_variables():
    """Test environment variable configuration."""
    # Set test environment variables
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['DATABASE_URL'] = 'sqlite:///test.db'
    os.environ['LOG_LEVEL'] = 'DEBUG'
    
    app = create_app()
    
    # Verify environment variables are loaded
    assert app.config['TESTING'] is True
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///test.db'
    assert app.config['LOG_LEVEL'] == 'DEBUG'
    
    # Clean up environment variables
    del os.environ['FLASK_ENV']
    del os.environ['DATABASE_URL']
    del os.environ['LOG_LEVEL']


def test_config_development():
    """Test development configuration."""
    os.environ['FLASK_ENV'] = 'development'
    app = create_app()
    
    assert app.config['DEBUG'] is True
    assert app.config['TESTING'] is False
    
    del os.environ['FLASK_ENV']


def test_config_production():
    """Test production configuration."""
    os.environ['FLASK_ENV'] = 'production'
    app = create_app()
    
    assert app.config['DEBUG'] is False
    assert app.config['TESTING'] is False
    
    del os.environ['FLASK_ENV']


def test_config_testing():
    """Test testing configuration."""
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app()
    
    assert app.config['TESTING'] is True
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'
    
    del os.environ['FLASK_ENV']


def test_config_security():
    """Test security configuration."""
    app = create_app()
    
    # Test security headers
    assert app.config['SECURE_HEADERS'] is not None
    assert 'X-Content-Type-Options' in app.config['SECURE_HEADERS']
    assert 'X-Frame-Options' in app.config['SECURE_HEADERS']
    assert 'X-XSS-Protection' in app.config['SECURE_HEADERS']
    
    # Test CORS configuration
    assert app.config['CORS_ORIGINS'] is not None
    assert isinstance(app.config['CORS_ORIGINS'], list)


def test_config_database():
    """Test database configuration."""
    app = create_app()
    
    # Test database configuration
    assert 'SQLALCHEMY_DATABASE_URI' in app.config
    assert 'SQLALCHEMY_TRACK_MODIFICATIONS' in app.config
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False
    
    # Test database pool configuration
    assert 'SQLALCHEMY_ENGINE_OPTIONS' in app.config
    assert 'pool_size' in app.config['SQLALCHEMY_ENGINE_OPTIONS']
    assert 'max_overflow' in app.config['SQLALCHEMY_ENGINE_OPTIONS']
    assert 'pool_timeout' in app.config['SQLALCHEMY_ENGINE_OPTIONS']


def test_config_logging():
    """Test logging configuration."""
    app = create_app()
    
    # Test logging configuration
    assert 'LOG_LEVEL' in app.config
    assert 'LOG_FORMAT' in app.config
    assert 'LOG_FILE' in app.config
    
    # Test log rotation configuration
    assert 'LOG_MAX_BYTES' in app.config
    assert 'LOG_BACKUP_COUNT' in app.config
    assert app.config['LOG_MAX_BYTES'] > 0
    assert app.config['LOG_BACKUP_COUNT'] > 0


def test_config_rate_limiting():
    """Test rate limiting configuration."""
    app = create_app()
    
    # Test rate limiting configuration
    assert 'RATELIMIT_ENABLED' in app.config
    assert 'RATELIMIT_STORAGE_URL' in app.config
    assert 'RATELIMIT_STRATEGY' in app.config
    
    # Test rate limit values
    assert 'RATELIMIT_DEFAULT' in app.config
    assert 'RATELIMIT_HEADERS_ENABLED' in app.config
    assert app.config['RATELIMIT_HEADERS_ENABLED'] is True


def test_config_error_handling():
    """Test error handling configuration."""
    app = create_app()
    
    # Test error handling configuration
    assert 'PROPAGATE_EXCEPTIONS' in app.config
    assert app.config['PROPAGATE_EXCEPTIONS'] is True
    
    # Test error response format
    assert 'ERROR_RESPONSE_FORMAT' in app.config
    assert isinstance(app.config['ERROR_RESPONSE_FORMAT'], dict)
    assert 'error' in app.config['ERROR_RESPONSE_FORMAT']
    assert 'message' in app.config['ERROR_RESPONSE_FORMAT'] 