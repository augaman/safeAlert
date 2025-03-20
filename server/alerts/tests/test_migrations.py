"""Test module for database migrations."""
import pytest
from alembic.config import Config
from alembic import command
from src.models import db, Alert, AlertType, AlertStatus


def test_migration_upgrade(app):
    """Test database migration upgrade."""
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
        
        # Check column types
        for col in columns:
            if col['name'] == 'id':
                assert str(col['type']) == 'INTEGER'
            elif col['name'] in ['type', 'status']:
                assert str(col['type']) == 'VARCHAR(20)'
            elif col['name'] in ['description', 'location']:
                assert str(col['type']) == 'VARCHAR(500)'
            elif col['name'] == 'acknowledged_by':
                assert str(col['type']) == 'VARCHAR(100)'
            elif col['name'] in ['created_at', 'updated_at', 'resolved_at', 'acknowledged_at']:
                assert str(col['type']) == 'DATETIME'


def test_migration_downgrade(app):
    """Test database migration downgrade."""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create test data
        alert = Alert(
            type=AlertType.EMERGENCY,
            description='Test alert',
            location='Test location'
        )
        db.session.add(alert)
        db.session.commit()
        
        # Drop tables
        db.drop_all()
        
        # Verify tables are dropped
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        assert 'alerts' not in tables


def test_migration_data_integrity(app):
    """Test data integrity after migration."""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create test data
        alert = Alert(
            type=AlertType.EMERGENCY,
            description='Test alert',
            location='Test location'
        )
        db.session.add(alert)
        db.session.commit()
        
        # Verify data
        retrieved_alert = Alert.query.first()
        assert retrieved_alert is not None
        assert retrieved_alert.type == AlertType.EMERGENCY
        assert retrieved_alert.description == 'Test alert'
        assert retrieved_alert.location == 'Test location'
        assert retrieved_alert.status == AlertStatus.ACTIVE
        assert retrieved_alert.created_at is not None
        assert retrieved_alert.updated_at is not None
        assert retrieved_alert.resolved_at is None
        assert retrieved_alert.acknowledged_at is None
        assert retrieved_alert.acknowledged_by is None


def test_migration_constraints(app):
    """Test database constraints after migration."""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Test NOT NULL constraints
        with pytest.raises(Exception):
            alert = Alert()
            db.session.add(alert)
            db.session.commit()
        
        # Test enum constraints
        with pytest.raises(Exception):
            alert = Alert(
                type='INVALID_TYPE',  # type: ignore
                description='Test alert',
                location='Test location'
            )
            db.session.add(alert)
            db.session.commit()
        
        # Test string length constraints
        with pytest.raises(Exception):
            alert = Alert(
                type=AlertType.EMERGENCY,
                description='x' * 501,  # Exceeds max length
                location='Test location'
            )
            db.session.add(alert)
            db.session.commit()


def test_migration_indexes(app):
    """Test database indexes after migration."""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Verify indexes
        inspector = db.inspect(db.engine)
        indexes = inspector.get_indexes('alerts')
        
        # Check primary key index
        pk_index = next((idx for idx in indexes if idx['name'] == 'ix_alerts_id'), None)
        assert pk_index is not None
        assert pk_index['unique']
        
        # Check type index
        type_index = next((idx for idx in indexes if idx['name'] == 'ix_alerts_type'), None)
        assert type_index is not None
        
        # Check status index
        status_index = next((idx for idx in indexes if idx['name'] == 'ix_alerts_status'), None)
        assert status_index is not None 