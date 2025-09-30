from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class ConnectionStatus(enum.Enum):
    """Status of connection between users."""
    PENDING = "pending"  # Connection request sent, awaiting response
    ACCEPTED = "accepted"  # Connection accepted, users can communicate
    REJECTED = "rejected"  # Connection request rejected
    BLOCKED = "blocked"  # One user blocked the other
    EXPIRED = "expired"  # Connection request expired


class ConnectionType(enum.Enum):
    """Type of connection/interaction."""
    LENDING_INQUIRY = "lending_inquiry"  # Borrower interested in lender
    BORROWING_REQUEST = "borrowing_request"  # Lender interested in borrower
    GENERAL_CONNECTION = "general_connection"  # General networking
    REFERRAL = "referral"  # User referred by another user


class Connection(Base):
    """
    Connection model representing relationships between users.
    This handles the matching/connection system between lenders and borrowers.
    """
    __tablename__ = "connections"

    # Primary identification
    id = Column(Integer, primary_key=True, index=True)

    # User relationships
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Connection details
    connection_type = Column(SQLEnum(ConnectionType), nullable=False, default=ConnectionType.GENERAL_CONNECTION)
    status = Column(SQLEnum(ConnectionStatus), nullable=False, default=ConnectionStatus.PENDING)

    # Request details
    message = Column(Text, nullable=True)  # Initial message from requester
    response_message = Column(Text, nullable=True)  # Response from receiver

    # Financial details (if applicable)
    loan_amount_requested = Column(Float, nullable=True)
    loan_term_months = Column(Integer, nullable=True)
    interest_rate_proposed = Column(Float, nullable=True)
    loan_purpose = Column(String(200), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    responded_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)  # When pending request expires

    # Additional metadata
    is_mutual = Column(Boolean, default=False)  # Both users connected to each other
    priority_level = Column(Integer, default=1)  # 1=normal, 2=high, 3=urgent
    requester_notes = Column(Text, nullable=True)  # Private notes from requester
    receiver_notes = Column(Text, nullable=True)  # Private notes from receiver

    # Communication tracking
    last_message_at = Column(DateTime, nullable=True)
    message_count = Column(Integer, default=0)

    # Relationships
    requester = relationship("User", foreign_keys=[requester_id], back_populates="sent_connections")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_connections")
    messages = relationship("Message", back_populates="connection", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Connection(id={self.id}, requester_id={self.requester_id}, receiver_id={self.receiver_id}, status='{self.status.value}')>"

    @property
    def is_pending(self) -> bool:
        """Check if connection is pending."""
        return self.status == ConnectionStatus.PENDING

    @property
    def is_active(self) -> bool:
        """Check if connection is active (accepted)."""
        return self.status == ConnectionStatus.ACCEPTED

    @property
    def is_expired(self) -> bool:
        """Check if pending connection has expired."""
        if self.expires_at and self.status == ConnectionStatus.PENDING:
            return datetime.utcnow() > self.expires_at
        return False

    @property
    def days_since_created(self) -> int:
        """Get number of days since connection was created."""
        return (datetime.utcnow() - self.created_at).days

    def accept_connection(self, response_message: str = None):
        """Accept the connection request."""
        self.status = ConnectionStatus.ACCEPTED
        self.responded_at = datetime.utcnow()
        if response_message:
            self.response_message = response_message

    def reject_connection(self, response_message: str = None):
        """Reject the connection request."""
        self.status = ConnectionStatus.REJECTED
        self.responded_at = datetime.utcnow()
        if response_message:
            self.response_message = response_message

    def block_connection(self):
        """Block the connection."""
        self.status = ConnectionStatus.BLOCKED
        self.responded_at = datetime.utcnow()

    def expire_connection(self):
        """Mark connection as expired."""
        if self.status == ConnectionStatus.PENDING:
            self.status = ConnectionStatus.EXPIRED


class Message(Base):
    """
    Message model for communication between connected users.
    """
    __tablename__ = "messages"

    # Primary identification
    id = Column(Integer, primary_key=True, index=True)
    connection_id = Column(Integer, ForeignKey("connections.id"), nullable=False, index=True)

    # Message details
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    content = Column(Text, nullable=False)
    message_type = Column(String(50), default="text")  # text, image, document, etc.

    # Message status
    is_read = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    deleted_by_sender = Column(Boolean, default=False)
    deleted_by_receiver = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    read_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    # File attachments (if any)
    attachment_url = Column(String(500), nullable=True)
    attachment_filename = Column(String(255), nullable=True)
    attachment_size = Column(Integer, nullable=True)  # in bytes

    # Relationships
    connection = relationship("Connection", back_populates="messages")
    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])

    def __repr__(self):
        return f"<Message(id={self.id}, connection_id={self.connection_id}, sender_id={self.sender_id})>"

    def mark_as_read(self):
        """Mark message as read."""
        if not self.is_read:
            self.is_read = True
            self.read_at = datetime.utcnow()

    def soft_delete(self, deleted_by_user_id: int):
        """Soft delete message for a specific user."""
        if deleted_by_user_id == self.sender_id:
            self.deleted_by_sender = True
        elif deleted_by_user_id == self.receiver_id:
            self.deleted_by_receiver = True

        # If both users deleted, mark as fully deleted
        if self.deleted_by_sender and self.deleted_by_receiver:
            self.is_deleted = True
            self.deleted_at = datetime.utcnow()

    @property
    def is_visible_to_user(self, user_id: int) -> bool:
        """Check if message is visible to a specific user."""
        if self.is_deleted:
            return False

        if user_id == self.sender_id:
            return not self.deleted_by_sender
        elif user_id == self.receiver_id:
            return not self.deleted_by_receiver

        return False