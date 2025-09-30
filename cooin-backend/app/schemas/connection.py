from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum

from app.models.connection import ConnectionStatus, ConnectionType


class ConnectionStatusSchema(str, Enum):
    """Connection status schema for API."""
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    BLOCKED = "blocked"
    EXPIRED = "expired"


class ConnectionTypeSchema(str, Enum):
    """Connection type schema for API."""
    LENDING_INQUIRY = "lending_inquiry"
    BORROWING_REQUEST = "borrowing_request"
    GENERAL_CONNECTION = "general_connection"
    REFERRAL = "referral"


class ConnectionBase(BaseModel):
    """Base connection schema."""
    connection_type: ConnectionTypeSchema = ConnectionTypeSchema.GENERAL_CONNECTION
    message: Optional[str] = Field(None, max_length=1000, description="Initial message from requester")

    # Financial details (optional)
    loan_amount_requested: Optional[float] = Field(None, ge=100, le=1000000, description="Loan amount requested")
    loan_term_months: Optional[int] = Field(None, ge=1, le=360, description="Loan term in months")
    interest_rate_proposed: Optional[float] = Field(None, ge=0.1, le=50, description="Proposed interest rate")
    loan_purpose: Optional[str] = Field(None, max_length=200, description="Purpose of the loan")

    # Priority level
    priority_level: Optional[int] = Field(1, ge=1, le=3, description="Priority level (1=normal, 2=high, 3=urgent)")

    @validator('message')
    def validate_message(cls, v):
        if v is not None and len(v.strip()) < 10:
            raise ValueError('Message must be at least 10 characters long')
        return v

    @validator('loan_amount_requested')
    def validate_loan_amount(cls, v, values):
        if v is not None and v < 100:
            raise ValueError('Loan amount must be at least $100')
        return v


class ConnectionCreate(ConnectionBase):
    """Schema for creating a connection request."""
    receiver_id: int = Field(..., description="ID of the user to connect with")

    class Config:
        json_schema_extra = {
            "example": {
                "receiver_id": 2,
                "connection_type": "lending_inquiry",
                "message": "Hi! I'm interested in your lending services for a home improvement project.",
                "loan_amount_requested": 25000.0,
                "loan_term_months": 60,
                "interest_rate_proposed": 7.5,
                "loan_purpose": "Kitchen renovation",
                "priority_level": 2
            }
        }


class ConnectionUpdate(BaseModel):
    """Schema for updating a connection."""
    status: Optional[ConnectionStatusSchema] = None
    response_message: Optional[str] = Field(None, max_length=1000)
    interest_rate_proposed: Optional[float] = Field(None, ge=0.1, le=50)
    requester_notes: Optional[str] = Field(None, max_length=500)
    receiver_notes: Optional[str] = Field(None, max_length=500)

    @validator('response_message')
    def validate_response_message(cls, v):
        if v is not None and len(v.strip()) < 5:
            raise ValueError('Response message must be at least 5 characters long')
        return v


class ConnectionResponse(ConnectionBase):
    """Schema for connection response."""
    id: int
    requester_id: int
    receiver_id: int
    status: ConnectionStatusSchema
    response_message: Optional[str] = None

    # Additional metadata
    is_mutual: bool
    requester_notes: Optional[str] = None
    receiver_notes: Optional[str] = None

    # Communication tracking
    last_message_at: Optional[datetime] = None
    message_count: int

    # Timestamps
    created_at: datetime
    updated_at: datetime
    responded_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    # Computed fields
    days_since_created: int
    is_expired: bool

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "requester_id": 1,
                "receiver_id": 2,
                "connection_type": "lending_inquiry",
                "status": "pending",
                "message": "Hi! I'm interested in your lending services.",
                "loan_amount_requested": 25000.0,
                "loan_term_months": 60,
                "is_mutual": False,
                "message_count": 0,
                "days_since_created": 0,
                "is_expired": False,
                "created_at": "2023-10-01T12:00:00Z"
            }
        }


class ConnectionPublicResponse(BaseModel):
    """Schema for public connection information (limited data)."""
    id: int
    connection_type: ConnectionTypeSchema
    status: ConnectionStatusSchema
    loan_amount_requested: Optional[float] = None
    loan_term_months: Optional[int] = None
    loan_purpose: Optional[str] = None
    created_at: datetime
    is_mutual: bool

    class Config:
        from_attributes = True


class ConnectionListResponse(BaseModel):
    """Schema for paginated connection list."""
    connections: List[ConnectionResponse]
    total_count: int
    page: int
    page_size: int
    has_next: bool
    has_previous: bool

    class Config:
        json_schema_extra = {
            "example": {
                "connections": [],
                "total_count": 25,
                "page": 1,
                "page_size": 20,
                "has_next": True,
                "has_previous": False
            }
        }


