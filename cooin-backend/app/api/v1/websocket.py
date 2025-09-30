"""
WebSocket API endpoints for real-time communication.
"""

import json
import logging
from typing import Optional, Dict, Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.deps import get_current_user_websocket, get_database
from app.core.mobile_responses import MobileResponseFormatter, MobileJSONResponse
from app.services.websocket_service import get_websocket_manager
from app.services.push_notification_service import get_push_notification_service
from app.models import User

logger = logging.getLogger(__name__)

router = APIRouter()
websocket_manager = get_websocket_manager()
push_service = get_push_notification_service()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: Optional[str] = None,
    user_id: Optional[int] = None
):
    """
    WebSocket endpoint for real-time communication.

    Connection URL: ws://localhost:8000/api/v1/websocket/ws?token=<jwt_token>

    Messages sent to client:
    - connection_established: Welcome message after successful connection
    - connection_request: New connection request notification
    - connection_accepted: Connection request accepted notification
    - new_message: New message notification
    - profile_updated: Profile update notification
    - typing_indicator: User typing status
    - pong: Response to ping for keepalive

    Messages accepted from client:
    - ping: Keepalive ping
    - mark_notification_read: Mark notification as read
    - typing_indicator: Send typing status to another user
    - presence_update: Update user presence status
    """

    # Extract user info from token
    user_info = None
    if token:
        try:
            # Validate token and get user (simplified for WebSocket)
            from app.core.security import jwt_handler
            payload = jwt_handler.decode_access_token(token)
            user_id = payload.get("user_id")
            user_info = {"user_id": user_id}
        except Exception as e:
            logger.warning(f"Invalid WebSocket token: {e}")
            await websocket.close(code=4001, reason="Invalid token")
            return

    if not user_id:
        await websocket.close(code=4000, reason="Authentication required")
        return

    # Get device info from query parameters
    device_info = {
        "app_version": websocket.query_params.get("app_version"),
        "device_model": websocket.query_params.get("device_model"),
        "ios_version": websocket.query_params.get("ios_version")
    }

    try:
        # Connect to WebSocket manager
        await websocket_manager.connect(websocket, user_id, device_info)

        # Keep connection alive and handle messages
        while True:
            try:
                # Wait for message from client
                data = await websocket.receive_text()
                await websocket_manager.handle_message(websocket, data)

            except WebSocketDisconnect:
                logger.info(f"WebSocket client disconnected: user_id={user_id}")
                break
            except Exception as e:
                logger.error(f"Error in WebSocket communication: {e}")
                break

    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")

    finally:
        # Clean up connection
        await websocket_manager.disconnect(websocket)


@router.post("/push-token/register")
async def register_push_token(
    request: Request,
    token_data: dict,
    current_user: User = Depends(get_current_user_websocket),
    db: Session = Depends(get_database)
):
    """
    Register iOS device token for push notifications.

    Request body:
    {
        "device_token": "string",
        "device_model": "iPhone15,2",
        "ios_version": "17.0",
        "app_version": "1.0.0"
    }
    """
    try:
        device_token = token_data.get("device_token")
        if not device_token:
            return MobileJSONResponse(
                content=MobileResponseFormatter.error(
                    error_code="MISSING_DEVICE_TOKEN",
                    detail="Device token is required",
                    status_code=400,
                    request=request
                ),
                status_code=400
            )

        device_info = {
            "device_model": token_data.get("device_model"),
            "ios_version": token_data.get("ios_version"),
            "app_version": token_data.get("app_version")
        }

        # Register token with push service
        success = await push_service.register_device_token(
            user_id=current_user.id,
            device_token=device_token,
            device_info=device_info
        )

        if success:
            return MobileJSONResponse(
                content=MobileResponseFormatter.success(
                    data={"registered": True},
                    message="Device token registered successfully",
                    request=request
                )
            )
        else:
            return MobileJSONResponse(
                content=MobileResponseFormatter.error(
                    error_code="REGISTRATION_FAILED",
                    detail="Failed to register device token",
                    status_code=500,
                    request=request
                ),
                status_code=500
            )

    except Exception as e:
        logger.error(f"Error registering push token: {e}")
        return MobileJSONResponse(
            content=MobileResponseFormatter.error(
                error_code="INTERNAL_ERROR",
                detail="Failed to register push token",
                status_code=500,
                request=request
            ),
            status_code=500
        )


