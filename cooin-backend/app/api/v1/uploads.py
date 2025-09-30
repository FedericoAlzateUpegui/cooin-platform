"""
File upload endpoints for profile pictures and documents.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Form, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional, List
import logging
import os

from app.db.base import get_database
from app.models import User, UserProfile
from app.core.deps import get_current_active_user
from app.core.file_upload import get_file_upload_service, FileType
from app.core.exceptions import ValidationError, NotFoundError, BusinessLogicError
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/profile/avatar")
async def upload_profile_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Upload a profile avatar image.

    Accepts image files (jpg, png, gif, webp) up to 5MB.
    Automatically resizes to 400x400px square format.
    """
    file_service = get_file_upload_service()

    try:
        # Upload and process the file
        filename, file_path, file_size = await file_service.upload_file(
            file=file,
            file_type=FileType.PROFILE_AVATAR,
            user_id=current_user.id
        )

        # Update user profile with new avatar URL
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        if not profile:
            # Create profile if it doesn't exist
            profile = UserProfile(user_id=current_user.id)
            db.add(profile)

        # Delete old avatar file if it exists
        if profile.avatar_url:
            old_file_path = profile.avatar_url.replace("/uploads/", "")
            file_service.delete_file(old_file_path)

        # Update profile with new avatar URL
        profile.avatar_url = file_service.get_file_url(file_path)
        profile.update_last_profile_update()

        db.commit()
        db.refresh(profile)

        logger.info(f"Profile avatar updated for user {current_user.id}: {filename}")

        return {
            "message": "Avatar uploaded successfully",
            "filename": filename,
            "url": profile.avatar_url,
            "file_size": file_size
        }

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.detail
        )
    except Exception as e:
        logger.error(f"Error uploading avatar for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload avatar"
        )


@router.post("/profile/banner")
async def upload_profile_banner(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Upload a profile banner image.

    Accepts image files (jpg, png, gif, webp) up to 10MB.
    Automatically resizes to 1200x400px banner format.
    """
    file_service = get_file_upload_service()

    try:
        # Upload and process the file
        filename, file_path, file_size = await file_service.upload_file(
            file=file,
            file_type=FileType.PROFILE_BANNER,
            user_id=current_user.id
        )

        # Update user profile with new banner URL
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        if not profile:
            # Create profile if it doesn't exist
            profile = UserProfile(user_id=current_user.id)
            db.add(profile)

        # Delete old banner file if it exists
        if profile.banner_url:
            old_file_path = profile.banner_url.replace("/uploads/", "")
            file_service.delete_file(old_file_path)

        # Update profile with new banner URL
        profile.banner_url = file_service.get_file_url(file_path)
        profile.update_last_profile_update()

        db.commit()
        db.refresh(profile)

        logger.info(f"Profile banner updated for user {current_user.id}: {filename}")

        return {
            "message": "Banner uploaded successfully",
            "filename": filename,
            "url": profile.banner_url,
            "file_size": file_size
        }

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.detail
        )
    except Exception as e:
        logger.error(f"Error uploading banner for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload banner"
        )


@router.delete("/profile/avatar")
async def delete_profile_avatar(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Remove the current user's profile avatar."""
    file_service = get_file_upload_service()

    try:
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        if not profile or not profile.avatar_url:
            raise NotFoundError(
                detail="No avatar found to delete",
                resource_type="avatar",
                resource_id=str(current_user.id)
            )

        # Delete the file
        old_file_path = profile.avatar_url.replace("/uploads/", "")
        file_deleted = file_service.delete_file(old_file_path)

        # Update profile
        profile.avatar_url = None
        profile.update_last_profile_update()

        db.commit()

        logger.info(f"Profile avatar deleted for user {current_user.id}")

        return {
            "message": "Avatar deleted successfully",
            "file_deleted": file_deleted
        }

    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error deleting avatar for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete avatar"
        )


@router.delete("/profile/banner")
async def delete_profile_banner(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Remove the current user's profile banner."""
    file_service = get_file_upload_service()

    try:
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        if not profile or not profile.banner_url:
            raise NotFoundError(
                detail="No banner found to delete",
                resource_type="banner",
                resource_id=str(current_user.id)
            )

        # Delete the file
        old_file_path = profile.banner_url.replace("/uploads/", "")
        file_deleted = file_service.delete_file(old_file_path)

        # Update profile
        profile.banner_url = None
        profile.update_last_profile_update()

        db.commit()

        logger.info(f"Profile banner deleted for user {current_user.id}")

        return {
            "message": "Banner deleted successfully",
            "file_deleted": file_deleted
        }

    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error deleting banner for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete banner"
        )


