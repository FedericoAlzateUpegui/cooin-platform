from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc, or_
from datetime import datetime

from app.models.rating import Rating
from app.models.user import User
from app.models.connection import Connection, ConnectionStatus
from app.schemas.rating import (
    RatingCreate, RatingUpdate, RatingStats, UserRatingStats,
    RatingListResponse, RatingResponse
)


class RatingService:

    @staticmethod
    def create_rating(
        db: Session,
        rater_id: int,
        rating_data: RatingCreate
    ) -> Optional[Rating]:
        """Create a new rating for a connection."""

        # Verify connection exists and user is part of it
        connection = db.query(Connection).filter(
            Connection.id == rating_data.connection_id,
            and_(
                Connection.status == ConnectionStatus.ACCEPTED,
                or_(
                    Connection.requester_id == rater_id,
                    Connection.receiver_id == rater_id
                )
            )
        ).first()

        if not connection:
            return None

        # Determine rated_user_id (the other person in the connection)
        rated_user_id = connection.receiver_id if connection.requester_id == rater_id else connection.requester_id

        # Check if rating already exists
        existing_rating = db.query(Rating).filter(
            Rating.connection_id == rating_data.connection_id,
            Rating.rater_id == rater_id
        ).first()

        if existing_rating:
            return None  # User already rated this connection

        # Get financial context from connection
        rating = Rating(
            connection_id=rating_data.connection_id,
            rater_id=rater_id,
            rated_user_id=rated_user_id,
            rating_type=rating_data.rating_type.value,
            overall_rating=rating_data.overall_rating,
            communication_rating=rating_data.communication_rating,
            reliability_rating=rating_data.reliability_rating,
            professionalism_rating=rating_data.professionalism_rating,
            timeliness_rating=rating_data.timeliness_rating,
            transparency_rating=rating_data.transparency_rating,
            review_title=rating_data.review_title,
            review_text=rating_data.review_text,
            is_anonymous=rating_data.is_anonymous,

            # Financial context from connection
            loan_amount=connection.loan_amount_requested,
            loan_term=connection.loan_term_months,
            interest_rate=connection.interest_rate_proposed,

            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.add(rating)
        db.commit()
        db.refresh(rating)

        # Update user rating statistics
        RatingService._update_user_stats(db, rated_user_id)

        return rating

    @staticmethod
    def get_rating_by_id(
        db: Session,
        rating_id: int,
        user_id: Optional[int] = None
    ) -> Optional[Rating]:
        """Get a rating by ID."""
        query = db.query(Rating).filter(Rating.id == rating_id)

        # If user_id provided, ensure they can access this rating
        if user_id:
            query = query.filter(
                or_(
                    Rating.rater_id == user_id,
                    Rating.rated_user_id == user_id
                )
            )

        return query.first()

    @staticmethod
    def get_user_ratings(
        db: Session,
        user_id: int,
        page: int = 1,
        page_size: int = 20,
        rating_type: Optional[str] = None,
        as_rater: bool = False
    ) -> Tuple[List[Rating], int]:
        """Get ratings for or by a user with pagination."""

        # Base query - ratings received by user (default) or given by user
        if as_rater:
            query = db.query(Rating).filter(Rating.rater_id == user_id)
        else:
            query = db.query(Rating).filter(Rating.rated_user_id == user_id)

        # Filter by rating type if specified
        if rating_type:
            query = query.filter(Rating.rating_type == rating_type)

        # Get total count
        total_count = query.count()

        # Apply pagination and sorting
        ratings = query.order_by(desc(Rating.created_at)) \
                      .offset((page - 1) * page_size) \
                      .limit(page_size) \
                      .all()

        return ratings, total_count

    @staticmethod
    def get_connection_ratings(
        db: Session,
        connection_id: int,
        user_id: int
    ) -> List[Rating]:
        """Get ratings for a specific connection (user must be part of connection)."""

        # Verify user is part of the connection
        connection = db.query(Connection).filter(
            Connection.id == connection_id,
            or_(
                Connection.requester_id == user_id,
                Connection.receiver_id == user_id
            )
        ).first()

        if not connection:
            return []

        return db.query(Rating).filter(
            Rating.connection_id == connection_id
        ).order_by(desc(Rating.created_at)).all()

    @staticmethod
    def update_rating(
        db: Session,
        rating_id: int,
        user_id: int,
        update_data: RatingUpdate
    ) -> Optional[Rating]:
        """Update a rating (only by the rater)."""

        rating = db.query(Rating).filter(
            Rating.id == rating_id,
            Rating.rater_id == user_id
        ).first()

        if not rating:
            return None

        # Update fields
        for field, value in update_data.dict(exclude_unset=True).items():
            if hasattr(rating, field):
                setattr(rating, field, value)

        rating.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(rating)

        # Update user statistics
        RatingService._update_user_stats(db, rating.rated_user_id)

        return rating

    @staticmethod
    def delete_rating(
        db: Session,
        rating_id: int,
        user_id: int
    ) -> bool:
        """Delete a rating (only by the rater)."""

        rating = db.query(Rating).filter(
            Rating.id == rating_id,
            Rating.rater_id == user_id
        ).first()

        if not rating:
            return False

        rated_user_id = rating.rated_user_id
        db.delete(rating)
        db.commit()

        # Update user statistics
        RatingService._update_user_stats(db, rated_user_id)

        return True

    @staticmethod
    def get_user_rating_stats(
        db: Session,
        user_id: int
    ) -> UserRatingStats:
        """Get comprehensive rating statistics for a user."""

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        # Get all ratings received by this user
        ratings = db.query(Rating).filter(Rating.rated_user_id == user_id).all()

        # Calculate overall stats
        total_ratings = len(ratings)
        average_rating = sum(r.overall_rating for r in ratings) / total_ratings if total_ratings > 0 else 0.0

        # Calculate stats by rating type
        lender_ratings = [r for r in ratings if r.rating_type == "lender_rating"]
        borrower_ratings = [r for r in ratings if r.rating_type == "borrower_rating"]

        # Get recent ratings (last 5)
        recent_ratings = sorted(ratings, key=lambda x: x.created_at, reverse=True)[:5]

        return UserRatingStats(
            user_id=user_id,
            username=user.username,
            role=user.role.value,
            total_ratings_received=total_ratings,
            average_rating=round(average_rating, 1),
            lender_ratings=RatingService._calculate_rating_stats(lender_ratings),
            borrower_ratings=RatingService._calculate_rating_stats(borrower_ratings),
            recent_ratings=[RatingResponse.model_validate(r) for r in recent_ratings]
        )

    @staticmethod
    def update_helpfulness(
        db: Session,
        rating_id: int,
        user_id: int,
        is_helpful: bool
    ) -> Optional[Rating]:
        """Update the helpfulness count of a rating."""

        rating = db.query(Rating).filter(Rating.id == rating_id).first()
        if not rating:
            return None

        # User cannot vote on their own rating
        if rating.rater_id == user_id:
            return None

        # For simplicity, just increment counters (in production, track individual votes)
        if is_helpful:
            rating.helpful_count += 1
        else:
            rating.not_helpful_count += 1

        db.commit()
        db.refresh(rating)

        return rating

    @staticmethod
    def flag_rating(
        db: Session,
        rating_id: int,
        user_id: int
    ) -> Optional[Rating]:
        """Flag a rating for review."""

        rating = db.query(Rating).filter(Rating.id == rating_id).first()
        if not rating:
            return None

        rating.is_flagged = True
        rating.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(rating)

        return rating

    @staticmethod
    def _calculate_rating_stats(ratings: List[Rating]) -> RatingStats:
        """Calculate statistics for a list of ratings."""

        if not ratings:
            return RatingStats()

        total_count = len(ratings)
        avg_overall = sum(r.overall_rating for r in ratings) / total_count

        # Calculate category averages
        def calc_avg(attr):
            values = [getattr(r, attr) for r in ratings if getattr(r, attr) is not None]
            return sum(values) / len(values) if values else None

        # Count distribution
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for rating in ratings:
            star = int(rating.overall_rating)
            if star in distribution:
                distribution[star] += 1

        return RatingStats(
            total_ratings=total_count,
            average_rating=round(avg_overall, 1),
            average_communication=calc_avg('communication_rating'),
            average_reliability=calc_avg('reliability_rating'),
            average_professionalism=calc_avg('professionalism_rating'),
            average_timeliness=calc_avg('timeliness_rating'),
            average_transparency=calc_avg('transparency_rating'),
            one_star_count=distribution[1],
            two_star_count=distribution[2],
            three_star_count=distribution[3],
            four_star_count=distribution[4],
            five_star_count=distribution[5]
        )

    @staticmethod
    def _update_user_stats(db: Session, user_id: int):
        """Update cached rating statistics for a user."""

        # Calculate new stats
        ratings = db.query(Rating).filter(Rating.rated_user_id == user_id).all()

        total_ratings = len(ratings)
        average_rating = sum(r.overall_rating for r in ratings) / total_ratings if total_ratings > 0 else 0.0

        # Update user record
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.total_ratings = total_ratings
            user.average_rating = round(average_rating, 1)
            db.commit()


