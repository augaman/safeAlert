"""Test module for database operations."""
import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from src.models import db, Alert, AlertType, AlertStatus
import os


def test_database_connection(app):
    """Test database connection."""
    with app.app_context():
        # Test connection
        result = db.session.execute('SELECT 1').scalar()
        assert result == 1


def test_database_transactions(app):
    """Test database transactions."""
    with app.app_context():
        # Start transaction
        alert = Alert(
            type=AlertType.EMERGENCY,
            description='Test alert',
            location='Test location'
        )
        db.session.add(alert)
        
        # Verify alert is in session but not committed
        assert alert in db.session
        assert alert.id is None
        
        # Commit transaction
        db.session.commit()
        
        # Verify alert is committed
        assert alert.id is not None
        
        # Rollback transaction
        alert.description = 'Updated description'
        db.session.rollback()
        
        # Verify changes are rolled back
        assert alert.description == 'Test alert'


def test_database_constraints(app):
    """Test database constraints."""
    with app.app_context():
        # Test NOT NULL constraint
        alert = Alert()
        with pytest.raises(IntegrityError):
            db.session.add(alert)
            db.session.commit()
        
        # Test enum constraint
        alert = Alert(
            type='INVALID_TYPE',  # type: ignore
            description='Test alert',
            location='Test location'
        )
        with pytest.raises(IntegrityError):
            db.session.add(alert)
            db.session.commit()
        
        # Test string length constraint
        alert = Alert(
            type=AlertType.EMERGENCY,
            description='x' * 501,  # Exceeds max length
            location='Test location'
        )
        with pytest.raises(IntegrityError):
            db.session.add(alert)
            db.session.commit()


def test_database_indexes(app):
    """Test database indexes."""
    with app.app_context():
        # Create test alerts
        alerts = [
            Alert(
                type=AlertType.EMERGENCY,
                description=f'Alert {i}',
                location=f'Location {i}'
            )
            for i in range(10)
        ]
        for alert in alerts:
            db.session.add(alert)
        db.session.commit()
        
        # Test index on type
        emergency_alerts = Alert.query.filter_by(type=AlertType.EMERGENCY).all()
        assert len(emergency_alerts) > 0
        
        # Test index on status
        active_alerts = Alert.query.filter_by(status=AlertStatus.ACTIVE).all()
        assert len(active_alerts) > 0


def test_database_relationships(app):
    """Test database relationships."""
    with app.app_context():
        # Create test alert
        alert = Alert(
            type=AlertType.EMERGENCY,
            description='Test alert',
            location='Test location'
        )
        db.session.add(alert)
        db.session.commit()
        
        # Test relationship queries
        retrieved_alert = Alert.query.get(alert.id)
        assert retrieved_alert is not None
        assert retrieved_alert.id == alert.id


def test_database_migrations(app):
    """Test database migrations."""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Verify table structure
        inspector = db.inspect(db.engine)
        columns = inspector.get_columns('alerts')
        
        # Check required columns
        column_names = [col['name'] for col in columns]
        required_columns = [
            'id', 'type', 'status', 'description', 'location',
            'created_at', 'updated_at', 'resolved_at', 'acknowledged_at',
            'acknowledged_by'
        ]
        
        for col in required_columns:
            assert col in column_names


def test_database_performance(app):
    """Test database performance."""
    with app.app_context():
        # Create large number of alerts
        alerts = [
            Alert(
                type=AlertType.EMERGENCY,
                description=f'Alert {i}',
                location=f'Location {i}'
            )
            for i in range(1000)
        ]
        
        # Test bulk insert performance
        start_time = datetime.utcnow()
        for alert in alerts:
            db.session.add(alert)
        db.session.commit()
        insert_time = (datetime.utcnow() - start_time).total_seconds()
        assert insert_time < 5.0  # Should complete within 5 seconds
        
        # Test query performance
        start_time = datetime.utcnow()
        emergency_alerts = Alert.query.filter_by(type=AlertType.EMERGENCY).all()
        query_time = (datetime.utcnow() - start_time).total_seconds()
        assert query_time < 1.0  # Should complete within 1 second


def test_database_concurrency(app):
    """Test database concurrency."""
    with app.app_context():
        # Create test alert
        alert = Alert(
            type=AlertType.EMERGENCY,
            description='Test alert',
            location='Test location'
        )
        db.session.add(alert)
        db.session.commit()
        
        # Simulate concurrent updates
        alert1 = Alert.query.get(alert.id)
        alert2 = Alert.query.get(alert.id)
        
        alert1.description = 'Update 1'
        alert2.description = 'Update 2'
        
        db.session.add(alert1)
        db.session.commit()
        
        with pytest.raises(Exception):
            db.session.add(alert2)
            db.session.commit()


def test_database_backup(app):
    """Test database backup functionality."""
    with app.app_context():
        # Create test data
        alert = Alert(
            type=AlertType.EMERGENCY,
            description='Test alert',
            location='Test location'
        )
        db.session.add(alert)
        db.session.commit()
        
        # Verify backup file exists
        backup_file = 'backup.sql'
        assert os.path.exists(backup_file)
        
        # Verify backup contains data
        with open(backup_file, 'r') as f:
            backup_content = f.read()
            assert 'Test alert' in backup_content 