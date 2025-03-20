"""Test module for error handling."""
import pytest
from src.app import create_app
from src.models import db, Alert, AlertType, AlertStatus


def test_404_error(client):
    """Test 404 error handling."""
    response = client.get('/alerts/999')
    assert response.status_code == 404
    assert response.json['error'] == 'Alert not found'


def test_400_error_invalid_data(client):
    """Test 400 error handling for invalid data."""
    # Test invalid alert type
    data = {
        'type': 'INVALID_TYPE',
        'description': 'Test alert',
        'location': 'Test location'
    }
    response = client.post('/alerts', json=data)
    assert response.status_code == 400
    assert 'error' in response.json
    
    # Test missing required fields
    data = {
        'type': 'EMERGENCY'
    }
    response = client.post('/alerts', json=data)
    assert response.status_code == 400
    assert 'error' in response.json


def test_500_error_database(client):
    """Test 500 error handling for database errors."""
    with pytest.MonkeyPatch.context() as m:
        # Simulate database error
        def mock_commit(*args, **kwargs):
            raise Exception('Database error')
        
        m.setattr(db.session, 'commit', mock_commit)
        
        data = {
            'type': 'EMERGENCY',
            'description': 'Test alert',
            'location': 'Test location'
        }
        response = client.post('/alerts', json=data)
        assert response.status_code == 500
        assert response.json['error'] == 'Internal server error'


def test_validation_error(client):
    """Test validation error handling."""
    # Test invalid status update
    data = {
        'status': 'INVALID_STATUS',
        'acknowledged_by': 'Test User'
    }
    response = client.put('/alerts/1', json=data)
    assert response.status_code == 400
    assert 'error' in response.json
    
    # Test invalid acknowledged_by length
    data = {
        'status': 'ACKNOWLEDGED',
        'acknowledged_by': 'x' * 101  # Exceeds max length
    }
    response = client.put('/alerts/1', json=data)
    assert response.status_code == 400
    assert 'error' in response.json


def test_error_logging(client, caplog):
    """Test error logging."""
    # Test database error logging
    with pytest.MonkeyPatch.context() as m:
        def mock_commit(*args, **kwargs):
            raise Exception('Database error')
        
        m.setattr(db.session, 'commit', mock_commit)
        
        data = {
            'type': 'EMERGENCY',
            'description': 'Test alert',
            'location': 'Test location'
        }
        response = client.post('/alerts', json=data)
        assert response.status_code == 500
        assert 'Database error' in caplog.text


def test_error_response_format(client):
    """Test error response format."""
    # Test 404 error format
    response = client.get('/alerts/999')
    assert response.status_code == 404
    assert 'error' in response.json
    assert 'message' in response.json
    
    # Test 400 error format
    data = {
        'type': 'INVALID_TYPE',
        'description': 'Test alert',
        'location': 'Test location'
    }
    response = client.post('/alerts', json=data)
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'message' in response.json
    
    # Test 500 error format
    with pytest.MonkeyPatch.context() as m:
        def mock_commit(*args, **kwargs):
            raise Exception('Database error')
        
        m.setattr(db.session, 'commit', mock_commit)
        
        data = {
            'type': 'EMERGENCY',
            'description': 'Test alert',
            'location': 'Test location'
        }
        response = client.post('/alerts', json=data)
        assert response.status_code == 500
        assert 'error' in response.json
        assert 'message' in response.json


def test_error_handling_middleware(client):
    """Test error handling middleware."""
    # Test unhandled exception
    with pytest.MonkeyPatch.context() as m:
        def mock_route(*args, **kwargs):
            raise Exception('Unhandled error')
        
        m.setattr(client.application, 'route', mock_route)
        
        response = client.get('/alerts')
        assert response.status_code == 500
        assert response.json['error'] == 'Internal server error' 