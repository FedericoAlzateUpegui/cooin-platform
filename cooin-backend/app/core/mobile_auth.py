"""
Mobile-specific authentication enhancements for iOS app.
Provides secure token handling and device-specific features.
"""

import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple, List
import logging

from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.security import jwt_handler
from app.core.cache import get_cache_service
from app.models import User
from app.db.base import get_database

logger = logging.getLogger(__name__)

# Enhanced security scheme for mobile
mobile_bearer = HTTPBearer(auto_error=False)


class MobileAuthService:
    """Enhanced authentication service for mobile applications."""

    def __init__(self):
        self.cache = get_cache_service()

    async def create_device_session(
        self,
        user_id: int,
        device_id: str,
        device_info: Dict[str, Any],
        ip_address: str
    ) -> str:
        """Create a device-specific session for enhanced security."""

        # Generate device session ID
        device_session_id = secrets.token_urlsafe(32)

        # Create device fingerprint
        device_fingerprint = self._create_device_fingerprint(device_info)

        # Store device session
        session_data = {
            "user_id": user_id,
            "device_id": device_id,
            "device_fingerprint": device_fingerprint,
            "device_info": device_info,
            "ip_address": ip_address,
            "created_at": datetime.utcnow().isoformat(),
            "last_activity": datetime.utcnow().isoformat(),
            "is_active": True
        }

        # Store for 30 days
        await self.cache.set(
            f"device_session:{device_session_id}",
            session_data,
            86400 * 30
        )

        # Also maintain user-to-sessions mapping
        user_sessions_key = f"user_sessions:{user_id}"
        user_sessions = await self.cache.get(user_sessions_key) or []
        user_sessions.append(device_session_id)
        await self.cache.set(user_sessions_key, user_sessions, 86400 * 30)

        logger.info(f"Created device session for user {user_id}, device {device_id[:8]}...")
        return device_session_id

    async def validate_device_session(
        self,
        device_session_id: str,
        device_info: Dict[str, Any],
        ip_address: str
    ) -> Tuple[bool, Optional[Dict]]:
        """Validate device session and check for suspicious activity."""

        session_data = await self.cache.get(f"device_session:{device_session_id}")
        if not session_data:
            return False, None

        # Check if session is active
        if not session_data.get("is_active"):
            return False, None

        # Verify device fingerprint
        current_fingerprint = self._create_device_fingerprint(device_info)
        stored_fingerprint = session_data.get("device_fingerprint")

        if current_fingerprint != stored_fingerprint:
            logger.warning(f"Device fingerprint mismatch for session {device_session_id[:8]}...")
            # Don't immediately reject - device info can change with OS updates
            # Instead, log for security monitoring

        # Check for suspicious IP changes
        stored_ip = session_data.get("ip_address")
        if ip_address != stored_ip:
            # Log IP change for security monitoring
            logger.info(f"IP address changed for session {device_session_id[:8]}... ({stored_ip} -> {ip_address})")
            session_data["ip_address"] = ip_address
            session_data["ip_changed_at"] = datetime.utcnow().isoformat()

        # Update last activity
        session_data["last_activity"] = datetime.utcnow().isoformat()
        await self.cache.set(
            f"device_session:{device_session_id}",
            session_data,
            86400 * 30
        )

        return True, session_data

    async def revoke_device_session(self, device_session_id: str, user_id: Optional[int] = None):
        """Revoke a device session."""
        session_data = await self.cache.get(f"device_session:{device_session_id}")
        if session_data:
            # Mark as inactive
            session_data["is_active"] = False
            session_data["revoked_at"] = datetime.utcnow().isoformat()
            await self.cache.set(f"device_session:{device_session_id}", session_data, 86400)

            # Remove from user sessions
            if user_id:
                user_sessions_key = f"user_sessions:{user_id}"
                user_sessions = await self.cache.get(user_sessions_key) or []
                if device_session_id in user_sessions:
                    user_sessions.remove(device_session_id)
                    await self.cache.set(user_sessions_key, user_sessions, 86400 * 30)

            logger.info(f"Revoked device session {device_session_id[:8]}...")

    async def get_user_device_sessions(self, user_id: int) -> List[Dict]:
        """Get all active device sessions for a user."""
        user_sessions_key = f"user_sessions:{user_id}"
        session_ids = await self.cache.get(user_sessions_key) or []

        sessions = []
        for session_id in session_ids:
            session_data = await self.cache.get(f"device_session:{session_id}")
            if session_data and session_data.get("is_active"):
                # Sanitize sensitive data
                safe_session = {
                    "session_id": session_id,
                    "device_info": {
                        "device_model": session_data.get("device_info", {}).get("device_model"),
                        "ios_version": session_data.get("device_info", {}).get("ios_version"),
                        "app_version": session_data.get("device_info", {}).get("app_version")
                    },
                    "created_at": session_data.get("created_at"),
                    "last_activity": session_data.get("last_activity"),
                    "ip_address": session_data.get("ip_address", "").replace(".", ".*")  # Mask IP
                }
                sessions.append(safe_session)

        return sessions

    def _create_device_fingerprint(self, device_info: Dict[str, Any]) -> str:
        """Create a device fingerprint for security validation."""
        fingerprint_data = "|".join([
            str(device_info.get("device_model", "")),
            str(device_info.get("ios_version", "")),
            str(device_info.get("app_version", "")),
            str(device_info.get("device_id", ""))
        ])

        return hashlib.sha256(fingerprint_data.encode()).hexdigest()

    async def create_enhanced_tokens(
        self,
        user: User,
        device_session_id: str,
        include_refresh: bool = True
    ) -> Dict[str, Any]:
        """Create enhanced JWT tokens with device session binding."""

        # Enhanced payload with device binding
        access_payload = {
            "user_id": user.id,
            "username": user.username,
            "role": user.role.value if hasattr(user.role, 'value') else user.role,
            "device_session_id": device_session_id,
            "token_type": "access"
        }

        access_token = jwt_handler.create_access_token(access_payload)

        tokens = {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": jwt_handler.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "device_session_id": device_session_id
        }

        if include_refresh:
            refresh_payload = {
                "user_id": user.id,
                "device_session_id": device_session_id,
                "token_type": "refresh"
            }
            refresh_token = jwt_handler.create_refresh_token(refresh_payload)
            tokens["refresh_token"] = refresh_token
            tokens["refresh_expires_in"] = jwt_handler.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600

        return tokens

    async def validate_and_refresh_token(
        self,
        refresh_token: str,
        device_info: Dict[str, Any],
        ip_address: str
    ) -> Tuple[bool, Optional[Dict]]:
        """Validate refresh token and create new access token."""

        try:
            # Decode refresh token
            payload = jwt_handler.decode_refresh_token(refresh_token)
            user_id = payload.get("user_id")
            device_session_id = payload.get("device_session_id")

            if not user_id or not device_session_id:
                return False, None

            # Validate device session
            session_valid, session_data = await self.validate_device_session(
                device_session_id, device_info, ip_address
            )

            if not session_valid:
                return False, None

            return True, {
                "user_id": user_id,
                "device_session_id": device_session_id
            }

        except JWTError as e:
            logger.warning(f"Invalid refresh token: {e}")
            return False, None


