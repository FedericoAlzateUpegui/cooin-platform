from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class SystemMessageType(enum.Enum):
    """Type of system message."""
    MATCH_NOTIFICATION = "match_notification"  # Match updates
    EDUCATIONAL = "educational"  # Educational content about lending
    ANNOUNCEMENT = "announcement"  # Platform announcements
    REMINDER = "reminder"  # Activity reminders
    SAFETY_TIP = "safety_tip"  # Safety and security tips
    FEATURE_UPDATE = "feature_update"  # New feature notifications


class SystemMessagePriority(enum.Enum):
    """Priority level of system message."""
    LOW = "low"  # Optional reading
    MEDIUM = "medium"  # Important but not urgent
    HIGH = "high"  # Important, should read soon
    URGENT = "urgent"  # Critical, requires immediate attention


class SystemMessage(Base):
    """
    System message model for app-to-user communications.
    Includes notifications, educational content, and announcements.
    """
    __tablename__ = "system_messages"

    # Primary identification
    id = Column(Integer, primary_key=True, index=True)

    # Recipient
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Message content
    title = Column(String(200), nullable=False)  # Message title/subject
    content = Column(Text, nullable=False)  # Main message content
    message_type = Column(SQLEnum(SystemMessageType), nullable=False, default=SystemMessageType.ANNOUNCEMENT)
    priority = Column(SQLEnum(SystemMessagePriority), nullable=False, default=SystemMessagePriority.MEDIUM)

    # Optional metadata
    action_url = Column(String(500), nullable=True)  # Deep link or URL for action
    action_label = Column(String(100), nullable=True)  # Button/link label (e.g., "Learn More", "View Match")
    image_url = Column(String(500), nullable=True)  # Optional image/icon URL

    # Educational content specific
    category = Column(String(100), nullable=True)  # e.g., "Credit Assessment", "Risk Management"
    tags = Column(String(500), nullable=True)  # Comma-separated tags for filtering

    # Status tracking
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    read_at = Column(DateTime, nullable=True)
    is_archived = Column(Boolean, default=False, nullable=False)
    archived_at = Column(DateTime, nullable=True)

    # Soft delete
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Expiration (optional - for time-sensitive messages)
    expires_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="system_messages")

    def mark_as_read(self):
        """Mark message as read."""
        if not self.is_read:
            self.is_read = True
            self.read_at = datetime.utcnow()

    def archive(self):
        """Archive message."""
        if not self.is_archived:
            self.is_archived = True
            self.archived_at = datetime.utcnow()

    def soft_delete(self):
        """Soft delete message."""
        if not self.is_deleted:
            self.is_deleted = True
            self.deleted_at = datetime.utcnow()

    def is_expired(self):
        """Check if message has expired."""
        if self.expires_at:
            return datetime.utcnow() > self.expires_at
        return False

    def __repr__(self):
        return f"<SystemMessage(id={self.id}, user_id={self.user_id}, type={self.message_type}, title='{self.title}')>"
