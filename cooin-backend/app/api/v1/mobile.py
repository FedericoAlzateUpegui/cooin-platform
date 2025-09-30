"""
Mobile API router that consolidates all mobile-optimized endpoints.
Main entry point for iOS app integration.
"""

from fastapi import APIRouter

from app.api.v1 import mobile_uploads, websocket, matching, analytics, search
from app.core.mobile_docs import MOBILE_API_TAGS

# Create mobile API router
mobile_router = APIRouter()

# Include mobile-optimized upload routes
mobile_router.include_router(
    mobile_uploads.router,
    prefix="/uploads",
    tags=["Mobile File Upload"]
)

# Include WebSocket and notification routes
mobile_router.include_router(
    websocket.router,
    prefix="/websocket",
    tags=["Real-time Communication"]
)

# Include mobile matching routes
mobile_router.include_router(
    matching.router,
    prefix="/matching",
    tags=["Mobile Matching"]
)

# Include mobile analytics routes
mobile_router.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["Mobile Analytics"]
)

# Mobile-specific health check
@mobile_router.get("/health")
async def mobile_health_check():
    """
    Mobile-specific health check endpoint.
    Returns additional information useful for mobile apps.
    """
    return {
        "status": "healthy",
        "service": "Cooin Mobile API",
        "version": "1.0.0",
        "timestamp": "2025-01-15T10:00:00Z",
        "features": {
            "push_notifications": True,
            "websocket_support": True,
            "heic_support": True,
            "multi_size_images": True,
            "enhanced_auth": True
        },
        "endpoints": {
            "websocket": "/api/v1/mobile/websocket/ws",
            "push_token_register": "/api/v1/mobile/websocket/push-token/register",
            "avatar_upload": "/api/v1/mobile/uploads/avatar",
            "banner_upload": "/api/v1/mobile/uploads/banner",
            "document_upload": "/api/v1/mobile/uploads/document",
            "borrower_matches": "/api/v1/mobile/matching/mobile/borrower/matches/{loan_request_id}",
            "lender_matches": "/api/v1/mobile/matching/mobile/lender/matches/{lending_offer_id}",
            "analytics_summary": "/api/v1/mobile/analytics/mobile/summary",
            "personal_insights": "/api/v1/mobile/analytics/mobile/user-insights/{user_id}"
        }
    }