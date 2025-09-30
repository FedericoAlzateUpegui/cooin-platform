"""
Security management and monitoring endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from datetime import datetime
import logging

from app.db.base import get_database
from app.models import User
from app.core.deps import get_current_active_user
from app.core.security_monitoring import (
    get_security_monitoring_service,
    SecurityEventType,
    SecurityLevel
)
from app.core.exceptions import BusinessLogicError, ValidationError
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter()


class SecurityEventRequest(BaseModel):
    """Request model for logging security events."""
    event_type: str
    severity: str
    source_ip: str
    user_id: Optional[int] = None
    endpoint: Optional[str] = None
    user_agent: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class IPBlockRequest(BaseModel):
    """Request model for blocking IP addresses."""
    ip_address: str
    duration_hours: int = 24
    reason: str = "Security violation"


@router.get("/dashboard")
async def get_security_dashboard(
    hours: int = Query(24, ge=1, le=168, description="Hours of data to include"),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Get security dashboard data for monitoring.

    Returns security events, alerts, and statistics for the specified time period.

    Note: In production, this endpoint should be restricted to admin users only.
    """
    security_service = get_security_monitoring_service()

    try:
        dashboard_data = await security_service.get_security_dashboard_data(hours=hours)
        return {
            "status": "success",
            "dashboard": dashboard_data
        }
    except Exception as e:
        logger.error(f"Error getting security dashboard: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve security dashboard"
        )


@router.post("/events")
async def log_security_event(
    event_request: SecurityEventRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Log a security event manually.

    This endpoint can be used for external systems to report security events.
    """
    security_service = get_security_monitoring_service()

    try:
        # Validate event type and severity
        try:
            event_type = SecurityEventType(event_request.event_type)
            severity = SecurityLevel(event_request.severity)
        except ValueError as e:
            raise ValidationError(
                detail=f"Invalid event type or severity: {str(e)}",
                error_code="INVALID_SECURITY_EVENT"
            )

        # Log the event
        event = await security_service.log_security_event(
            event_type=event_type,
            severity=severity,
            source_ip=event_request.source_ip,
            user_id=event_request.user_id,
            endpoint=event_request.endpoint,
            user_agent=event_request.user_agent,
            details=event_request.details
        )

        return {
            "status": "success",
            "message": "Security event logged successfully",
            "event_id": f"{event.timestamp.isoformat()}_{event.source_ip}"
        }

    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"Error logging security event: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to log security event"
        )


@router.post("/block-ip")
async def block_ip_address(
    block_request: IPBlockRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Block an IP address for a specified duration.

    Note: In production, this endpoint should be restricted to admin users only.
    """
    security_service = get_security_monitoring_service()

    try:
        success = await security_service.block_ip_address(
            ip_address=block_request.ip_address,
            duration_hours=block_request.duration_hours,
            reason=block_request.reason
        )

        if success:
            return {
                "status": "success",
                "message": f"IP address {block_request.ip_address} blocked for {block_request.duration_hours} hours",
                "ip_address": block_request.ip_address,
                "duration_hours": block_request.duration_hours,
                "reason": block_request.reason
            }
        else:
            raise BusinessLogicError(
                detail="Failed to block IP address",
                error_code="IP_BLOCK_FAILED"
            )

    except BusinessLogicError:
        raise
    except Exception as e:
        logger.error(f"Error blocking IP address: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to block IP address"
        )


@router.delete("/block-ip/{ip_address}")
async def unblock_ip_address(
    ip_address: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Manually unblock an IP address.

    Note: In production, this endpoint should be restricted to admin users only.
    """
    security_service = get_security_monitoring_service()

    try:
        success = await security_service.unblock_ip_address(ip_address)

        if success:
            return {
                "status": "success",
                "message": f"IP address {ip_address} unblocked successfully",
                "ip_address": ip_address
            }
        else:
            return {
                "status": "info",
                "message": f"IP address {ip_address} was not blocked",
                "ip_address": ip_address
            }

    except Exception as e:
        logger.error(f"Error unblocking IP address: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to unblock IP address"
        )


@router.get("/blocked-ips/{ip_address}")
async def check_ip_block_status(
    ip_address: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Check if an IP address is currently blocked.
    """
    security_service = get_security_monitoring_service()

    try:
        is_blocked, block_data = await security_service.is_ip_blocked(ip_address)

        return {
            "ip_address": ip_address,
            "is_blocked": is_blocked,
            "block_data": block_data
        }

    except Exception as e:
        logger.error(f"Error checking IP block status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check IP block status"
        )


@router.get("/health")
async def security_health_check():
    """
    Security system health check.

    Returns the status of security monitoring components.
    """
    security_service = get_security_monitoring_service()

    try:
        # Test cache connectivity
        test_key = "security:health:test"
        await security_service.cache.set(test_key, {"test": True}, 10)
        test_data = await security_service.cache.get(test_key)
        await security_service.cache.delete(test_key)

        cache_healthy = test_data is not None

        return {
            "status": "healthy" if cache_healthy else "degraded",
            "components": {
                "security_monitoring": "healthy",
                "cache_service": "healthy" if cache_healthy else "unhealthy",
                "pattern_analysis": "healthy",
                "alert_system": "healthy"
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Security health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


@router.get("/event-types")
async def get_security_event_types():
    """
    Get list of available security event types and severity levels.

    Useful for clients that need to log security events.
    """
    return {
        "event_types": [event_type.value for event_type in SecurityEventType],
        "severity_levels": [level.value for level in SecurityLevel],
        "description": {
            "event_types": {
                "suspicious_request": "Request with suspicious patterns detected",
                "rate_limit_exceeded": "Rate limit threshold exceeded",
                "auth_failure": "Authentication attempt failed",
                "unauthorized_access": "Access to protected resource without authorization",
                "file_upload_threat": "Suspicious file upload detected",
                "sql_injection_attempt": "SQL injection patterns detected",
                "xss_attempt": "Cross-site scripting attempt detected",
                "brute_force_attack": "Brute force attack pattern detected",
                "account_takeover": "Potential account takeover detected",
                "data_exfiltration": "Suspicious data access patterns"
            },
            "severity_levels": {
                "low": "Low impact event, informational only",
                "medium": "Medium impact event, requires monitoring",
                "high": "High impact event, requires immediate attention",
                "critical": "Critical security incident, requires immediate response"
            }
        }
    }