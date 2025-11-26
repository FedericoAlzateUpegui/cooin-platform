"""
Advanced rate limiting middleware for the Cooin API.
Provides protection against abuse and ensures API stability.
"""

import time
from typing import Dict, Optional, Callable
from collections import defaultdict, deque
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import logging

logger = logging.getLogger(__name__)


class InMemoryRateLimiter:
    """In-memory rate limiter using sliding window algorithm."""

    def __init__(self):
        # Store request timestamps for each client
        self.requests: Dict[str, deque] = defaultdict(lambda: deque())
        self.blocked_until: Dict[str, float] = {}

    def is_allowed(
        self,
        identifier: str,
        limit: int,
        window_seconds: int,
        block_duration: int = 300  # 5 minutes default block
    ) -> tuple[bool, Optional[int]]:
        """
        Check if request is allowed using sliding window algorithm.

        Returns:
            tuple[bool, Optional[int]]: (is_allowed, retry_after_seconds)
        """
        current_time = time.time()

        # Check if client is currently blocked
        if identifier in self.blocked_until:
            if current_time < self.blocked_until[identifier]:
                retry_after = int(self.blocked_until[identifier] - current_time)
                return False, retry_after
            else:
                # Block period expired
                del self.blocked_until[identifier]

        # Get request history for this identifier
        request_times = self.requests[identifier]

        # Remove requests outside the time window
        cutoff_time = current_time - window_seconds
        while request_times and request_times[0] < cutoff_time:
            request_times.popleft()

        # Check if limit exceeded
        if len(request_times) >= limit:
            # Block the client
            self.blocked_until[identifier] = current_time + block_duration
            logger.warning(f"Rate limit exceeded for {identifier}. Blocked for {block_duration}s")
            return False, block_duration

        # Add current request
        request_times.append(current_time)
        return True, None

    def cleanup_old_entries(self):
        """Periodic cleanup of old entries to prevent memory leaks."""
        current_time = time.time()
        cutoff_time = current_time - 3600  # Clean entries older than 1 hour

        # Clean request histories
        for identifier in list(self.requests.keys()):
            request_times = self.requests[identifier]
            while request_times and request_times[0] < cutoff_time:
                request_times.popleft()

            # Remove empty deques
            if not request_times:
                del self.requests[identifier]

        # Clean expired blocks
        for identifier in list(self.blocked_until.keys()):
            if current_time >= self.blocked_until[identifier]:
                del self.blocked_until[identifier]


