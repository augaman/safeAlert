"""Test module for alert routes."""
import pytest
from datetime import datetime
from src.app import create_app
from src.models import db, Alert, AlertType, AlertStatus


@pytest.fixture
def app():
    """Create a test Flask application."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/alerts/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'


def test_create_alert(client):
    """Test creating a new alert."""
    data = {
        'type': 'EMERGENCY',
        'description': 'Test emergency alert',
        'location': 'Test location'
    }
    response = client.post('/alerts', json=data)
    assert response.status_code == 201
    assert response.json['type'] == data['type']
    assert response.json['description'] == data['description']
    assert response.json['location'] == data['location']
    assert response.json['status'] == 'ACTIVE'


def test_create_alert_invalid_data(client):
    """Test creating an alert with invalid data."""
    data = {
        'type': 'INVALID_TYPE',
        'description': '',  # Empty description
        'location': ''  # Empty location
    }
    response = client.post('/alerts', json=data)
    assert response.status_code == 400


def test_update_alert(client):
    """Test updating an alert."""
    # Create an alert first
    alert = Alert(
        type=AlertType.EMERGENCY,
        description='Test alert',
        location='Test location'
    )
    with client.application.app_context():
        db.session.add(alert)
        db.session.commit()
        alert_id = alert.id

    # Update the alert
    data = {
        'status': 'ACKNOWLEDGED',
        'acknowledged_by': 'Test User'
    }
    response = client.put(f'/alerts/{alert_id}', json=data)
    assert response.status_code == 200
    assert response.json['status'] == 'ACKNOWLEDGED'
    assert response.json['acknowledged_by'] == 'Test User'


def test_update_nonexistent_alert(client):
    """Test updating a nonexistent alert."""
    data = {
        'status': 'ACKNOWLEDGED',
        'acknowledged_by': 'Test User'
    }
    response = client.put('/alerts/999', json=data)
    assert response.status_code == 404


def test_get_alerts(client):
    """Test retrieving alerts."""
    # Create some test alerts
    alerts = [
        Alert(
            type=AlertType.EMERGENCY,
            description='Emergency alert',
            location='Location 1'
        ),
        Alert(
            type=AlertType.WARNING,
            description='Warning alert',
            location='Location 2'
        )
    ]
    with client.application.app_context():
        db.session.add_all(alerts)
        db.session.commit()

    # Test getting all alerts
    response = client.get('/alerts')
    assert response.status_code == 200
    assert len(response.json) == 2

    # Test filtering by type
    response = client.get('/alerts?type=EMERGENCY')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['type'] == 'EMERGENCY'

    # Test filtering by status
    response = client.get('/alerts?status=ACTIVE')
    assert response.status_code == 200
    assert len(response.json) == 2 