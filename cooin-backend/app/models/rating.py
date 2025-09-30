from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class RatingType(enum.Enum):
    """Type of rating given."""
    LENDER_RATING = "lender_rating"  # Rating given to a lender
    BORROWER_RATING = "borrower_rating"  # Rating given to a borrower
    GENERAL_RATING = "general_rating"  # General platform interaction rating


class RatingCategory(enum.Enum):
    """Categories for detailed ratings."""
    COMMUNICATION = "communication"
    RELIABILITY = "reliability"
    PROFESSIONALISM = "professionalism"
    TIMELINESS = "timeliness"
    TRANSPARENCY = "transparency"
    OVERALL = "overall"


class Rating(Base):
    """
    Rating model for users to rate each other after interactions.
    This helps build trust and reputation in the platform.
    """
    __tablename__ = "ratings"

    # Primary identification
    id = Column(Integer, primary_key=True, index=True)

    # User relationships
    rater_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # Who gave the rating
    rated_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # Who was rated

    # Connection reference (optional - if rating is related to a specific connection)
    connection_id = Column(Integer, ForeignKey("connections.id"), nullable=True, index=True)

    # Rating details
    rating_type = Column(SQLEnum(RatingType), nullable=False, default=RatingType.GENERAL_RATING)
    overall_rating = Column(Float, nullable=False)  # 1.0 to 5.0

    # Detailed ratings (optional)
    communication_rating = Column(Float, nullable=True)  # 1.0 to 5.0
    reliability_rating = Column(Float, nullable=True)  # 1.0 to 5.0
    professionalism_rating = Column(Float, nullable=True)  # 1.0 to 5.0
    timeliness_rating = Column(Float, nullable=True)  # 1.0 to 5.0
    transparency_rating = Column(Float, nullable=True)  # 1.0 to 5.0

    # Review text
    review_title = Column(String(200), nullable=True)
    review_text = Column(Text, nullable=True)

    # Financial transaction details (if applicable)
    loan_amount = Column(Float, nullable=True)
    loan_term_months = Column(Integer, nullable=True)
    interest_rate = Column(Float, nullable=True)
    was_loan_completed = Column(Boolean, nullable=True)
    loan_completion_date = Column(DateTime, nullable=True)

    # Rating metadata
    is_verified = Column(Boolean, default=False)  # If rating is verified by platform
    is_anonymous = Column(Boolean, default=False)  # If rater wants to remain anonymous
    is_flagged = Column(Boolean, default=False)  # If rating is flagged for review
    flag_reason = Column(String(500), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Response from rated user
    response_text = Column(Text, nullable=True)
    response_created_at = Column(DateTime, nullable=True)

    # Helpfulness tracking
    helpful_count = Column(Integer, default=0)
    not_helpful_count = Column(Integer, default=0)

    # Relationships
    rater = relationship("User", foreign_keys=[rater_id], back_populates="given_ratings")
    rated_user = relationship("User", foreign_keys=[rated_user_id], back_populates="received_ratings")
    connection = relationship("Connection")

    def __repr__(self):
        return f"<Rating(id={self.id}, rater_id={self.rater_id}, rated_user_id={self.rated_user_id}, rating={self.overall_rating})>"

    @property
    def rating_summary(self) -> dict:
        """Get a summary of all ratings."""
        return {
            "overall": self.overall_rating,
            "communication": self.communication_rating,
            "reliability": self.reliability_rating,
            "professionalism": self.professionalism_rating,
            "timeliness": self.timeliness_rating,
            "transparency": self.transparency_rating
        }

    @property
    def average_detailed_rating(self) -> float:
        """Calculate average of all detailed ratings."""
        ratings = [
            self.communication_rating,
            self.reliability_rating,
            self.professionalism_rating,
            self.timeliness_rating,
            self.transparency_rating
        ]
        valid_ratings = [r for r in ratings if r is not None]

        if not valid_ratings:
            return self.overall_rating

        return sum(valid_ratings) / len(valid_ratings)

    @property
    def helpfulness_ratio(self) -> float:
        """Calculate helpfulness ratio (helpful / total votes)."""
        total_votes = self.helpful_count + self.not_helpful_count
        if total_votes == 0:
            return 0.0
        return self.helpful_count / total_votes

    @property
    def days_since_rating(self) -> int:
        """Get number of days since rating was created."""
        return (datetime.utcnow() - self.created_at).days

    def add_response(self, response_text: str):
        """Add a response from the rated user."""
        self.response_text = response_text
        self.response_created_at = datetime.utcnow()

    def mark_helpful(self, is_helpful: bool):
        """Mark rating as helpful or not helpful."""
        if is_helpful:
            self.helpful_count += 1
        else:
            self.not_helpful_count += 1

    def flag_for_review(self, reason: str):
        """Flag rating for administrative review."""
        self.is_flagged = True
        self.flag_reason = reason

    def verify_rating(self):
        """Mark rating as verified by platform."""
        self.is_verified = True

    @classmethod
    def get_user_average_rating(cls, db_session, user_id: int, rating_type: RatingType = None) -> dict:
        """Get average ratings for a user."""
        query = db_session.query(cls).filter(cls.rated_user_id == user_id)

        if rating_type:
            query = query.filter(cls.rating_type == rating_type)

        ratings = query.all()

        if not ratings:
            return {
                "overall_average": 0.0,
                "total_ratings": 0,
                "rating_breakdown": {}
            }

        # Calculate averages
        total_ratings = len(ratings)
        overall_sum = sum(r.overall_rating for r in ratings)
        overall_average = overall_sum / total_ratings

        # Calculate detailed averages
        detailed_categories = ['communication', 'reliability', 'professionalism', 'timeliness', 'transparency']
        rating_breakdown = {}

        for category in detailed_categories:
            category_ratings = [getattr(r, f"{category}_rating") for r in ratings if getattr(r, f"{category}_rating") is not None]
            if category_ratings:
                rating_breakdown[category] = {
                    "average": sum(category_ratings) / len(category_ratings),
                    "count": len(category_ratings)
                }
            else:
                rating_breakdown[category] = {
                    "average": 0.0,
                    "count": 0
                }

        return {
            "overall_average": round(overall_average, 2),
            "total_ratings": total_ratings,
            "rating_breakdown": rating_breakdown,
            "recent_ratings": len([r for r in ratings if r.days_since_rating <= 30])  # Ratings in last 30 days
        }