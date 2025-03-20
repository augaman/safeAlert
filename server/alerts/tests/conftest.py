"""Test configuration for pytest."""
import pytest
import os
from src.app import create_app
from src.models import db


@pytest.fixture(scope='session')
def app():
    """Create a test Flask application."""
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='session')
def client(app):
    """Create a test client."""
    return app.test_client()


@pytest.fixture(scope='session')
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture(scope='session')
def sample_alert_data():
    """Create sample alert data for testing."""
    return {
        'type': 'EMERGENCY',
        'description': 'Test emergency alert',
        'location': 'Test location'
    }


@pytest.fixture(scope='session')
def sample_alert_update_data():
    """Create sample alert update data for testing."""
    return {
        'status': 'ACKNOWLEDGED',
        'acknowledged_by': 'Test User'
    } 