class RateLimitMiddleware(BaseHTTPMiddleware):
    """FastAPI middleware for rate limiting with different rules for different endpoints."""

    def __init__(self, app, rate_limiter: Optional[InMemoryRateLimiter] = None):
        super().__init__(app)
        self.rate_limiter = rate_limiter or InMemoryRateLimiter()

        # Check if we're in development mode
        from app.core.config import settings
        is_dev = settings.DEBUG or settings.ENVIRONMENT == 'development'

        # Define rate limits for different endpoint categories
        # In development: Use generous limits to avoid blocking legitimate testing
        # In production: Use strict limits for security
        if is_dev:
            self.rate_limits = {
                # Authentication endpoints - relaxed for testing
                'auth_register': {'limit': 20, 'window': 3600, 'block': 600},   # 20 per hour, block 10min
                'auth_login': {'limit': 50, 'window': 900, 'block': 300},       # 50 per 15min, block 5min
                'auth_refresh': {'limit': 100, 'window': 3600, 'block': 180},   # 100 per hour, block 3min

                # Profile endpoints - generous for development
                'profile_write': {'limit': 100, 'window': 3600, 'block': 180},  # 100 per hour
                'profile_read': {'limit': 300, 'window': 3600, 'block': 60},    # 300 per hour

                # Search endpoints - high limits for testing
                'search': {'limit': 200, 'window': 3600, 'block': 120},         # 200 per hour

                # Connection and messaging - very generous for development workflow
                'connections': {'limit': 500, 'window': 3600, 'block': 180},    # 500 per hour (dev)
                'messages': {'limit': 300, 'window': 3600, 'block': 120},       # 300 per hour

                # Default for other endpoints - very generous
                'default': {'limit': 1000, 'window': 3600, 'block': 60},        # 1000 per hour
            }
        else:
            # Production limits - strict for security
            self.rate_limits = {
                # Authentication endpoints - strict limits
                'auth_register': {'limit': 5, 'window': 3600, 'block': 1800},  # 5 per hour, block 30min
                'auth_login': {'limit': 10, 'window': 900, 'block': 600},      # 10 per 15min, block 10min
                'auth_refresh': {'limit': 20, 'window': 3600, 'block': 300},   # 20 per hour, block 5min

                # Profile endpoints - moderate limits
                'profile_write': {'limit': 30, 'window': 3600, 'block': 300},  # 30 per hour
                'profile_read': {'limit': 100, 'window': 3600, 'block': 60},   # 100 per hour

                # Search endpoints - higher limits but still controlled
                'search': {'limit': 60, 'window': 3600, 'block': 180},         # 60 per hour

                # Connection and messaging - moderate limits
                'connections': {'limit': 50, 'window': 3600, 'block': 300},    # 50 per hour
                'messages': {'limit': 100, 'window': 3600, 'block': 180},      # 100 per hour

                # Default for other endpoints
                'default': {'limit': 200, 'window': 3600, 'block': 60},        # 200 per hour
            }

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request through rate limiting."""

        # Get client identifier (IP + user if authenticated)
        client_id = self._get_client_identifier(request)

        # Determine rate limit category
        category = self._get_rate_limit_category(request)
        limit_config = self.rate_limits.get(category, self.rate_limits['default'])

        # Check rate limit
        is_allowed, retry_after = self.rate_limiter.is_allowed(
            identifier=f"{category}:{client_id}",
            limit=limit_config['limit'],
            window_seconds=limit_config['window'],
            block_duration=limit_config['block']
        )

        if not is_allowed:
            # Rate limit exceeded
            logger.warning(
                f"Rate limit exceeded for {client_id} on {request.url.path} "
                f"(category: {category})"
            )

            # Create rate limit response
            error_response = {
                "error": {
                    "code": "RATE_LIMIT_EXCEEDED",
                    "message": "Rate limit exceeded. Please slow down and try again later.",
                    "status_code": 429,
                    "retry_after_seconds": retry_after,
                    "category": category
                }
            }

            response = Response(
                content=str(error_response).replace("'", '"'),  # Basic JSON conversion
                status_code=429,
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Category": category,
                    "X-RateLimit-Limit": str(limit_config['limit']),
                    "X-RateLimit-Window": str(limit_config['window'])
                }
            )
            return response

        # Process request normally
        response = await call_next(request)

        # Add rate limit headers to response
        response.headers["X-RateLimit-Category"] = category
        response.headers["X-RateLimit-Limit"] = str(limit_config['limit'])
        response.headers["X-RateLimit-Window"] = str(limit_config['window'])

        return response

    def _get_client_identifier(self, request: Request) -> str:
        """Get unique identifier for the client."""
        # Get IP address
        client_ip = request.client.host if request.client else "unknown"

        # Try to get forwarded IP
        x_forwarded_for = request.headers.get('X-Forwarded-For')
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(',')[0].strip()

        x_real_ip = request.headers.get('X-Real-IP')
        if x_real_ip:
            client_ip = x_real_ip

        # Try to get user ID from JWT token if available
        auth_header = request.headers.get('Authorization', '')
        user_part = ""

        if auth_header.startswith('Bearer '):
            try:
                # Basic JWT parsing without verification (just for user ID extraction)
                token = auth_header[7:]  # Remove 'Bearer '
                import base64
                import json

                # Split token and decode payload (second part)
                parts = token.split('.')
                if len(parts) >= 2:
                    # Add padding if needed
                    payload = parts[1]
                    payload += '=' * (4 - len(payload) % 4)

                    decoded = base64.urlsafe_b64decode(payload)
                    payload_data = json.loads(decoded)

                    if 'sub' in payload_data:
                        user_part = f":user_{payload_data['sub']}"

            except Exception:
                # If JWT parsing fails, just use IP
                pass

        return f"{client_ip}{user_part}"

    def _get_rate_limit_category(self, request: Request) -> str:
        """Determine the rate limit category based on the request path and method."""
        path = request.url.path.lower()
        method = request.method.upper()

        # Authentication endpoints
        if '/auth/register' in path:
            return 'auth_register'
        elif '/auth/login' in path:
            return 'auth_login'
        elif '/auth/refresh' in path:
            return 'auth_refresh'

        # Profile endpoints
        elif '/profiles/' in path:
            if method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                return 'profile_write'
            else:
                return 'profile_read'

        # Search endpoints
        elif '/search' in path or (path.endswith('/profiles') and 'role=' in str(request.query_params)):
            return 'search'

        # Connection endpoints
        elif '/connections' in path:
            return 'connections'

        # Message endpoints
        elif '/messages' in path or 'message' in path:
            return 'messages'

        # Default category
        return 'default'


# Global rate limiter instance
_rate_limiter = InMemoryRateLimiter()

def get_rate_limiter() -> InMemoryRateLimiter:
    """Get the global rate limiter instance."""
    return _rate_limiter


def create_rate_limit_middleware(app):
    """Create and return rate limiting middleware."""
    return RateLimitMiddleware(app, _rate_limiter)


# Periodic cleanup function (can be called by a background task)
def cleanup_rate_limiter():
    """Clean up old rate limiter entries."""
    global _rate_limiter
    _rate_limiter.cleanup_old_entries()
    logger.info("Rate limiter cleanup completed")


# Decorator for additional rate limiting on specific endpoints
def rate_limit(limit: int, window_seconds: int, block_duration: int = 300):
    """
    Decorator for additional rate limiting on specific endpoints.

    Args:
        limit: Number of requests allowed
        window_seconds: Time window in seconds
        block_duration: How long to block after limit exceeded
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # This would need to be implemented with access to the request object
            # For now, we'll rely on the middleware for rate limiting
            return await func(*args, **kwargs)
        return wrapper
    return decorator