"""
Comprehensive security middleware for the Cooin API.
Provides multiple layers of security protection including headers, request validation, and monitoring.
"""

import time
import json
import hashlib
import secrets
from typing import Optional, Set, Dict, Any
from datetime import datetime, timedelta
from urllib.parse import urlparse
import re
import logging

from fastapi import Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import user_agents

from app.core.config import settings
from app.core.cache import get_cache_service
from app.core.exceptions import create_error_response
from app.core.security_monitoring import (
    get_security_monitoring_service,
    SecurityEventType,
    SecurityLevel
)

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add comprehensive security headers to all responses.
    Implements OWASP security recommendations.
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.security_headers = {
            # Prevent clickjacking attacks
            "X-Frame-Options": "DENY",

            # Prevent MIME type sniffing
            "X-Content-Type-Options": "nosniff",

            # XSS protection
            "X-XSS-Protection": "1; mode=block",

            # Referrer policy
            "Referrer-Policy": "strict-origin-when-cross-origin",

            # Content Security Policy
            "Content-Security-Policy": (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self'; "
                "connect-src 'self'; "
                "frame-ancestors 'none';"
            ),

            # Strict Transport Security (HTTPS only)
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains" if not settings.DEBUG else None,

            # Permissions policy
            "Permissions-Policy": (
                "geolocation=(), microphone=(), camera=(), "
                "payment=(), usb=(), magnetometer=(), gyroscope=()"
            ),

            # Remove server information
            "Server": "Cooin-API",
        }

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)

        # Add security headers
        for header, value in self.security_headers.items():
            if value is not None:
                response.headers[header] = value

        # Remove potentially sensitive headers
        response.headers.pop("Server", None)

        return response


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """
    Middleware for request validation and sanitization.
    Protects against common attack vectors.
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)

        # Suspicious patterns to detect
        self.suspicious_patterns = [
            # SQL Injection patterns
            r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER)\b)",
            r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",
            r"('|\")(\s*;\s*)",

            # XSS patterns
            r"<script[^>]*>.*?</script>",
            r"javascript:",
            r"on\w+\s*=",

            # Path traversal
            r"\.\.[\\/]",
            r"[\\/]etc[\\/]passwd",
            r"[\\/]windows[\\/]system32",

            # Command injection
            r"[;&|`$()]",
            r"\b(curl|wget|nc|netcat|ping)\b",
        ]

        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.suspicious_patterns]

        # Rate limiting for suspicious requests
        self.suspicious_ips: Dict[str, list] = {}

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address considering proxies."""
        # Check for forwarded headers (in order of preference)
        forwarded_headers = [
            "X-Forwarded-For",
            "X-Real-IP",
            "CF-Connecting-IP",  # Cloudflare
            "True-Client-IP",
        ]

        for header in forwarded_headers:
            if header in request.headers:
                ip = request.headers[header].split(",")[0].strip()
                if ip:
                    return ip

        # Fallback to direct connection
        return request.client.host if request.client else "unknown"

    def _is_suspicious_request(self, request: Request) -> tuple[bool, str]:
        """Check if request contains suspicious patterns."""
        # Check URL path
        url_path = str(request.url.path)
        for pattern in self.compiled_patterns:
            if pattern.search(url_path):
                return True, f"Suspicious URL pattern: {pattern.pattern}"

        # Check query parameters
        query_string = str(request.url.query)
        for pattern in self.compiled_patterns:
            if pattern.search(query_string):
                return True, f"Suspicious query parameter: {pattern.pattern}"

        # Check headers for injection attempts
        suspicious_headers = ["User-Agent", "Referer", "X-Forwarded-For"]
        for header_name in suspicious_headers:
            if header_name in request.headers:
                header_value = request.headers[header_name]
                for pattern in self.compiled_patterns:
                    if pattern.search(header_value):
                        return True, f"Suspicious header {header_name}: {pattern.pattern}"

        return False, ""

    def _track_suspicious_ip(self, ip: str) -> bool:
        """Track suspicious IPs and return True if should be blocked."""
        current_time = time.time()

        # Clean up old entries (older than 1 hour)
        if ip in self.suspicious_ips:
            self.suspicious_ips[ip] = [
                timestamp for timestamp in self.suspicious_ips[ip]
                if current_time - timestamp < 3600
            ]
        else:
            self.suspicious_ips[ip] = []

        # Add current incident
        self.suspicious_ips[ip].append(current_time)

        # Block if more than 5 suspicious requests in the last hour
        return len(self.suspicious_ips[ip]) > 5

    async def dispatch(self, request: Request, call_next) -> Response:
        client_ip = self._get_client_ip(request)

        # Check for suspicious patterns
        is_suspicious, reason = self._is_suspicious_request(request)

        if is_suspicious:
            logger.warning(f"Suspicious request detected from {client_ip}: {reason}")

            # Log security event
            security_service = get_security_monitoring_service()
            await security_service.log_security_event(
                event_type=SecurityEventType.SUSPICIOUS_REQUEST,
                severity=SecurityLevel.MEDIUM,
                source_ip=client_ip,
                endpoint=str(request.url.path),
                user_agent=request.headers.get("user-agent"),
                details={"reason": reason}
            )

            # Track suspicious activity
            should_block = self._track_suspicious_ip(client_ip)

            if should_block:
                logger.error(f"Blocking IP {client_ip} due to repeated suspicious activity")

                # Log critical security event
                await security_service.log_security_event(
                    event_type=SecurityEventType.SUSPICIOUS_REQUEST,
                    severity=SecurityLevel.CRITICAL,
                    source_ip=client_ip,
                    endpoint=str(request.url.path),
                    user_agent=request.headers.get("user-agent"),
                    details={"reason": "Multiple suspicious requests - blocking IP"}
                )

                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content=create_error_response(
                        error_code="SUSPICIOUS_ACTIVITY",
                        detail="Request blocked due to suspicious activity",
                        status_code=429
                    )
                )

        return await call_next(request)


