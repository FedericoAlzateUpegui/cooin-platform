"""
Mobile-optimized file upload API endpoints.
Enhanced endpoints specifically designed for iOS app integration.
"""

import logging
from typing import Optional, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status, Request, File, UploadFile, Form
from sqlalchemy.orm import Session

from app.core.deps import get_database
from app.core.mobile_auth import get_current_user_mobile
from app.core.mobile_responses import MobileResponseFormatter, MobileJSONResponse
from app.core.mobile_file_upload import get_mobile_file_upload_service
from app.models import User, UserProfile
from app.services.cache_service import get_app_cache_service

logger = logging.getLogger(__name__)

router = APIRouter()
mobile_upload_service = get_mobile_file_upload_service()
cache_service = get_app_cache_service()


@router.post("/avatar")
async def upload_avatar_mobile(
    request: Request,
    file: UploadFile = File(..., description="Avatar image file (JPEG, PNG, HEIC, WEBP)"),
    current_user: User = Depends(get_current_user_mobile),
    db: Session = Depends(get_database)
):
    """
    Upload profile avatar optimized for mobile devices.

    Automatically generates multiple sizes:
    - thumbnail (150x150) - for lists and small displays
    - medium (300x300) - for profile cards
    - large (600x600) - for detail views
    - original - optimized original (max 1000x1000)

    Supports HEIC/HEIF from iOS cameras with automatic conversion.
    """
    try:
        # Extract device info from headers
        device_info = {
            "device_model": request.headers.get("X-Device-Model"),
            "ios_version": request.headers.get("X-iOS-Version"),
            "app_version": request.headers.get("X-App-Version")
        }

        # Upload and process avatar
        result = await mobile_upload_service.upload_avatar_mobile(
            file=file,
            user_id=current_user.id,
            device_info=device_info
        )

        # Update user profile with new avatar URL
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        if profile:
            profile.avatar_url = result["primary_url"]
            db.commit()

            # Clear profile cache
            await cache_service.invalidate_user_profile_cache(current_user.id)

        return MobileJSONResponse(
            content=MobileResponseFormatter.success(
                data={
                    "avatar_urls": result["urls"],
                    "primary_url": result["primary_url"],
                    "metadata": {
                        "file_id": result["metadata"]["file_id"],
                        "processed_sizes": list(result["urls"].keys()),
                        "original_size": result["metadata"]["original_size"],
                        "compression_ratio": round((1 - sum([
                            len(open(mobile_upload_service.upload_base / "mobile" / "avatars" / size / result["urls"][size].split("/")[-1], "rb").read())
                            for size in result["urls"].keys() if size != "original"
                        ]) / result["metadata"]["original_size"]) * 100, 2)
                    }
                },
                message="Avatar uploaded and processed successfully",
                request=request
            )
        )

    except Exception as e:
        logger.error(f"Error uploading mobile avatar: {e}")
        return MobileJSONResponse(
            content=MobileResponseFormatter.error(
                error_code="AVATAR_UPLOAD_FAILED",
                detail=str(e),
                status_code=500,
                request=request
            ),
            status_code=500
        )


@router.post("/banner")
async def upload_banner_mobile(
    request: Request,
    file: UploadFile = File(..., description="Banner image file (JPEG, PNG, HEIC, WEBP)"),
    current_user: User = Depends(get_current_user_mobile),
    db: Session = Depends(get_database)
):
    """
    Upload profile banner optimized for mobile devices.

    Automatically generates multiple sizes:
    - mobile (800x300) - for mobile displays
    - tablet (1200x400) - for tablet displays
    - desktop (1600x500) - for desktop displays
    - original - optimized original (max 2000x800)

    Smart cropping maintains important content in frame.
    """
    try:
        # Extract device info from headers
        device_info = {
            "device_model": request.headers.get("X-Device-Model"),
            "ios_version": request.headers.get("X-iOS-Version"),
            "app_version": request.headers.get("X-App-Version")
        }

        # Upload and process banner
        result = await mobile_upload_service.upload_banner_mobile(
            file=file,
            user_id=current_user.id,
            device_info=device_info
        )

        # Update user profile with new banner URL
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        if profile:
            profile.banner_url = result["primary_url"]
            db.commit()

            # Clear profile cache
            await cache_service.invalidate_user_profile_cache(current_user.id)

        return MobileJSONResponse(
            content=MobileResponseFormatter.success(
                data={
                    "banner_urls": result["urls"],
                    "primary_url": result["primary_url"],
                    "metadata": {
                        "file_id": result["metadata"]["file_id"],
                        "processed_sizes": list(result["urls"].keys()),
                        "original_size": result["metadata"]["original_size"],
                        "aspect_ratios": {
                            size: f"{mobile_upload_service.BANNER_SIZES[size][0]}x{mobile_upload_service.BANNER_SIZES[size][1]}"
                            for size in result["urls"].keys() if mobile_upload_service.BANNER_SIZES[size] is not None
                        }
                    }
                },
                message="Banner uploaded and processed successfully",
                request=request
            )
        )

    except Exception as e:
        logger.error(f"Error uploading mobile banner: {e}")
        return MobileJSONResponse(
            content=MobileResponseFormatter.error(
                error_code="BANNER_UPLOAD_FAILED",
                detail=str(e),
                status_code=500,
                request=request
            ),
            status_code=500
        )


