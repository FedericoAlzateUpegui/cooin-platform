"""
Push notification service for iOS app integration.
Handles APNs (Apple Push Notification Service) integration.
"""

import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

try:
    from aioapns import APNs, NotificationRequest, PushType
    APNS_AVAILABLE = True
except ImportError:
    APNS_AVAILABLE = False
    logging.warning("aioapns not installed. Push notifications disabled.")

from app.core.config import settings
from app.core.cache import get_cache_service

logger = logging.getLogger(__name__)


class PushNotificationService:
    """Service for managing iOS push notifications."""

    def __init__(self):
        self.cache = get_cache_service()
        self.apns = None
        self._initialize_apns()

    def _initialize_apns(self):
        """Initialize Apple Push Notification Service."""
        if not APNS_AVAILABLE:
            logger.warning("APNs not available - push notifications disabled")
            return

        if settings.APNS_KEY_ID and settings.APNS_TEAM_ID:
            try:
                self.apns = APNs(
                    key_id=settings.APNS_KEY_ID,
                    team_id=settings.APNS_TEAM_ID,
                    bundle_id=settings.APNS_BUNDLE_ID,
                    use_sandbox=settings.DEBUG,  # Use sandbox in development
                    key_path=settings.APNS_KEY_PATH if hasattr(settings, 'APNS_KEY_PATH') else None
                )
                logger.info("APNs initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize APNs: {e}")
                self.apns = None
        else:
            logger.warning("APNs credentials not configured")

    async def register_device_token(self, user_id: int, device_token: str, device_info: Optional[Dict] = None):
        """Register iOS device token for push notifications."""
        try:
            device_data = {
                "token": device_token,
                "user_id": user_id,
                "platform": "ios",
                "registered_at": datetime.utcnow().isoformat(),
                "active": True
            }

            if device_info:
                device_data.update({
                    "device_model": device_info.get("device_model"),
                    "ios_version": device_info.get("ios_version"),
                    "app_version": device_info.get("app_version")
                })

            # Store device token in cache and database
            cache_key = f"device_token:ios:{user_id}:{device_token}"
            await self.cache.set(cache_key, device_data, 86400 * 30)  # 30 days

            # Also maintain a user-to-tokens mapping
            user_tokens_key = f"user_tokens:ios:{user_id}"
            user_tokens = await self.cache.get(user_tokens_key) or []
            if device_token not in user_tokens:
                user_tokens.append(device_token)
                await self.cache.set(user_tokens_key, user_tokens, 86400 * 30)

            logger.info(f"Device token registered for user {user_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to register device token: {e}")
            return False

    async def unregister_device_token(self, user_id: int, device_token: str):
        """Unregister iOS device token."""
        try:
            # Remove from cache
            cache_key = f"device_token:ios:{user_id}:{device_token}"
            await self.cache.delete(cache_key)

            # Remove from user tokens list
            user_tokens_key = f"user_tokens:ios:{user_id}"
            user_tokens = await self.cache.get(user_tokens_key) or []
            if device_token in user_tokens:
                user_tokens.remove(device_token)
                await self.cache.set(user_tokens_key, user_tokens, 86400 * 30)

            logger.info(f"Device token unregistered for user {user_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to unregister device token: {e}")
            return False

    async def send_notification(
        self,
        user_id: int,
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None,
        badge: Optional[int] = None,
        sound: str = "default"
    ) -> bool:
        """Send push notification to user's iOS devices."""
        if not self.apns:
            logger.warning("APNs not available - notification not sent")
            return False

        try:
            # Get user's device tokens
            user_tokens_key = f"user_tokens:ios:{user_id}"
            device_tokens = await self.cache.get(user_tokens_key) or []

            if not device_tokens:
                logger.warning(f"No device tokens found for user {user_id}")
                return False

            # Prepare notification payload
            payload = {
                "aps": {
                    "alert": {
                        "title": title,
                        "body": body
                    },
                    "sound": sound,
                    "badge": badge
                }
            }

            # Add custom data
            if data:
                payload.update(data)

            # Send to all user devices
            successful_sends = 0
            for token in device_tokens:
                try:
                    request = NotificationRequest(
                        device_token=token,
                        message=payload,
                        push_type=PushType.ALERT
                    )

                    await self.apns.send_notification(request)
                    successful_sends += 1
                    logger.debug(f"Notification sent to token: {token[:10]}...")

                except Exception as e:
                    logger.error(f"Failed to send notification to token {token[:10]}...: {e}")
                    # Remove invalid tokens
                    if "invalid" in str(e).lower() or "unregistered" in str(e).lower():
                        await self.unregister_device_token(user_id, token)

            logger.info(f"Sent {successful_sends}/{len(device_tokens)} notifications to user {user_id}")
            return successful_sends > 0

        except Exception as e:
            logger.error(f"Failed to send push notification: {e}")
            return False

    async def send_bulk_notification(
        self,
        user_ids: List[int],
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None,
        badge: Optional[int] = None,
        sound: str = "default"
    ) -> Dict[str, int]:
        """Send push notification to multiple users."""
        results = {"sent": 0, "failed": 0}

        # Use asyncio to send notifications concurrently
        tasks = []
        for user_id in user_ids:
            task = self.send_notification(user_id, title, body, data, badge, sound)
            tasks.append(task)

        # Wait for all notifications to complete
        if tasks:
            notification_results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in notification_results:
                if isinstance(result, bool) and result:
                    results["sent"] += 1
                else:
                    results["failed"] += 1

        return results

    async def get_user_devices(self, user_id: int) -> List[Dict[str, Any]]:
        """Get registered devices for a user."""
        try:
            user_tokens_key = f"user_tokens:ios:{user_id}"
            device_tokens = await self.cache.get(user_tokens_key) or []

            devices = []
            for token in device_tokens:
                cache_key = f"device_token:ios:{user_id}:{token}"
                device_data = await self.cache.get(cache_key)
                if device_data:
                    devices.append({
                        "token": token[:10] + "..." + token[-10:],  # Masked for security
                        "device_model": device_data.get("device_model"),
                        "ios_version": device_data.get("ios_version"),
                        "app_version": device_data.get("app_version"),
                        "registered_at": device_data.get("registered_at"),
                        "active": device_data.get("active", True)
                    })

            return devices

        except Exception as e:
            logger.error(f"Failed to get user devices: {e}")
            return []

    async def send_connection_request_notification(self, user_id: int, from_user_name: str):
        """Send notification for new connection request."""
        await self.send_notification(
            user_id=user_id,
            title="New Connection Request",
            body=f"{from_user_name} sent you a connection request",
            data={
                "type": "connection_request",
                "action": "view_connections"
            },
            badge=1
        )

    async def send_connection_accepted_notification(self, user_id: int, accepter_name: str):
        """Send notification for accepted connection."""
        await self.send_notification(
            user_id=user_id,
            title="Connection Accepted",
            body=f"{accepter_name} accepted your connection request",
            data={
                "type": "connection_accepted",
                "action": "view_connections"
            },
            badge=1
        )

    async def send_message_notification(self, user_id: int, sender_name: str, message_preview: str):
        """Send notification for new message."""
        await self.send_notification(
            user_id=user_id,
            title=f"Message from {sender_name}",
            body=message_preview[:100] + "..." if len(message_preview) > 100 else message_preview,
            data={
                "type": "new_message",
                "action": "view_messages"
            },
            badge=1
        )

    async def send_system_notification(self, user_ids: List[int], title: str, body: str):
        """Send system notification to multiple users."""
        await self.send_bulk_notification(
            user_ids=user_ids,
            title=title,
            body=body,
            data={
                "type": "system_notification",
                "action": "view_notifications"
            }
        )


# Global push notification service instance
_push_notification_service: Optional[PushNotificationService] = None


def get_push_notification_service() -> PushNotificationService:
    """Get push notification service instance."""
    global _push_notification_service
    if _push_notification_service is None:
        _push_notification_service = PushNotificationService()
    return _push_notification_service