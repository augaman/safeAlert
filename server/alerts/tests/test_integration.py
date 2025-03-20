"""Test module for integration tests."""
import pytest
from datetime import datetime
import jwt
from src.models import db, Alert, AlertType, AlertStatus


def test_alert_lifecycle(client):
    """Test complete alert lifecycle."""
    # Create alert
    data = {
        'type': 'EMERGENCY',
        'description': 'Test emergency alert',
        'location': 'Test location'
    }
    response = client.post('/alerts', json=data)
    assert response.status_code == 201
    alert_id = response.json['id']
    
    # Get alert
    response = client.get(f'/alerts/{alert_id}')
    assert response.status_code == 200
    assert response.json['type'] == data['type']
    
    # Update alert status
    update_data = {
        'status': 'ACKNOWLEDGED',
        'acknowledged_by': 'Test User'
    }
    response = client.put(f'/alerts/{alert_id}', json=update_data)
    assert response.status_code == 200
    assert response.json['status'] == update_data['status']
    
    # Get updated alert
    response = client.get(f'/alerts/{alert_id}')
    assert response.status_code == 200
    assert response.json['status'] == update_data['status']
    assert response.json['acknowledged_by'] == update_data['acknowledged_by']
    
    # Resolve alert
    resolve_data = {
        'status': 'RESOLVED'
    }
    response = client.put(f'/alerts/{alert_id}', json=resolve_data)
    assert response.status_code == 200
    assert response.json['status'] == resolve_data['status']
    
    # Delete alert
    response = client.delete(f'/alerts/{alert_id}')
    assert response.status_code == 204
    
    # Verify alert is deleted
    response = client.get(f'/alerts/{alert_id}')
    assert response.status_code == 404


def test_alert_filtering(client):
    """Test alert filtering and pagination."""
    # Create multiple alerts
    alerts = [
        {
            'type': 'EMERGENCY',
            'description': f'Emergency alert {i}',
            'location': f'Location {i}'
        }
        for i in range(15)
    ]
    
    for alert_data in alerts:
        response = client.post('/alerts', json=alert_data)
        assert response.status_code == 201
    
    # Test filtering by type
    response = client.get('/alerts?type=EMERGENCY')
    assert response.status_code == 200
    assert len(response.json) == 15
    
    # Test filtering by status
    response = client.get('/alerts?status=ACTIVE')
    assert response.status_code == 200
    assert len(response.json) == 15
    
    # Test pagination
    response = client.get('/alerts?page=1&per_page=10')
    assert response.status_code == 200
    assert len(response.json) == 10
    
    response = client.get('/alerts?page=2&per_page=10')
    assert response.status_code == 200
    assert len(response.json) == 5


def test_alert_validation(client):
    """Test alert validation and error handling."""
    # Test invalid alert type
    data = {
        'type': 'INVALID_TYPE',
        'description': 'Test alert',
        'location': 'Test location'
    }
    response = client.post('/alerts', json=data)
    assert response.status_code == 400
    
    # Test missing required fields
    data = {
        'type': 'EMERGENCY'
    }
    response = client.post('/alerts', json=data)
    assert response.status_code == 400
    
    # Test invalid status update
    data = {
        'type': 'EMERGENCY',
        'description': 'Test alert',
        'location': 'Test location'
    }
    response = client.post('/alerts', json=data)
    assert response.status_code == 201
    alert_id = response.json['id']
    
    update_data = {
        'status': 'INVALID_STATUS'
    }
    response = client.put(f'/alerts/{alert_id}', json=update_data)
    assert response.status_code == 400


def test_alert_authentication(client):
    """Test alert authentication and authorization."""
    # Create test token
    token = jwt.encode(
        {
            'user_id': 1,
            'role': 'admin',
            'exp': datetime.utcnow().timestamp() + 3600
        },
        'test_secret',
        algorithm='HS256'
    )
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test authenticated endpoints
    data = {
        'type': 'EMERGENCY',
        'description': 'Test alert',
        'location': 'Test location'
    }
    
    # Create alert with authentication
    response = client.post('/alerts', json=data, headers=headers)
    assert response.status_code == 201
    alert_id = response.json['id']
    
    # Get alert with authentication
    response = client.get(f'/alerts/{alert_id}', headers=headers)
    assert response.status_code == 200
    
    # Update alert with authentication
    update_data = {
        'status': 'ACKNOWLEDGED',
        'acknowledged_by': 'Test User'
    }
    response = client.put(f'/alerts/{alert_id}', json=update_data, headers=headers)
    assert response.status_code == 200
    
    # Delete alert with authentication
    response = client.delete(f'/alerts/{alert_id}', headers=headers)
    assert response.status_code == 204


def test_alert_rate_limiting(client):
    """Test rate limiting for alert endpoints."""
    # Create test token
    token = jwt.encode(
        {
            'user_id': 1,
            'role': 'admin',
            'exp': datetime.utcnow().timestamp() + 3600
        },
        'test_secret',
        algorithm='HS256'
    )
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test rate limiting
    for _ in range(100):  # Assuming rate limit is 100 requests per minute
        response = client.get('/alerts', headers=headers)
        assert response.status_code == 200
    
    # Test rate limit exceeded
    response = client.get('/alerts', headers=headers)
    assert response.status_code == 429
    assert 'X-RateLimit-Reset' in response.headers


def test_alert_error_handling(client):
    """Test error handling for alert endpoints."""
    # Test invalid JSON
    response = client.post('/alerts', data='invalid json')
    assert response.status_code == 400
    
    # Test invalid alert ID
    response = client.get('/alerts/invalid_id')
    assert response.status_code == 404
    
    # Test database error simulation
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


def test_alert_logging(client, caplog):
    """Test logging for alert operations."""
    # Set log level to INFO
    caplog.set_level('INFO')
    
    # Create alert
    data = {
        'type': 'EMERGENCY',
        'description': 'Test alert',
        'location': 'Test location'
    }
    response = client.post('/alerts', json=data)
    assert response.status_code == 201
    
    # Verify logging
    assert any(
        'Creating new alert' in record.message and
        'type=EMERGENCY' in record.message
        for record in caplog.records
    )
    
    # Update alert
    alert_id = response.json['id']
    update_data = {
        'status': 'ACKNOWLEDGED',
        'acknowledged_by': 'Test User'
    }
    response = client.put(f'/alerts/{alert_id}', json=update_data)
    assert response.status_code == 200
    
    # Verify logging
    assert any(
        'Updating alert' in record.message and
        f'alert_id={alert_id}' in record.message
        for record in caplog.records
    ) 