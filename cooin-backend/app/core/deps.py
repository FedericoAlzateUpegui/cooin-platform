from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import logging

from app.db.base import get_db
from app.models import User, RefreshToken
from app.core.security import jwt_handler
from app.schemas.auth import TokenData

logger = logging.getLogger(__name__)

# Security scheme for JWT authentication
security = HTTPBearer()
optional_security = HTTPBearer(auto_error=False)  # For optional authentication


def get_database() -> Generator:
    """Database dependency."""
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


async def get_current_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_database)
) -> User:
    """
    Extract current user from JWT access token.
    This dependency validates the JWT token and returns the current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Extract token from credentials
        token = credentials.credentials

        # Decode and validate token
        payload = jwt_handler.decode_token(token)

        # Verify token type
        if not jwt_handler.verify_token_type(payload, "access"):
            raise credentials_exception

        # Extract user ID
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        # Get user from database
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None:
            raise credentials_exception

        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user",
            )

        # Check if account is locked
        if user.is_account_locked:
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="Account is temporarily locked due to failed login attempts",
            )

        return user

    except Exception as e:
        logger.error(f"Token validation error: {e}")
        raise credentials_exception


async def get_current_active_user(
    current_user: User = Depends(get_current_user_from_token)
) -> User:
    """Get current active user (additional validation layer)."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


async def get_current_verified_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Get current verified user."""
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User email not verified"
        )
    return current_user


async def get_current_lender(
    current_user: User = Depends(get_current_verified_user)
) -> User:
    """Get current user if they are a lender."""
    if not current_user.is_lender:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to perform lending operations"
        )
    return current_user


async def get_current_borrower(
    current_user: User = Depends(get_current_verified_user)
) -> User:
    """Get current user if they are a borrower."""
    if not current_user.is_borrower:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to perform borrowing operations"
        )
    return current_user


def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(optional_security),
    db: Session = Depends(get_database)
) -> Optional[User]:
    """
    Get current user if token is provided, otherwise return None.
    Useful for endpoints that can work with or without authentication.
    """
    if not credentials:
        return None

    try:
        token = credentials.credentials
        payload = jwt_handler.decode_token(token)

        if not jwt_handler.verify_token_type(payload, "access"):
            return None

        user_id = payload.get("sub")
        if user_id is None:
            return None

        user = db.query(User).filter(User.id == int(user_id)).first()
        if user and user.is_active and not user.is_account_locked:
            return user

    except Exception as e:
        logger.warning(f"Optional token validation failed: {e}")

    return None


def validate_refresh_token(
    refresh_token: str,
    db: Session
) -> tuple[User, RefreshToken]:
    """
    Validate refresh token and return user and token record.
    Used for token refresh operations.
    """
    try:
        # Decode refresh token
        payload = jwt_handler.decode_token(refresh_token)

        # Verify token type
        if not jwt_handler.verify_token_type(payload, "refresh"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

        # Extract user ID
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )

        # Get refresh token from database
        token_record = db.query(RefreshToken).filter(
            RefreshToken.token == refresh_token,
            RefreshToken.user_id == int(user_id)
        ).first()

        if not token_record:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token not found",
            )

        # Check if token is valid
        if not token_record.is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is expired or revoked",
            )

        # Get user
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is inactive",
            )

        return user, token_record

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Refresh token validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate refresh token",
        )


def get_user_by_id(user_id: int, db: Session) -> Optional[User]:
    """Get user by ID with basic validation."""
    user = db.query(User).filter(User.id == user_id).first()
    return user


def check_user_permissions(current_user: User, target_user_id: int) -> bool:
    """
    Check if current user has permission to access target user's data.
    Users can always access their own data.
    """
    return current_user.id == target_user_id


def require_user_permission(
    target_user_id: int,
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Dependency that ensures current user has permission to access target user's data.
    """
    if not check_user_permissions(current_user, target_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this resource"
        )
    return current_user