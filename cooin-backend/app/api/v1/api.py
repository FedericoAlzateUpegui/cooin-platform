from fastapi import APIRouter

from app.api.v1 import auth, profiles, connections, ratings, email, uploads, cache, security, tickets, system_messages
# mobile, matching, analytics, search temporarily disabled due to missing models

# Create main API router
api_router = APIRouter()

# Include authentication routes
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["authentication"]
)

# Include profile routes
api_router.include_router(
    profiles.router,
    prefix="/profiles",
    tags=["profiles"]
)

# Include connection routes
api_router.include_router(
    connections.router,
    prefix="/connections",
    tags=["connections"]
)

# Include rating routes
api_router.include_router(
    ratings.router,
    prefix="/ratings",
    tags=["ratings"]
)

# Include email routes
api_router.include_router(
    email.router,
    prefix="/email",
    tags=["email"]
)

# Include file upload routes
api_router.include_router(
    uploads.router,
    prefix="/uploads",
    tags=["file-uploads"]
)

# Include cache management routes
api_router.include_router(
    cache.router,
    prefix="/cache",
    tags=["cache-management"]
)

# Include security management routes
api_router.include_router(
    security.router,
    prefix="/security",
    tags=["security-management"]
)

# Include tickets routes
api_router.include_router(
    tickets.router,
    prefix="/tickets",
    tags=["tickets"]
)

# Include system messages routes
api_router.include_router(
    system_messages.router,
    prefix="/system-messages",
    tags=["system-messages"]
)

# ========================================================================
# DISABLED ROUTES - Replaced by Tickets System (Session 12+)
# ========================================================================
# The following routes are disabled because they depend on the old
# LoanRequest and LendingOffer models which were replaced by the
# unified Tickets system in Session 12.
#
# Status: Kept for reference, may be removed or refactored in future
# Date Disabled: 2023-11 (Session 12)
# Alternative: Use /tickets endpoints for lending/borrowing functionality
# ========================================================================
#
# api_router.include_router(
#     mobile.mobile_router,
#     prefix="/mobile",
#     tags=["mobile-api"]
# )
# api_router.include_router(
#     matching.router,
#     prefix="/matching",
#     tags=["intelligent-matching"]
# )
# api_router.include_router(
#     analytics.router,
#     prefix="/analytics",
#     tags=["analytics-reporting"]
# )
# api_router.include_router(
#     search.router,
#     prefix="/search",
#     tags=["advanced-search"]
# )

# Health check endpoint for this API version
@api_router.get("/health")
async def api_health():
    """API health check endpoint."""
    return {
        "status": "healthy",
        "version": "v1",
        "message": "Cooin API v1 is running"
    }