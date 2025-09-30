"""
Application-specific caching service that integrates with business logic.
Provides high-level caching operations for common use cases.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import logging

from sqlalchemy.orm import Session

from app.core.cache import get_cache_service, CacheKeyGenerator, cached
from app.models import User, UserProfile, Connection, Rating
from app.models.user import UserStatus

logger = logging.getLogger(__name__)


class ApplicationCacheService:
    """High-level caching service for application-specific operations."""

    def __init__(self):
        self.cache = get_cache_service()

    # User Profile Caching
    async def cache_user_profile(self, user_id: int, profile_data: dict, expire_hours: int = 24):
        """Cache user profile data."""
        key = CacheKeyGenerator.user_profile(user_id)
        expire_seconds = expire_hours * 3600
        await self.cache.set(key, profile_data, expire_seconds)

    async def get_cached_user_profile(self, user_id: int) -> Optional[dict]:
        """Get cached user profile."""
        key = CacheKeyGenerator.user_profile(user_id)
        return await self.cache.get(key)

    async def invalidate_user_profile(self, user_id: int):
        """Invalidate user profile cache."""
        key = CacheKeyGenerator.user_profile(user_id)
        await self.cache.delete(key)

    # Public Profiles Caching
    async def cache_public_profiles(self, page: int, limit: int, profiles_data: List[dict], expire_minutes: int = 30):
        """Cache public profiles list."""
        key = CacheKeyGenerator.public_profiles(page, limit)
        expire_seconds = expire_minutes * 60
        await self.cache.set(key, profiles_data, expire_seconds)

    async def get_cached_public_profiles(self, page: int, limit: int) -> Optional[List[dict]]:
        """Get cached public profiles list."""
        key = CacheKeyGenerator.public_profiles(page, limit)
        return await self.cache.get(key)

    async def invalidate_public_profiles_cache(self):
        """Invalidate all public profiles cache entries."""
        pattern = "profiles:public:*"
        deleted_count = await self.cache.delete_pattern(pattern)
        logger.info(f"Invalidated {deleted_count} public profile cache entries")

    # User Connections Caching
    async def cache_user_connections(self, user_id: int, connections_data: List[dict], expire_hours: int = 6):
        """Cache user connections."""
        key = CacheKeyGenerator.user_connections(user_id)
        expire_seconds = expire_hours * 3600
        await self.cache.set(key, connections_data, expire_seconds)

    async def get_cached_user_connections(self, user_id: int) -> Optional[List[dict]]:
        """Get cached user connections."""
        key = CacheKeyGenerator.user_connections(user_id)
        return await self.cache.get(key)

    async def invalidate_user_connections(self, user_id: int):
        """Invalidate user connections cache."""
        key = CacheKeyGenerator.user_connections(user_id)
        await self.cache.delete(key)

    # User Ratings Caching
    async def cache_user_ratings(self, user_id: int, ratings_data: dict, expire_hours: int = 12):
        """Cache user ratings summary."""
        key = CacheKeyGenerator.user_ratings(user_id)
        expire_seconds = expire_hours * 3600
        await self.cache.set(key, ratings_data, expire_seconds)

    async def get_cached_user_ratings(self, user_id: int) -> Optional[dict]:
        """Get cached user ratings."""
        key = CacheKeyGenerator.user_ratings(user_id)
        return await self.cache.get(key)

    async def invalidate_user_ratings(self, user_id: int):
        """Invalidate user ratings cache."""
        key = CacheKeyGenerator.user_ratings(user_id)
        await self.cache.delete(key)

    # Search Results Caching
    async def cache_search_results(self, query_params: dict, results: List[dict], expire_minutes: int = 15):
        """Cache search results."""
        import hashlib
        import json

        # Create a hash of query parameters for consistent caching
        query_str = json.dumps(query_params, sort_keys=True)
        query_hash = hashlib.md5(query_str.encode()).hexdigest()

        key = CacheKeyGenerator.search_results(query_hash)
        expire_seconds = expire_minutes * 60
        await self.cache.set(key, results, expire_seconds)

    async def get_cached_search_results(self, query_params: dict) -> Optional[List[dict]]:
        """Get cached search results."""
        import hashlib
        import json

        query_str = json.dumps(query_params, sort_keys=True)
        query_hash = hashlib.md5(query_str.encode()).hexdigest()

        key = CacheKeyGenerator.search_results(query_hash)
        return await self.cache.get(key)

    # Session Management
    async def cache_user_session(self, user_id: int, session_data: dict, expire_hours: int = 24):
        """Cache user session data."""
        key = CacheKeyGenerator.user_session(user_id)
        expire_seconds = expire_hours * 3600
        await self.cache.set(key, session_data, expire_seconds)

    async def get_cached_user_session(self, user_id: int) -> Optional[dict]:
        """Get cached user session."""
        key = CacheKeyGenerator.user_session(user_id)
        return await self.cache.get(key)

    async def invalidate_user_session(self, user_id: int):
        """Invalidate user session cache."""
        key = CacheKeyGenerator.user_session(user_id)
        await self.cache.delete(key)

    # JWT Token Blacklist
    async def blacklist_jwt_token(self, jti: str, expire_seconds: int):
        """Add JWT token to blacklist."""
        key = CacheKeyGenerator.jwt_blacklist(jti)
        await self.cache.set(key, True, expire_seconds)

    async def is_jwt_blacklisted(self, jti: str) -> bool:
        """Check if JWT token is blacklisted."""
        key = CacheKeyGenerator.jwt_blacklist(jti)
        return await self.cache.exists(key)

    # Rate Limiting Support
    async def increment_rate_limit(self, identifier: str, endpoint: str, window_seconds: int) -> int:
        """Increment rate limit counter."""
        key = CacheKeyGenerator.rate_limit(identifier, endpoint)
        count = await self.cache.increment(key)

        # Set expiration on first increment
        if count == 1:
            await self.cache.expire(key, window_seconds)

        return count

    async def get_rate_limit_count(self, identifier: str, endpoint: str) -> int:
        """Get current rate limit count."""
        key = CacheKeyGenerator.rate_limit(identifier, endpoint)
        count = await self.cache.get(key)
        return count or 0

    # Email Verification Tracking
    async def track_email_verification_attempt(self, email: str, attempts: int = 1, expire_hours: int = 24):
        """Track email verification attempts."""
        key = f"email:verification:attempts:{email}"
        current_attempts = await self.cache.get(key) or 0
        new_attempts = current_attempts + attempts

        expire_seconds = expire_hours * 3600
        await self.cache.set(key, new_attempts, expire_seconds)
        return new_attempts

    async def get_email_verification_attempts(self, email: str) -> int:
        """Get email verification attempt count."""
        key = f"email:verification:attempts:{email}"
        return await self.cache.get(key) or 0

    # Cache Statistics and Management
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics."""
        return await self.cache.get_stats()

    async def clear_user_related_cache(self, user_id: int):
        """Clear all cache entries related to a specific user."""
        keys_to_delete = [
            CacheKeyGenerator.user_profile(user_id),
            CacheKeyGenerator.user_connections(user_id),
            CacheKeyGenerator.user_ratings(user_id),
            CacheKeyGenerator.user_session(user_id)
        ]

        deleted_count = 0
        for key in keys_to_delete:
            if await self.cache.delete(key):
                deleted_count += 1

        # Also invalidate public profiles cache since user might be listed there
        await self.invalidate_public_profiles_cache()

        logger.info(f"Cleared {deleted_count} cache entries for user {user_id}")
        return deleted_count

    async def warm_up_cache(self, db: Session):
        """Pre-populate cache with frequently accessed data."""
        logger.info("Starting cache warm-up...")

        try:
            # Cache active user profiles
            active_users = db.query(User).filter(
                User.is_active == True,
                User.status == UserStatus.ACTIVE
            ).limit(100).all()

            warmed_profiles = 0
            for user in active_users:
                if user.profile:
                    profile_data = {
                        "id": user.profile.id,
                        "user_id": user.id,
                        "display_name": user.profile.display_name,
                        "bio": user.profile.bio,
                        "location": user.profile.location_string,
                        "avatar_url": user.profile.avatar_url,
                        "banner_url": user.profile.banner_url,
                        "profile_completion": user.profile.profile_completion_percentage,
                        "last_updated": user.profile.updated_at.isoformat() if user.profile.updated_at else None
                    }
                    await self.cache_user_profile(user.id, profile_data, expire_hours=12)
                    warmed_profiles += 1

            logger.info(f"Cache warm-up completed. Warmed {warmed_profiles} user profiles.")

        except Exception as e:
            logger.error(f"Error during cache warm-up: {e}")

    async def cleanup_expired_entries(self):
        """Clean up expired cache entries (mainly for memory cache backend)."""
        if not self.cache.use_redis:
            # For memory cache, we need to manually clean expired entries
            current_time = datetime.utcnow()
            expired_keys = []

            for key, (value, expiry) in self.cache.memory_cache.items():
                if expiry and current_time > expiry:
                    expired_keys.append(key)

            for key in expired_keys:
                del self.cache.memory_cache[key]

            if expired_keys:
                logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")


