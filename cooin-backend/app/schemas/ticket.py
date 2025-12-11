from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from app.models.ticket import TicketType, TicketStatus, LoanType, WarrantyType


# Base Ticket Schema
class TicketBase(BaseModel):
    """Base ticket schema with common fields."""
    ticket_type: TicketType
    title: str = Field(..., min_length=10, max_length=200, description="Short title for the offer")
    description: str = Field(..., min_length=50, description="Detailed description")

    # Financial details
    amount: float = Field(..., gt=0, description="Amount to lend or borrow")
    min_amount: Optional[float] = Field(None, gt=0, description="Minimum amount (for flexible offers)")
    max_amount: Optional[float] = Field(None, gt=0, description="Maximum amount (for flexible offers)")

    interest_rate: float = Field(..., ge=0, le=100, description="Annual interest rate (%)")
    min_interest_rate: Optional[float] = Field(None, ge=0, le=100)
    max_interest_rate: Optional[float] = Field(None, ge=0, le=100)

    term_months: int = Field(..., gt=0, le=360, description="Loan term in months")
    min_term_months: Optional[int] = Field(None, gt=0, le=360)
    max_term_months: Optional[int] = Field(None, gt=0, le=360)

    # Loan details
    loan_type: LoanType
    loan_purpose: str = Field(..., min_length=20, description="Purpose/reason for the loan")

    # Warranty/Collateral
    warranty_type: WarrantyType = Field(default=WarrantyType.NONE)
    warranty_description: Optional[str] = Field(None, description="Details about collateral")
    warranty_value: Optional[float] = Field(None, gt=0, description="Estimated value of collateral")

    # Additional details
    requirements: Optional[str] = Field(None, description="Requirements for applicants")
    preferred_location: Optional[str] = Field(None, max_length=100)
    flexible_terms: bool = Field(default=False, description="Open to negotiation")

    # Visibility
    is_public: bool = Field(default=True, description="Visible in marketplace")
    expires_at: Optional[datetime] = Field(None, description="When ticket expires")

    @field_validator('max_amount')
    @classmethod
    def validate_max_amount(cls, v, info):
        """Ensure max_amount is greater than min_amount and amount."""
        if v is not None:
            amount = info.data.get('amount')
            min_amount = info.data.get('min_amount')
            if amount and v < amount:
                raise ValueError('max_amount must be greater than or equal to amount')
            if min_amount and v < min_amount:
                raise ValueError('max_amount must be greater than min_amount')
        return v

    @field_validator('warranty_value')
    @classmethod
    def validate_warranty_value(cls, v, info):
        """Ensure warranty_value is provided if warranty_type is not NONE."""
        warranty_type = info.data.get('warranty_type')
        if warranty_type and warranty_type != WarrantyType.NONE and not v:
            raise ValueError('warranty_value is required when warranty_type is not NONE')
        return v


# Create Ticket Schema
class TicketCreate(TicketBase):
    """Schema for creating a new ticket."""
    pass


# Update Ticket Schema
class TicketUpdate(BaseModel):
    """Schema for updating an existing ticket."""
    title: Optional[str] = Field(None, min_length=10, max_length=200)
    description: Optional[str] = Field(None, min_length=50)

    amount: Optional[float] = Field(None, gt=0)
    min_amount: Optional[float] = Field(None, gt=0)
    max_amount: Optional[float] = Field(None, gt=0)

    interest_rate: Optional[float] = Field(None, ge=0, le=100)
    min_interest_rate: Optional[float] = Field(None, ge=0, le=100)
    max_interest_rate: Optional[float] = Field(None, ge=0, le=100)

    term_months: Optional[int] = Field(None, gt=0, le=360)
    min_term_months: Optional[int] = Field(None, gt=0, le=360)
    max_term_months: Optional[int] = Field(None, gt=0, le=360)

    loan_type: Optional[LoanType] = None
    loan_purpose: Optional[str] = Field(None, min_length=20)

    warranty_type: Optional[WarrantyType] = None
    warranty_description: Optional[str] = None
    warranty_value: Optional[float] = Field(None, gt=0)

    requirements: Optional[str] = None
    preferred_location: Optional[str] = Field(None, max_length=100)
    flexible_terms: Optional[bool] = None

    is_public: Optional[bool] = None
    expires_at: Optional[datetime] = None
    status: Optional[TicketStatus] = None


