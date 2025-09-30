from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, validator, Field
from enum import Enum

from app.models.profile import IncomeRange, EmploymentStatus, LoanPurpose


class IncomeRangeSchema(str, Enum):
    """Income range schema for API."""
    UNDER_30K = "under_30k"
    RANGE_30K_50K = "30k_50k"
    RANGE_50K_75K = "50k_75k"
    RANGE_75K_100K = "75k_100k"
    RANGE_100K_150K = "100k_150k"
    OVER_150K = "over_150k"
    PREFER_NOT_SAY = "prefer_not_say"


class EmploymentStatusSchema(str, Enum):
    """Employment status schema for API."""
    EMPLOYED_FULL_TIME = "employed_full_time"
    EMPLOYED_PART_TIME = "employed_part_time"
    SELF_EMPLOYED = "self_employed"
    UNEMPLOYED = "unemployed"
    STUDENT = "student"
    RETIRED = "retired"
    OTHER = "other"


class LoanPurposeSchema(str, Enum):
    """Loan purpose schema for API."""
    DEBT_CONSOLIDATION = "debt_consolidation"
    HOME_IMPROVEMENT = "home_improvement"
    MEDICAL_EXPENSES = "medical_expenses"
    EDUCATION = "education"
    BUSINESS = "business"
    AUTO_FINANCING = "auto_financing"
    EMERGENCY = "emergency"
    VACATION = "vacation"
    OTHER = "other"


class UserProfileBase(BaseModel):
    """Base user profile schema."""
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    display_name: Optional[str] = Field(None, max_length=150)
    bio: Optional[str] = Field(None, max_length=1000)
    date_of_birth: Optional[date] = None
    phone_number: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$')

    # Location
    country: Optional[str] = Field(None, max_length=100)
    state_province: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    timezone: Optional[str] = Field(None, max_length=50)

    @validator('date_of_birth')
    def validate_age(cls, v):
        if v is not None:
            today = date.today()
            age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
            if age < 18:
                raise ValueError('User must be at least 18 years old')
            if age > 120:
                raise ValueError('Invalid date of birth')
        return v

    @validator('phone_number')
    def validate_phone(cls, v):
        if v is not None:
            # Remove all non-digit characters except +
            cleaned = ''.join(c for c in v if c.isdigit() or c == '+')
            if len(cleaned) < 10:
                raise ValueError('Phone number must be at least 10 digits')
        return v


class UserProfileCreate(UserProfileBase):
    """Schema for creating user profile."""
    pass


class UserProfileUpdate(UserProfileBase):
    """Schema for updating user profile."""
    # Privacy settings
    show_real_name: Optional[bool] = None
    show_location: Optional[bool] = None
    show_income_range: Optional[bool] = None
    show_employment: Optional[bool] = None
    is_profile_public: Optional[bool] = None


