"""Pydantic models for request validation."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from models import AlertType, AlertStatus


class AlertBase(BaseModel):
    """Base alert schema."""
    type: AlertType
    description: str = Field(..., min_length=1, max_length=500)
    location: str = Field(..., min_length=1, max_length=200)


class AlertCreate(AlertBase):
    """Schema for creating a new alert."""
    pass


class AlertUpdate(BaseModel):
    """Schema for updating an alert."""
    status: Optional[AlertStatus] = None
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    location: Optional[str] = Field(None, min_length=1, max_length=200)
    acknowledged_by: Optional[str] = Field(None, min_length=1, max_length=100)


class AlertResponse(AlertBase):
    """Schema for alert response."""
    id: int
    status: AlertStatus
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None
    acknowledged_by: Optional[str] = None

    class Config:
        """Pydantic config."""
        from_attributes = True 