@router.post("/document")
async def upload_document_mobile(
    request: Request,
    file: UploadFile = File(..., description="Document file (PDF, DOC, DOCX, TXT)"),
    document_type: str = Form("other", description="Document type (verification, loan, other)"),
    current_user: User = Depends(get_current_user_mobile),
    db: Session = Depends(get_database)
):
    """
    Upload document optimized for mobile access.

    Supports common document formats with mobile-friendly handling.
    """
    try:
        # Extract device info from headers
        device_info = {
            "device_model": request.headers.get("X-Device-Model"),
            "ios_version": request.headers.get("X-iOS-Version"),
            "app_version": request.headers.get("X-App-Version")
        }

        # Upload document
        result = await mobile_upload_service.upload_document_mobile(
            file=file,
            user_id=current_user.id,
            document_type=document_type,
            device_info=device_info
        )

        return MobileJSONResponse(
            content=MobileResponseFormatter.success(
                data={
                    "document_url": result["url"],
                    "filename": result["filename"],
                    "metadata": {
                        "file_id": result["metadata"]["file_id"],
                        "document_type": result["metadata"]["document_type"],
                        "file_size": result["metadata"]["file_size"],
                        "mime_type": result["metadata"]["mime_type"],
                        "size_mb": round(result["metadata"]["file_size"] / (1024 * 1024), 2)
                    }
                },
                message="Document uploaded successfully",
                request=request
            )
        )

    except Exception as e:
        logger.error(f"Error uploading mobile document: {e}")
        return MobileJSONResponse(
            content=MobileResponseFormatter.error(
                error_code="DOCUMENT_UPLOAD_FAILED",
                detail=str(e),
                status_code=500,
                request=request
            ),
            status_code=500
        )


@router.get("/image-info/{file_id}")
async def get_image_info(
    request: Request,
    file_id: str,
    current_user: User = Depends(get_current_user_mobile)
):
    """Get detailed information about an uploaded image."""
    try:
        # This is a simplified implementation
        # In a real app, you'd store file metadata in the database

        return MobileJSONResponse(
            content=MobileResponseFormatter.success(
                data={
                    "file_id": file_id,
                    "message": "File info endpoint - implement based on your storage strategy"
                },
                message="Image info retrieved",
                request=request
            )
        )

    except Exception as e:
        logger.error(f"Error getting image info: {e}")
        return MobileJSONResponse(
            content=MobileResponseFormatter.error(
                error_code="IMAGE_INFO_FAILED",
                detail="Failed to retrieve image information",
                status_code=500,
                request=request
            ),
            status_code=500
        )


@router.delete("/files/{file_type}")
async def delete_user_files(
    request: Request,
    file_type: str,
    current_user: User = Depends(get_current_user_mobile),
    db: Session = Depends(get_database)
):
    """
    Delete user files by type.

    Types: avatar, banner, document, all
    """
    try:
        if file_type not in ["avatar", "banner", "document", "all"]:
            return MobileJSONResponse(
                content=MobileResponseFormatter.error(
                    error_code="INVALID_FILE_TYPE",
                    detail="Invalid file type. Use: avatar, banner, document, or all",
                    status_code=400,
                    request=request
                ),
                status_code=400
            )

        # Delete files
        success = await mobile_upload_service.delete_user_files(
            user_id=current_user.id,
            file_type=file_type
        )

        if success:
            # Update profile to remove URLs if avatar/banner deleted
            if file_type in ["avatar", "all"]:
                profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
                if profile:
                    if file_type in ["avatar", "all"]:
                        profile.avatar_url = None
                    if file_type in ["banner", "all"]:
                        profile.banner_url = None
                    db.commit()

                    # Clear profile cache
                    await cache_service.invalidate_user_profile_cache(current_user.id)

            return MobileJSONResponse(
                content=MobileResponseFormatter.success(
                    data={"deleted_type": file_type},
                    message=f"Successfully deleted {file_type} files",
                    request=request
                )
            )
        else:
            return MobileJSONResponse(
                content=MobileResponseFormatter.error(
                    error_code="DELETE_FAILED",
                    detail="Failed to delete files",
                    status_code=500,
                    request=request
                ),
                status_code=500
            )

    except Exception as e:
        logger.error(f"Error deleting user files: {e}")
        return MobileJSONResponse(
            content=MobileResponseFormatter.error(
                error_code="DELETE_FILES_FAILED",
                detail="Failed to delete files",
                status_code=500,
                request=request
            ),
            status_code=500
        )


@router.get("/upload-limits")
async def get_upload_limits(
    request: Request,
    current_user: User = Depends(get_current_user_mobile)
):
    """Get upload limits and supported formats for mobile app."""

    return MobileJSONResponse(
        content=MobileResponseFormatter.success(
            data={
                "limits": {
                    "avatar_max_size_mb": mobile_upload_service.AVATAR_MAX_SIZE / (1024 * 1024),
                    "banner_max_size_mb": mobile_upload_service.BANNER_MAX_SIZE / (1024 * 1024),
                    "document_max_size_mb": mobile_upload_service.DOCUMENT_MAX_SIZE / (1024 * 1024)
                },
                "supported_formats": {
                    "images": list(mobile_upload_service.MOBILE_IMAGE_EXTENSIONS),
                    "documents": list(mobile_upload_service.DOCUMENT_EXTENSIONS)
                },
                "generated_sizes": {
                    "avatar": list(mobile_upload_service.AVATAR_SIZES.keys()),
                    "banner": list(mobile_upload_service.BANNER_SIZES.keys())
                },
                "features": [
                    "HEIC/HEIF support (iOS photos)",
                    "Automatic image optimization",
                    "Multiple size generation",
                    "Smart cropping",
                    "EXIF rotation correction",
                    "Progressive JPEG encoding"
                ]
            },
            message="Upload limits and capabilities",
            request=request
        )
    )