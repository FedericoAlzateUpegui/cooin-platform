"""
WebSocket service for real-time updates in mobile app.
Handles live notifications, connection updates, and messaging.
"""

import json
import asyncio
from typing import Dict, List, Set, Optional, Any
from datetime import datetime
import logging

from fastapi import WebSocket, WebSocketDisconnect
from app.core.cache import get_cache_service
from app.services.push_notification_service import get_push_notification_service

logger = logging.getLogger(__name__)


class WebSocketManager:
    """Manages WebSocket connections for real-time communication."""

    def __init__(self):
        # Active connections: user_id -> set of WebSocket connections
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        # Connection metadata: websocket -> user_info
        self.connection_info: Dict[WebSocket, Dict[str, Any]] = {}
        self.cache = get_cache_service()
        self.push_service = get_push_notification_service()

    async def connect(self, websocket: WebSocket, user_id: int, device_info: Optional[Dict] = None):
        """Accept and register a new WebSocket connection."""
        await websocket.accept()

        # Add to active connections
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)

        # Store connection metadata
        self.connection_info[websocket] = {
            "user_id": user_id,
            "connected_at": datetime.utcnow(),
            "device_info": device_info or {},
            "last_ping": datetime.utcnow()
        }

        # Update user online status
        await self._update_user_online_status(user_id, True)

        logger.info(f"WebSocket connected for user {user_id}. Total connections: {len(self.active_connections[user_id])}")

        # Send welcome message
        await self.send_to_user(user_id, {
            "type": "connection_established",
            "data": {
                "message": "Connected to Cooin real-time service",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "user_id": user_id
            }
        })

    async def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection and clean up."""
        if websocket in self.connection_info:
            user_id = self.connection_info[websocket]["user_id"]

            # Remove from active connections
            if user_id in self.active_connections:
                self.active_connections[user_id].discard(websocket)
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]
                    # Update user offline status if no connections left
                    await self._update_user_online_status(user_id, False)

            # Remove connection info
            del self.connection_info[websocket]

            logger.info(f"WebSocket disconnected for user {user_id}")

    async def send_to_user(self, user_id: int, message: Dict[str, Any]) -> bool:
        """Send message to all connections of a specific user."""
        if user_id not in self.active_connections:
            logger.debug(f"No active connections for user {user_id}")
            return False

        message["timestamp"] = datetime.utcnow().isoformat() + "Z"
        message_str = json.dumps(message)

        # Send to all user connections
        disconnected_connections = []
        successful_sends = 0

        for websocket in self.active_connections[user_id].copy():
            try:
                await websocket.send_text(message_str)
                successful_sends += 1
            except Exception as e:
                logger.warning(f"Failed to send message via WebSocket: {e}")
                disconnected_connections.append(websocket)

        # Clean up disconnected connections
        for websocket in disconnected_connections:
            await self.disconnect(websocket)

        if successful_sends == 0 and message.get("type") != "ping":
            # If no WebSocket connections, try push notification as fallback
            await self._fallback_to_push_notification(user_id, message)

        return successful_sends > 0

    async def send_to_multiple_users(self, user_ids: List[int], message: Dict[str, Any]) -> Dict[str, int]:
        """Send message to multiple users."""
        results = {"sent": 0, "failed": 0}

        tasks = []
        for user_id in user_ids:
            task = self.send_to_user(user_id, message.copy())
            tasks.append(task)

        if tasks:
            send_results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in send_results:
                if isinstance(result, bool) and result:
                    results["sent"] += 1
                else:
                    results["failed"] += 1

        return results

    async def broadcast_to_all(self, message: Dict[str, Any]) -> int:
        """Broadcast message to all connected users."""
        user_ids = list(self.active_connections.keys())
        results = await self.send_to_multiple_users(user_ids, message)
        return results["sent"]

    async def handle_message(self, websocket: WebSocket, message: str):
        """Handle incoming WebSocket message from client."""
        try:
            data = json.loads(message)
            message_type = data.get("type")
            user_id = self.connection_info.get(websocket, {}).get("user_id")

            if not user_id:
                logger.warning("Received message from unauthenticated WebSocket")
                return

            # Handle different message types
            if message_type == "ping":
                await self._handle_ping(websocket, data)
            elif message_type == "mark_notification_read":
                await self._handle_mark_notification_read(user_id, data)
            elif message_type == "typing_indicator":
                await self._handle_typing_indicator(user_id, data)
            elif message_type == "presence_update":
                await self._handle_presence_update(user_id, data)
            else:
                logger.warning(f"Unknown message type: {message_type}")

        except json.JSONDecodeError:
            logger.warning("Received invalid JSON from WebSocket")
        except Exception as e:
            logger.error(f"Error handling WebSocket message: {e}")

    async def _handle_ping(self, websocket: WebSocket, data: Dict):
        """Handle ping message to keep connection alive."""
        if websocket in self.connection_info:
            self.connection_info[websocket]["last_ping"] = datetime.utcnow()

        await websocket.send_text(json.dumps({
            "type": "pong",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "server_time": datetime.utcnow().timestamp()
        }))

    async def _handle_mark_notification_read(self, user_id: int, data: Dict):
        """Handle notification read status update."""
        notification_id = data.get("notification_id")
        if notification_id:
            # Update notification status in database/cache
            await self.cache.set(f"notification_read:{user_id}:{notification_id}", True, 86400 * 7)
            logger.info(f"Marked notification {notification_id} as read for user {user_id}")

    async def _handle_typing_indicator(self, user_id: int, data: Dict):
        """Handle typing indicator for conversations."""
        target_user_id = data.get("target_user_id")
        is_typing = data.get("is_typing", False)

        if target_user_id:
            await self.send_to_user(target_user_id, {
                "type": "typing_indicator",
                "data": {
                    "from_user_id": user_id,
                    "is_typing": is_typing
                }
            })

    async def _handle_presence_update(self, user_id: int, data: Dict):
        """Handle user presence status update."""
        status = data.get("status", "online")  # online, away, busy, invisible

        # Update presence in cache
        await self.cache.set(f"user_presence:{user_id}", {
            "status": status,
            "last_seen": datetime.utcnow().isoformat() + "Z"
        }, 300)  # 5 minutes

    async def _update_user_online_status(self, user_id: int, is_online: bool):
        """Update user online status in cache."""
        status_data = {
            "online": is_online,
            "last_seen": datetime.utcnow().isoformat() + "Z"
        }
        await self.cache.set(f"user_online:{user_id}", status_data, 300)

    async def _fallback_to_push_notification(self, user_id: int, message: Dict[str, Any]):
        """Send push notification as fallback when WebSocket is not available."""
        message_type = message.get("type")
        data = message.get("data", {})

        if message_type == "connection_request":
            await self.push_service.send_connection_request_notification(
                user_id=user_id,
                from_user_name=data.get("from_user_name", "Someone")
            )
        elif message_type == "connection_accepted":
            await self.push_service.send_connection_accepted_notification(
                user_id=user_id,
                accepter_name=data.get("accepter_name", "Someone")
            )
        elif message_type == "new_message":
            await self.push_service.send_message_notification(
                user_id=user_id,
                sender_name=data.get("sender_name", "Someone"),
                message_preview=data.get("message_preview", "New message")
            )

    async def get_connection_stats(self) -> Dict[str, Any]:
        """Get WebSocket connection statistics."""
        total_connections = sum(len(connections) for connections in self.active_connections.values())

        return {
            "total_connections": total_connections,
            "total_users": len(self.active_connections),
            "connections_per_user": {
                user_id: len(connections)
                for user_id, connections in self.active_connections.items()
            }
        }

    async def cleanup_stale_connections(self):
        """Clean up stale connections periodically."""
        current_time = datetime.utcnow()
        stale_connections = []

        for websocket, info in self.connection_info.items():
            last_ping = info.get("last_ping", info["connected_at"])
            if (current_time - last_ping).total_seconds() > 300:  # 5 minutes
                stale_connections.append(websocket)

        for websocket in stale_connections:
            await self.disconnect(websocket)
            logger.info("Cleaned up stale WebSocket connection")

    # Notification methods for different events
    async def notify_connection_request(self, user_id: int, from_user: Dict, connection_data: Dict):
        """Notify user of new connection request."""
        await self.send_to_user(user_id, {
            "type": "connection_request",
            "data": {
                "from_user": from_user,
                "connection": connection_data,
                "message": f"{from_user.get('display_name', 'Someone')} sent you a connection request"
            }
        })

    async def notify_connection_accepted(self, user_id: int, accepter: Dict, connection_data: Dict):
        """Notify user that their connection request was accepted."""
        await self.send_to_user(user_id, {
            "type": "connection_accepted",
            "data": {
                "accepter": accepter,
                "connection": connection_data,
                "message": f"{accepter.get('display_name', 'Someone')} accepted your connection request"
            }
        })

    async def notify_new_message(self, user_id: int, sender: Dict, message_data: Dict):
        """Notify user of new message."""
        await self.send_to_user(user_id, {
            "type": "new_message",
            "data": {
                "sender": sender,
                "message": message_data,
                "preview": message_data.get("content", "")[:100]
            }
        })

    async def notify_profile_update(self, user_id: int, updated_fields: List[str]):
        """Notify user of profile updates."""
        await self.send_to_user(user_id, {
            "type": "profile_updated",
            "data": {
                "updated_fields": updated_fields,
                "message": "Your profile has been updated successfully"
            }
        })


# Global WebSocket manager instance
websocket_manager = WebSocketManager()


def get_websocket_manager() -> WebSocketManager:
    """Get WebSocket manager instance."""
    return websocket_manager