@router.post("/documents/verification")
async def upload_verification_document(
    file: UploadFile = File(...),
    document_type: str = Form(..., description="Type of verification document"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Upload a verification document (ID, income proof, etc.).

    Accepts document files (pdf, doc, docx) up to 25MB.
    """
    file_service = get_file_upload_service()

    try:
        # Upload the file
        filename, file_path, file_size = await file_service.upload_file(
            file=file,
            file_type=FileType.VERIFICATION_DOCUMENT,
            user_id=current_user.id
        )

        # In a real application, you might want to store document metadata
        # in a separate DocumentUpload model with verification status, etc.

        logger.info(f"Verification document uploaded for user {current_user.id}: {filename} (type: {document_type})")

        return {
            "message": "Verification document uploaded successfully",
            "filename": filename,
            "document_type": document_type,
            "file_size": file_size,
            "upload_id": filename  # Could be used to track the document
        }

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.detail
        )
    except Exception as e:
        logger.error(f"Error uploading verification document for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload verification document"
        )


@router.post("/documents/loan")
async def upload_loan_document(
    file: UploadFile = File(...),
    document_type: str = Form(..., description="Type of loan document"),
    loan_id: Optional[int] = Form(None, description="Associated loan ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Upload a loan-related document.

    Accepts document files (pdf, doc, docx) up to 25MB.
    """
    file_service = get_file_upload_service()

    try:
        # Upload the file
        filename, file_path, file_size = await file_service.upload_file(
            file=file,
            file_type=FileType.LOAN_DOCUMENT,
            user_id=current_user.id
        )

        logger.info(f"Loan document uploaded for user {current_user.id}: {filename} (type: {document_type}, loan_id: {loan_id})")

        return {
            "message": "Loan document uploaded successfully",
            "filename": filename,
            "document_type": document_type,
            "loan_id": loan_id,
            "file_size": file_size,
            "upload_id": filename
        }

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.detail
        )
    except Exception as e:
        logger.error(f"Error uploading loan document for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload loan document"
        )


@router.get("/info/{file_path:path}")
async def get_file_info(
    file_path: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get information about an uploaded file."""
    file_service = get_file_upload_service()

    try:
        # Basic security: ensure user can only access their own files
        if not file_path.startswith(f"profiles/") and not file_path.startswith(f"documents/"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )

        # Check if file contains user ID (basic ownership check)
        if f"user_{current_user.id}_" not in file_path:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )

        file_info = file_service.get_file_info(file_path)
        if not file_info:
            raise NotFoundError(
                detail="File not found",
                resource_type="file",
                resource_id=file_path
            )

        return file_info

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting file info for {file_path}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get file information"
        )


@router.get("/{file_path:path}")
async def serve_file(file_path: str):
    """
    Serve uploaded files.

    In production, this should be handled by a web server (nginx, Apache)
    or a CDN for better performance and security.
    """
    file_service = get_file_upload_service()

    try:
        # Basic security checks
        if ".." in file_path or file_path.startswith("/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file path"
            )

        full_file_path = file_service.upload_base / file_path

        if not full_file_path.exists() or not full_file_path.is_file():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )

        # Determine media type
        import mimetypes
        media_type = mimetypes.guess_type(str(full_file_path))[0]

        return FileResponse(
            path=str(full_file_path),
            media_type=media_type,
            filename=full_file_path.name
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving file {file_path}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to serve file"
        )


@router.post("/cleanup/temp")
async def cleanup_temp_files(
    current_user: User = Depends(get_current_active_user)
):
    """
    Clean up temporary files older than 24 hours.

    This is an admin function that could be called by a scheduled task.
    """
    # In a real application, you might want to restrict this to admin users
    file_service = get_file_upload_service()

    try:
        cleaned_count = file_service.cleanup_temp_files(older_than_hours=24)

        logger.info(f"Temp file cleanup completed. Cleaned {cleaned_count} files.")

        return {
            "message": f"Cleanup completed. Removed {cleaned_count} temporary files.",
            "cleaned_count": cleaned_count
        }

    except Exception as e:
        logger.error(f"Error during temp file cleanup: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cleanup temporary files"
        )