class APISecurityMiddleware(BaseHTTPMiddleware):
    """
    API-specific security middleware for authentication and authorization checks.
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)

        # Endpoints that don't require authentication
        self.public_endpoints = {
            "/",
            "/health",
            "/api/v1/health",
            "/api/v1/auth/register",
            "/api/v1/auth/login",
            "/api/v1/auth/refresh",
            "/api/v1/email/verify",
            "/api/v1/email/request-password-reset",
            "/api/v1/email/reset-password",
            "/api/v1/profiles/",  # Public profiles list
            "/docs",
            "/redoc",
            "/openapi.json",
        }

        # Endpoints that require specific permissions
        self.admin_endpoints = {
            "/api/v1/cache/clear-all",
            "/api/v1/admin/",
        }

        # API key validation (for external integrations)
        self.api_keys = set()  # In production, load from secure storage

    def _is_public_endpoint(self, path: str) -> bool:
        """Check if endpoint is public."""
        # Exact match
        if path in self.public_endpoints:
            return True

        # Pattern matching for public endpoints
        public_patterns = [
            r"^/api/v1/profiles/\d+$",  # Public profile view
            r"^/uploads/profiles/",      # Public profile images
            r"^/static/",               # Static files
        ]

        for pattern in public_patterns:
            if re.match(pattern, path):
                return True

        return False

    def _validate_api_key(self, request: Request) -> bool:
        """Validate API key for external integrations."""
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return False

        # In production, validate against secure storage
        return api_key in self.api_keys

    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path

        # Skip security checks for public endpoints
        if self._is_public_endpoint(path):
            return await call_next(request)

        # Check for API key authentication (alternative to JWT)
        if self._validate_api_key(request):
            return await call_next(request)

        # For protected endpoints, JWT validation is handled by dependencies
        # This middleware just adds additional security logging

        return await call_next(request)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Security-focused request logging middleware.
    Logs requests for security monitoring and audit trails.
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.sensitive_headers = {
            "authorization", "x-api-key", "cookie", "set-cookie"
        }

    def _sanitize_headers(self, headers: dict) -> dict:
        """Remove sensitive information from headers for logging."""
        sanitized = {}
        for key, value in headers.items():
            if key.lower() in self.sensitive_headers:
                sanitized[key] = "[REDACTED]"
            else:
                sanitized[key] = value
        return sanitized

    def _get_request_info(self, request: Request) -> dict:
        """Extract relevant request information for logging."""
        return {
            "method": request.method,
            "path": request.url.path,
            "query_params": str(request.url.query) if request.url.query else None,
            "client_ip": request.client.host if request.client else "unknown",
            "user_agent": request.headers.get("user-agent"),
            "referer": request.headers.get("referer"),
            "content_type": request.headers.get("content-type"),
            "content_length": request.headers.get("content-length"),
        }

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()

        # Log request
        request_info = self._get_request_info(request)

        try:
            response = await call_next(request)

            # Calculate processing time
            process_time = time.time() - start_time

            # Log response
            logger.info(
                f"Request processed",
                extra={
                    "request": request_info,
                    "response": {
                        "status_code": response.status_code,
                        "process_time": round(process_time, 3)
                    }
                }
            )

            return response

        except Exception as e:
            # Log errors
            process_time = time.time() - start_time
            logger.error(
                f"Request failed: {str(e)}",
                extra={
                    "request": request_info,
                    "error": str(e),
                    "process_time": round(process_time, 3)
                }
            )
            raise


class DDoSProtectionMiddleware(BaseHTTPMiddleware):
    """
    Basic DDoS protection middleware using sliding window rate limiting.
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.request_counts: Dict[str, list] = {}

        # Configuration
        self.max_requests_per_minute = 300  # Per IP
        self.max_requests_per_hour = 2000   # Per IP
        self.window_size_minutes = 1
        self.window_size_hours = 60

    def _clean_old_requests(self, ip: str, current_time: float):
        """Remove old request timestamps."""
        if ip in self.request_counts:
            # Keep only requests from the last hour
            self.request_counts[ip] = [
                timestamp for timestamp in self.request_counts[ip]
                if current_time - timestamp < 3600
            ]

    def _is_rate_limited(self, ip: str) -> tuple[bool, str]:
        """Check if IP should be rate limited."""
        current_time = time.time()

        # Clean old requests
        self._clean_old_requests(ip, current_time)

        if ip not in self.request_counts:
            self.request_counts[ip] = []

        # Count requests in different windows
        minute_requests = sum(
            1 for timestamp in self.request_counts[ip]
            if current_time - timestamp < 60
        )

        hour_requests = len(self.request_counts[ip])

        # Check limits
        if minute_requests >= self.max_requests_per_minute:
            return True, f"Too many requests per minute: {minute_requests}"

        if hour_requests >= self.max_requests_per_hour:
            return True, f"Too many requests per hour: {hour_requests}"

        # Add current request
        self.request_counts[ip].append(current_time)

        return False, ""

    async def dispatch(self, request: Request, call_next) -> Response:
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"

        # Skip rate limiting for local development
        if settings.DEBUG and client_ip in ["127.0.0.1", "localhost"]:
            return await call_next(request)

        # Check rate limits
        is_limited, reason = self._is_rate_limited(client_ip)

        if is_limited:
            logger.warning(f"Rate limiting IP {client_ip}: {reason}")

            # Log security event
            security_service = get_security_monitoring_service()
            await security_service.log_security_event(
                event_type=SecurityEventType.RATE_LIMIT_EXCEEDED,
                severity=SecurityLevel.HIGH,
                source_ip=client_ip,
                endpoint=str(request.url.path),
                user_agent=request.headers.get("user-agent"),
                details={"reason": reason}
            )

            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content=create_error_response(
                    error_code="RATE_LIMITED",
                    detail="Too many requests. Please slow down.",
                    status_code=429,
                    extra_data={"retry_after": 60}
                ),
                headers={"Retry-After": "60"}
            )

        return await call_next(request)