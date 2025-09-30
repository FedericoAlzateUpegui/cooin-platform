from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

from app.schemas.user import UserRole
from app.schemas.profile import EmploymentStatus, IncomeRange


class SearchType(str, Enum):
    """Type of search to perform."""
    LENDERS = "lenders"
    BORROWERS = "borrowers"
    ALL_USERS = "all_users"


class SortBy(str, Enum):
    """Sorting options for search results."""
    RELEVANCE = "relevance"
    RATING = "rating"
    DISTANCE = "distance"
    LOAN_AMOUNT = "loan_amount"
    INTEREST_RATE = "interest_rate"
    CREATED_AT = "created_at"
    LAST_ACTIVE = "last_active"


class SortOrder(str, Enum):
    """Sort order."""
    ASC = "asc"
    DESC = "desc"


class SearchFilters(BaseModel):
    """Search filter parameters."""

    # Location filters
    country: Optional[str] = Field(None, description="Country filter")
    state_province: Optional[str] = Field(None, description="State/Province filter")
    city: Optional[str] = Field(None, description="City filter")
    max_distance_km: Optional[int] = Field(None, ge=0, le=10000, description="Maximum distance in kilometers")

    # Financial filters
    min_loan_amount: Optional[float] = Field(None, ge=0, description="Minimum loan amount")
    max_loan_amount: Optional[float] = Field(None, ge=0, description="Maximum loan amount")
    min_interest_rate: Optional[float] = Field(None, ge=0, description="Minimum interest rate")
    max_interest_rate: Optional[float] = Field(None, ge=0, description="Maximum interest rate")
    loan_term_min: Optional[int] = Field(None, ge=1, description="Minimum loan term in months")
    loan_term_max: Optional[int] = Field(None, ge=1, description="Maximum loan term in months")

    # User criteria filters
    min_credit_score: Optional[int] = Field(None, ge=300, le=850, description="Minimum credit score")
    max_credit_score: Optional[int] = Field(None, ge=300, le=850, description="Maximum credit score")
    employment_status: Optional[List[EmploymentStatus]] = Field(None, description="Employment status filter")
    income_range: Optional[List[IncomeRange]] = Field(None, description="Income range filter")
    min_years_employed: Optional[float] = Field(None, ge=0, description="Minimum years employed")

    # Rating and trust filters
    min_rating: Optional[float] = Field(None, ge=1.0, le=5.0, description="Minimum average rating")
    min_rating_count: Optional[int] = Field(None, ge=1, description="Minimum number of ratings")
    identity_verified: Optional[bool] = Field(None, description="Identity verified filter")
    income_verified: Optional[bool] = Field(None, description="Income verified filter")
    bank_account_verified: Optional[bool] = Field(None, description="Bank account verified filter")

    # Activity filters
    recently_active: Optional[bool] = Field(None, description="Filter for recently active users")
    has_profile_picture: Optional[bool] = Field(None, description="Filter for users with profile pictures")
    profile_completion_min: Optional[float] = Field(None, ge=0, le=100, description="Minimum profile completion percentage")


class SearchRequest(BaseModel):
    """Search request parameters."""

    search_type: SearchType = Field(..., description="Type of users to search for")
    query: Optional[str] = Field(None, max_length=200, description="Text search query")
    filters: Optional[SearchFilters] = Field(None, description="Search filters")

    # Pagination
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")

    # Sorting
    sort_by: SortBy = Field(SortBy.RELEVANCE, description="Sort criteria")
    sort_order: SortOrder = Field(SortOrder.DESC, description="Sort order")


class UserSearchResult(BaseModel):
    """Individual user search result."""

    # Basic user info
    id: int
    username: str
    role: str
    created_at: str
    last_login: Optional[str] = None

    # Profile summary
    display_name: Optional[str] = None
    bio: Optional[str] = None
    country: Optional[str] = None
    state_province: Optional[str] = None
    city: Optional[str] = None

    # Financial info (based on privacy settings)
    min_loan_amount: Optional[float] = None
    max_loan_amount: Optional[float] = None
    preferred_interest_rate: Optional[float] = None
    willing_to_lend_unsecured: Optional[bool] = None

    # Trust indicators
    average_rating: float = 0.0
    total_ratings: int = 0
    identity_verified: bool = False
    income_verified: bool = False
    bank_account_verified: bool = False
    profile_completion_percentage: float = 0.0

    # Activity
    is_recently_active: bool = False
    days_since_last_login: Optional[int] = None

    # Distance (if location-based search)
    distance_km: Optional[float] = None

    # Match score (relevance score)
    match_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Relevance/match score")

    class Config:
        from_attributes = True


class SearchStats(BaseModel):
    """Search statistics."""

    total_users: int = 0
    lenders_count: int = 0
    borrowers_count: int = 0
    both_role_count: int = 0
    verified_users: int = 0
    average_rating: float = 0.0


class SearchResponse(BaseModel):
    """Search results response."""

    results: List[UserSearchResult]
    total_count: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool

    # Search metadata
    search_type: SearchType
    query: Optional[str] = None
    filters_applied: int = 0  # Number of filters applied
    search_time_ms: Optional[float] = None  # Search execution time

    # Aggregated statistics
    stats: Optional[SearchStats] = None


class SavedSearchCreate(BaseModel):
    """Create a saved search."""

    name: str = Field(..., max_length=100, description="Search name")
    description: Optional[str] = Field(None, max_length=500, description="Search description")
    search_request: SearchRequest = Field(..., description="Search parameters")
    notify_on_new_matches: bool = Field(False, description="Send notifications for new matches")


class SavedSearchUpdate(BaseModel):
    """Update a saved search."""

    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    search_request: Optional[SearchRequest] = None
    notify_on_new_matches: Optional[bool] = None
    is_active: Optional[bool] = None


class SavedSearchResponse(BaseModel):
    """Saved search response."""

    id: int
    name: str
    description: Optional[str] = None
    search_request: SearchRequest
    notify_on_new_matches: bool
    is_active: bool
    created_at: str
    updated_at: str
    last_run_at: Optional[str] = None
    match_count: int = 0  # Current number of matches

    class Config:
        from_attributes = True


class SearchSuggestion(BaseModel):
    """Search suggestion for autocomplete."""

    type: str  # "location", "skill", "industry", etc.
    value: str
    count: int  # Number of users with this value


class SearchSuggestionsResponse(BaseModel):
    """Search suggestions response."""

    query: str
    suggestions: List[SearchSuggestion]