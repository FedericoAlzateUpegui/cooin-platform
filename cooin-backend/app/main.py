from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
import time
import re

from app.core.config import settings
from app.api.v1.api import api_router
from app.core.exceptions import (
    CooinException,
    ValidationError,
    create_error_response,
    format_validation_errors
)
from app.core.rate_limiting import RateLimitMiddleware, get_rate_limiter, cleanup_rate_limiter
from app.core.cache import init_cache, cleanup_cache
from app.services.cache_service import get_app_cache_service
from app.core.security_middleware import (
    SecurityHeadersMiddleware,
    RequestValidationMiddleware,
    APISecurityMiddleware,
    RequestLoggingMiddleware,
    DDoSProtectionMiddleware
)
import asyncio

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description="Cooin - A matching/connection platform with financial elements",
        openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.DEBUG else None,
        docs_url=f"{settings.API_V1_STR}/docs" if settings.DEBUG else None,
        redoc_url=f"{settings.API_V1_STR}/redoc" if settings.DEBUG else None,
    )

    # CORS middleware - MUST be added first to handle preflight OPTIONS requests
    # Use regex to match origins with or without trailing slash
    cors_origins_regex = '|'.join([
        re.escape(str(origin).rstrip('/')) + '/?'
        for origin in settings.BACKEND_CORS_ORIGINS
    ])
    
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=cors_origins_regex,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
    )

    # Environment-aware Security Middleware Stack
    # Security headers (always enabled, adjusted for environment)
    if settings.ENABLE_SECURITY_HEADERS:
        app.add_middleware(SecurityHeadersMiddleware)
        logger.info(f"SecurityHeadersMiddleware enabled (env: {settings.ENVIRONMENT})")

    # Request logging (enabled in all environments, level varies)
    if settings.ENABLE_SECURITY_LOGGING:
        app.add_middleware(RequestLoggingMiddleware)
        logger.info(f"RequestLoggingMiddleware enabled (env: {settings.ENVIRONMENT})")

    # API security (enabled in all environments)
    app.add_middleware(APISecurityMiddleware)
    logger.info(f"APISecurityMiddleware enabled (env: {settings.ENVIRONMENT})")

    # Request validation (enabled in all environments)
    if settings.ENABLE_REQUEST_VALIDATION:
        app.add_middleware(RequestValidationMiddleware)
        logger.info(f"RequestValidationMiddleware enabled (env: {settings.ENVIRONMENT})")

    # DDoS protection (relaxed in development, strict in production)
    if settings.ENABLE_DDOS_PROTECTION:
        app.add_middleware(DDoSProtectionMiddleware)
        logger.info(f"DDoSProtectionMiddleware enabled (env: {settings.ENVIRONMENT})")

    # Rate limiting (relaxed in development, strict in production)
    if settings.ENABLE_RATE_LIMITING:
        app.add_middleware(RateLimitMiddleware)
        logger.info(f"RateLimitMiddleware enabled (env: {settings.ENVIRONMENT})")

    # Trusted Host Middleware (relaxed in development, strict in production)
    if settings.is_production:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["app.cooin.com", "www.cooin.com", "api.cooin.com"]
        )
        logger.info("TrustedHostMiddleware enabled (production mode)")
    elif settings.DEBUG:
        # In development, allow all hosts
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
        logger.info("TrustedHostMiddleware enabled (development mode - all hosts allowed)")

    # Add request timing middleware
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    # Custom exception handlers
    @app.exception_handler(CooinException)
    async def cooin_exception_handler(request: Request, exc: CooinException):
        """Handle custom Cooin exceptions with structured responses."""
        response_content = create_error_response(
            error_code=exc.error_code or "UNKNOWN_ERROR",
            detail=exc.detail,
            status_code=exc.status_code,
            extra_data=exc.extra_data
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=response_content
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle Pydantic validation errors with user-friendly messages."""
        formatted_errors = format_validation_errors(exc.errors())
        response_content = create_error_response(
            error_code="VALIDATION_ERROR",
            detail="Please check your input data and try again",
            status_code=422,
            field_errors=formatted_errors
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=response_content
        )

    @app.exception_handler(500)
    async def internal_server_error_handler(request: Request, exc: Exception):
        """Handle unexpected server errors."""
        logger.error(f"Internal server error: {exc}", exc_info=True)
        response_content = create_error_response(
            error_code="INTERNAL_SERVER_ERROR",
            detail="An unexpected error occurred. Please try again later.",
            status_code=500,
            extra_data={"error_id": str(int(time.time()))}
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=response_content
        )

    # Include API routes
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


# Create the FastAPI app instance
app = create_application()


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "message": "Welcome to Cooin API",
        "version": settings.PROJECT_VERSION,
        "status": "healthy",
        "docs_url": f"{settings.API_V1_STR}/docs" if settings.DEBUG else None
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": settings.PROJECT_VERSION
    }


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting up Cooin API...")

    # Initialize cache service (will fall back to in-memory if Redis unavailable)
    await init_cache()
    logger.info("Cache service initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup services on shutdown."""
    logger.info("Shutting down Cooin API...")

    # Cleanup cache service
    await cleanup_cache()
    logger.info("Cache service cleaned up")


# B