class ConnectionStatsResponse(BaseModel):
    """Schema for connection statistics."""
    total_connections: int
    pending_sent: int
    pending_received: int
    accepted_connections: int
    rejected_connections: int
    mutual_connections: int
    recent_activity: int  # connections in last 7 days

    class Config:
        json_schema_extra = {
            "example": {
                "total_connections": 15,
                "pending_sent": 3,
                "pending_received": 2,
                "accepted_connections": 8,
                "rejected_connections": 2,
                "mutual_connections": 1,
                "recent_activity": 5
            }
        }


# Message Schemas
class MessageBase(BaseModel):
    """Base message schema."""
    content: str = Field(..., min_length=1, max_length=2000)
    message_type: Optional[str] = Field("text", description="Type of message")

    @validator('content')
    def validate_content(cls, v):
        if len(v.strip()) < 1:
            raise ValueError('Message content cannot be empty')
        return v


class MessageCreate(MessageBase):
    """Schema for creating a message."""

    class Config:
        json_schema_extra = {
            "example": {
                "content": "Thanks for accepting my connection request! When would be a good time to discuss the loan details?",
                "message_type": "text"
            }
        }


class MessageUpdate(BaseModel):
    """Schema for updating a message."""
    content: Optional[str] = Field(None, min_length=1, max_length=2000)

    @validator('content')
    def validate_content(cls, v):
        if v is not None and len(v.strip()) < 1:
            raise ValueError('Message content cannot be empty')
        return v


class MessageResponse(MessageBase):
    """Schema for message response."""
    id: int
    connection_id: int
    sender_id: int
    receiver_id: int

    # Message status
    is_read: bool
    is_deleted: bool

    # File attachments
    attachment_url: Optional[str] = None
    attachment_filename: Optional[str] = None
    attachment_size: Optional[int] = None

    # Timestamps
    created_at: datetime
    updated_at: datetime
    read_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "connection_id": 1,
                "sender_id": 1,
                "receiver_id": 2,
                "content": "Thanks for accepting my connection request!",
                "message_type": "text",
                "is_read": False,
                "is_deleted": False,
                "created_at": "2023-10-01T12:00:00Z"
            }
        }


class MessageListResponse(BaseModel):
    """Schema for paginated message list."""
    messages: List[MessageResponse]
    total_count: int
    unread_count: int
    page: int
    page_size: int
    has_next: bool
    has_previous: bool

    class Config:
        json_schema_extra = {
            "example": {
                "messages": [],
                "total_count": 12,
                "unread_count": 3,
                "page": 1,
                "page_size": 20,
                "has_next": False,
                "has_previous": False
            }
        }


# Matching Schemas
class MatchingCriteria(BaseModel):
    """Schema for matching criteria."""
    user_role: Optional[str] = Field(None, description="Role to match (lender/borrower)")
    location: Optional[str] = Field(None, description="Location filter")
    min_loan_amount: Optional[float] = Field(None, ge=100)
    max_loan_amount: Optional[float] = Field(None, ge=100)
    loan_purpose: Optional[str] = None
    max_interest_rate: Optional[float] = Field(None, ge=0.1, le=50)
    min_loan_term: Optional[int] = Field(None, ge=1, le=360)
    max_loan_term: Optional[int] = Field(None, ge=1, le=360)
    income_range: Optional[str] = None
    credit_score_min: Optional[int] = Field(None, ge=300, le=850)
    verified_only: bool = Field(False, description="Only show verified users")

    class Config:
        json_schema_extra = {
            "example": {
                "user_role": "lender",
                "location": "California",
                "min_loan_amount": 20000,
                "max_loan_amount": 50000,
                "loan_purpose": "home_improvement",
                "max_interest_rate": 8.0,
                "verified_only": True
            }
        }


class MatchingResult(BaseModel):
    """Schema for matching results."""
    user_id: int
    compatibility_score: float = Field(..., ge=0, le=100, description="Compatibility percentage")
    match_reasons: List[str] = Field(..., description="Why this user is a good match")

    # User preview data
    public_name: str
    location_string: str
    profile_completion_percentage: float
    is_verified: bool

    # Relevant matching data
    loan_amount_range: Optional[str] = None
    interest_rate_range: Optional[str] = None
    loan_terms: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 2,
                "compatibility_score": 85.5,
                "match_reasons": [
                    "Loan amount matches your range ($20K-$50K)",
                    "Located in your preferred area (California)",
                    "Verified lender with good ratings"
                ],
                "public_name": "Sarah L.",
                "location_string": "Los Angeles, California",
                "profile_completion_percentage": 95.0,
                "is_verified": True,
                "loan_amount_range": "$10K - $50K",
                "interest_rate_range": "5.5% - 8.0%"
            }
        }


class MatchingResponse(BaseModel):
    """Schema for matching results response."""
    matches: List[MatchingResult]
    total_matches: int
    search_criteria: MatchingCriteria
    search_time_ms: int

    class Config:
        json_schema_extra = {
            "example": {
                "matches": [],
                "total_matches": 8,
                "search_criteria": {},
                "search_time_ms": 125
            }
        }