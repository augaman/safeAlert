"""Alert routes."""
from datetime import datetime
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from models import db, Alert, AlertStatus
from schemas import AlertCreate, AlertUpdate, AlertResponse
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
alerts_bp = Blueprint('alerts', __name__)


@alerts_bp.route('/alerts/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        # Try to query the database
        db.session.execute('SELECT 1')
        return jsonify({"status": "healthy"}), 200
    except SQLAlchemyError as e:
        logger.error(f"Database health check failed: {str(e)}")
        return jsonify({"status": "unhealthy", "error": "Database connection failed"}), 500


@alerts_bp.route('/alerts', methods=['POST'])
def create_alert():
    """Create a new alert."""
    try:
        data = AlertCreate(**request.get_json())
        alert = Alert(
            type=data.type,
            description=data.description,
            location=data.location
        )
        db.session.add(alert)
        db.session.commit()
        logger.info(f"Created new alert with ID: {alert.id}")
        return jsonify(AlertResponse.from_orm(alert).dict()), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to create alert: {str(e)}")
        return jsonify({"error": str(e)}), 400


@alerts_bp.route('/alerts/<int:alert_id>', methods=['PUT'])
def update_alert(alert_id):
    """Update an existing alert."""
    try:
        alert = Alert.query.get_or_404(alert_id)
        data = AlertUpdate(**request.get_json())
        
        # Update fields if provided
        if data.status is not None:
            alert.status = data.status
            if data.status == AlertStatus.RESOLVED:
                alert.resolved_at = datetime.utcnow()
            elif data.status == AlertStatus.ACKNOWLEDGED:
                alert.acknowledged_at = datetime.utcnow()
                alert.acknowledged_by = data.acknowledged_by
        
        if data.description is not None:
            alert.description = data.description
        if data.location is not None:
            alert.location = data.location
        
        db.session.commit()
        logger.info(f"Updated alert with ID: {alert_id}")
        return jsonify(AlertResponse.from_orm(alert).dict()), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to update alert {alert_id}: {str(e)}")
        return jsonify({"error": str(e)}), 400


@alerts_bp.route('/alerts', methods=['GET'])
def get_alerts():
    """Get list of alerts with optional filtering."""
    try:
        status = request.args.get('status')
        alert_type = request.args.get('type')
        
        query = Alert.query
        
        if status:
            query = query.filter(Alert.status == status)
        if alert_type:
            query = query.filter(Alert.type == alert_type)
        
        alerts = query.order_by(Alert.created_at.desc()).all()
        return jsonify([AlertResponse.from_orm(alert).dict() for alert in alerts]), 200
    except Exception as e:
        logger.error(f"Failed to retrieve alerts: {str(e)}")
        return jsonify({"error": str(e)}), 400 