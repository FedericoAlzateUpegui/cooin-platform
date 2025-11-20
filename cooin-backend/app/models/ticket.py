from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class TicketType(enum.Enum):
    """Type of ticket - who is creating the offer."""
    LENDING_OFFER = "lending_offer"  # Lender offering money
    BORROWING_REQUEST = "borrowing_request"  # Borrower requesting money


class TicketStatus(enum.Enum):
    """Status of ticket."""
    ACTIVE = "active"  # Ticket is active and visible
    INACTIVE = "inactive"  # Ticket is inactive (paused by user)
    COMPLETED = "completed"  # Deal was created from this ticket
    EXPIRED = "expired"  # Ticket expired
    CANCELLED = "cancelled"  # User cancelled the ticket


class LoanType(enum.Enum):
    """Type of loan."""
    PERSONAL = "personal"  # Personal loan
    BUSINESS = "business"  # Business loan
    MORTGAGE = "mortgage"  # Mortgage/real estate
    AUTO = "auto"  # Auto loan
    EDUCATION = "education"  # Education loan
    MEDICAL = "medical"  # Medical expenses
    OTHER = "other"  # Other purpose


class WarrantyType(enum.Enum):
    """Type of warranty/collateral."""
    NONE = "none"  # No warranty
    PROPERTY = "property"  # Real estate
    VEHICLE = "vehicle"  # Car/motorcycle
    EQUIPMENT = "equipment"  # Business equipment
    INVESTMENTS = "investments"  # Stocks/bonds
    COSIGNER = "cosigner"  # Co-signer/guarantor
    OTHER = "other"  # Other collateral


class Ticket(Base):
    """
    Ticket (Offer) model representing lending offers or borrowing requests.
    Users create tickets to advertise their lending capacity or borrowing needs.
    Other users can respond to tickets to create deals/connections.
    """
    __tablename__ = "tickets"

    # Primary identification
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Ticket type and status
    ticket_type = Column(SQLEnum(TicketType), nullable=False, index=True)
    status = Column(SQLEnum(TicketStatus), nullable=False, default=TicketStatus.ACTIVE, index=True)

    # Financial details
    amount = Column(Float, nullable=False)  # Amount to lend or borrow
    min_amount = Column(Float, nullable=True)  # Minimum amount (flexible offers)
    max_amount = Column(Float, nullable=True)  # Maximum amount (flexible offers)

    interest_rate = Column(Float, nullable=False)  # Annual interest rate (%)
    min_interest_rate = Column(Float, nullable=True)  # Minimum acceptable rate
    max_interest_rate = Column(Float, nullable=True)  # Maximum acceptable rate

    term_months = Column(Integer, nullable=False)  # Loan term in months
    min_term_months = Column(Integer, nullable=True)  # Minimum term
    max_term_months = Column(Integer, nullable=True)  # Maximum term

    # Loan details
    loan_type = Column(SQLEnum(LoanType), nullable=False)
    loan_purpose = Column(Text, nullable=False)  # Detailed purpose/reason

    # Warranty/Collateral
    warranty_type = Column(SQLEnum(WarrantyType), nullable=False, default=WarrantyType.NONE)
    warranty_description = Column(Text, nullable=True)  # Details about collateral
    warranty_value = Column(Float, nullable=True)  # Estimated value of collateral

    # Additional details
    title = Column(String(200), nullable=False)  # Short title for the offer
    description = Column(Text, nullable=False)  # Detailed description
    requirements = Column(Text, nullable=True)  # Requirements for applicants

    # Preferences
    preferred_location = Column(String(100), nullable=True)  # Preferred borrower/lender location
    flexible_terms = Column(Boolean, default=False)  # Open to negotiation

    # Visibility and expiration
    is_public = Column(Boolean, default=True)  # Visible in marketplace
    expires_at = Column(DateTime, nullable=True)  # When ticket expires

    # Engagement tracking
    views_count = Column(Integer, default=0)  # Number of views
    responses_count = Column(Integer, default=0)  # Number of connection requests from this ticket
    deals_created = Column(Integer, default=0)  # Number of deals created

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_viewed_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="tickets")
    connections = relationship("Connection", back_populates="source_ticket", foreign_keys="Connection.source_ticket_id")

    def __repr__(self):
        return f"<Ticket(id={self.id}, user_id={self.user_id}, type='{self.ticket_type.value}', status='{self.status.value}', amount={self.amount})>"

    @property
    def is_active(self) -> bool:
        """Check if ticket is active."""
        return self.status == TicketStatus.ACTIVE

    @property
    def is_expired(self) -> bool:
        """Check if ticket has expired."""
        if self.expires_at and self.status == TicketStatus.ACTIVE:
            return datetime.utcnow() > self.expires_at
        return False

    @property
    def days_active(self) -> int:
        """Get number of days ticket has been active."""
        return (datetime.utcnow() - self.created_at).days

    @property
    def is_lending_offer(self) -> bool:
        """Check if this is a lending offer."""
        return self.ticket_type == TicketType.LENDING_OFFER

    @property
    def is_borrowing_request(self) -> bool:
        """Check if this is a borrowing request."""
        return self.ticket_type == TicketType.BORROWING_REQUEST

    @property
    def has_warranty(self) -> bool:
        """Check if ticket has collateral/warranty."""
        return self.warranty_type != WarrantyType.NONE

    def increment_views(self):
        """Increment view count."""
        self.views_count += 1
        self.last_viewed_at = datetime.utcnow()

    def increment_responses(self):
        """Increment response count when someone creates a connection."""
        self.responses_count += 1

    def mark_completed(self):
        """Mark ticket as completed when a deal is created."""
        self.status = TicketStatus.COMPLETED
        self.deals_created += 1

    def deactivate(self):
        """Deactivate the ticket."""
        self.status = TicketStatus.INACTIVE

    def reactivate(self):
        """Reactivate the ticket."""
        if self.status == TicketStatus.INACTIVE:
            self.status = TicketStatus.ACTIVE
