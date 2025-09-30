"""
Cache management and monitoring endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
import logging

from app.db.base import get_database
from app.models import User
from app.core.deps import get_current_active_user
from app.services.cache_service import get_app_cache_service
from app.core.exceptions import BusinessLogicError

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/stats")
async def get_cache_stats(
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Get cache statistics and health information.

    Returns cache backend type, connection status, and performance metrics.
    """
    cache_service = get_app_cache_service()

    try:
        stats = await cache_service.get_cache_stats()
        return {
            "status": "success",
            "cache_stats": stats,
            "message": "Cache statistics retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting cache stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve cache statistics"
        )


@router.post("/clear/user/{user_id}")
async def clear_user_cache(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Clear all cache entries for a specific user.

    Only users can clear their own cache, unless they have admin privileges.
    """
    # Check if user is trying to clear their own cache or is an admin
    if current_user.id != user_id:
        # In a real application, you would check for admin role here
        # For now, only allow users to clear their own cache
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only clear your own cache"
        )

    cache_service = get_app_cache_service()

    try:
        cleared_count = await cache_service.clear_user_related_cache(user_id)
        return {
            "status": "success",
            "cleared_entries": cleared_count,
            "user_id": user_id,
            "message": f"Cleared {cleared_count} cache entries for user {user_id}"
        }
    except Exception as e:
        logger.error(f"Error clearing user cache for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear user cache"
        )


@router.post("/clear/search")
async def clear_search_cache(
    current_user: User = Depends(get_current_active_user)
):
    """
    Clear all search result cache entries.

    This is useful when search algorithm or data changes significantly.
    """
    cache_service = get_app_cache_service()

    try:
        # Clear search results cache
        pattern = "search:results:*"
        cleared_count = await cache_service.cache.delete_pattern(pattern)

        return {
            "status": "success",
            "cleared_entries": cleared_count,
            "message": f"Cleared {cleared_count} search cache entries"
        }
    except Exception as e:
        logger.error(f"Error clearing search cache: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear search cache"
        )


@router.post("/clear/profiles")
async def clear_profiles_cache(
    current_user: User = Depends(get_current_active_user)
):
    """
    Clear all public profiles cache entries.

    This is useful when profile display logic changes.
    """
    cache_service = get_app_cache_service()

    try:
        await cache_service.invalidate_public_profiles_cache()

        return {
            "status": "success",
            "message": "Public profiles cache cleared successfully"
        }
    except Exception as e:
        logger.error(f"Error clearing profiles cache: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear profiles cache"
        )


@router.post("/warm-up")
async def warm_up_cache(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Pre-populate cache with frequently accessed data.

    This endpoint can be called after deployments or cache clears
    to improve initial response times.
    """
    cache_service = get_app_cache_service()

    try:
        await cache_service.warm_up_cache(db)

        return {
            "status": "success",
            "message": "Cache warm-up completed successfully"
        }
    except Exception as e:
        logger.error(f"Error during cache warm-up: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to warm up cache"
        )


@router.delete("/clear-all")
async def clear_all_cache(
    current_user: User = Depends(get_current_active_user)
):
    """
    Clear all cache entries.

    ⚠️ Warning: This will clear ALL cached data and may impact performance
    until the cache is repopulated.

    This endpoint should typically be restricted to admin users only.
    """
    # In a real application, you would check for admin role here
    # For now, allow all authenticated users (for development/testing)

    cache_service = get_app_cache_service()

    try:
        success = await cache_service.cache.clear_all()

        if success:
            return {
                "status": "success",
                "message": "All cache entries cleared successfully"
            }
        else:
            raise BusinessLogicError(
                detail="Failed to clear cache",
                error_code="CACHE_CLEAR_FAILED"
            )

    except Exception as e:
        logger.error(f"Error clearing all cache: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear all cache"
        )


@router.get("/health")
async def cache_health_check():
    """
    Check cache service health and connectivity.

    Returns cache backend information and connection status.
    """
    cache_service = get_app_cache_service()

    try:
        stats = await cache_service.get_cache_stats()

        # Determine health status
        is_healthy = True
        if "error" in stats:
            is_healthy = False

        health_status = "healthy" if is_healthy else "unhealthy"

        return {
            "status": health_status,
            "backend": stats.get("backend", "unknown"),
            "connected": stats.get("connected", False),
            "cache_type": "redis" if cache_service.cache.use_redis else "memory",
            "details": stats
        }

    except Exception as e:
        logger.error(f"Error checking cache health: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "cache_type": "unknown"
        }