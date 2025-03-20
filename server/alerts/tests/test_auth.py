"""Test module for authentication and authorization."""
import pytest
from datetime import datetime, timedelta
import jwt
from src.models import Alert, AlertType, AlertStatus


def test_jwt_token_validation(client):
    """Test JWT token validation."""
    # Test missing token
    response = client.get('/alerts')
    assert response.status_code == 401
    
    # Test invalid token
    headers = {'Authorization': 'Bearer invalid_token'}
    response = client.get('/alerts', headers=headers)
    assert response.status_code == 401
    
    # Test expired token
    expired_token = jwt.encode(
        {
            'user_id': 1,
            'exp': datetime.utcnow() - timedelta(hours=1)
        },
        'test_secret',
        algorithm='HS256'
    )
    headers = {'Authorization': f'Bearer {expired_token}'}
    response = client.get('/alerts', headers=headers)
    assert response.status_code == 401


def test_role_based_access(client):
    """Test role-based access control."""
    # Create test tokens for different roles
    admin_token = jwt.encode(
        {
            'user_id': 1,
            'role': 'admin',
            'exp': datetime.utcnow() + timedelta(hours=1)
        },
        'test_secret',
        algorithm='HS256'
    )
    
    operator_token = jwt.encode(
        {
            'user_id': 2,
            'role': 'operator',
            'exp': datetime.utcnow() + timedelta(hours=1)
        },
        'test_secret',
        algorithm='HS256'
    )
    
    # Test admin access
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = client.get('/alerts', headers=headers)
    assert response.status_code == 200
    
    # Test operator access
    headers = {'Authorization': f'Bearer {operator_token}'}
    response = client.get('/alerts', headers=headers)
    assert response.status_code == 200
    
    # Test restricted endpoint access
    data = {
        'type': 'EMERGENCY',
        'description': 'Test alert',
        'location': 'Test location'
    }
    
    # Admin can create alerts
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = client.post('/alerts', json=data, headers=headers)
    assert response.status_code == 201
    
    # Operator cannot create alerts
    headers = {'Authorization': f'Bearer {operator_token}'}
    response = client.post('/alerts', json=data, headers=headers)
    assert response.status_code == 403


def test_permission_checks(client):
    """Test permission checks for different operations."""
    # Create test tokens
    admin_token = jwt.encode(
        {
            'user_id': 1,
            'role': 'admin',
            'exp': datetime.utcnow() + timedelta(hours=1)
        },
        'test_secret',
        algorithm='HS256'
    )
    
    operator_token = jwt.encode(
        {
            'user_id': 2,
            'role': 'operator',
            'exp': datetime.utcnow() + timedelta(hours=1)
        },
        'test_secret',
        algorithm='HS256'
    )
    
    # Create a test alert
    alert = Alert(
        type=AlertType.EMERGENCY,
        description='Test alert',
        location='Test location'
    )
    with client.application.app_context():
        client.application.extensions['sqlalchemy'].db.session.add(alert)
        client.application.extensions['sqlalchemy'].db.session.commit()
        alert_id = alert.id
    
    # Test update permissions
    data = {
        'status': 'ACKNOWLEDGED',
        'acknowledged_by': 'Test User'
    }
    
    # Admin can update any alert
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = client.put(f'/alerts/{alert_id}', json=data, headers=headers)
    assert response.status_code == 200
    
    # Operator can only update their own alerts
    headers = {'Authorization': f'Bearer {operator_token}'}
    response = client.put(f'/alerts/{alert_id}', json=data, headers=headers)
    assert response.status_code == 403
    
    # Test delete permissions
    # Admin can delete any alert
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = client.delete(f'/alerts/{alert_id}', headers=headers)
    assert response.status_code == 204
    
    # Operator cannot delete alerts
    headers = {'Authorization': f'Bearer {operator_token}'}
    response = client.delete(f'/alerts/{alert_id}', headers=headers)
    assert response.status_code == 403


def test_token_refresh(client):
    """Test token refresh functionality."""
    # Create a token with short expiration
    token = jwt.encode(
        {
            'user_id': 1,
            'role': 'admin',
            'exp': datetime.utcnow() + timedelta(minutes=5)
        },
        'test_secret',
        algorithm='HS256'
    )
    
    # Test token refresh
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/auth/refresh', headers=headers)
    assert response.status_code == 200
    assert 'token' in response.json
    
    # Verify new token works
    new_token = response.json['token']
    headers = {'Authorization': f'Bearer {new_token}'}
    response = client.get('/alerts', headers=headers)
    assert response.status_code == 200


def test_rate_limiting(client):
    """Test rate limiting for authenticated endpoints."""
    # Create a valid token
    token = jwt.encode(
        {
            'user_id': 1,
            'role': 'admin',
            'exp': datetime.utcnow() + timedelta(hours=1)
        },
        'test_secret',
        algorithm='HS256'
    )
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Make multiple requests
    for _ in range(100):  # Assuming rate limit is 100 requests per minute
        response = client.get('/alerts', headers=headers)
        assert response.status_code == 200
    
    # Test rate limit exceeded
    response = client.get('/alerts', headers=headers)
    assert response.status_code == 429
    assert 'X-RateLimit-Reset' in response.headers


def test_audit_logging(client, caplog):
    """Test audit logging for authenticated actions."""
    # Create a valid token
    token = jwt.encode(
        {
            'user_id': 1,
            'role': 'admin',
            'exp': datetime.utcnow() + timedelta(hours=1)
        },
        'test_secret',
        algorithm='HS256'
    )
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Perform authenticated action
    data = {
        'type': 'EMERGENCY',
        'description': 'Test alert',
        'location': 'Test location'
    }
    response = client.post('/alerts', json=data, headers=headers)
    
    # Verify audit log
    assert any(
        'user_id=1' in record.message and
        'action=create_alert' in record.message
        for record in caplog.records
    ) 