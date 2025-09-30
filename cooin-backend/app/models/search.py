from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship

from app.db.base import Base


class SavedSearch(Base):
    """Model for saved user searches."""
    __tablename__ = "saved_searches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Search details
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    search_parameters = Column(JSON, nullable=False)  # Stores SearchRequest as JSON

    # Settings
    notify_on_new_matches = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_run_at = Column(DateTime, nullable=True)
    match_count = Column(Integer, default=0, nullable=False)

    # Relationships
    user = relationship("User", back_populates="saved_searches")

    def __repr__(self):
        return f"<SavedSearch(id={self.id}, user_id={self.user_id}, name='{self.name}')>"

    def update_match_count(self, count: int):
        """Update the match count and last run time."""
        self.match_count = count
        self.last_run_at = datetime.utcnow()


class SearchLog(Base):
    """Model for logging search activity for analytics."""
    __tablename__ = "search_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)  # Nullable for anonymous searches

    # Search details
    search_type = Column(String(50), nullable=False, index=True)
    query = Column(String(200), nullable=True)
    filters_used = Column(JSON, nullable=True)  # Stores filters as JSON

    # Results
    result_count = Column(Integer, nullable=False)
    page = Column(Integer, nullable=False, default=1)
    page_size = Column(Integer, nullable=False, default=20)

    # Performance
    execution_time_ms = Column(Float, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    ip_address = Column(String(45), nullable=True)  # Support IPv6
    user_agent = Column(String(500), nullable=True)

    # Relationships
    user = relationship("User", back_populates="search_logs")

    def __repr__(self):
        return f"<SearchLog(id={self.id}, user_id={self.user_id}, search_type='{self.search_type}')>"