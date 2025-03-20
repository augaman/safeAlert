"""Test module for performance testing."""
import pytest
import time
from datetime import datetime
import jwt
from src.models import db, Alert, AlertType, AlertStatus


def test_alert_creation_performance(client):
    """Test alert creation performance."""
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
    
    # Test single alert creation
    start_time = time.time()
    data = {
        'type': 'EMERGENCY',
        'description': 'Test alert',
        'location': 'Test location'
    }
    response = client.post('/alerts', json=data, headers=headers)
    end_time = time.time()
    
    assert response.status_code == 201
    assert end_time - start_time < 0.5  # Should complete within 500ms
    
    # Test bulk alert creation
    alerts = [
        {
            'type': 'EMERGENCY',
            'description': f'Test alert {i}',
            'location': f'Location {i}'
        }
        for i in range(100)
    ]
    
    start_time = time.time()
    for alert_data in alerts:
        response = client.post('/alerts', json=alert_data, headers=headers)
        assert response.status_code == 201
    end_time = time.time()
    
    assert end_time - start_time < 10.0  # Should complete within 10 seconds


def test_alert_retrieval_performance(client):
    """Test alert retrieval performance."""
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
    
    # Create test alerts
    alerts = [
        {
            'type': 'EMERGENCY',
            'description': f'Test alert {i}',
            'location': f'Location {i}'
        }
        for i in range(1000)
    ]
    
    for alert_data in alerts:
        response = client.post('/alerts', json=alert_data, headers=headers)
        assert response.status_code == 201
    
    # Test single alert retrieval
    alert_id = response.json['id']
    start_time = time.time()
    response = client.get(f'/alerts/{alert_id}', headers=headers)
    end_time = time.time()
    
    assert response.status_code == 200
    assert end_time - start_time < 0.2  # Should complete within 200ms
    
    # Test list retrieval with pagination
    start_time = time.time()
    response = client.get('/alerts?page=1&per_page=100', headers=headers)
    end_time = time.time()
    
    assert response.status_code == 200
    assert len(response.json) == 100
    assert end_time - start_time < 0.5  # Should complete within 500ms


def test_alert_filtering_performance(client):
    """Test alert filtering performance."""
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
    
    # Create test alerts
    alerts = [
        {
            'type': 'EMERGENCY' if i % 2 == 0 else 'WARNING',
            'description': f'Test alert {i}',
            'location': f'Location {i}'
        }
        for i in range(1000)
    ]
    
    for alert_data in alerts:
        response = client.post('/alerts', json=alert_data, headers=headers)
        assert response.status_code == 201
    
    # Test filtering by type
    start_time = time.time()
    response = client.get('/alerts?type=EMERGENCY', headers=headers)
    end_time = time.time()
    
    assert response.status_code == 200
    assert len(response.json) == 500
    assert end_time - start_time < 0.5  # Should complete within 500ms
    
    # Test filtering by status
    start_time = time.time()
    response = client.get('/alerts?status=ACTIVE', headers=headers)
    end_time = time.time()
    
    assert response.status_code == 200
    assert len(response.json) == 1000
    assert end_time - start_time < 0.5  # Should complete within 500ms


def test_alert_update_performance(client):
    """Test alert update performance."""
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
    
    # Create test alert
    data = {
        'type': 'EMERGENCY',
        'description': 'Test alert',
        'location': 'Test location'
    }
    response = client.post('/alerts', json=data, headers=headers)
    assert response.status_code == 201
    alert_id = response.json['id']
    
    # Test single update
    update_data = {
        'status': 'ACKNOWLEDGED',
        'acknowledged_by': 'Test User'
    }
    start_time = time.time()
    response = client.put(f'/alerts/{alert_id}', json=update_data, headers=headers)
    end_time = time.time()
    
    assert response.status_code == 200
    assert end_time - start_time < 0.3  # Should complete within 300ms
    
    # Test bulk updates
    alerts = [
        {
            'type': 'EMERGENCY',
            'description': f'Test alert {i}',
            'location': f'Location {i}'
        }
        for i in range(100)
    ]
    
    alert_ids = []
    for alert_data in alerts:
        response = client.post('/alerts', json=alert_data, headers=headers)
        assert response.status_code == 201
        alert_ids.append(response.json['id'])
    
    update_data = {
        'status': 'ACKNOWLEDGED',
        'acknowledged_by': 'Test User'
    }
    
    start_time = time.time()
    for alert_id in alert_ids:
        response = client.put(f'/alerts/{alert_id}', json=update_data, headers=headers)
        assert response.status_code == 200
    end_time = time.time()
    
    assert end_time - start_time < 5.0  # Should complete within 5 seconds


def test_alert_deletion_performance(client):
    """Test alert deletion performance."""
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
    
    # Create test alert
    data = {
        'type': 'EMERGENCY',
        'description': 'Test alert',
        'location': 'Test location'
    }
    response = client.post('/alerts', json=data, headers=headers)
    assert response.status_code == 201
    alert_id = response.json['id']
    
    # Test single deletion
    start_time = time.time()
    response = client.delete(f'/alerts/{alert_id}', headers=headers)
    end_time = time.time()
    
    assert response.status_code == 204
    assert end_time - start_time < 0.3  # Should complete within 300ms
    
    # Test bulk deletions
    alerts = [
        {
            'type': 'EMERGENCY',
            'description': f'Test alert {i}',
            'location': f'Location {i}'
        }
        for i in range(100)
    ]
    
    alert_ids = []
    for alert_data in alerts:
        response = client.post('/alerts', json=alert_data, headers=headers)
        assert response.status_code == 201
        alert_ids.append(response.json['id'])
    
    start_time = time.time()
    for alert_id in alert_ids:
        response = client.delete(f'/alerts/{alert_id}', headers=headers)
        assert response.status_code == 204
    end_time = time.time()
    
    assert end_time - start_time < 5.0  # Should complete within 5 seconds


def test_concurrent_operations(client):
    """Test concurrent operations performance."""
    import concurrent.futures
    
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
    
    # Create test alerts
    alerts = [
        {
            'type': 'EMERGENCY',
            'description': f'Test alert {i}',
            'location': f'Location {i}'
        }
        for i in range(100)
    ]
    
    for alert_data in alerts:
        response = client.post('/alerts', json=alert_data, headers=headers)
        assert response.status_code == 201
        alert_ids.append(response.json['id'])
    
    # Test concurrent reads
    def read_alert(alert_id):
        return client.get(f'/alerts/{alert_id}', headers=headers)
    
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(read_alert, alert_id) for alert_id in alert_ids]
        concurrent.futures.wait(futures)
    end_time = time.time()
    
    assert end_time - start_time < 2.0  # Should complete within 2 seconds
    
    # Test concurrent updates
    def update_alert(alert_id):
        update_data = {
            'status': 'ACKNOWLEDGED',
            'acknowledged_by': 'Test User'
        }
        return client.put(f'/alerts/{alert_id}', json=update_data, headers=headers)
    
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(update_alert, alert_id) for alert_id in alert_ids]
        concurrent.futures.wait(futures)
    end_time = time.time()
    
    assert end_time - start_time < 5.0  # Should complete within 5 seconds 