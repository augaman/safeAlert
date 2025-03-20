"""Test module for alert schemas."""
import pytest
from datetime import datetime
from src.schemas import AlertSchema, AlertCreateSchema, AlertUpdateSchema
from src.models import Alert, AlertType, AlertStatus


def test_alert_schema_serialization():
    """Test alert schema serialization."""
    alert = Alert(
        id=1,
        type=AlertType.EMERGENCY,
        status=AlertStatus.ACTIVE,
        description='Test alert',
        location='Test location',
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    schema = AlertSchema()
    result = schema.dump(alert)
    
    assert result['id'] == 1
    assert result['type'] == 'EMERGENCY'
    assert result['status'] == 'ACTIVE'
    assert result['description'] == 'Test alert'
    assert result['location'] == 'Test location'
    assert 'created_at' in result
    assert 'updated_at' in result


def test_alert_create_schema_validation():
    """Test alert create schema validation."""
    # Valid data
    valid_data = {
        'type': 'EMERGENCY',
        'description': 'Test alert',
        'location': 'Test location'
    }
    schema = AlertCreateSchema()
    result = schema.load(valid_data)
    
    assert result['type'] == AlertType.EMERGENCY
    assert result['description'] == 'Test alert'
    assert result['location'] == 'Test location'
    
    # Invalid type
    invalid_data = {
        'type': 'INVALID_TYPE',
        'description': 'Test alert',
        'location': 'Test location'
    }
    with pytest.raises(ValueError):
        schema.load(invalid_data)
    
    # Missing required fields
    incomplete_data = {
        'type': 'EMERGENCY'
    }
    with pytest.raises(ValueError):
        schema.load(incomplete_data)


def test_alert_update_schema_validation():
    """Test alert update schema validation."""
    # Valid data
    valid_data = {
        'status': 'ACKNOWLEDGED',
        'acknowledged_by': 'Test User'
    }
    schema = AlertUpdateSchema()
    result = schema.load(valid_data)
    
    assert result['status'] == AlertStatus.ACKNOWLEDGED
    assert result['acknowledged_by'] == 'Test User'
    
    # Invalid status
    invalid_data = {
        'status': 'INVALID_STATUS',
        'acknowledged_by': 'Test User'
    }
    with pytest.raises(ValueError):
        schema.load(invalid_data)
    
    # Empty data (should be valid as all fields are optional)
    empty_data = {}
    result = schema.load(empty_data)
    assert result == {}


def test_alert_schema_deserialization():
    """Test alert schema deserialization."""
    data = {
        'id': 1,
        'type': 'EMERGENCY',
        'status': 'ACTIVE',
        'description': 'Test alert',
        'location': 'Test location',
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    
    schema = AlertSchema()
    result = schema.load(data)
    
    assert result['id'] == 1
    assert result['type'] == AlertType.EMERGENCY
    assert result['status'] == AlertStatus.ACTIVE
    assert result['description'] == 'Test alert'
    assert result['location'] == 'Test location'
    assert isinstance(result['created_at'], datetime)
    assert isinstance(result['updated_at'], datetime)


def test_alert_schema_with_optional_fields():
    """Test alert schema with optional fields."""
    data = {
        'id': 1,
        'type': 'EMERGENCY',
        'status': 'RESOLVED',
        'description': 'Test alert',
        'location': 'Test location',
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat(),
        'resolved_at': datetime.utcnow().isoformat(),
        'acknowledged_at': datetime.utcnow().isoformat(),
        'acknowledged_by': 'Test User'
    }
    
    schema = AlertSchema()
    result = schema.load(data)
    
    assert result['id'] == 1
    assert result['type'] == AlertType.EMERGENCY
    assert result['status'] == AlertStatus.RESOLVED
    assert result['description'] == 'Test alert'
    assert result['location'] == 'Test location'
    assert isinstance(result['resolved_at'], datetime)
    assert isinstance(result['acknowledged_at'], datetime)
    assert result['acknowledged_by'] == 'Test User' 