class FinancialInfoBase(BaseModel):
    """Base financial information schema."""
    income_range: Optional[IncomeRangeSchema] = None
    employment_status: Optional[EmploymentStatusSchema] = None
    employer_name: Optional[str] = Field(None, max_length=200)
    years_employed: Optional[float] = Field(None, ge=0, le=50)
    monthly_income: Optional[float] = Field(None, ge=0)
    monthly_expenses: Optional[float] = Field(None, ge=0)
    debt_to_income_ratio: Optional[float] = Field(None, ge=0, le=100)

    @validator('debt_to_income_ratio')
    def validate_dti_ratio(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('Debt-to-income ratio must be between 0 and 100')
        return v


class FinancialInfoUpdate(FinancialInfoBase):
    """Schema for updating financial information."""
    pass


class LendingPreferencesBase(BaseModel):
    """Base lending preferences schema."""
    min_loan_amount: Optional[float] = Field(None, ge=100)
    max_loan_amount: Optional[float] = Field(None, ge=100)
    preferred_loan_term_min: Optional[int] = Field(None, ge=1, le=360)  # months
    preferred_loan_term_max: Optional[int] = Field(None, ge=1, le=360)
    preferred_interest_rate: Optional[float] = Field(None, ge=0.1, le=50)
    willing_to_lend_unsecured: Optional[bool] = None

    @validator('max_loan_amount')
    def validate_loan_amounts(cls, v, values):
        if v is not None and 'min_loan_amount' in values and values['min_loan_amount'] is not None:
            if v < values['min_loan_amount']:
                raise ValueError('Maximum loan amount must be greater than minimum loan amount')
        return v

    @validator('preferred_loan_term_max')
    def validate_loan_terms(cls, v, values):
        if v is not None and 'preferred_loan_term_min' in values and values['preferred_loan_term_min'] is not None:
            if v < values['preferred_loan_term_min']:
                raise ValueError('Maximum loan term must be greater than minimum loan term')
        return v


class LendingPreferencesUpdate(LendingPreferencesBase):
    """Schema for updating lending preferences."""
    pass


class BorrowingPreferencesBase(BaseModel):
    """Base borrowing preferences schema."""
    loan_purpose: Optional[LoanPurposeSchema] = None
    requested_loan_amount: Optional[float] = Field(None, ge=100)
    preferred_loan_term: Optional[int] = Field(None, ge=1, le=360)  # months
    max_acceptable_rate: Optional[float] = Field(None, ge=0.1, le=50)


class BorrowingPreferencesUpdate(BorrowingPreferencesBase):
    """Schema for updating borrowing preferences."""
    pass


class UserProfileResponse(UserProfileBase):
    """Schema for user profile response."""
    id: int
    user_id: int

    # Financial information (conditional based on privacy settings)
    income_range: Optional[IncomeRangeSchema] = None
    employment_status: Optional[EmploymentStatusSchema] = None
    employer_name: Optional[str] = None
    years_employed: Optional[float] = None

    # Lending preferences
    min_loan_amount: Optional[float] = None
    max_loan_amount: Optional[float] = None
    preferred_loan_term_min: Optional[int] = None
    preferred_loan_term_max: Optional[int] = None
    preferred_interest_rate: Optional[float] = None
    willing_to_lend_unsecured: Optional[bool] = None

    # Borrowing preferences
    loan_purpose: Optional[LoanPurposeSchema] = None
    requested_loan_amount: Optional[float] = None
    preferred_loan_term: Optional[int] = None
    max_acceptable_rate: Optional[float] = None

    # Profile status
    profile_completion_percentage: float
    is_profile_public: bool
    identity_verified: bool
    income_verified: bool
    bank_account_verified: bool

    # Profile media
    avatar_url: Optional[str] = None
    banner_url: Optional[str] = None

    # Privacy settings
    show_real_name: bool
    show_location: bool
    show_income_range: bool
    show_employment: bool

    # Timestamps
    created_at: datetime
    updated_at: datetime
    last_profile_update: Optional[datetime] = None

    # Computed fields
    age: Optional[int] = None
    location_string: str
    public_name: str
    full_name: str

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "display_name": "JohnD",
                "bio": "Experienced borrower looking for home improvement loan",
                "date_of_birth": "1990-01-15",
                "phone_number": "+1234567890",
                "country": "United States",
                "state_province": "California",
                "city": "San Francisco",
                "income_range": "75k_100k",
                "employment_status": "employed_full_time",
                "loan_purpose": "home_improvement",
                "requested_loan_amount": 25000.0,
                "profile_completion_percentage": 85.5,
                "is_profile_public": True,
                "identity_verified": True
            }
        }


class UserProfilePublicResponse(BaseModel):
    """Schema for public user profile (what other users can see)."""
    id: int
    user_id: int
    public_name: str
    display_name: Optional[str] = None
    bio: Optional[str] = None
    age: Optional[int] = None
    location_string: str

    # Financial information (if user allows)
    income_range: Optional[IncomeRangeSchema] = None
    employment_status: Optional[EmploymentStatusSchema] = None

    # Preferences (relevant to connection type)
    loan_purpose: Optional[LoanPurposeSchema] = None
    requested_loan_amount: Optional[float] = None
    min_loan_amount: Optional[float] = None
    max_loan_amount: Optional[float] = None

    # Profile status
    profile_completion_percentage: float
    identity_verified: bool
    income_verified: bool

    # Profile media
    avatar_url: Optional[str] = None

    # Timestamps
    created_at: datetime

    class Config:
        from_attributes = True


class ProfileCompletionResponse(BaseModel):
    """Schema for profile completion status."""
    completion_percentage: float
    missing_fields: List[str]
    suggestions: List[str]
    next_steps: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "completion_percentage": 75.0,
                "missing_fields": ["bio", "employment_status", "avatar_url"],
                "suggestions": [
                    "Add a bio to help others understand your background",
                    "Upload a profile picture to increase trust",
                    "Complete employment information for better matching"
                ],
                "next_steps": [
                    "Verify your identity",
                    "Add financial preferences",
                    "Upload required documents"
                ]
            }
        }


class ProfileStats(BaseModel):
    """Schema for profile statistics."""
    profile_views: int
    connection_requests_received: int
    connection_success_rate: float
    average_response_time_hours: Optional[float] = None
    last_active: Optional[datetime] = None

    class Config:
        from_attributes = True