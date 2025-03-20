"""SQLAlchemy models for billing and audit service."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Invoice(Base):
    """Model for storing invoice information."""
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True)
    invoice_number = Column(String(50), unique=True, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum('PENDING', 'PAID', 'OVERDUE', name='invoice_status'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        """String representation of the Invoice model."""
        return f"<Invoice {self.invoice_number}>"


class AuditLog(Base):
    """Model for storing audit log entries."""
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True)
    event_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    user_id = Column(String(100), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        """String representation of the AuditLog model."""
        return f"<AuditLog {self.event_type}>" 