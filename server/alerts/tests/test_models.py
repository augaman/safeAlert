"""Test module for alert models."""
import pytest
from datetime import datetime
from src.models import Alert, AlertType, AlertStatus, db


def test_alert_creation(app):
    """Test creating an alert model."""
    with app.app_context():
        alert = Alert(
            type=AlertType.EMERGENCY,
            description='Test emergency alert',
            location='Test location'
        )
        db.session.add(alert)
        db.session.commit()

        assert alert.id is not None
        assert alert.type == AlertType.EMERGENCY
        assert alert.description == 'Test emergency alert'
        assert alert.location == 'Test location'
        assert alert.status == AlertStatus.ACTIVE
        assert alert.created_at is not None
        assert alert.updated_at is not None
        assert alert.resolved_at is None
        assert alert.acknowledged_at is None
        assert alert.acknowledged_by is None


def test_alert_update(app):
    """Test updating an alert model."""
    with app.app_context():
        alert = Alert(
            type=AlertType.EMERGENCY,
            description='Test emergency alert',
            location='Test location'
        )
        db.session.add(alert)
        db.session.commit()

        # Update alert status
        alert.status = AlertStatus.ACKNOWLEDGED
        alert.acknowledged_by = 'Test User'
        alert.acknowledged_at = datetime.utcnow()
        db.session.commit()

        assert alert.status == AlertStatus.ACKNOWLEDGED
        assert alert.acknowledged_by == 'Test User'
        assert alert.acknowledged_at is not None

        # Resolve alert
        alert.status = AlertStatus.RESOLVED
        alert.resolved_at = datetime.utcnow()
        db.session.commit()

        assert alert.status == AlertStatus.RESOLVED
        assert alert.resolved_at is not None


def test_alert_validation(app):
    """Test alert model validation."""
    with app.app_context():
        # Test invalid alert type
        with pytest.raises(ValueError):
            Alert(
                type='INVALID_TYPE',  # type: ignore
                description='Test alert',
                location='Test location'
            )

        # Test invalid status
        alert = Alert(
            type=AlertType.EMERGENCY,
            description='Test alert',
            location='Test location'
        )
        with pytest.raises(ValueError):
            alert.status = 'INVALID_STATUS'  # type: ignore


def test_alert_timestamps(app):
    """Test alert model timestamps."""
    with app.app_context():
        alert = Alert(
            type=AlertType.EMERGENCY,
            description='Test alert',
            location='Test location'
        )
        db.session.add(alert)
        db.session.commit()

        created_at = alert.created_at
        updated_at = alert.updated_at

        # Update alert
        alert.description = 'Updated description'
        db.session.commit()

        assert alert.created_at == created_at
        assert alert.updated_at > updated_at


def test_alert_relationships(app):
    """Test alert model relationships."""
    with app.app_context():
        alert = Alert(
            type=AlertType.EMERGENCY,
            description='Test alert',
            location='Test location'
        )
        db.session.add(alert)
        db.session.commit()

        # Test that alert can be retrieved
        retrieved_alert = Alert.query.get(alert.id)
        assert retrieved_alert is not None
        assert retrieved_alert.id == alert.id 