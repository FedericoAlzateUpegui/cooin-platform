from datetime import datetime, timedelta
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DataError
from fastapi import HTTPException, status
import secrets
import logging

from app.models import User, UserProfile, RefreshToken
from app.models.user import UserRole, UserStatus
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import password_handler, jwt_handler
from app.core.config import settings
from app.core.exceptions import (
    ConflictError,
    ValidationError,
    DatabaseError,
    ErrorMessages,
    format_validation_errors
)
from app.core.email import get_email_service

logger = logging.getLogger(__name__)


class UserService:
    """Service class for user-related operations."""

    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash a password using the configured password handler."""
        return password_handler.hash_password(password)

    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> User:
        """Create a new user with profile."""
        try:
            # Check if user already exists with detailed error messages
            email_exists = db.query(User).filter(User.email == user_create.email).first()
            if email_exists:
                raise ConflictError(
                    detail=ErrorMessages.EMAIL_ALREADY_EXISTS,
                    error_code="EMAIL_ALREADY_EXISTS",
                    conflicting_field="email",
                    conflicting_value=user_create.email
                )

            if user_create.username:
                username_exists = db.query(User).filter(User.username == user_create.username).first()
                if username_exists:
                    raise ConflictError(
                        detail=ErrorMessages.USERNAME_ALREADY_EXISTS,
                        error_code="USERNAME_ALREADY_EXISTS",
                        conflicting_field="username",
                        conflicting_value=user_create.username
                    )

            # Hash password
            hashed_password = password_handler.hash_password(user_create.password)

            # Generate verification token
            verification_token = secrets.token_urlsafe(32)

            # Validate role
            try:
                user_role = UserRole(user_create.role)
            except ValueError:
                raise ValidationError(
                    detail=f"Invalid role '{user_create.role}'. Must be one of: lender, borrower, both",
                    error_code="INVALID_ROLE"
                )

            # Create user
            user = User(
                email=user_create.email,
                username=user_create.username,
                hashed_password=hashed_password,
                role=user_role,
                verification_token=verification_token,
                is_active=True,
                is_verified=False,
                status=UserStatus.PENDING_VERIFICATION
            )

            db.add(user)
            db.flush()  # Get user ID

            # Create associated profile
            profile = UserProfile(user_id=user.id)
            db.add(profile)

            db.commit()
            db.refresh(user)

            # Send verification email
            try:
                email_service = get_email_service()
                email_sent = email_service.send_verification_email(
                    email=user.email,
                    username=user.username,
                    verification_token=verification_token
                )
                if email_sent:
                    logger.info(f"Verification email sent to {user.email}")
                else:
                    logger.warning(f"Failed to send verification email to {user.email}")
            except Exception as e:
                logger.error(f"Error sending verification email to {user.email}: {str(e)}")
                # Don't fail user creation if email sending fails

            logger.info(f"User created successfully: {user.email} (ID: {user.id})")
            return user

        except (ConflictError, ValidationError):
            db.rollback()
            raise  # Re-raise custom exceptions as-is

        except IntegrityError as e:
            db.rollback()
            logger.error(f"Database integrity constraint violation: {str(e)}")

            # Parse specific constraint violations
            error_msg = str(e.orig).lower()
            if "email" in error_msg:
                raise ConflictError(
                    detail=ErrorMessages.EMAIL_ALREADY_EXISTS,
                    error_code="EMAIL_CONSTRAINT_VIOLATION",
                    conflicting_field="email"
                )
            elif "username" in error_msg:
                raise ConflictError(
                    detail=ErrorMessages.USERNAME_ALREADY_EXISTS,
                    error_code="USERNAME_CONSTRAINT_VIOLATION",
                    conflicting_field="username"
                )
            else:
                raise DatabaseError(
                    detail="A database constraint was violated. Please check your input.",
                    error_code="INTEGRITY_CONSTRAINT_VIOLATION",
                    operation="user_creation"
                )

        except DataError as e:
            db.rollback()
            logger.error(f"Database data error during user creation: {str(e)}")
            raise ValidationError(
                detail="Invalid data format provided",
                error_code="DATABASE_DATA_ERROR"
            )

        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error creating user: {str(e)}", exc_info=True)
            raise DatabaseError(
                detail=ErrorMessages.INTERNAL_SERVER_ERROR,
                error_code="USER_CREATION_FAILED",
                operation="user_creation"
            )

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                logger.info(f"DEBUG: User not found for email: {email}")
                return None

            # Check if account is locked
            if user.is_account_locked:
                logger.warning(f"Login attempt on locked account: {email}")
                return None

            # DEBUG: Log password verification attempt
            logger.info(f"DEBUG: Verifying password for {email}, password len: {len(password)}, hash: {user.hashed_password[:20]}...")
            password_valid = password_handler.verify_password(password, user.hashed_password)
            logger.info(f"DEBUG: Password verification result: {password_valid}")

            # Verify password
            if not password_valid:
                # Increment failed login attempts
                user.increment_failed_login()
                db.commit()
                return None

            # Reset failed login attempts on successful authentication
            user.reset_failed_login()
            db.commit()

            return user

        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return None

    @staticmethod
    def create_refresh_token(
        db: Session,
        user: User,
        device_info: Optional[str] = None,
        ip_address: Optional[str] = None,
        remember_me: bool = False
    ) -> RefreshToken:
        """Create a new refresh token for user."""
        try:
            # Calculate expiration time
            expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
            if remember_me:
                expires_delta = timedelta(days=30)  # Extended expiry for "remember me"

            # Create JWT refresh token
            token_string = jwt_handler.create_refresh_token(
                subject=str(user.id),
                expires_delta=expires_delta
            )

            # Create refresh token record
            refresh_token = RefreshToken(
                token=token_string,
                user_id=user.id,
                expires_at=datetime.utcnow() + expires_delta,
                device_info=device_info,
                ip_address=ip_address
            )

            db.add(refresh_token)
            db.commit()
            db.refresh(refresh_token)

            return refresh_token

        except Exception as e:
            db.rollback()
            logger.error(f"Error creating refresh token: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create refresh token"
            )

    @staticmethod
    def refresh_access_token(
        db: Session,
        refresh_token_string: str
    ) -> Tuple[str, RefreshToken]:
        """Create new access token using refresh token."""
        from app.core.deps import validate_refresh_token

        user, refresh_token = validate_refresh_token(refresh_token_string, db)

        # Create new access token
        access_token = jwt_handler.create_access_token(subject=str(user.id))

        # Update last used timestamp on refresh token
        refresh_token.created_at = datetime.utcnow()  # Track last usage
        db.commit()

        return access_token, refresh_token

    @staticmethod
    def revoke_refresh_token(db: Session, token_string: str) -> bool:
        """Revoke a specific refresh token."""
        try:
            token = db.query(RefreshToken).filter(RefreshToken.token == token_string).first()
            if token:
                token.revoke()
                db.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Error revoking refresh token: {e}")
            return False

    @staticmethod
    def revoke_all_refresh_tokens(db: Session, user_id: int) -> int:
        """Revoke all refresh tokens for a user."""
        try:
            tokens = db.query(RefreshToken).filter(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked == False
            ).all()

            count = 0
            for token in tokens:
                token.revoke()
                count += 1

            db.commit()
            return count
        except Exception as e:
            logger.error(f"Error revoking all refresh tokens: {e}")
            return 0

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username."""
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User:
        """Update user information."""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            # Check for email uniqueness if email is being updated
            if user_update.email and user_update.email != user.email:
                existing_user = db.query(User).filter(User.email == user_update.email).first()
                if existing_user:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already registered"
                    )
                user.email = user_update.email
                user.is_verified = False  # Re-verify email
                user.verification_token = secrets.token_urlsafe(32)

            # Check for username uniqueness if username is being updated
            if user_update.username and user_update.username != user.username:
                existing_user = db.query(User).filter(User.username == user_update.username).first()
                if existing_user:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Username already taken"
                    )
                user.username = user_update.username

            # Update role if provided
            if user_update.role:
                user.role = UserRole(user_update.role)

            user.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(user)

            return user

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not update user"
            )

    @staticmethod
    def change_password(
        db: Session,
        user_id: int,
        current_password: str,
        new_password: str
    ) -> bool:
        """Change user password."""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            # Verify current password
            if not password_handler.verify_password(current_password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Current password is incorrect"
                )

            # Hash new password
            user.hashed_password = password_handler.hash_password(new_password)
            user.updated_at = datetime.utcnow()

            # Revoke all refresh tokens to force re-login
            UserService.revoke_all_refresh_tokens(db, user_id)

            db.commit()
            return True

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error changing password: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not change password"
            )

    @staticmethod
    def verify_email(db: Session, token: str) -> bool:
        """Verify user email with token."""
        try:
            user = db.query(User).filter(User.verification_token == token).first()
            if not user:
                return False

            user.is_verified = True
            user.email_verified_at = datetime.utcnow()
            user.verification_token = None
            user.status = UserStatus.ACTIVE
            user.updated_at = datetime.utcnow()

            db.commit()
            return True

        except Exception as e:
            db.rollback()
            logger.error(f"Error verifying email: {e}")
            return False

    @staticmethod
    def initiate_password_reset(db: Session, email: str) -> Optional[str]:
        """Initiate password reset process."""
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                # Don't reveal whether email exists
                return None

            # Generate reset token
            reset_token = secrets.token_urlsafe(32)
            user.reset_password_token = reset_token
            user.reset_password_expires = datetime.utcnow() + timedelta(hours=1)  # 1 hour expiry
            user.updated_at = datetime.utcnow()

            db.commit()
            return reset_token

        except Exception as e:
            db.rollback()
            logger.error(f"Error initiating password reset: {e}")
            return None

    @staticmethod
    def reset_password(db: Session, token: str, new_password: str) -> bool:
        """Reset password using reset token."""
        try:
            user = db.query(User).filter(
                User.reset_password_token == token,
                User.reset_password_expires > datetime.utcnow()
            ).first()

            if not user:
                return False

            # Update password
            user.hashed_password = password_handler.hash_password(new_password)
            user.reset_password_token = None
            user.reset_password_expires = None
            user.updated_at = datetime.utcnow()

            # Revoke all refresh tokens
            UserService.revoke_all_refresh_tokens(db, user.id)

            db.commit()
            return True

        except Exception as e:
            db.rollback()
            logger.error(f"Error resetting password: {e}")
            return False

    @staticmethod
    def deactivate_user(db: Session, user_id: int) -> bool:
        """Deactivate user account."""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return False

            user.is_active = False
            user.status = UserStatus.INACTIVE
            user.updated_at = datetime.utcnow()

            # Revoke all refresh tokens
            UserService.revoke_all_refresh_tokens(db, user_id)

            db.commit()
            return True

        except Exception as e:
            db.rollback()
            logger.error(f"Error deactivating user: {e}")
            return False

    @staticmethod
    def get_user_sessions(db: Session, user_id: int) -> list[RefreshToken]:
        """Get all active sessions (refresh tokens) for a user."""
        return db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked == False,
            RefreshToken.expires_at > datetime.utcnow()
        ).order_by(RefreshToken.created_at.desc()).all()