# Ticket Response Schema
class TicketResponse(TicketBase):
    """Schema for ticket response."""
    id: int
    user_id: int
    status: TicketStatus

    # Engagement metrics
    views_count: int
    responses_count: int
    deals_created: int

    # Timestamps
    created_at: datetime
    updated_at: datetime
    last_viewed_at: Optional[datetime] = None

    # Computed properties
    is_active: bool
    is_expired: bool
    days_active: int
    is_lending_offer: bool
    is_borrowing_request: bool
    has_warranty: bool

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "ticket_type": "lending_offer",
                "status": "active",
                "title": "Offering $50,000 for small business loans",
                "description": "Experienced lender looking to support local small businesses...",
                "amount": 50000.0,
                "interest_rate": 8.5,
                "term_months": 24,
                "loan_type": "business",
                "loan_purpose": "Supporting small business growth and expansion",
                "warranty_type": "property",
                "warranty_value": 100000.0,
                "flexible_terms": True,
                "is_public": True,
                "views_count": 45,
                "responses_count": 3,
                "deals_created": 0
            }
        }


# Ticket with User Info
class TicketWithUser(TicketResponse):
    """Ticket response with user information."""
    user: dict  # Will contain basic user info (username, role, rating)

    class Config:
        from_attributes = True


# Ticket List Response
class TicketListResponse(BaseModel):
    """Paginated ticket list response."""
    tickets: List[TicketResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int

    class Config:
        json_schema_extra = {
            "example": {
                "tickets": [],
                "total_count": 25,
                "page": 1,
                "page_size": 20,
                "total_pages": 2
            }
        }


# Ticket Filter Schema
class TicketFilter(BaseModel):
    """Schema for filtering tickets."""
    ticket_type: Optional[TicketType] = None
    status: Optional[TicketStatus] = Field(default=TicketStatus.ACTIVE)
    loan_type: Optional[LoanType] = None
    warranty_type: Optional[WarrantyType] = None

    min_amount: Optional[float] = Field(None, gt=0)
    max_amount: Optional[float] = Field(None, gt=0)

    min_interest_rate: Optional[float] = Field(None, ge=0, le=100)
    max_interest_rate: Optional[float] = Field(None, ge=0, le=100)

    min_term_months: Optional[int] = Field(None, gt=0)
    max_term_months: Optional[int] = Field(None, gt=0)

    location: Optional[str] = None
    flexible_terms_only: bool = False

    # Pagination
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    # Sorting
    sort_by: str = Field(default="created_at", description="Field to sort by")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")


# Create Deal from Ticket Schema
class CreateDealFromTicket(BaseModel):
    """Schema for creating a deal/connection from a ticket."""
    ticket_id: int = Field(..., description="ID of the ticket to respond to")
    message: str = Field(..., min_length=20, description="Message to the ticket creator")

    # Optional: Override ticket terms if flexible
    proposed_amount: Optional[float] = Field(None, gt=0)
    proposed_interest_rate: Optional[float] = Field(None, ge=0, le=100)
    proposed_term_months: Optional[int] = Field(None, gt=0, le=360)

    class Config:
        json_schema_extra = {
            "example": {
                "ticket_id": 1,
                "message": "I'm interested in your lending offer. I have a solid business plan and good credit history.",
                "proposed_amount": 45000.0,
                "proposed_interest_rate": 8.0,
                "proposed_term_months": 24
            }
        }


# Ticket Statistics
class TicketStats(BaseModel):
    """Statistics for user's tickets."""
    total_tickets: int
    active_tickets: int
    completed_tickets: int
    total_views: int
    total_responses: int
    total_deals: int

    lending_offers: int
    borrowing_requests: int

    class Config:
        json_schema_extra = {
            "example": {
                "total_tickets": 5,
                "active_tickets": 3,
                "completed_tickets": 2,
                "total_views": 156,
                "total_responses": 12,
                "total_deals": 2,
                "lending_offers": 3,
                "borrowing_requests": 2
            }
        }
