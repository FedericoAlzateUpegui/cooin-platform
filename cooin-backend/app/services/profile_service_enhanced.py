from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func
import logging

from app.models import UserProfile, User
from app.models.profile import IncomeRange, EmploymentStatus, LoanPurpose
from app.models.user import UserRole, UserStatus
from app.schemas.profile import (
    UserProfileCreate, UserProfileUpdate, FinancialInfoUpdate,
    LendingPreferencesUpdate, BorrowingPreferencesUpdate,
    UserProfileResponse, UserProfilePublicResponse, ProfileCompletionResponse
)
from app.core.exceptions import (
    NotFoundError, ConflictError, ValidationError, BusinessLogicError, ErrorMessages
)

logger = logging.getLogger(__name__)


class ProfileService:
    """Enhanced service class for user profile operations with improved error handling."""

    @staticmethod
    def get_profile_by_user_id(db: Session, user_id: int) -> Optional[UserProfile]:
        """Get user profile by user ID with user relationship loaded."""
        return db.query(UserProfile).options(
            joinedload(UserProfile.user)
        ).filter(UserProfile.user_id == user_id).first()

    @staticmethod
    def create_profile(db: Session, user_id: int, profile_data: UserProfileCreate) -> UserProfile:
        """Create a new user profile with enhanced error handling."""
        # Check if profile already exists
        existing_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if existing_profile:
            raise ConflictError(
                detail="Profile already exists for this user. Use update instead.",
                error_code="PROFILE_ALREADY_EXISTS",
                conflicting_field="user_id",
                conflicting_value=str(user_id)
            )

        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundError(
                detail="User not found",
                resource_type="user",
                resource_id=str(user_id)
            )

        try:
            # Create profile
            profile_dict = profile_data.dict(exclude_unset=True)
            profile = UserProfile(
                user_id=user_id,
                **profile_dict
            )

            db.add(profile)
            db.flush()

            # Calculate initial completion percentage
            ProfileService._calculate_completion_percentage(profile)

            db.commit()
            db.refresh(profile)

            logger.info(f"Profile created for user {user_id}")
            return profile

        except Exception as e:
            db.rollback()
            logger.error(f"Error creating profile for user {user_id}: {str(e)}")
            raise ValidationError(
                detail="Failed to create profile. Please check your input data.",
                error_code="PROFILE_CREATION_FAILED"
            )

    @staticmethod
    def update_profile(
        db: Session,
        user_id: int,
        profile_update: UserProfileUpdate
    ) -> UserProfile:
        """Update user profile with enhanced validation."""
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            raise NotFoundError(
                detail="Profile not found. Please create a profile first.",
                resource_type="profile",
                resource_id=str(user_id)
            )

        try:
            # Update fields that were provided
            update_data = profile_update.dict(exclude_unset=True)

            for field, value in update_data.items():
                if hasattr(profile, field):
                    setattr(profile, field, value)

            # Update timestamps
            profile.updated_at = datetime.utcnow()
            profile.last_profile_update = datetime.utcnow()

            # Recalculate completion percentage
            ProfileService._calculate_completion_percentage(profile)

            db.commit()
            db.refresh(profile)

            logger.info(f"Profile updated for user {user_id}")
            return profile

        except Exception as e:
            db.rollback()
            logger.error(f"Error updating profile for user {user_id}: {str(e)}")
            raise ValidationError(
                detail="Failed to update profile. Please check your input data.",
                error_code="PROFILE_UPDATE_FAILED"
            )

    @staticmethod
    def delete_profile(db: Session, user_id: int) -> None:
        """Reset profile to default values."""
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            raise NotFoundError(
                detail="Profile not found",
                resource_type="profile",
                resource_id=str(user_id)
            )

        try:
            # Reset to default values instead of deleting
            ProfileService._reset_profile_to_defaults(profile)
            db.commit()

            logger.info(f"Profile reset for user {user_id}")

        except Exception as e:
            db.rollback()
            logger.error(f"Error resetting profile for user {user_id}: {str(e)}")
            raise ValidationError(
                detail="Failed to reset profile",
                error_code="PROFILE_RESET_FAILED"
            )

    @staticmethod
    def get_public_profile(db: Session, user_id: int, viewer_id: Optional[int] = None) -> Optional[UserProfile]:
        """Get public profile with privacy settings applied."""
        profile = ProfileService.get_profile_by_user_id(db, user_id)
        if not profile:
            return None

        # Apply privacy filters unless viewing own profile
        if viewer_id != user_id and not profile.is_profile_public:
            return None

        return profile

    @staticmethod
    def search_profiles(
        db: Session,
        role: Optional[str] = None,
        location: Optional[str] = None,
        min_loan_amount: Optional[float] = None,
        max_loan_amount: Optional[float] = None,
        income_range: Optional[str] = None,
        employment_status: Optional[str] = None,
        verified_only: bool = False,
        skip: int = 0,
        limit: int = 20,
        current_user_id: Optional[int] = None
    ) -> List[UserProfile]:
        """Search profiles with advanced filters."""
        query = db.query(UserProfile).options(
            joinedload(UserProfile.user)
        ).filter(
            UserProfile.is_profile_public == True
        )

        # Filter by role
        if role:
            try:
                user_role = UserRole(role.lower())
                query = query.join(User).filter(
                    or_(
                        User.role == user_role,
                        User.role == UserRole.BOTH
                    )
                )
            except ValueError:
                raise ValidationError(
                    detail=f"Invalid role '{role}'. Must be one of: lender, borrower, both",
                    error_code="INVALID_ROLE_FILTER"
                )

        # Filter by location (city, state, or country)
        if location:
            location_filter = f"%{location.lower()}%"
            query = query.filter(
                or_(
                    func.lower(UserProfile.city).like(location_filter),
                    func.lower(UserProfile.state_province).like(location_filter),
                    func.lower(UserProfile.country).like(location_filter)
                )
            )

        # Filter by loan amount ranges
        if min_loan_amount is not None:
            query = query.filter(
                or_(
                    UserProfile.min_loan_amount >= min_loan_amount,
                    UserProfile.requested_loan_amount >= min_loan_amount
                )
            )

        if max_loan_amount is not None:
            query = query.filter(
                or_(
                    UserProfile.max_loan_amount <= max_loan_amount,
                    UserProfile.requested_loan_amount <= max_loan_amount
                )
            )

        # Filter by income range
        if income_range:
            try:
                income_enum = IncomeRange(income_range.lower())
                query = query.filter(UserProfile.income_range == income_enum)
            except ValueError:
                raise ValidationError(
                    detail=f"Invalid income range '{income_range}'",
                    error_code="INVALID_INCOME_RANGE_FILTER"
                )

        # Filter by employment status
        if employment_status:
            try:
                employment_enum = EmploymentStatus(employment_status.lower())
                query = query.filter(UserProfile.employment_status == employment_enum)
            except ValueError:
                raise ValidationError(
                    detail=f"Invalid employment status '{employment_status}'",
                    error_code="INVALID_EMPLOYMENT_STATUS_FILTER"
                )

        # Filter by verification status
        if verified_only:
            query = query.filter(
                and_(
                    UserProfile.identity_verified == True,
                    UserProfile.income_verified == True
                )
            )

        # Exclude current user from results
        if current_user_id:
            query = query.filter(UserProfile.user_id != current_user_id)

        # Apply pagination
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def calculate_profile_completion(db: Session, user_id: int) -> ProfileCompletionResponse:
        """Calculate profile completion percentage and identify missing fields."""
        profile = ProfileService.get_profile_by_user_id(db, user_id)
        if not profile:
            raise NotFoundError(
                detail="Profile not found",
                resource_type="profile",
                resource_id=str(user_id)
            )

        # Define required fields and their weights
        field_weights = {
            'first_name': 5,
            'last_name': 5,
            'bio': 10,
            'phone_number': 5,
            'country': 5,
            'city': 5,
            'income_range': 15,
            'employment_status': 15,
            'employer_name': 5,
            'years_employed': 5,
        }

        total_weight = sum(field_weights.values())
        completed_weight = 0
        missing_fields = []

        for field, weight in field_weights.items():
            value = getattr(profile, field)
            if value is not None and str(value).strip():
                completed_weight += weight
            else:
                missing_fields.append(field)

        # Add role-specific fields
        user = profile.user
        if user.is_lender:
            lender_fields = {
                'min_loan_amount': 10,
                'max_loan_amount': 10,
                'preferred_interest_rate': 10,
            }
            for field, weight in lender_fields.items():
                total_weight += weight
                value = getattr(profile, field)
                if value is not None and value > 0:
                    completed_weight += weight
                else:
                    missing_fields.append(field)

        if user.is_borrower:
            borrower_fields = {
                'requested_loan_amount': 10,
                'loan_purpose': 10,
                'preferred_loan_term': 5,
            }
            for field, weight in borrower_fields.items():
                total_weight += weight
                value = getattr(profile, field)
                if value is not None and (isinstance(value, (int, float)) and value > 0 or value):
                    completed_weight += weight
                else:
                    missing_fields.append(field)

        completion_percentage = round((completed_weight / total_weight) * 100, 1)

        return ProfileCompletionResponse(
            completion_percentage=completion_percentage,
            missing_fields=missing_fields,
            total_fields=len(field_weights),
            completed_fields=len(field_weights) - len(missing_fields)
        )

    @staticmethod
    def update_financial_info(
        db: Session,
        user_id: int,
        financial_data: FinancialInfoUpdate
    ) -> UserProfile:
        """Update financial information with additional validation."""
        profile = ProfileService.get_profile_by_user_id(db, user_id)
        if not profile:
            raise NotFoundError(
                detail="Profile not found",
                resource_type="profile",
                resource_id=str(user_id)
            )

        try:
            update_data = financial_data.dict(exclude_unset=True)

            # Additional validation for financial data
            if 'monthly_income' in update_data and 'monthly_expenses' in update_data:
                if update_data['monthly_expenses'] > update_data['monthly_income']:
                    raise ValidationError(
                        detail="Monthly expenses cannot exceed monthly income",
                        error_code="INVALID_FINANCIAL_DATA"
                    )

            # Update fields
            for field, value in update_data.items():
                setattr(profile, field, value)

            profile.updated_at = datetime.utcnow()
            ProfileService._calculate_completion_percentage(profile)

            db.commit()
            db.refresh(profile)

            return profile

        except ValidationError:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating financial info for user {user_id}: {str(e)}")
            raise ValidationError(
                detail="Failed to update financial information",
                error_code="FINANCIAL_UPDATE_FAILED"
            )

    @staticmethod
    def update_lending_preferences(
        db: Session,
        user_id: int,
        lending_data: LendingPreferencesUpdate
    ) -> UserProfile:
        """Update lending preferences with validation."""
        profile = ProfileService.get_profile_by_user_id(db, user_id)
        if not profile:
            raise NotFoundError(
                detail="Profile not found",
                resource_type="profile",
                resource_id=str(user_id)
            )

        try:
            update_data = lending_data.dict(exclude_unset=True)

            # Validate loan amount ranges
            if 'min_loan_amount' in update_data and 'max_loan_amount' in update_data:
                if update_data['min_loan_amount'] >= update_data['max_loan_amount']:
                    raise ValidationError(
                        detail="Minimum loan amount must be less than maximum loan amount",
                        error_code="INVALID_LOAN_RANGE"
                    )

            # Update fields
            for field, value in update_data.items():
                setattr(profile, field, value)

            profile.updated_at = datetime.utcnow()
            ProfileService._calculate_completion_percentage(profile)

            db.commit()
            db.refresh(profile)

            return profile

        except ValidationError:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating lending preferences for user {user_id}: {str(e)}")
            raise ValidationError(
                detail="Failed to update lending preferences",
                error_code="LENDING_PREFERENCES_UPDATE_FAILED"
            )

    @staticmethod
    def update_borrowing_preferences(
        db: Session,
        user_id: int,
        borrowing_data: BorrowingPreferencesUpdate
    ) -> UserProfile:
        """Update borrowing preferences with validation."""
        profile = ProfileService.get_profile_by_user_id(db, user_id)
        if not profile:
            raise NotFoundError(
                detail="Profile not found",
                resource_type="profile",
                resource_id=str(user_id)
            )

        try:
            update_data = borrowing_data.dict(exclude_unset=True)

            # Validate loan terms
            if 'preferred_loan_term_min' in update_data and 'preferred_loan_term_max' in update_data:
                if update_data['preferred_loan_term_min'] >= update_data['preferred_loan_term_max']:
                    raise ValidationError(
                        detail="Minimum loan term must be less than maximum loan term",
                        error_code="INVALID_LOAN_TERM_RANGE"
                    )

            # Update fields
            for field, value in update_data.items():
                setattr(profile, field, value)

            profile.updated_at = datetime.utcnow()
            ProfileService._calculate_completion_percentage(profile)

            db.commit()
            db.refresh(profile)

            return profile

        except ValidationError:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating borrowing preferences for user {user_id}: {str(e)}")
            raise ValidationError(
                detail="Failed to update borrowing preferences",
                error_code="BORROWING_PREFERENCES_UPDATE_FAILED"
            )

    @staticmethod
    def _calculate_completion_percentage(profile: UserProfile) -> None:
        """Internal method to calculate and update profile completion percentage."""
        # This is a simplified version - you can expand based on your requirements
        required_fields = [
            'first_name', 'last_name', 'bio', 'phone_number',
            'country', 'city', 'income_range', 'employment_status'
        ]

        completed_fields = sum(1 for field in required_fields
                             if getattr(profile, field) is not None and str(getattr(profile, field)).strip())

        profile.profile_completion_percentage = (completed_fields / len(required_fields)) * 100

    @staticmethod
    def _reset_profile_to_defaults(profile: UserProfile) -> None:
        """Reset profile fields to default values."""
        # Reset personal info
        profile.first_name = None
        profile.last_name = None
        profile.display_name = None
        profile.bio = None
        profile.date_of_birth = None
        profile.phone_number = None

        # Reset location
        profile.country = None
        profile.state_province = None
        profile.city = None
        profile.postal_code = None

        # Reset financial info
        profile.income_range = None
        profile.employment_status = None
        profile.employer_name = None
        profile.years_employed = None
        profile.monthly_income = None
        profile.monthly_expenses = None

        # Reset loan preferences
        profile.min_loan_amount = None
        profile.max_loan_amount = None
        profile.requested_loan_amount = None
        profile.loan_purpose = None
        profile.preferred_loan_term = None
        profile.preferred_interest_rate = None
        profile.max_acceptable_rate = None

        # Update timestamps
        profile.updated_at = datetime.utcnow()
        profile.last_profile_update = datetime.utcnow()
        profile.profile_completion_percentage = 0.0