# Cached decorators for common operations
@cached(expire_seconds=1800)  # 30 minutes
async def get_user_profile_summary(db: Session, user_id: int) -> Optional[dict]:
    """Get cached user profile summary."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.profile:
        return None

    return {
        "id": user.id,
        "username": user.username,
        "display_name": user.profile.display_name,
        "bio": user.profile.bio,
        "location": user.profile.location_string,
        "avatar_url": user.profile.avatar_url,
        "role": user.role.value,
        "is_verified": user.is_verified,
        "profile_completion": user.profile.profile_completion_percentage
    }


@cached(expire_seconds=3600)  # 1 hour
async def get_user_rating_summary(db: Session, user_id: int) -> dict:
    """Get cached user rating summary."""
    ratings = db.query(Rating).filter(Rating.rated_user_id == user_id).all()

    if not ratings:
        return {
            "average_rating": 0.0,
            "total_ratings": 0,
            "rating_distribution": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        }

    total = sum(r.rating for r in ratings)
    count = len(ratings)
    average = round(total / count, 2)

    distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for rating in ratings:
        distribution[rating.rating] += 1

    return {
        "average_rating": average,
        "total_ratings": count,
        "rating_distribution": distribution
    }


# Global cache service instance
_app_cache_service: Optional[ApplicationCacheService] = None


def get_app_cache_service() -> ApplicationCacheService:
    """Get application cache service instance."""
    global _app_cache_service
    if _app_cache_service is None:
        _app_cache_service = ApplicationCacheService()
    return _app_cache_service