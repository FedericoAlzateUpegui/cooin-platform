"""
Redis-based caching service for improved performance.
Provides comprehensive caching functionality with automatic key generation and expiration.
"""

import json
import pickle
import hashlib
from typing import Any, Optional, Union, Dict, List, Callable
from datetime import datetime, timedelta
from functools import wraps
import asyncio
import logging

import redis.asyncio as redis
from redis.exceptions import RedisError, ConnectionError as RedisConnectionError

from app.core.config import settings

logger = logging.getLogger(__name__)


class CacheKeyGenerator:
    """Generate consistent cache keys for different data types."""

    @staticmethod
    def user_profile(user_id: int) -> str:
        """Generate cache key for user profile."""
        return f"user:profile:{user_id}"

    @staticmethod
    def user_connections(user_id: int) -> str:
        """Generate cache key for user connections."""
        return f"user:connections:{user_id}"

    @staticmethod
    def user_ratings(user_id: int) -> str:
        """Generate cache key for user ratings."""
        return f"user:ratings:{user_id}"

    @staticmethod
    def public_profiles(page: int = 1, limit: int = 20) -> str:
        """Generate cache key for public profiles list."""
        return f"profiles:public:page:{page}:limit:{limit}"

    @staticmethod
    def search_results(query_hash: str) -> str:
        """Generate cache key for search results."""
        return f"search:results:{query_hash}"

    @staticmethod
    def user_session(user_id: int) -> str:
        """Generate cache key for user session data."""
        return f"session:user:{user_id}"

    @staticmethod
    def rate_limit(identifier: str, endpoint: str) -> str:
        """Generate cache key for rate limiting."""
        return f"rate_limit:{endpoint}:{identifier}"

    @staticmethod
    def jwt_blacklist(jti: str) -> str:
        """Generate cache key for JWT blacklist."""
        return f"jwt:blacklist:{jti}"

    @staticmethod
    def email_verification(token: str) -> str:
        """Generate cache key for email verification attempts."""
        return f"email:verification:{token}"

    @staticmethod
    def password_reset(token: str) -> str:
        """Generate cache key for password reset attempts."""
        return f"password:reset:{token}"

    @staticmethod
    def function_result(func_name: str, *args, **kwargs) -> str:
        """Generate cache key for function results."""
        # Create a hash of the function arguments for consistent keys
        key_data = {
            'function': func_name,
            'args': args,
            'kwargs': sorted(kwargs.items())
        }
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        key_hash = hashlib.md5(key_str.encode()).hexdigest()
        return f"func:{func_name}:{key_hash}"


