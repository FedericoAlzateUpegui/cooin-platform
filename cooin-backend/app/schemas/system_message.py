from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator

from app.models.system_message import SystemMessageType, SystemMessagePriority


# Base schema
class SystemMessageBase(BaseModel):
    """Base schema for system messages."""
    title: str = Field(..., min_length=1, max_length=200, description="Message title")
    content: str = Field(..., min_length=1, description="Message content")
    message_type: SystemMessageType = Field(default=SystemMessageType.ANNOUNCEMENT)
    priority: SystemMessagePriority = Field(default=SystemMessagePriority.MEDIUM)
    action_url: Optional[str] = Field(None, max_length=500, description="Action URL or deep link")
    action_label: Optional[str] = Field(None, max_length=100, description="Action button label")
    image_url: Optional[str] = Field(None, max_length=500, description="Image URL")
    category: Optional[str] = Field(None, max_length=100, description="Message category")
    tags: Optional[str] = Field(None, max_length=500, description="Comma-separated tags")
    expires_at: Optional[datetime] = Field(None, description="Expiration timestamp")


# Create schema
class SystemMessageCreate(SystemMessageBase):
    """Schema for creating system messages."""
    user_id: int = Field(..., description="Recipient user ID")

    class Config:
        use_enum_values = True


# Bulk create schema
class SystemMessageBulkCreate(SystemMessageBase):
    """Schema for creating system messages for multiple users."""
    user_ids: List[int] = Field(..., min_items=1, description="List of recipient user IDs")

    class Config:
        use_enum_values = True


# Update schema
class SystemMessageUpdate(BaseModel):
    """Schema for updating system messages."""
    is_read: Optional[bool] = None
    is_archived: Optional[bool] = None

    class Config:
        use_enum_values = True


# Response schema
class SystemMessageResponse(SystemMessageBase):
    """Schema for system message responses."""
    id: int
    user_id: int
    is_read: bool
    read_at: Optional[datetime]
    is_archived: bool
    archived_at: Optional[datetime]
    is_deleted: bool
    deleted_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    @validator('message_type', 'priority', pre=True)
    def enum_to_string(cls, v):
        """Convert enum to string for JSON serialization."""
        if hasattr(v, 'value'):
            return v.value
        return v

    class Config:
        from_attributes = True
        use_enum_values = True


# List response schema
class SystemMessageListResponse(BaseModel):
    """Schema for paginated system message list."""
    messages: List[SystemMessageResponse]
    total_count: int
    unread_count: int
    page: int
    page_size: int
    total_pages: int

    class Config:
        from_attributes = True


# Statistics schema
class SystemMessageStats(BaseModel):
    """Schema for system message statistics."""
    total_messages: int
    unread_messages: int
    archived_messages: int
    messages_by_type: dict
    messages_by_priority: dict

    class Config:
        from_attributes = True
