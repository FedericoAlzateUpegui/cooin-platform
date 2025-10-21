from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
import time

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

    # Security middleware stack (in reverse order of execution)
    # 1. Security headers (executed last, applied to all responses)
    app.add_middleware(SecurityHeadersMiddleware)

    # 2. Request logging for security monitoring
    app.add_middleware(RequestLoggingMiddleware)

    # 3. API security checks
    app.add_middleware(APISecurityMiddleware)

    # 4. Request validation and sanitization
    app.add_middleware(RequestValidationMiddleware)

    # 5. DDoS protection
    app.add_middleware(DDoSProtectionMiddleware)

    # 6. Trusted host middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "*.cooin.com"] if not settings.DEBUG else ["*"]
    )

    # 7. Rate limiting middleware (before CORS to catch requests early)
    app.add_middleware(RateLimitMiddleware)

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin).rstrip('/') for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
    )

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
            extra_data={"error_id": str(int(time.time()))}  # Simple error tracking
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


# Background task for rate limiter and cache cleanup
async def periodic_cleanup():
    """Periodically clean up rate limiter entries and cache to prevent memory leaks."""
    while True:
        await asyncio.sleep(1800)  # Run every 30 minutes
        try:
            cleanup_rate_limiter()

            # Clean up expired cache entries (mainly for memory cache)
            cache_service = get_app_cache_service()
            await cache_service.cleanup_expired_entries()

            logger.debug("Periodic cleanup completed successfully")
        except Exception as e:
            logger.error(f"Periodic cleanup failed: {e}")

# Event handlers
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"CORS origins: {settings.BACKEND_CORS_ORIGINS}")
    logger.info("Security middleware stack enabled:")
    logger.info("  - Security headers")
    logger.info("  - Request logging and monitoring")
    logger.info("  - API security validation")
    logger.info("  - Request sanitization")
    logger.info("  - DDoS protection")
    logger.info("  - Rate limiting")

    # Initialize cache
    try:
        await init_cache()
        logger.info("Cache service initialized successfully")
    except Exception as e:
        logger.warning(f"Cache initialization failed, using fallback: {e}")

    # Start background cleanup task
    asyncio.create_task(periodic_cleanup())
    logger.info("Started background cleanup tasks")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info(f"Shutting down {settings.PROJECT_NAME}")

    # Cleanup cache connections
    try:
        await cleanup_cache()
        logger.info("Cache connections closed")
    except Exception as e:
        logger.error(f"Error during cache cleanup: {e}")

    # Cleanup task will be automatically cancelled on shutdown


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )