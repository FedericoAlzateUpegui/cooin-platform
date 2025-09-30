"""
File upload service with comprehensive security and validation.
Handles profile pictures, documents, and various file types with proper validation.
"""

import os
import secrets
import shutil
from datetime import datetime
from typing import Optional, List, Tuple, BinaryIO
from pathlib import Path
import mimetypes
import hashlib

from fastapi import HTTPException, UploadFile, status
from PIL import Image, ImageOps
import logging

from app.core.config import settings
from app.core.exceptions import ValidationError, BusinessLogicError

logger = logging.getLogger(__name__)


class FileType:
    """File type categories for upload validation."""
    PROFILE_AVATAR = "profile_avatar"
    PROFILE_BANNER = "profile_banner"
    VERIFICATION_DOCUMENT = "verification_document"
    LOAN_DOCUMENT = "loan_document"
    OTHER_DOCUMENT = "other_document"


class FileUploadService:
    """Service for handling file uploads with security and validation."""

    # File type configurations
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    DOCUMENT_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt'}

    AVATAR_MAX_SIZE = 5 * 1024 * 1024  # 5MB
    BANNER_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    DOCUMENT_MAX_SIZE = 25 * 1024 * 1024  # 25MB

    AVATAR_DIMENSIONS = (400, 400)  # Square avatar
    BANNER_DIMENSIONS = (1200, 400)  # Banner aspect ratio

    def __init__(self):
        self.upload_base = Path(settings.UPLOAD_FOLDER)
        self._ensure_directories_exist()

    def _ensure_directories_exist(self):
        """Create necessary upload directories."""
        directories = [
            self.upload_base / "profiles" / "avatars",
            self.upload_base / "profiles" / "banners",
            self.upload_base / "documents" / "verification",
            self.upload_base / "documents" / "loans",
            self.upload_base / "documents" / "temp"
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            # Create .gitkeep files to ensure directories are tracked
            gitkeep = directory / ".gitkeep"
            if not gitkeep.exists():
                gitkeep.touch()

    def _validate_file_basic(self, file: UploadFile) -> None:
        """Basic file validation."""
        if not file.filename:
            raise ValidationError(
                detail="No filename provided",
                error_code="MISSING_FILENAME"
            )

        if file.size == 0:
            raise ValidationError(
                detail="File is empty",
                error_code="EMPTY_FILE"
            )

    def _get_file_extension(self, filename: str) -> str:
        """Get file extension in lowercase."""
        return Path(filename).suffix.lower()

    def _validate_file_type(self, file: UploadFile, file_type: str) -> None:
        """Validate file type and size based on upload category."""
        extension = self._get_file_extension(file.filename)

        # Validate file extension
        if file_type in [FileType.PROFILE_AVATAR, FileType.PROFILE_BANNER]:
            if extension not in self.IMAGE_EXTENSIONS:
                raise ValidationError(
                    detail=f"Invalid image format. Allowed: {', '.join(self.IMAGE_EXTENSIONS)}",
                    error_code="INVALID_IMAGE_FORMAT"
                )
        elif "document" in file_type:
            if extension not in self.DOCUMENT_EXTENSIONS:
                raise ValidationError(
                    detail=f"Invalid document format. Allowed: {', '.join(self.DOCUMENT_EXTENSIONS)}",
                    error_code="INVALID_DOCUMENT_FORMAT"
                )

        # Validate file size
        max_size = self._get_max_size(file_type)
        if file.size > max_size:
            max_mb = max_size / (1024 * 1024)
            raise ValidationError(
                detail=f"File too large. Maximum size: {max_mb:.1f}MB",
                error_code="FILE_TOO_LARGE"
            )

    def _get_max_size(self, file_type: str) -> int:
        """Get maximum file size for file type."""
        size_mapping = {
            FileType.PROFILE_AVATAR: self.AVATAR_MAX_SIZE,
            FileType.PROFILE_BANNER: self.BANNER_MAX_SIZE,
            FileType.VERIFICATION_DOCUMENT: self.DOCUMENT_MAX_SIZE,
            FileType.LOAN_DOCUMENT: self.DOCUMENT_MAX_SIZE,
            FileType.OTHER_DOCUMENT: self.DOCUMENT_MAX_SIZE,
        }
        return size_mapping.get(file_type, self.DOCUMENT_MAX_SIZE)

    def _validate_image_content(self, file_path: Path) -> None:
        """Validate image file content using PIL."""
        try:
            with Image.open(file_path) as img:
                # Verify it's a valid image
                img.verify()

            # Re-open for further processing (verify closes the file)
            with Image.open(file_path) as img:
                # Check image dimensions (reasonable limits)
                if img.width > 5000 or img.height > 5000:
                    raise ValidationError(
                        detail="Image dimensions too large (max: 5000x5000)",
                        error_code="IMAGE_TOO_LARGE"
                    )

                if img.width < 50 or img.height < 50:
                    raise ValidationError(
                        detail="Image dimensions too small (min: 50x50)",
                        error_code="IMAGE_TOO_SMALL"
                    )

        except Exception as e:
            logger.error(f"Image validation failed: {e}")
            raise ValidationError(
                detail="Invalid or corrupted image file",
                error_code="CORRUPTED_IMAGE"
            )

    def _generate_unique_filename(self, original_filename: str, user_id: int) -> str:
        """Generate unique filename with user ID and timestamp."""
        extension = self._get_file_extension(original_filename)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        unique_id = secrets.token_hex(8)
        return f"user_{user_id}_{timestamp}_{unique_id}{extension}"

    def _get_file_path(self, file_type: str, filename: str) -> Path:
        """Get the full file path for a given file type."""
        path_mapping = {
            FileType.PROFILE_AVATAR: self.upload_base / "profiles" / "avatars" / filename,
            FileType.PROFILE_BANNER: self.upload_base / "profiles" / "banners" / filename,
            FileType.VERIFICATION_DOCUMENT: self.upload_base / "documents" / "verification" / filename,
            FileType.LOAN_DOCUMENT: self.upload_base / "documents" / "loans" / filename,
            FileType.OTHER_DOCUMENT: self.upload_base / "documents" / "temp" / filename,
        }
        return path_mapping.get(file_type, self.upload_base / "documents" / "temp" / filename)

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file for integrity checking."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    async def _save_uploaded_file(self, file: UploadFile, file_path: Path) -> None:
        """Save uploaded file to disk."""
        try:
            with open(file_path, "wb") as buffer:
                # Read file in chunks to handle large files efficiently
                while chunk := await file.read(8192):
                    buffer.write(chunk)
        except Exception as e:
            logger.error(f"Error saving file {file_path}: {e}")
            # Clean up partial file if it exists
            if file_path.exists():
                file_path.unlink()
            raise ValidationError(
                detail="Failed to save file",
                error_code="FILE_SAVE_ERROR"
            )

    def _process_profile_image(self, file_path: Path, file_type: str) -> None:
        """Process and optimize profile images."""
        try:
            with Image.open(file_path) as img:
                # Convert to RGB if necessary (for JPEG output)
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')

                # Apply orientation from EXIF data
                img = ImageOps.exif_transpose(img)

                # Resize based on type
                if file_type == FileType.PROFILE_AVATAR:
                    # Create square thumbnail for avatar
                    img.thumbnail(self.AVATAR_DIMENSIONS, Image.Resampling.LANCZOS)
                    # Center crop to square
                    width, height = img.size
                    if width != height:
                        size = min(width, height)
                        left = (width - size) // 2
                        top = (height - size) // 2
                        img = img.crop((left, top, left + size, top + size))
                        img = img.resize(self.AVATAR_DIMENSIONS, Image.Resampling.LANCZOS)

                elif file_type == FileType.PROFILE_BANNER:
                    # Resize banner maintaining aspect ratio
                    img.thumbnail(self.BANNER_DIMENSIONS, Image.Resampling.LANCZOS)

                # Save optimized image as JPEG with good quality
                img.save(file_path, 'JPEG', quality=85, optimize=True)

        except Exception as e:
            logger.error(f"Error processing image {file_path}: {e}")
            raise ValidationError(
                detail="Failed to process image",
                error_code="IMAGE_PROCESSING_ERROR"
            )

    async def upload_file(
        self,
        file: UploadFile,
        file_type: str,
        user_id: int,
        replace_existing: bool = True
    ) -> Tuple[str, str, int]:
        """
        Upload and process a file.

        Returns: (filename, file_path, file_size)
        """
        try:
            # Basic validations
            self._validate_file_basic(file)
            self._validate_file_type(file, file_type)

            # Generate unique filename
            unique_filename = self._generate_unique_filename(file.filename, user_id)
            file_path = self._get_file_path(file_type, unique_filename)

            # Save file
            await self._save_uploaded_file(file, file_path)

            # Validate image content if it's an image
            if file_type in [FileType.PROFILE_AVATAR, FileType.PROFILE_BANNER]:
                self._validate_image_content(file_path)
                self._process_profile_image(file_path, file_type)

            # Calculate final file size (after processing)
            final_size = file_path.stat().st_size

            # Calculate file hash for integrity
            file_hash = self._calculate_file_hash(file_path)

            logger.info(f"File uploaded successfully: {unique_filename} (size: {final_size}, hash: {file_hash[:8]}...)")

            # Return relative path from uploads folder
            relative_path = str(file_path.relative_to(self.upload_base))
            return unique_filename, relative_path, final_size

        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error during file upload: {e}")
            raise ValidationError(
                detail="File upload failed",
                error_code="UPLOAD_FAILED"
            )

    def delete_file(self, file_path: str) -> bool:
        """Delete a file from the uploads directory."""
        try:
            full_path = self.upload_base / file_path
            if full_path.exists() and full_path.is_file():
                full_path.unlink()
                logger.info(f"File deleted: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            return False

    def get_file_info(self, file_path: str) -> Optional[dict]:
        """Get information about an uploaded file."""
        try:
            full_path = self.upload_base / file_path
            if not full_path.exists():
                return None

            stat = full_path.stat()
            return {
                "filename": full_path.name,
                "file_path": file_path,
                "size": stat.st_size,
                "created_at": datetime.fromtimestamp(stat.st_ctime),
                "modified_at": datetime.fromtimestamp(stat.st_mtime),
                "mime_type": mimetypes.guess_type(str(full_path))[0]
            }
        except Exception as e:
            logger.error(f"Error getting file info for {file_path}: {e}")
            return None

    def get_file_url(self, file_path: Optional[str]) -> Optional[str]:
        """Get public URL for a file."""
        if not file_path:
            return None
        # In production, this would return a proper URL (e.g., CDN URL)
        # For development, return a relative URL that the API can serve
        return f"/uploads/{file_path}"

    def cleanup_temp_files(self, older_than_hours: int = 24) -> int:
        """Clean up temporary files older than specified hours."""
        try:
            temp_dir = self.upload_base / "documents" / "temp"
            if not temp_dir.exists():
                return 0

            cutoff_time = datetime.utcnow().timestamp() - (older_than_hours * 3600)
            cleaned_count = 0

            for file_path in temp_dir.iterdir():
                if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                    try:
                        file_path.unlink()
                        cleaned_count += 1
                    except Exception as e:
                        logger.error(f"Error deleting temp file {file_path}: {e}")

            logger.info(f"Cleaned up {cleaned_count} temporary files")
            return cleaned_count

        except Exception as e:
            logger.error(f"Error during temp file cleanup: {e}")
            return 0


# Global service instance
_file_upload_service: Optional[FileUploadService] = None


def get_file_upload_service() -> FileUploadService:
    """Get file upload service instance."""
    global _file_upload_service
    if _file_upload_service is None:
        _file_upload_service = FileUploadService()
    return _file_upload_service