@router.delete("/push-token/unregister")
async def unregister_push_token(
    request: Request,
    token_data: dict,
    current_user: User = Depends(get_current_user_websocket),
    db: Session = Depends(get_database)
):
    """
    Unregister iOS device token for push notifications.

    Request body:
    {
        "device_token": "string"
    }
    """
    try:
        device_token = token_data.get("device_token")
        if not device_token:
            return MobileJSONResponse(
                content=MobileResponseFormatter.error(
                    error_code="MISSING_DEVICE_TOKEN",
                    detail="Device token is required",
                    status_code=400,
                    request=request
                ),
                status_code=400
            )

        # Unregister token with push service
        success = await push_service.unregister_device_token(
            user_id=current_user.id,
            device_token=device_token
        )

        if success:
            return MobileJSONResponse(
                content=MobileResponseFormatter.success(
                    data={"unregistered": True},
                    message="Device token unregistered successfully",
                    request=request
                )
            )
        else:
            return MobileJSONResponse(
                content=MobileResponseFormatter.error(
                    error_code="UNREGISTRATION_FAILED",
                    detail="Failed to unregister device token",
                    status_code=500,
                    request=request
                ),
                status_code=500
            )

    except Exception as e:
        logger.error(f"Error unregistering push token: {e}")
        return MobileJSONResponse(
            content=MobileResponseFormatter.error(
                error_code="INTERNAL_ERROR",
                detail="Failed to unregister push token",
                status_code=500,
                request=request
            ),
            status_code=500
        )


@router.get("/devices")
async def get_user_devices(
    request: Request,
    current_user: User = Depends(get_current_user_websocket)
):
    """Get list of registered devices for current user."""
    try:
        devices = await push_service.get_user_devices(current_user.id)

        return MobileJSONResponse(
            content=MobileResponseFormatter.success(
                data={"devices": devices},
                message="Devices retrieved successfully",
                request=request
            )
        )

    except Exception as e:
        logger.error(f"Error getting user devices: {e}")
        return MobileJSONResponse(
            content=MobileResponseFormatter.error(
                error_code="INTERNAL_ERROR",
                detail="Failed to retrieve devices",
                status_code=500,
                request=request
            ),
            status_code=500
        )


@router.get("/connection-stats")
async def get_connection_stats(
    request: Request,
    current_user: User = Depends(get_current_user_websocket)
):
    """Get WebSocket connection statistics (admin only)."""
    try:
        # Check if user is admin (simplified check)
        if not hasattr(current_user, 'role') or current_user.role != 'ADMIN':
            return MobileJSONResponse(
                content=MobileResponseFormatter.error(
                    error_code="INSUFFICIENT_PERMISSIONS",
                    detail="Admin access required",
                    status_code=403,
                    request=request
                ),
                status_code=403
            )

        stats = await websocket_manager.get_connection_stats()

        return MobileJSONResponse(
            content=MobileResponseFormatter.success(
                data=stats,
                message="Connection stats retrieved successfully",
                request=request
            )
        )

    except Exception as e:
        logger.error(f"Error getting connection stats: {e}")
        return MobileJSONResponse(
            content=MobileResponseFormatter.error(
                error_code="INTERNAL_ERROR",
                detail="Failed to retrieve connection stats",
                status_code=500,
                request=request
            ),
            status_code=500
        )


@router.post("/test-notification")
async def send_test_notification(
    request: Request,
    notification_data: dict,
    current_user: User = Depends(get_current_user_websocket)
):
    """
    Send test notification to current user's devices.
    For development and testing purposes.

    Request body:
    {
        "title": "Test Notification",
        "body": "This is a test notification",
        "data": {"key": "value"}
    }
    """
    try:
        title = notification_data.get("title", "Test Notification")
        body = notification_data.get("body", "This is a test notification")
        data = notification_data.get("data", {})

        # Send push notification
        push_success = await push_service.send_notification(
            user_id=current_user.id,
            title=title,
            body=body,
            data=data
        )

        # Send WebSocket notification
        websocket_success = await websocket_manager.send_to_user(current_user.id, {
            "type": "test_notification",
            "data": {
                "title": title,
                "body": body,
                "custom_data": data
            }
        })

        return MobileJSONResponse(
            content=MobileResponseFormatter.success(
                data={
                    "push_notification_sent": push_success,
                    "websocket_notification_sent": websocket_success
                },
                message="Test notification sent",
                request=request
            )
        )

    except Exception as e:
        logger.error(f"Error sending test notification: {e}")
        return MobileJSONResponse(
            content=MobileResponseFormatter.error(
                error_code="INTERNAL_ERROR",
                detail="Failed to send test notification",
                status_code=500,
                request=request
            ),
            status_code=500
        )


# Background task to cleanup stale connections
import asyncio
from contextlib import asynccontextmanager

async def cleanup_stale_connections():
    """Background task to cleanup stale WebSocket connections."""
    while True:
        try:
            await websocket_manager.cleanup_stale_connections()
            await asyncio.sleep(300)  # Run every 5 minutes
        except Exception as e:
            logger.error(f"Error in cleanup task: {e}")
            await asyncio.sleep(60)  # Retry after 1 minute on error