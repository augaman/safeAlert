"""Routes for the billing service."""
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional
import logging

from .database import get_db
from .models import Invoice, AuditLog
from .schemas import (
    InvoiceCreate, InvoiceResponse, InvoiceList,
    AuditLogCreate, AuditLogResponse, HealthCheck
)

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
billing_bp = Blueprint('billing', __name__)


@billing_bp.route('/billing/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        from datetime import datetime
        from .database import check_db_connection
        
        db_status = "healthy" if check_db_connection() else "unhealthy"
        response = HealthCheck(
            status="healthy",
            database=db_status,
            timestamp=datetime.utcnow()
        )
        return jsonify(response.dict()), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


@billing_bp.route('/billing/invoices', methods=['GET'])
def get_invoices():
    """Get list of invoices with pagination and filtering."""
    try:
        db: Session = next(get_db())
        
        # Get query parameters
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        status = request.args.get('status')
        
        # Build query
        query = db.query(Invoice)
        if status:
            query = query.filter(Invoice.status == status)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        invoices = query.order_by(desc(Invoice.created_at)) \
            .offset((page - 1) * size) \
            .limit(size) \
            .all()
        
        # Create response
        response = InvoiceList(
            items=invoices,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )
        
        return jsonify(response.dict()), 200
        
    except Exception as e:
        logger.error(f"Failed to get invoices: {str(e)}")
        return jsonify({"error": str(e)}), 400


@billing_bp.route('/billing/log', methods=['POST'])
def create_audit_log():
    """Create a new audit log entry."""
    try:
        # Validate request data
        data = AuditLogCreate(**request.get_json())
        
        # Create audit log entry
        db: Session = next(get_db())
        audit_log = AuditLog(
            event_type=data.event_type,
            description=data.description,
            user_id=data.user_id
        )
        
        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)
        
        logger.info(f"Created audit log entry: {audit_log.id}")
        return jsonify(AuditLogResponse.from_orm(audit_log).dict()), 201
        
    except Exception as e:
        logger.error(f"Failed to create audit log: {str(e)}")
        return jsonify({"error": str(e)}), 400 