"""Pydantic models for message validation."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    """Base message schema."""
    sender: str = Field(..., min_length=1, max_length=100)
    recipient: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=5000)
    message_type: str = Field(..., min_length=1, max_length=50)
    priority: str = Field(..., pattern="^(LOW|MEDIUM|HIGH)$")


class MessageCreate(MessageBase):
    """Schema for creating a new message."""
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)


class MessageResponse(MessageBase):
    """Schema for message response."""
    id: str
    timestamp: datetime
    status: str = Field(..., pattern="^(PENDING|SENT|FAILED)$")
    error_message: Optional[str] = None

    class Config:
        """Pydantic config."""
        from_attributes = True


class MessageStatus(BaseModel):
    """Schema for message status update."""
    status: str = Field(..., pattern="^(PENDING|SENT|FAILED)$")
    error_message: Optional[str] = None 