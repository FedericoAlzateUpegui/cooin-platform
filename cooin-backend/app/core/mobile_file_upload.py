"""
Mobile-optimized file upload service for iOS app integration.
Provides enhanced image processing, compression, and mobile-specific features.
"""

import os
import io
import secrets
import asyncio
from datetime import datetime
from typing import Optional, List, Tuple, Dict, Any
from pathlib import Path
import mimetypes
import hashlib
import logging

from fastapi import HTTPException, UploadFile, status
from PIL import Image, ImageOps, ImageFilter
import pillow_heif  # For HEIF/HEIC support (iOS photos)

from app.core.config import settings
from app.core.exceptions import ValidationError, BusinessLogicError
from app.core.mobile_responses import MobileResponseFormatter

logger = logging.getLogger(__name__)

# Register HEIF opener with Pillow for iOS photo support
pillow_heif.register_heif_opener()


class MobileFileUploadService:
    """Mobile-optimized file upload service with enhanced image processing."""

    # Enhanced mobile file type support
    MOBILE_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.heic', '.heif'}
    DOCUMENT_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt'}

    # Mobile-optimized size limits
    AVATAR_MAX_SIZE = 10 * 1024 * 1024  # 10MB (allowing for high-res mobile photos)
    BANNER_MAX_SIZE = 15 * 1024 * 1024  # 15MB
    DOCUMENT_MAX_SIZE = 50 * 1024 * 1024  # 50MB

    # Target dimensions for mobile optimization
    AVATAR_SIZES = {
        'thumbnail': (150, 150),      # For lists and small displays
        'medium': (300, 300),         # For profile cards
        'large': (600, 600),          # For detail views
        'original': None              # Keep original (up to max)
    }

    BANNER_SIZES = {
        'mobile': (800, 300),         # Mobile banner
        'tablet': (1200, 400),        # Tablet banner
        'desktop': (1600, 500),       # Desktop banner
        'original': None
    }

    # Image quality settings for mobile optimization
    JPEG_QUALITY = 85  # High quality but compressed
    WEBP_QUALITY = 80  # Good quality with better compression

    def __init__(self):
        self.upload_base = Path(settings.UPLOAD_FOLDER)
        self._ensure_directories_exist()

    def _ensure_directories_exist(self):
        """Create necessary upload directories including mobile-specific folders."""
        directories = [
            self.upload_base / "mobile" / "avatars" / "thumbnails",
            self.upload_base / "mobile" / "avatars" / "medium",
            self.upload_base / "mobile" / "avatars" / "large",
            self.upload_base / "mobile" / "avatars" / "original",
            self.upload_base / "mobile" / "banners" / "mobile",
            self.upload_base / "mobile" / "banners" / "tablet",
            self.upload_base / "mobile" / "banners" / "desktop",
            self.upload_base / "mobile" / "banners" / "original",
            self.upload_base / "mobile" / "documents",
            self.upload_base / "mobile" / "temp"
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    async def upload_avatar_mobile(
        self,
        file: UploadFile,
        user_id: int,
        device_info: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Upload and process avatar image optimized for mobile."""

        try:
            # Validate file
            await self._validate_mobile_image(file, "avatar")

            # Generate unique filename
            file_id = secrets.token_urlsafe(16)
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            base_filename = f"user_{user_id}_{timestamp}_{file_id}"

            # Read image data
            image_data = await file.read()
            image = Image.open(io.BytesIO(image_data))

            # Convert HEIC/HEIF to RGB if needed
            if image.format in ['HEIF', 'HEIC']:
                image = image.convert('RGB')

            # Auto-rotate based on EXIF data
            image = ImageOps.exif_transpose(image)

            # Generate multiple sizes for different mobile uses
            avatar_urls = {}
            for size_name, dimensions in self.AVATAR_SIZES.items():
                if dimensions is None:
                    # Keep original but limit max size
                    processed_image = self._resize_image_smart(image, (1000, 1000))
                    filename = f"{base_filename}_original.jpg"
                else:
                    # Create specific size
                    processed_image = self._resize_and_crop_square(image, dimensions)
                    filename = f"{base_filename}_{size_name}.jpg"

                # Save processed image
                file_path = self.upload_base / "mobile" / "avatars" / size_name / filename
                await self._save_image_optimized(processed_image, file_path, "JPEG")

                # Generate URL
                avatar_urls[size_name] = f"/uploads/mobile/avatars/{size_name}/{filename}"

            # Generate metadata
            metadata = {
                "original_filename": file.filename,
                "original_size": len(image_data),
                "original_format": image.format,
                "original_dimensions": image.size,
                "processed_at": datetime.utcnow().isoformat(),
                "device_info": device_info,
                "file_id": file_id
            }

            return {
                "urls": avatar_urls,
                "metadata": metadata,
                "primary_url": avatar_urls["medium"]  # Default for mobile display
            }

        except Exception as e:
            logger.error(f"Error uploading mobile avatar: {e}")
            raise BusinessLogicError(
                detail="Failed to upload avatar image",
                error_code="AVATAR_UPLOAD_FAILED"
            )

    async def upload_banner_mobile(
        self,
        file: UploadFile,
        user_id: int,
        device_info: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Upload and process banner image optimized for mobile."""

        try:
            # Validate file
            await self._validate_mobile_image(file, "banner")

            # Generate unique filename
            file_id = secrets.token_urlsafe(16)
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            base_filename = f"user_{user_id}_{timestamp}_{file_id}"

            # Read and process image
            image_data = await file.read()
            image = Image.open(io.BytesIO(image_data))

            # Convert HEIC/HEIF to RGB if needed
            if image.format in ['HEIF', 'HEIC']:
                image = image.convert('RGB')

            # Auto-rotate based on EXIF data
            image = ImageOps.exif_transpose(image)

            # Generate multiple sizes for different devices
            banner_urls = {}
            for size_name, dimensions in self.BANNER_SIZES.items():
                if dimensions is None:
                    # Keep original but limit max size
                    processed_image = self._resize_image_smart(image, (2000, 800))
                    filename = f"{base_filename}_original.jpg"
                else:
                    # Create specific size maintaining aspect ratio
                    processed_image = self._resize_and_crop_banner(image, dimensions)
                    filename = f"{base_filename}_{size_name}.jpg"

                # Save processed image
                file_path = self.upload_base / "mobile" / "banners" / size_name / filename
                await self._save_image_optimized(processed_image, file_path, "JPEG")

                # Generate URL
                banner_urls[size_name] = f"/uploads/mobile/banners/{size_name}/{filename}"

            # Generate metadata
            metadata = {
                "original_filename": file.filename,
                "original_size": len(image_data),
                "original_format": image.format,
                "original_dimensions": image.size,
                "processed_at": datetime.utcnow().isoformat(),
                "device_info": device_info,
                "file_id": file_id
            }

            return {
                "urls": banner_urls,
                "metadata": metadata,
                "primary_url": banner_urls["mobile"]  # Default for mobile display
            }

        except Exception as e:
            logger.error(f"Error uploading mobile banner: {e}")
            raise BusinessLogicError(
                detail="Failed to upload banner image",
                error_code="BANNER_UPLOAD_FAILED"
            )

    async def upload_document_mobile(
        self,
        file: UploadFile,
        user_id: int,
        document_type: str = "other",
        device_info: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Upload document optimized for mobile access."""

        try:
            # Validate file
            await self._validate_mobile_document(file)

            # Generate unique filename
            file_id = secrets.token_urlsafe(16)
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            extension = Path(file.filename).suffix.lower()
            filename = f"user_{user_id}_{document_type}_{timestamp}_{file_id}{extension}"

            # Save document
            file_path = self.upload_base / "mobile" / "documents" / filename
            content = await file.read()

            with open(file_path, "wb") as f:
                f.write(content)

            # Generate metadata
            metadata = {
                "original_filename": file.filename,
                "file_size": len(content),
                "document_type": document_type,
                "uploaded_at": datetime.utcnow().isoformat(),
                "device_info": device_info,
                "file_id": file_id,
                "mime_type": file.content_type
            }

            return {
                "url": f"/uploads/mobile/documents/{filename}",
                "filename": filename,
                "metadata": metadata
            }

        except Exception as e:
            logger.error(f"Error uploading mobile document: {e}")
            raise BusinessLogicError(
                detail="Failed to upload document",
                error_code="DOCUMENT_UPLOAD_FAILED"
            )

    def _resize_and_crop_square(self, image: Image.Image, dimensions: Tuple[int, int]) -> Image.Image:
        """Resize and crop image to square maintaining face detection if possible."""
        target_size = dimensions[0]  # Square, so width == height

        # Get current dimensions
        width, height = image.size

        # Calculate crop area to get square
        if width > height:
            # Landscape - crop sides
            left = (width - height) // 2
            top = 0
            right = left + height
            bottom = height
        else:
            # Portrait or square - crop top/bottom
            left = 0
            top = (height - width) // 2
            right = width
            bottom = top + width

        # Crop to square
        image = image.crop((left, top, right, bottom))

        # Resize to target size with high-quality resampling
        image = image.resize((target_size, target_size), Image.Resampling.LANCZOS)

        return image

    def _resize_and_crop_banner(self, image: Image.Image, dimensions: Tuple[int, int]) -> Image.Image:
        """Resize and crop image for banner with smart cropping."""
        target_width, target_height = dimensions

        # Calculate current aspect ratio
        width, height = image.size
        current_ratio = width / height
        target_ratio = target_width / target_height

        if current_ratio > target_ratio:
            # Image is wider - crop width
            new_width = int(height * target_ratio)
            left = (width - new_width) // 2
            image = image.crop((left, 0, left + new_width, height))
        else:
            # Image is taller - crop height
            new_height = int(width / target_ratio)
            top = (height - new_height) // 3  # Crop more from bottom (rule of thirds)
            image = image.crop((0, top, width, top + new_height))

        # Resize to target dimensions
        image = image.resize(dimensions, Image.Resampling.LANCZOS)

        return image

    def _resize_image_smart(self, image: Image.Image, max_dimensions: Tuple[int, int]) -> Image.Image:
        """Smart resize maintaining aspect ratio within max dimensions."""
        max_width, max_height = max_dimensions
        width, height = image.size

        # Calculate scaling factor
        scale_w = max_width / width
        scale_h = max_height / height
        scale = min(scale_w, scale_h, 1.0)  # Don't upscale

        if scale < 1.0:
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        return image

    async def _save_image_optimized(self, image: Image.Image, file_path: Path, format: str):
        """Save image with mobile-optimized settings."""
        # Ensure RGB mode for JPEG
        if format == "JPEG" and image.mode in ("RGBA", "P"):
            # Create white background for transparency
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
            image = background

        # Save with optimization
        save_kwargs = {
            "format": format,
            "optimize": True,
            "quality": self.JPEG_QUALITY if format == "JPEG" else self.WEBP_QUALITY
        }

        if format == "JPEG":
            save_kwargs["progressive"] = True  # Progressive JPEG for faster loading

        await asyncio.to_thread(image.save, file_path, **save_kwargs)

    async def _validate_mobile_image(self, file: UploadFile, image_type: str):
        """Enhanced validation for mobile image uploads."""
        if not file.filename:
            raise ValidationError(
                detail="No filename provided",
                error_code="MISSING_FILENAME"
            )

        # Check file extension
        extension = Path(file.filename).suffix.lower()
        if extension not in self.MOBILE_IMAGE_EXTENSIONS:
            raise ValidationError(
                detail=f"Invalid image format. Supported: {', '.join(self.MOBILE_IMAGE_EXTENSIONS)}",
                error_code="INVALID_IMAGE_FORMAT"
            )

        # Check file size
        max_size = self.AVATAR_MAX_SIZE if image_type == "avatar" else self.BANNER_MAX_SIZE
        if file.size and file.size > max_size:
            max_mb = max_size / (1024 * 1024)
            raise ValidationError(
                detail=f"File too large. Maximum size: {max_mb}MB",
                error_code="FILE_TOO_LARGE"
            )

        # Reset file pointer for further processing
        await file.seek(0)

    async def _validate_mobile_document(self, file: UploadFile):
        """Validate document uploads for mobile."""
        if not file.filename:
            raise ValidationError(
                detail="No filename provided",
                error_code="MISSING_FILENAME"
            )

        # Check file extension
        extension = Path(file.filename).suffix.lower()
        if extension not in self.DOCUMENT_EXTENSIONS:
            raise ValidationError(
                detail=f"Invalid document format. Supported: {', '.join(self.DOCUMENT_EXTENSIONS)}",
                error_code="INVALID_DOCUMENT_FORMAT"
            )

        # Check file size
        if file.size and file.size > self.DOCUMENT_MAX_SIZE:
            max_mb = self.DOCUMENT_MAX_SIZE / (1024 * 1024)
            raise ValidationError(
                detail=f"Document too large. Maximum size: {max_mb}MB",
                error_code="DOCUMENT_TOO_LARGE"
            )

        # Reset file pointer
        await file.seek(0)

    async def delete_user_files(self, user_id: int, file_type: str = "all") -> bool:
        """Delete user files (for account deletion or cleanup)."""
        try:
            deleted_count = 0

            if file_type in ["all", "avatar"]:
                # Delete avatar files
                for size_name in self.AVATAR_SIZES.keys():
                    avatar_dir = self.upload_base / "mobile" / "avatars" / size_name
                    if avatar_dir.exists():
                        for file_path in avatar_dir.glob(f"user_{user_id}_*"):
                            file_path.unlink()
                            deleted_count += 1

            if file_type in ["all", "banner"]:
                # Delete banner files
                for size_name in self.BANNER_SIZES.keys():
                    banner_dir = self.upload_base / "mobile" / "banners" / size_name
                    if banner_dir.exists():
                        for file_path in banner_dir.glob(f"user_{user_id}_*"):
                            file_path.unlink()
                            deleted_count += 1

            if file_type in ["all", "document"]:
                # Delete document files
                doc_dir = self.upload_base / "mobile" / "documents"
                if doc_dir.exists():
                    for file_path in doc_dir.glob(f"user_{user_id}_*"):
                        file_path.unlink()
                        deleted_count += 1

            logger.info(f"Deleted {deleted_count} files for user {user_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting user files: {e}")
            return False


# Global mobile file upload service instance
_mobile_file_upload_service: Optional[MobileFileUploadService] = None


def get_mobile_file_upload_service() -> MobileFileUploadService:
    """Get mobile file upload service instance."""
    global _mobile_file_upload_service
    if _mobile_file_upload_service is None:
        _mobile_file_upload_service = MobileFileUploadService()
    return _mobile_file_upload_service