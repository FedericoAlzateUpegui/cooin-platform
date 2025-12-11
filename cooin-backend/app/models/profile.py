from datetime import datetime, date
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Date, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class IncomeRange(enum.Enum):
    """Income range categories."""
    UNDER_30K = "under_30k"
    RANGE_30K_50K = "30k_50k"
    RANGE_50K_75K = "50k_75k"
    RANGE_75K_100K = "75k_100k"
    RANGE_100K_150K = "100k_150k"
    OVER_150K = "over_150k"
    PREFER_NOT_SAY = "prefer_not_say"


class EmploymentStatus(enum.Enum):
    """Employment status options."""
    EMPLOYED_FULL_TIME = "employed_full_time"
    EMPLOYED_PART_TIME = "employed_part_time"
    SELF_EMPLOYED = "self_employed"
    UNEMPLOYED = "unemployed"
    STUDENT = "student"
    RETIRED = "retired"
    OTHER = "other"


class LoanPurpose(enum.Enum):
    """Loan purpose categories."""
    DEBT_CONSOLIDATION = "debt_consolidation"
    HOME_IMPROVEMENT = "home_improvement"
    MEDICAL_EXPENSES = "medical_expenses"
    EDUCATION = "education"
    BUSINESS = "business"
    AUTO_FINANCING = "auto_financing"
    EMERGENCY = "emergency"
    VACATION = "vacation"
    OTHER = "other"


class UserProfile(Base):
    """
    Extended user profile with detailed personal and financial information.
    This is separate from the User model to keep authentication data separate.
    """
    __tablename__ = "user_profiles"

    # Primary key and user relationship
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    # Personal Information
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    display_name = Column(String(150), nullable=True)  # What other users see
    bio = Column(Text, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    phone_number = Column(String(20), nullable=True)

    # Location Information
    country = Column(String(100), nullable=True)
    state_province = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    timezone = Column(String(50), nullable=True)

    # Financial Information
    income_range = Column(SQLEnum(IncomeRange, values_callable=lambda x: [e.value for e in x]), nullable=True)
    employment_status = Column(SQLEnum(EmploymentStatus, values_callable=lambda x: [e.value for e in x]), nullable=True)
    employer_name = Column(String(200), nullable=True)
    years_employed = Column(Float, nullable=True)

    # Credit and Financial History
    credit_score = Column(Integer, nullable=True)  # If provided/verified
    debt_to_income_ratio = Column(Float, nullable=True)
    monthly_income = Column(Float, nullable=True)  # Actual amount if user chooses to share
    monthly_expenses = Column(Float, nullable=True)

    # Lending Preferences (for lenders)
    min_loan_amount = Column(Float, nullable=True)
    max_loan_amount = Column(Float, nullable=True)
    preferred_loan_term_min = Column(Integer, nullable=True)  # in months
    preferred_loan_term_max = Column(Integer, nullable=True)  # in months
    preferred_interest_rate = Column(Float, nullable=True)
    willing_to_lend_unsecured = Column(Boolean, default=False)

    # Borrowing Preferences (for borrowers)
    loan_purpose = Column(SQLEnum(LoanPurpose, values_callable=lambda x: [e.value for e in x]), nullable=True)
    requested_loan_amount = Column(Float, nullable=True)
    preferred_loan_term = Column(Integer, nullable=True)  # in months
    max_acceptable_rate = Column(Float, nullable=True)

    # Profile completeness and verification
    profile_completion_percentage = Column(Float, default=0.0)
    is_profile_public = Column(Boolean, default=True)
    identity_verified = Column(Boolean, default=False)
    income_verified = Column(Boolean, default=False)
    bank_account_verified = Column(Boolean, default=False)

    # Profile media
    avatar_url = Column(String(500), nullable=True)
    banner_url = Column(String(500), nullable=True)

    # Privacy settings
    show_real_name = Column(Boolean, default=False)
    show_location = Column(Boolean, default=True)
    show_income_range = Column(Boolean, default=True)
    show_employment = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_profile_update = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<UserProfile(id={self.id}, user_id={self.user_id}, display_name='{self.display_name}')>"

    @property
    def full_name(self) -> str:
        """Get full name if available."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.display_name or f"User {self.user_id}"

    @property
    def public_name(self) -> str:
        """Get the name to show to other users based on privacy settings."""
        if self.show_real_name and self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.display_name or f"User {self.user_id}"

    @property
    def age(self) -> int:
        """Calculate age from date of birth."""
        if not self.date_of_birth:
            return None
        today = date.today()
        age = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month or (
            today.month == self.date_of_birth.month and today.day < self.date_of_birth.day
        ):
            age -= 1
        return age

    @property
    def location_string(self) -> str:
        """Get formatted location string based on privacy settings."""
        if not self.show_location:
            return "Location hidden"

        location_parts = []
        if self.city:
            location_parts.append(self.city)
        if self.state_province:
            location_parts.append(self.state_province)
        if self.country:
            location_parts.append(self.country)

        return ", ".join(location_parts) if location_parts else "Location not specified"

    def calculate_profile_completion(self) -> float:
        """Calculate profile completion percentage."""
        total_fields = 15  # Number of important fields to consider
        completed_fields = 0

        # Basic info
        if self.first_name:
            completed_fields += 1
        if self.last_name:
            completed_fields += 1
        if self.display_name:
            completed_fields += 1
        if self.bio:
            completed_fields += 1
        if self.date_of_birth:
            completed_fields += 1

        # Location
        if self.city:
            completed_fields += 1
        if self.state_province:
            completed_fields += 1
        if self.country:
            completed_fields += 1

        # Financial info
        if self.income_range:
            completed_fields += 1
        if self.employment_status:
            completed_fields += 1

        # Profile media
        if self.avatar_url:
            completed_fields += 1

        # Role-specific fields
        if self.user and self.user.is_lender:
            if self.min_loan_amount and self.max_loan_amount:
                completed_fields += 1

        if self.user and self.user.is_borrower:
            if self.loan_purpose:
                completed_fields += 1
            if self.requested_loan_amount:
                completed_fields += 1

        completion_percentage = (completed_fields / total_fields) * 100
        self.profile_completion_percentage = round(completion_percentage, 1)
        return self.profile_completion_percentage

    def update_last_profile_update(self):
        """Update the last profile update timestamp."""
        self.last_profile_update = datetime.utcnow()
        self.updated_at = datetime.utcnow()