class CacheService:
    """Redis-based caching service with fallback to in-memory cache."""

    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.memory_cache: Dict[str, tuple] = {}  # (value, expiry)
        self.connected = False
        self.use_redis = True

    async def connect(self) -> bool:
        """Connect to Redis server with connection pooling and retry logic."""
        max_retries = 3
        retry_delay = 1  # seconds

        for attempt in range(max_retries):
            try:
                # Create connection pool for better performance and resource management
                pool = redis.ConnectionPool.from_url(
                    settings.REDIS_URL,
                    encoding="utf-8",
                    decode_responses=False,  # We handle encoding manually
                    max_connections=50,  # Maximum connections in pool
                    socket_timeout=2,  # Socket timeout in seconds
                    socket_connect_timeout=2,  # Connection timeout
                    socket_keepalive=False,  # Disable TCP keepalive for faster failure
                    retry_on_timeout=False,  # Don't retry on timeout
                    health_check_interval=30,  # Check connection health every 30s
                )

                self.redis_client = redis.Redis(connection_pool=pool)

                # Test connection
                await self.redis_client.ping()
                self.connected = True
                self.use_redis = True
                logger.info(f"Connected to Redis cache server (attempt {attempt + 1}/{max_retries})")
                return True

            except (RedisConnectionError, RedisError) as e:
                logger.warning(
                    f"Failed to connect to Redis (attempt {attempt + 1}/{max_retries}): {e}"
                )
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    logger.warning("All Redis connection attempts failed. Using in-memory cache fallback.")
                    self.connected = False
                    self.use_redis = False
                    return False

        return False

    async def disconnect(self):
        """Disconnect from Redis server."""
        if self.redis_client:
            await self.redis_client.close()
            self.connected = False

    def _serialize_value(self, value: Any) -> bytes:
        """Serialize value for storage."""
        try:
            # Try JSON first for simple types
            json_str = json.dumps(value, default=str)
            return json_str.encode('utf-8')
        except (TypeError, ValueError):
            # Fall back to pickle for complex objects
            return pickle.dumps(value)

    def _deserialize_value(self, data: bytes) -> Any:
        """Deserialize value from storage."""
        try:
            # Try JSON first
            return json.loads(data.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            # Fall back to pickle
            return pickle.loads(data)

    async def set(
        self,
        key: str,
        value: Any,
        expire_seconds: Optional[int] = None,
        expire_at: Optional[datetime] = None
    ) -> bool:
        """Set a value in cache with optional expiration."""
        try:
            serialized_value = self._serialize_value(value)

            if self.use_redis and self.connected:
                # Use Redis
                if expire_at:
                    expire_seconds = int((expire_at - datetime.utcnow()).total_seconds())

                if expire_seconds and expire_seconds > 0:
                    await self.redis_client.setex(key, expire_seconds, serialized_value)
                else:
                    await self.redis_client.set(key, serialized_value)
            else:
                # Use memory cache fallback
                expiry = None
                if expire_seconds:
                    expiry = datetime.utcnow() + timedelta(seconds=expire_seconds)
                elif expire_at:
                    expiry = expire_at

                self.memory_cache[key] = (value, expiry)

            return True

        except Exception as e:
            logger.error(f"Error setting cache key {key}: {e}")
            return False

    async def get(self, key: str) -> Optional[Any]:
        """Get a value from cache."""
        try:
            if self.use_redis and self.connected:
                # Use Redis
                data = await self.redis_client.get(key)
                if data is None:
                    return None
                return self._deserialize_value(data)
            else:
                # Use memory cache fallback
                if key not in self.memory_cache:
                    return None

                value, expiry = self.memory_cache[key]

                # Check expiration
                if expiry and datetime.utcnow() > expiry:
                    del self.memory_cache[key]
                    return None

                return value

        except Exception as e:
            logger.error(f"Error getting cache key {key}: {e}")
            return None

    async def delete(self, key: str) -> bool:
        """Delete a value from cache."""
        try:
            if self.use_redis and self.connected:
                result = await self.redis_client.delete(key)
                return result > 0
            else:
                if key in self.memory_cache:
                    del self.memory_cache[key]
                    return True
                return False

        except Exception as e:
            logger.error(f"Error deleting cache key {key}: {e}")
            return False

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        try:
            if self.use_redis and self.connected:
                return bool(await self.redis_client.exists(key))
            else:
                if key not in self.memory_cache:
                    return False

                value, expiry = self.memory_cache[key]
                if expiry and datetime.utcnow() > expiry:
                    del self.memory_cache[key]
                    return False

                return True

        except Exception as e:
            logger.error(f"Error checking cache key existence {key}: {e}")
            return False

    async def increment(self, key: str, amount: int = 1) -> int:
        """Increment a numeric value in cache."""
        try:
            if self.use_redis and self.connected:
                return await self.redis_client.incrby(key, amount)
            else:
                current = await self.get(key) or 0
                new_value = int(current) + amount
                await self.set(key, new_value)
                return new_value

        except Exception as e:
            logger.error(f"Error incrementing cache key {key}: {e}")
            return 0

    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiration for existing key."""
        try:
            if self.use_redis and self.connected:
                return await self.redis_client.expire(key, seconds)
            else:
                if key in self.memory_cache:
                    value, _ = self.memory_cache[key]
                    expiry = datetime.utcnow() + timedelta(seconds=seconds)
                    self.memory_cache[key] = (value, expiry)
                    return True
                return False

        except Exception as e:
            logger.error(f"Error setting expiration for cache key {key}: {e}")
            return False

    async def keys_pattern(self, pattern: str) -> List[str]:
        """Get keys matching a pattern."""
        try:
            if self.use_redis and self.connected:
                keys = await self.redis_client.keys(pattern)
                return [key.decode('utf-8') if isinstance(key, bytes) else key for key in keys]
            else:
                import fnmatch
                # Simple pattern matching for memory cache
                matching_keys = []
                for key in self.memory_cache.keys():
                    if fnmatch.fnmatch(key, pattern):
                        # Check if not expired
                        value, expiry = self.memory_cache[key]
                        if not expiry or datetime.utcnow() <= expiry:
                            matching_keys.append(key)
                return matching_keys

        except Exception as e:
            logger.error(f"Error getting keys with pattern {pattern}: {e}")
            return []

    async def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching a pattern."""
        try:
            keys = await self.keys_pattern(pattern)
            deleted_count = 0

            if self.use_redis and self.connected:
                if keys:
                    deleted_count = await self.redis_client.delete(*keys)
            else:
                for key in keys:
                    if key in self.memory_cache:
                        del self.memory_cache[key]
                        deleted_count += 1

            return deleted_count

        except Exception as e:
            logger.error(f"Error deleting keys with pattern {pattern}: {e}")
            return 0

    async def clear_all(self) -> bool:
        """Clear all cache data."""
        try:
            if self.use_redis and self.connected:
                await self.redis_client.flushdb()
            else:
                self.memory_cache.clear()

            logger.info("Cache cleared successfully")
            return True

        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False

    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        try:
            if self.use_redis and self.connected:
                info = await self.redis_client.info()
                return {
                    "backend": "redis",
                    "connected": True,
                    "keys": info.get("db0", {}).get("keys", 0),
                    "memory_usage": info.get("used_memory_human"),
                    "hits": info.get("keyspace_hits", 0),
                    "misses": info.get("keyspace_misses", 0)
                }
            else:
                # Clean expired keys from memory cache
                current_time = datetime.utcnow()
                expired_keys = [
                    key for key, (value, expiry) in self.memory_cache.items()
                    if expiry and current_time > expiry
                ]
                for key in expired_keys:
                    del self.memory_cache[key]

                return {
                    "backend": "memory",
                    "connected": False,
                    "keys": len(self.memory_cache),
                    "memory_usage": "N/A"
                }

        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {"error": str(e)}


def cached(
    expire_seconds: Optional[int] = 3600,
    key_func: Optional[Callable] = None,
    condition: Optional[Callable] = None
):
    """
    Decorator to cache function results.

    Args:
        expire_seconds: Cache expiration in seconds (default: 1 hour)
        key_func: Custom function to generate cache key
        condition: Function that returns True if result should be cached
    """
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            cache = get_cache_service()

            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = CacheKeyGenerator.function_result(func.__name__, *args, **kwargs)

            # Try to get from cache first
            cached_result = await cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for key: {cache_key}")
                return cached_result

            # Execute function
            result = await func(*args, **kwargs)

            # Cache the result if condition is met
            if condition is None or condition(result):
                await cache.set(cache_key, result, expire_seconds)
                logger.debug(f"Cached result for key: {cache_key}")

            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # For sync functions, we need to handle caching differently
            # This is a simplified version - in production you might want async cache operations
            result = func(*args, **kwargs)
            return result

        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


# Global cache service instance
_cache_service: Optional[CacheService] = None


def get_cache_service() -> CacheService:
    """Get cache service instance."""
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service


async def init_cache() -> CacheService:
    """Initialize cache service."""
    cache = get_cache_service()
    await cache.connect()
    return cache


async def cleanup_cache():
    """Cleanup cache service."""
    cache = get_cache_service()
    await cache.disconnect()