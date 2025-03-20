"""Alert model definition."""
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class AlertStatus(str, Enum):
    """Enum for alert statuses."""
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class AlertType(str, Enum):
    """Enum for alert types."""
    EMERGENCY = "emergency"
    WARNING = "warning"
    INFO = "info"


class Alert(db.Model):
    """Alert model for storing alert information."""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    type = Column(SQLEnum(AlertType), nullable=False)
    status = Column(SQLEnum(AlertStatus), nullable=False, default=AlertStatus.ACTIVE)
    description = Column(String(500), nullable=False)
    location = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    acknowledged_by = Column(String(100), nullable=True)

    def to_dict(self):
        """Convert alert to dictionary."""
        return {
            "id": self.id,
            "type": self.type,
            "status": self.status,
            "description": self.description,
            "location": self.location,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "acknowledged_at": self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            "acknowledged_by": self.acknowledged_by
        } 