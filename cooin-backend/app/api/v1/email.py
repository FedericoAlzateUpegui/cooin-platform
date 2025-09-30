"""
Email verification and management endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import secrets
import logging

from app.db.base import get_db
from app.models import User
from app.core.deps import get_current_active_user, get_database
from app.core.email import get_email_service
from app.core.exceptions import NotFoundError, ValidationError, BusinessLogicError
from app.services.user_service import UserService

logger = logging.getLogger(__name__)

router = APIRouter()


class EmailVerificationRequest(BaseModel):
    """Request to resend verification email."""
    email: EmailStr


class VerifyEmailRequest(BaseModel):
    """Request to verify email with token."""
    token: str


class PasswordResetRequest(BaseModel):
    """Request to reset password."""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Request to confirm password reset."""
    token: str
    new_password: str


@router.post("/send-verification")
async def send_verification_email(
    request: EmailVerificationRequest,
    db: Session = Depends(get_database)
):
    """
    Send or resend email verification email.

    This endpoint can be used to resend verification emails to users
    who haven't verified their email addresses yet.
    """
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        # Don't reveal if email exists for security
        return {"message": "If this email exists, a verification email has been sent."}

    # Check if already verified
    if user.email_verified_at:
        raise BusinessLogicError(
            detail="Email is already verified",
            error_code="EMAIL_ALREADY_VERIFIED"
        )

    # Generate new verification token
    verification_token = secrets.token_urlsafe(32)
    user.verification_token = verification_token
    db.commit()

    # Send verification email
    email_service = get_email_service()
    success = email_service.send_verification_email(
        email=user.email,
        username=user.username,
        verification_token=verification_token
    )

    if not success:
        raise ValidationError(
            detail="Failed to send verification email. Please try again later.",
            error_code="EMAIL_SEND_FAILED"
        )

    logger.info(f"Verification email sent to {user.email}")
    return {"message": "Verification email sent successfully."}


@router.post("/verify")
async def verify_email(
    request: VerifyEmailRequest,
    db: Session = Depends(get_database)
):
    """
    Verify email address using the verification token.

    This endpoint is called when users click the verification link
    in their email.
    """
    user = db.query(User).filter(User.verification_token == request.token).first()
    if not user:
        raise NotFoundError(
            detail="Invalid or expired verification token",
            resource_type="verification_token",
            resource_id=request.token
        )

    # Check if already verified
    if user.email_verified_at:
        raise BusinessLogicError(
            detail="Email is already verified",
            error_code="EMAIL_ALREADY_VERIFIED"
        )

    # Verify email
    user.email_verified_at = datetime.utcnow()
    user.verification_token = None
    user.is_verified = True

    # Update user status if they were pending verification
    if user.status.value == "pending_verification":
        user.status = "active"

    db.commit()

    logger.info(f"Email verified for user {user.email}")
    return {
        "message": "Email verified successfully!",
        "user_id": user.id,
        "email": user.email
    }


@router.post("/request-password-reset")
async def request_password_reset(
    request: PasswordResetRequest,
    db: Session = Depends(get_database)
):
    """
    Request a password reset email.

    Sends a password reset email to the user if the email exists.
    """
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        # Don't reveal if email exists for security
        return {"message": "If this email exists, a password reset email has been sent."}

    # Generate reset token
    reset_token = secrets.token_urlsafe(32)
    user.reset_password_token = reset_token
    user.reset_password_expires = datetime.utcnow() + timedelta(hours=1)
    db.commit()

    # Send password reset email
    email_service = get_email_service()
    success = email_service.send_password_reset_email(
        email=user.email,
        username=user.username,
        reset_token=reset_token
    )

    if not success:
        logger.error(f"Failed to send password reset email to {user.email}")
        # Still return success to avoid revealing email existence
    else:
        logger.info(f"Password reset email sent to {user.email}")

    return {"message": "If this email exists, a password reset email has been sent."}


@router.post("/reset-password")
async def reset_password(
    request: PasswordResetConfirm,
    db: Session = Depends(get_database)
):
    """
    Reset password using the reset token.

    This endpoint is called when users submit the password reset form
    after clicking the reset link in their email.
    """
    user = db.query(User).filter(
        User.reset_password_token == request.token
    ).first()

    if not user:
        raise NotFoundError(
            detail="Invalid or expired reset token",
            resource_type="reset_token",
            resource_id=request.token
        )

    # Check if token is expired
    if user.reset_password_expires and datetime.utcnow() > user.reset_password_expires:
        raise ValidationError(
            detail="Reset token has expired. Please request a new password reset.",
            error_code="TOKEN_EXPIRED"
        )

    # Validate new password
    if len(request.new_password) < 8:
        raise ValidationError(
            detail="Password must be at least 8 characters long",
            error_code="WEAK_PASSWORD"
        )

    # Update password using UserService
    user_service = UserService()
    try:
        # Hash the new password
        hashed_password = user_service._hash_password(request.new_password)
        user.hashed_password = hashed_password

        # Clear reset token
        user.reset_password_token = None
        user.reset_password_expires = None

        # Reset failed login attempts
        user.failed_login_attempts = 0
        user.locked_until = None

        db.commit()

        logger.info(f"Password reset successfully for user {user.email}")
        return {"message": "Password reset successfully!"}

    except Exception as e:
        db.rollback()
        logger.error(f"Error resetting password for user {user.email}: {str(e)}")
        raise ValidationError(
            detail="Failed to reset password. Please try again.",
            error_code="PASSWORD_RESET_FAILED"
        )


@router.get("/verification-status")
async def get_verification_status(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user's email verification status.

    Returns information about whether the current user's email
    is verified and when it was verified.
    """
    return {
        "email": current_user.email,
        "is_verified": current_user.is_verified,
        "email_verified_at": current_user.email_verified_at,
        "needs_verification": not current_user.is_verified
    }


@router.post("/resend-verification")
async def resend_verification_email(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Resend verification email to current authenticated user.

    Allows authenticated users to request a new verification email
    if they haven't received or can't find the original one.
    """
    if current_user.is_verified:
        raise BusinessLogicError(
            detail="Your email is already verified",
            error_code="EMAIL_ALREADY_VERIFIED"
        )

    # Generate new verification token
    verification_token = secrets.token_urlsafe(32)
    current_user.verification_token = verification_token
    db.commit()

    # Send verification email
    email_service = get_email_service()
    success = email_service.send_verification_email(
        email=current_user.email,
        username=current_user.username,
        verification_token=verification_token
    )

    if not success:
        raise ValidationError(
            detail="Failed to send verification email. Please try again later.",
            error_code="EMAIL_SEND_FAILED"
        )

    logger.info(f"Verification email resent to {current_user.email}")
    return {"message": "Verification email sent successfully."}