# Global mobile auth service instance
_mobile_auth_service: Optional[MobileAuthService] = None


def get_mobile_auth_service() -> MobileAuthService:
    """Get mobile authentication service instance."""
    global _mobile_auth_service
    if _mobile_auth_service is None:
        _mobile_auth_service = MobileAuthService()
    return _mobile_auth_service


# Enhanced dependency for mobile authentication
async def get_current_user_mobile(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(mobile_bearer),
    db: Session = Depends(get_database)
) -> User:
    """Get current user with mobile-specific validation."""

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        # Decode JWT token
        payload = jwt_handler.decode_access_token(credentials.credentials)
        user_id = payload.get("user_id")
        device_session_id = payload.get("device_session_id")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        # Get user from database
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is disabled"
            )

        # Enhanced validation with device session
        if device_session_id:
            mobile_auth = get_mobile_auth_service()
            device_info = {
                "device_model": request.headers.get("X-Device-Model"),
                "ios_version": request.headers.get("X-iOS-Version"),
                "app_version": request.headers.get("X-App-Version"),
                "device_id": request.headers.get("X-Device-ID")
            }

            ip_address = request.client.host if request.client else "unknown"

            session_valid, _ = await mobile_auth.validate_device_session(
                device_session_id, device_info, ip_address
            )

            if not session_valid:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid device session"
                )

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )


# WebSocket authentication (simplified version)
def get_current_user_websocket(token: str, db: Session = Depends(get_database)) -> Optional[User]:
    """Get current user for WebSocket connections."""
    try:
        payload = jwt_handler.decode_access_token(token)
        user_id = payload.get("user_id")

        if user_id:
            return db.query(User).filter(User.id == user_id).first()
    except JWTError:
        pass

    return None