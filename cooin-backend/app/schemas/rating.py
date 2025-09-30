from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum


class RatingType(str, Enum):
    LENDER_RATING = "lender_rating"
    BORROWER_RATING = "borrower_rating"
    GENERAL_RATING = "general_rating"


class RatingCreate(BaseModel):
    connection_id: int = Field(..., description="ID of the connection being rated")
    rating_type: RatingType = Field(..., description="Type of rating")
    overall_rating: float = Field(..., ge=1.0, le=5.0, description="Overall rating from 1.0 to 5.0")

    # Category ratings (optional)
    communication_rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    reliability_rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    professionalism_rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    timeliness_rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    transparency_rating: Optional[float] = Field(None, ge=1.0, le=5.0)

    # Review content (optional)
    review_title: Optional[str] = Field(None, max_length=200, description="Short review title")
    review_text: Optional[str] = Field(None, max_length=2000, description="Detailed review text")

    # Privacy settings
    is_anonymous: bool = Field(False, description="Whether to post rating anonymously")

    @validator('overall_rating', 'communication_rating', 'reliability_rating',
              'professionalism_rating', 'timeliness_rating', 'transparency_rating')
    def validate_rating_values(cls, v):
        if v is not None and (v < 1.0 or v > 5.0):
            raise ValueError('Rating must be between 1.0 and 5.0')
        return v


class RatingUpdate(BaseModel):
    overall_rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    communication_rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    reliability_rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    professionalism_rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    timeliness_rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    transparency_rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    review_title: Optional[str] = Field(None, max_length=200)
    review_text: Optional[str] = Field(None, max_length=2000)
    is_anonymous: Optional[bool] = None


class RatingResponse(BaseModel):
    id: int
    connection_id: int
    rater_id: int
    ratee_id: int
    rating_type: str
    overall_rating: float

    # Category ratings
    communication_rating: Optional[float] = None
    reliability_rating: Optional[float] = None
    professionalism_rating: Optional[float] = None
    timeliness_rating: Optional[float] = None
    transparency_rating: Optional[float] = None

    # Review content
    review_title: Optional[str] = None
    review_text: Optional[str] = None

    # Financial context
    loan_amount: Optional[float] = None
    loan_term: Optional[int] = None
    interest_rate: Optional[float] = None
    loan_completed: bool = False

    # Metadata
    is_anonymous: bool = False
    is_verified: bool = False
    is_flagged: bool = False
    helpful_count: int = 0
    not_helpful_count: int = 0

    # Timestamps
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RatingListResponse(BaseModel):
    ratings: List[RatingResponse]
    total_count: int
    page: int
    page_size: int
    has_next: bool
    has_previous: bool


class RatingStats(BaseModel):
    total_ratings: int = 0
    average_rating: float = 0.0

    # Category averages
    average_communication: Optional[float] = None
    average_reliability: Optional[float] = None
    average_professionalism: Optional[float] = None
    average_timeliness: Optional[float] = None
    average_transparency: Optional[float] = None

    # Rating distribution
    five_star_count: int = 0
    four_star_count: int = 0
    three_star_count: int = 0
    two_star_count: int = 0
    one_star_count: int = 0


class UserRatingStats(BaseModel):
    user_id: int
    username: str
    role: str

    # Overall stats
    total_ratings_received: int = 0
    average_rating: float = 0.0

    # As lender stats
    lender_ratings: RatingStats = Field(default_factory=RatingStats)

    # As borrower stats
    borrower_ratings: RatingStats = Field(default_factory=RatingStats)

    # Recent ratings (last 5)
    recent_ratings: List[RatingResponse] = Field(default_factory=list)


class RatingHelpfulnessUpdate(BaseModel):
    is_helpful: bool = Field(..., description="True for helpful, False for not helpful")