from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class DocumentType(enum.Enum):
    """Document type categories."""
    IDENTITY_DOCUMENT = "identity_document"
    INCOME_PROOF = "income_proof"
    BANK_STATEMENT = "bank_statement"
    EMPLOYMENT_VERIFICATION = "employment_verification"
    LOAN_AGREEMENT = "loan_agreement"
    COLLATERAL_DOCUMENT = "collateral_document"
    OTHER = "other"


class DocumentStatus(enum.Enum):
    """Document verification status."""
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class DocumentUpload(Base):
    """
    Model for tracking uploaded documents and their verification status.
    """
    __tablename__ = "document_uploads"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # User relationship
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Document information
    document_type = Column(SQLEnum(DocumentType), nullable=False)
    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=True)
    file_hash = Column(String(64), nullable=True)  # SHA256 hash

    # Verification status
    status = Column(SQLEnum(DocumentStatus), default=DocumentStatus.PENDING, nullable=False)
    verification_notes = Column(Text, nullable=True)
    verified_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # Admin who verified
    verified_at = Column(DateTime, nullable=True)

    # Optional associations
    loan_id = Column(Integer, nullable=True)  # Associated loan application
    connection_id = Column(Integer, nullable=True)  # Associated connection

    # Metadata
    is_active = Column(Boolean, default=True, nullable=False)
    expires_at = Column(DateTime, nullable=True)  # For time-sensitive documents

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="documents")
    verifier = relationship("User", foreign_keys=[verified_by])

    def __repr__(self):
        return f"<DocumentUpload(id={self.id}, user_id={self.user_id}, type={self.document_type.value}, status={self.status.value})>"

    @property
    def is_verified(self) -> bool:
        """Check if document is verified."""
        return self.status == DocumentStatus.APPROVED

    @property
    def is_expired(self) -> bool:
        """Check if document has expired."""
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at

    def mark_as_reviewed(self, verifier_id: int, approved: bool, notes: str = None):
        """Mark document as reviewed."""
        self.verified_by = verifier_id
        self.verified_at = datetime.utcnow()
        self.status = DocumentStatus.APPROVED if approved else DocumentStatus.REJECTED
        if notes:
            self.verification_notes = notes
        self.updated_at = datetime.utcnow()

    def mark_as_expired(self):
        """Mark document as expired."""
        self.status = DocumentStatus.EXPIRED
        self.updated_at = datetime.utcnow()