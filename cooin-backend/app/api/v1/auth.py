from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
import logging

from app.db.base import get_db
from app.models import User, RefreshToken
from app.schemas.auth import (
    LoginRequest, LoginResponse, RegisterRequest, RegisterResponse,
    Token, TokenRefresh, AccessToken, LogoutRequest, LogoutResponse,
    ActiveSession, SessionsResponse
)
from app.schemas.user import UserResponse, UserCreate, UserUpdate, PasswordReset, PasswordResetConfirm, EmailVerification
from app.services.user_service import UserService
from app.core.deps import get_current_active_user, get_database
from app.core.security import jwt_handler
from app.core.config import settings
from app.utils.educational_messages import EducationalMessageSender

logger = logging.getLogger(__name__)

router = APIRouter()


def get_client_ip(request: Request) -> str:
    """Get client IP address from request."""
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    x_real_ip = request.headers.get('X-Real-IP')
    if x_real_ip:
        return x_real_ip
    return request.client.host if request.client else "unknown"


def get_device_info(request: Request) -> str:
    """Get device information from request headers."""
    user_agent = request.headers.get('User-Agent', 'Unknown')
    return user_agent[:500]  # Limit length


@router.post("/register", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: Request,
    user_data: RegisterRequest,
    db: Session = Depends(get_database)
):
    """
    Register a new user account.

    - Creates a new user with the provided information
    - Sends email verification (in production)
    - Auto-login: Returns user data and tokens for immediate authentication
    """
    # Create user schema
    user_create = UserCreate(
        email=user_data.email,
        username=user_data.username,
        password=user_data.password,
        confirm_password=user_data.confirm_password,
        role=user_data.role
    )

    # Create user - let custom exceptions bubble up to global handlers
    user = UserService.create_user(db, user_create)

    # Get client information for token creation
    ip_address = get_client_ip(request)
    device_info = get_device_info(request)

    # Create tokens for auto-login
    access_token = jwt_handler.create_access_token(subject=str(user.id))
    refresh_token_record = UserService.create_refresh_token(
        db=db,
        user=user,
        device_info=device_info,
        ip_address=ip_address,
        remember_me=False  # Default to session-based for registration
    )

    # Create token response
    tokens = Token(
        access_token=access_token,
        refresh_token=refresh_token_record.token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    # Convert to response schema
    user_response = UserResponse.from_orm(user)

    # Send welcome message with educational content
    try:
        EducationalMessageSender.send_welcome_message(db, user.id)
    except Exception as e:
        logger.error(f"Failed to send welcome message to user {user.id}: {e}")
        # Don't fail registration if message sending fails

    logger.info(f"New user registered: {user.email}")

    return LoginResponse(
        user=user_response.dict(),
        tokens=tokens,
        message="Registration successful. Please check your email for verification."
    )


@router.post("/login", response_model=LoginResponse)
async def login(
    request: Request,
    login_data: LoginRequest,
    db: Session = Depends(get_database)
):
    """
    Authenticate user and return tokens.

    - Validates user credentials
    - Creates access and refresh tokens
    - Returns user data and tokens
    """
    try:
        # DEBUG: Log login attempt details
        logger.info(f"Login attempt - Email: {login_data.email}, Password length: {len(login_data.password)}")

        # Authenticate user
        user = UserService.authenticate_user(db, login_data.email, login_data.password)

        if not user:
            # Log failed login attempt
            logger.warning(f"Failed login attempt for email: {login_data.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        # Check if account is locked
        if user.is_account_locked:
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="Account is temporarily locked due to failed login attempts"
            )

        # Get client information
        ip_address = get_client_ip(request)
        device_info = get_device_info(request)

        # Create tokens
        access_token = jwt_handler.create_access_token(subject=str(user.id))
        refresh_token_record = UserService.create_refresh_token(
            db=db,
            user=user,
            device_info=device_info,
            ip_address=ip_address,
            remember_me=login_data.remember_me
        )

        # Create token response
        tokens = Token(
            access_token=access_token,
            refresh_token=refresh_token_record.token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

        # Convert user to response schema
        user_response = UserResponse.from_orm(user)

        logger.info(f"User logged in successfully: {user.email}")

        return LoginResponse(
            user=user_response.dict(),
            tokens=tokens,
            message="Login successful"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/refresh", response_model=AccessToken)
async def refresh_token(
    token_data: TokenRefresh,
    db: Session = Depends(get_database)
):
    """
    Refresh access token using refresh token.

    - Validates refresh token
    - Returns new access token
    """
    try:
        access_token, refresh_token = UserService.refresh_access_token(
            db, token_data.refresh_token
        )

        return AccessToken(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not refresh token"
        )


@router.post("/logout", response_model=LogoutResponse)
async def logout(
    logout_data: LogoutRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Logout user and revoke tokens.

    - Revokes specified refresh token or all tokens
    - Invalidates user session(s)
    """
    try:
        revoked_count = 0

        if logout_data.logout_all_devices:
            # Revoke all refresh tokens for user
            revoked_count = UserService.revoke_all_refresh_tokens(db, current_user.id)
            message = f"Logged out from all devices ({revoked_count} sessions)"
        elif logout_data.refresh_token:
            # Revoke specific refresh token
            success = UserService.revoke_refresh_token(db, logout_data.refresh_token)
            revoked_count = 1 if success else 0
            message = "Logout successful" if success else "Token already revoked"
        else:
            message = "Logout successful"

        logger.info(f"User logged out: {current_user.email} (revoked {revoked_count} tokens)")

        return LogoutResponse(
            message=message,
            revoked_tokens_count=revoked_count
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )


@router.post("/verify-email")
async def verify_email(
    verification_data: EmailVerification,
    db: Session = Depends(get_database)
):
    """
    Verify user email address.

    - Validates verification token
    - Activates user account
    """
    try:
        success = UserService.verify_email(db, verification_data.token)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired verification token"
            )

        return {"message": "Email verified successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Email verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email verification failed"
        )


@router.post("/forgot-password")
async def forgot_password(
    reset_data: PasswordReset,
    db: Session = Depends(get_database)
):
    """
    Initiate password reset process.

    - Generates reset token
    - Sends reset email (in production)
    """
    try:
        reset_token = UserService.initiate_password_reset(db, reset_data.email)

        # Don't reveal whether email exists or not for security
        # TODO: Send password reset email here

        return {
            "message": "If an account with this email exists, a password reset link has been sent."
        }

    except Exception as e:
        logger.error(f"Password reset initiation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not initiate password reset"
        )


@router.post("/reset-password")
async def reset_password(
    reset_data: PasswordResetConfirm,
    db: Session = Depends(get_database)
):
    """
    Reset password using reset token.

    - Validates reset token
    - Updates user password
    - Revokes all existing sessions
    """
    try:
        success = UserService.reset_password(
            db, reset_data.token, reset_data.new_password
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )

        return {"message": "Password reset successful"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password reset error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset failed"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current authenticated user information.

    - Returns user profile data
    - Requires valid access token
    """
    return UserResponse.from_orm(current_user)


@router.get("/sessions", response_model=SessionsResponse)
async def get_user_sessions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Get all active sessions for current user.

    - Returns list of active refresh tokens/sessions
    - Shows device and location information
    """
    try:
        sessions = UserService.get_user_sessions(db, current_user.id)

        active_sessions = []
        for session in sessions:
            active_session = ActiveSession(
                token_id=session.id,
                device_info=session.device_info,
                ip_address=session.ip_address,
                created_at=session.created_at,
                expires_at=session.expires_at,
                is_current=False  # TODO: Determine current session
            )
            active_sessions.append(active_session)

        return SessionsResponse(
            sessions=active_sessions,
            total_sessions=len(active_sessions)
        )

    except Exception as e:
        logger.error(f"Get sessions error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not retrieve sessions"
        )


@router.delete("/sessions/{token_id}")
async def revoke_session(
    token_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Revoke a specific session by token ID.

    - Revokes refresh token
    - Ends session on specified device
    """
    try:
        # Get the refresh token
        token = db.query(RefreshToken).filter(
            RefreshToken.id == token_id,
            RefreshToken.user_id == current_user.id
        ).first()

        if not token:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        # Revoke the token
        token.revoke()
        db.commit()

        return {"message": "Session revoked successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Session revocation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not revoke session"
        )


@router.put("/me", response_model=UserResponse)
async def update_my_settings(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Update current user's settings.

    Allows users to update:
    - Email (will require re-verification)
    - Username
    - Role (lender, borrower, both)

    Only provided fields will be updated.
    """
    try:
        updated_user = UserService.update_user(db, current_user.id, user_update)

        logger.info(f"User settings updated for {current_user.email}")
        if user_update.role:
            logger.info(f"User role changed to {user_update.role} for user {current_user.id}")

        return UserResponse.from_orm(updated_user)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"User settings update error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not update user settings"
        )