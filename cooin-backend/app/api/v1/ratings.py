from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_active_user, get_database
from app.models.user import User
from app.schemas.rating import (
    RatingCreate, RatingUpdate, RatingResponse, RatingListResponse,
    UserRatingStats, RatingHelpfulnessUpdate
)
from app.services.rating_service import RatingService

router = APIRouter()


@router.post("/", response_model=RatingResponse, status_code=status.HTTP_201_CREATED)
async def create_rating(
    rating_data: RatingCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Create a new rating for a connection."""
    rating = RatingService.create_rating(
        db=db,
        rater_id=current_user.id,
        rating_data=rating_data
    )

    if not rating:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create rating. Connection may not exist, not be accepted, or you may have already rated it."
        )

    return rating


@router.get("/", response_model=RatingListResponse)
async def get_my_ratings(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    rating_type: Optional[str] = Query(None, description="Filter by rating type"),
    as_rater: bool = Query(False, description="Get ratings given by me instead of received"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Get ratings for the current user (received by default) or given by the user."""
    ratings, total_count = RatingService.get_user_ratings(
        db=db,
        user_id=current_user.id,
        page=page,
        page_size=page_size,
        rating_type=rating_type,
        as_rater=as_rater
    )

    response = RatingListResponse(
        ratings=[RatingResponse.model_validate(rating) for rating in ratings],
        total_count=total_count,
        page=page,
        page_size=page_size,
        has_next=(page * page_size) < total_count,
        has_previous=page > 1
    )

    return response


@router.get("/users/{user_id}", response_model=RatingListResponse)
async def get_user_ratings(
    user_id: int,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    rating_type: Optional[str] = Query(None, description="Filter by rating type"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Get public ratings for any user."""
    ratings, total_count = RatingService.get_user_ratings(
        db=db,
        user_id=user_id,
        page=page,
        page_size=page_size,
        rating_type=rating_type,
        as_rater=False  # Always get ratings received by the user
    )

    # Filter out anonymous ratings if current user is not the ratee
    if current_user.id != user_id:
        ratings = [r for r in ratings if not r.is_anonymous]
        total_count = len(ratings)

    response = RatingListResponse(
        ratings=[RatingResponse.model_validate(rating) for rating in ratings],
        total_count=total_count,
        page=page,
        page_size=page_size,
        has_next=(page * page_size) < total_count,
        has_previous=page > 1
    )

    return response


@router.get("/users/{user_id}/stats", response_model=UserRatingStats)
async def get_user_rating_stats(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Get rating statistics for a user."""
    stats = RatingService.get_user_rating_stats(db=db, user_id=user_id)

    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return stats


@router.get("/connections/{connection_id}", response_model=List[RatingResponse])
async def get_connection_ratings(
    connection_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Get all ratings for a specific connection."""
    ratings = RatingService.get_connection_ratings(
        db=db,
        connection_id=connection_id,
        user_id=current_user.id
    )

    return [RatingResponse.model_validate(rating) for rating in ratings]


@router.get("/{rating_id}", response_model=RatingResponse)
async def get_rating(
    rating_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Get a specific rating by ID."""
    rating = RatingService.get_rating_by_id(
        db=db,
        rating_id=rating_id,
        user_id=current_user.id
    )

    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found or you don't have permission to view it"
        )

    return rating


@router.put("/{rating_id}", response_model=RatingResponse)
async def update_rating(
    rating_id: int,
    rating_data: RatingUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Update a rating (only by the original rater)."""
    rating = RatingService.update_rating(
        db=db,
        rating_id=rating_id,
        user_id=current_user.id,
        update_data=rating_data
    )

    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found or you don't have permission to update it"
        )

    return rating


@router.delete("/{rating_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rating(
    rating_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Delete a rating (only by the original rater)."""
    success = RatingService.delete_rating(
        db=db,
        rating_id=rating_id,
        user_id=current_user.id
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found or you don't have permission to delete it"
        )


@router.post("/{rating_id}/helpful", response_model=RatingResponse)
async def update_rating_helpfulness(
    rating_id: int,
    helpfulness_data: RatingHelpfulnessUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Mark a rating as helpful or not helpful."""
    rating = RatingService.update_helpfulness(
        db=db,
        rating_id=rating_id,
        user_id=current_user.id,
        is_helpful=helpfulness_data.is_helpful
    )

    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found or you cannot vote on your own rating"
        )

    return rating


@router.post("/{rating_id}/flag", response_model=RatingResponse)
async def flag_rating(
    rating_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Flag a rating for moderation review."""
    rating = RatingService.flag_rating(
        db=db,
        rating_id=rating_id,
        user_id=current_user.id
    )

    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found"
        )

    return rating