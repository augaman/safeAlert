"""Pydantic models for request/response validation."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, condecimal


class InvoiceBase(BaseModel):
    """Base schema for invoice data."""
    invoice_number: str = Field(..., min_length=1, max_length=50)
    amount: condecimal(max_digits=10, decimal_places=2) = Field(..., gt=0)
    status: str = Field(..., pattern="^(PENDING|PAID|OVERDUE)$")


class InvoiceCreate(InvoiceBase):
    """Schema for creating a new invoice."""
    pass


class InvoiceResponse(InvoiceBase):
    """Schema for invoice response."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class InvoiceList(BaseModel):
    """Schema for list of invoices with pagination."""
    items: List[InvoiceResponse]
    total: int
    page: int
    size: int
    pages: int


class AuditLogBase(BaseModel):
    """Base schema for audit log data."""
    event_type: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    user_id: Optional[str] = Field(None, max_length=100)


class AuditLogCreate(AuditLogBase):
    """Schema for creating a new audit log entry."""
    pass


class AuditLogResponse(AuditLogBase):
    """Schema for audit log response."""
    id: int
    timestamp: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class HealthCheck(BaseModel):
    """Schema for health check response."""
    status: str
    database: str
    timestamp: datetime 