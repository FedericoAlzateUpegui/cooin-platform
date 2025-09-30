from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class UserRole(enum.Enum):
    """User roles in the platform."""
    LENDER = "lender"
    BORROWER = "borrower"
    BOTH = "both"  # Users who can be both lenders and borrowers


class UserStatus(enum.Enum):
    """User account status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"


class User(Base):
    """
    User model representing registered users in the platform.
    Contains authentication and basic user information.
    """
    __tablename__ = "users"

    # Primary identification
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(320), unique=True, index=True, nullable=False)  # RFC 5322 email max length
    username = Column(String(50), unique=True, index=True, nullable=True)

    # Authentication
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # User role and status
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.BORROWER)
    status = Column(SQLEnum(UserStatus), nullable=False, default=UserStatus.PENDING_VERIFICATION)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)

    # Verification and security
    email_verified_at = Column(DateTime, nullable=True)
    verification_token = Column(String(255), nullable=True)
    reset_password_token = Column(String(255), nullable=True)
    reset_password_expires = Column(DateTime, nullable=True)

    # Login attempts tracking (for security)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    sent_connections = relationship("Connection", foreign_keys="Connection.requester_id", back_populates="requester")
    received_connections = relationship("Connection", foreign_keys="Connection.receiver_id", back_populates="receiver")
    given_ratings = relationship("Rating", foreign_keys="Rating.rater_id", back_populates="rater")
    received_ratings = relationship("Rating", foreign_keys="Rating.rated_user_id", back_populates="rated_user")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    saved_searches = relationship("SavedSearch", back_populates="user", cascade="all, delete-orphan")
    search_logs = relationship("SearchLog", back_populates="user", cascade="all, delete-orphan")
    documents = relationship("DocumentUpload", foreign_keys="DocumentUpload.user_id", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role.value}')>"

    @property
    def is_lender(self) -> bool:
        """Check if user can lend."""
        return self.role in [UserRole.LENDER, UserRole.BOTH]

    @property
    def is_borrower(self) -> bool:
        """Check if user can borrow."""
        return self.role in [UserRole.BORROWER, UserRole.BOTH]

    @property
    def is_account_locked(self) -> bool:
        """Check if account is temporarily locked due to failed login attempts."""
        if self.locked_until is None:
            return False
        return datetime.utcnow() < self.locked_until

    def increment_failed_login(self):
        """Increment failed login attempts and lock account if necessary."""
        self.failed_login_attempts += 1
        # Lock account for 30 minutes after 5 failed attempts
        if self.failed_login_attempts >= 5:
            self.locked_until = datetime.utcnow() + timedelta(minutes=30)

    def reset_failed_login(self):
        """Reset failed login attempts after successful login."""
        self.failed_login_attempts = 0
        self.locked_until = None
        self.last_login = datetime.utcnow()


class RefreshToken(Base):
    """
    Refresh token model for JWT token management.
    Stores refresh tokens to manage user sessions securely.
    """
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(500), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    revoked = Column(Boolean, default=False)
    revoked_at = Column(DateTime, nullable=True)

    # Device/session tracking (optional)
    device_info = Column(Text, nullable=True)  # Store user agent, device info
    ip_address = Column(String(45), nullable=True)  # IPv6 max length

    # Relationships
    user = relationship("User", back_populates="refresh_tokens")

    def __repr__(self):
        return f"<RefreshToken(id={self.id}, user_id={self.user_id}, revoked={self.revoked})>"

    @property
    def is_expired(self) -> bool:
        """Check if refresh token is expired."""
        return datetime.utcnow() > self.expires_at

    @property
    def is_valid(self) -> bool:
        """Check if refresh token is valid (not expired and not revoked)."""
        return not self.revoked and not self.is_expired

    def revoke(self):
        """Revoke the refresh token."""
        self.revoked = True
        self.revoked_at = datetime.utcnow()