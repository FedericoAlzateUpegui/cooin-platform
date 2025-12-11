from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import logging

from app.db.base import get_db
from app.models import User, UserProfile
from app.schemas.profile import (
    UserProfileResponse, UserProfilePublicResponse, UserProfileCreate, UserProfileUpdate,
    FinancialInfoUpdate, LendingPreferencesUpdate, BorrowingPreferencesUpdate,
    ProfileCompletionResponse
)
from app.services.profile_service import ProfileService
from app.core.deps import get_current_active_user, get_optional_current_user, get_database
from app.core.exceptions import NotFoundError, ValidationError, BusinessLogicError, ConflictError

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/me", response_model=UserProfileResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Get current user's profile.

    Returns complete profile information including private data.
    """
    profile = ProfileService.get_profile_by_user_id(db, current_user.id)
    if not profile:
        raise NotFoundError(
            detail="Profile not found. Please complete your profile setup.",
            resource_type="profile",
            resource_id=str(current_user.id)
        )

    return profile


@router.post("/me", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_my_profile(
    profile_data: UserProfileCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Create current user's profile.

    Creates a new profile for the authenticated user.
    """
    profile = ProfileService.create_profile(db, current_user.id, profile_data)
    logger.info(f"Profile created for user {current_user.id}")
    return profile


@router.put("/me", response_model=UserProfileResponse)
async def update_my_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Update current user's profile.

    Allows partial updates - only provided fields will be updated.
    """
    profile = ProfileService.update_profile(db, current_user.id, profile_data)
    logger.info(f"Profile updated for user {current_user.id}")
    return profile


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Delete current user's profile.

    This will reset the profile to default values while keeping the user account.
    """
    ProfileService.delete_profile(db, current_user.id)
    logger.info(f"Profile deleted for user {current_user.id}")


@router.get("/me/completion", response_model=ProfileCompletionResponse)
async def get_profile_completion(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Get profile completion status.

    Returns completion percentage and missing fields.
    """
    completion_info = ProfileService.calculate_profile_completion(db, current_user.id)
    return completion_info


@router.get("/{user_id}", response_model=UserProfilePublicResponse)
async def get_public_profile(
    user_id: int,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_database)
):
    """
    Get public profile of another user.

    Returns only publicly visible information based on user's privacy settings.
    """
    profile = ProfileService.get_public_profile(db, user_id, current_user.id if current_user else None)
    if not profile:
        raise NotFoundError(
            detail="Profile not found or not public",
            resource_type="profile",
            resource_id=str(user_id)
        )

    return profile


@router.get("/", response_model=List[UserProfilePublicResponse])
async def search_profiles(
    role: Optional[str] = Query(None, description="Filter by user role (lender/borrower/both)"),
    location: Optional[str] = Query(None, description="Filter by location (city, state, or country)"),
    min_loan_amount: Optional[float] = Query(None, description="Minimum loan amount"),
    max_loan_amount: Optional[float] = Query(None, description="Maximum loan amount"),
    income_range: Optional[str] = Query(None, description="Filter by income range"),
    employment_status: Optional[str] = Query(None, description="Filter by employment status"),
    verified_only: bool = Query(False, description="Show only verified profiles"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of records to return"),
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_database)
):
    """
    Search profiles with filters.

    Returns paginated list of public profiles matching the search criteria.
    """
    profiles = ProfileService.search_profiles(
        db=db,
        role=role,
        location=location,
        min_loan_amount=min_loan_amount,
        max_loan_amount=max_loan_amount,
        income_range=income_range,
        employment_status=employment_status,
        verified_only=verified_only,
        skip=skip,
        limit=limit,
        current_user_id=current_user.id if current_user else None
    )

    return profiles


@router.patch("/me/financial", response_model=UserProfileResponse)
async def update_financial_info(
    financial_data: FinancialInfoUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Update financial information separately.

    Allows updating sensitive financial data with additional validation.
    """
    profile = ProfileService.update_financial_info(db, current_user.id, financial_data)
    logger.info(f"Financial info updated for user {current_user.id}")
    return profile


@router.patch("/me/lending", response_model=UserProfileResponse)
async def update_lending_preferences(
    lending_data: LendingPreferencesUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Update lending preferences.

    For users who can lend money - updates their lending criteria and preferences.
    """
    # Verify user can be a lender
    if not (current_user.is_lender):
        raise BusinessLogicError(
            detail="Only lenders can update lending preferences",
            error_code="INVALID_USER_ROLE"
        )

    profile = ProfileService.update_lending_preferences(db, current_user.id, lending_data)
    logger.info(f"Lending preferences updated for user {current_user.id}")
    return profile


@router.patch("/me/borrowing", response_model=UserProfileResponse)
async def update_borrowing_preferences(
    borrowing_data: BorrowingPreferencesUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Update borrowing preferences.

    For users who need to borrow money - updates their borrowing needs and preferences.
    """
    # Verify user can be a borrower
    if not (current_user.is_borrower):
        raise BusinessLogicError(
            detail="Only borrowers can update borrowing preferences",
            error_code="INVALID_USER_ROLE"
        )

    profile = ProfileService.update_borrowing_preferences(db, current_user.id, borrowing_data)
    logger.info(f"Borrowing preferences updated for user {current_user.id}")
    return profile