"""
Security monitoring and alerting service.
Tracks security events and provides alerting mechanisms.
"""

import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum
import logging
from dataclasses import dataclass, asdict

from app.core.cache import get_cache_service
from app.core.config import settings

logger = logging.getLogger(__name__)


class SecurityEventType(Enum):
    """Types of security events to monitor."""
    SUSPICIOUS_REQUEST = "suspicious_request"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    AUTHENTICATION_FAILURE = "auth_failure"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    FILE_UPLOAD_THREAT = "file_upload_threat"
    SQL_INJECTION_ATTEMPT = "sql_injection_attempt"
    XSS_ATTEMPT = "xss_attempt"
    BRUTE_FORCE_ATTACK = "brute_force_attack"
    ACCOUNT_TAKEOVER = "account_takeover"
    DATA_EXFILTRATION = "data_exfiltration"


class SecurityLevel(Enum):
    """Security event severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SecurityEvent:
    """Represents a security event."""
    event_type: SecurityEventType
    severity: SecurityLevel
    timestamp: datetime
    source_ip: str
    user_id: Optional[int] = None
    endpoint: Optional[str] = None
    user_agent: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    resolved: bool = False


class SecurityMonitoringService:
    """Service for monitoring and alerting on security events."""

    def __init__(self):
        self.cache = get_cache_service()

        # Security thresholds
        self.thresholds = {
            SecurityEventType.AUTHENTICATION_FAILURE: {
                "count": 5,
                "window_minutes": 5,
                "escalation_level": SecurityLevel.MEDIUM
            },
            SecurityEventType.SUSPICIOUS_REQUEST: {
                "count": 3,
                "window_minutes": 10,
                "escalation_level": SecurityLevel.HIGH
            },
            SecurityEventType.RATE_LIMIT_EXCEEDED: {
                "count": 10,
                "window_minutes": 15,
                "escalation_level": SecurityLevel.MEDIUM
            },
            SecurityEventType.SQL_INJECTION_ATTEMPT: {
                "count": 1,
                "window_minutes": 1,
                "escalation_level": SecurityLevel.CRITICAL
            },
            SecurityEventType.XSS_ATTEMPT: {
                "count": 1,
                "window_minutes": 1,
                "escalation_level": SecurityLevel.HIGH
            }
        }

        # Alert channels (in production, integrate with external services)
        self.alert_handlers = {
            SecurityLevel.LOW: self._log_alert,
            SecurityLevel.MEDIUM: self._log_alert,
            SecurityLevel.HIGH: self._critical_alert,
            SecurityLevel.CRITICAL: self._critical_alert
        }

    async def log_security_event(
        self,
        event_type: SecurityEventType,
        severity: SecurityLevel,
        source_ip: str,
        user_id: Optional[int] = None,
        endpoint: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> SecurityEvent:
        """Log a security event and check for patterns."""

        event = SecurityEvent(
            event_type=event_type,
            severity=severity,
            timestamp=datetime.utcnow(),
            source_ip=source_ip,
            user_id=user_id,
            endpoint=endpoint,
            user_agent=user_agent,
            details=details or {}
        )

        # Store event in cache for pattern analysis
        await self._store_event(event)

        # Check for concerning patterns
        await self._analyze_patterns(event)

        # Log the event
        logger.warning(
            f"Security event: {event_type.value}",
            extra={
                "security_event": asdict(event),
                "severity": severity.value,
                "source_ip": source_ip
            }
        )

        return event

    async def _store_event(self, event: SecurityEvent):
        """Store security event for pattern analysis."""
        try:
            # Create cache keys for different analysis dimensions
            keys = [
                f"security:events:ip:{event.source_ip}",
                f"security:events:type:{event.event_type.value}",
                f"security:events:endpoint:{event.endpoint}" if event.endpoint else None,
                f"security:events:user:{event.user_id}" if event.user_id else None
            ]

            # Remove None keys
            keys = [k for k in keys if k is not None]

            # Store event data
            event_data = {
                "timestamp": event.timestamp.isoformat(),
                "type": event.event_type.value,
                "severity": event.severity.value,
                "details": event.details
            }

            # Add to each relevant list (expire after 24 hours)
            for key in keys:
                # Get existing events
                existing_events = await self.cache.get(key) or []

                # Add new event
                existing_events.append(event_data)

                # Keep only events from last 24 hours
                cutoff_time = datetime.utcnow() - timedelta(hours=24)
                existing_events = [
                    e for e in existing_events
                    if datetime.fromisoformat(e["timestamp"]) > cutoff_time
                ]

                # Store updated list
                await self.cache.set(key, existing_events, 86400)  # 24 hours

        except Exception as e:
            logger.error(f"Error storing security event: {e}")

    async def _analyze_patterns(self, event: SecurityEvent):
        """Analyze security event patterns and trigger alerts."""
        try:
            # Get threshold configuration
            threshold_config = self.thresholds.get(event.event_type)
            if not threshold_config:
                return

            # Get recent events of the same type from same IP
            key = f"security:events:ip:{event.source_ip}"
            recent_events = await self.cache.get(key) or []

            # Filter by event type and time window
            cutoff_time = datetime.utcnow() - timedelta(minutes=threshold_config["window_minutes"])
            matching_events = [
                e for e in recent_events
                if (e["type"] == event.event_type.value and
                    datetime.fromisoformat(e["timestamp"]) > cutoff_time)
            ]

            # Check if threshold exceeded
            if len(matching_events) >= threshold_config["count"]:
                await self._trigger_alert(
                    event_type=event.event_type,
                    severity=threshold_config["escalation_level"],
                    source_ip=event.source_ip,
                    event_count=len(matching_events),
                    time_window=threshold_config["window_minutes"]
                )

        except Exception as e:
            logger.error(f"Error analyzing security patterns: {e}")

    async def _trigger_alert(
        self,
        event_type: SecurityEventType,
        severity: SecurityLevel,
        source_ip: str,
        event_count: int,
        time_window: int
    ):
        """Trigger security alert."""
        alert_data = {
            "event_type": event_type.value,
            "severity": severity.value,
            "source_ip": source_ip,
            "event_count": event_count,
            "time_window_minutes": time_window,
            "timestamp": datetime.utcnow().isoformat()
        }

        # Call appropriate alert handler
        handler = self.alert_handlers.get(severity, self._log_alert)
        await handler(alert_data)

        # Store alert to prevent duplicate notifications
        alert_key = f"security:alert:{event_type.value}:{source_ip}"
        await self.cache.set(alert_key, alert_data, 3600)  # 1 hour

    async def _log_alert(self, alert_data: dict):
        """Log security alert."""
        logger.error(
            f"SECURITY ALERT: {alert_data['event_type']} from {alert_data['source_ip']}",
            extra={"security_alert": alert_data}
        )

    async def _critical_alert(self, alert_data: dict):
        """Handle critical security alerts."""
        # Log the alert
        await self._log_alert(alert_data)

        # In production, integrate with external alerting systems:
        # - Send email notifications
        # - Post to Slack/Teams
        # - Create incident in PagerDuty
        # - Trigger automated blocking rules

        logger.critical(
            f"CRITICAL SECURITY INCIDENT: {alert_data['event_type']} "
            f"from {alert_data['source_ip']} - IMMEDIATE ATTENTION REQUIRED"
        )

    async def get_security_dashboard_data(self, hours: int = 24) -> Dict[str, Any]:
        """Get security dashboard data for monitoring."""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)

            # Get all security event keys
            event_keys = await self.cache.keys_pattern("security:events:*")

            dashboard_data = {
                "time_range_hours": hours,
                "total_events": 0,
                "events_by_type": {},
                "events_by_severity": {},
                "top_source_ips": {},
                "recent_alerts": [],
                "generated_at": datetime.utcnow().isoformat()
            }

            # Analyze events
            for key in event_keys:
                events = await self.cache.get(key) or []

                for event in events:
                    event_time = datetime.fromisoformat(event["timestamp"])
                    if event_time < cutoff_time:
                        continue

                    dashboard_data["total_events"] += 1

                    # Count by type
                    event_type = event["type"]
                    dashboard_data["events_by_type"][event_type] = (
                        dashboard_data["events_by_type"].get(event_type, 0) + 1
                    )

                    # Count by severity
                    severity = event["severity"]
                    dashboard_data["events_by_severity"][severity] = (
                        dashboard_data["events_by_severity"].get(severity, 0) + 1
                    )

            # Get recent alerts
            alert_keys = await self.cache.keys_pattern("security:alert:*")
            for key in alert_keys:
                alert = await self.cache.get(key)
                if alert:
                    dashboard_data["recent_alerts"].append(alert)

            # Sort alerts by timestamp
            dashboard_data["recent_alerts"].sort(
                key=lambda x: x["timestamp"], reverse=True
            )
            dashboard_data["recent_alerts"] = dashboard_data["recent_alerts"][:10]

            return dashboard_data

        except Exception as e:
            logger.error(f"Error generating security dashboard data: {e}")
            return {
                "error": str(e),
                "generated_at": datetime.utcnow().isoformat()
            }

    async def block_ip_address(self, ip_address: str, duration_hours: int = 24, reason: str = "Security violation") -> bool:
        """Block an IP address for a specified duration."""
        try:
            block_data = {
                "ip_address": ip_address,
                "blocked_at": datetime.utcnow().isoformat(),
                "duration_hours": duration_hours,
                "reason": reason,
                "expires_at": (datetime.utcnow() + timedelta(hours=duration_hours)).isoformat()
            }

            # Store block
            block_key = f"security:blocked_ip:{ip_address}"
            await self.cache.set(block_key, block_data, duration_hours * 3600)

            logger.warning(f"IP address {ip_address} blocked for {duration_hours} hours. Reason: {reason}")
            return True

        except Exception as e:
            logger.error(f"Error blocking IP address {ip_address}: {e}")
            return False

    async def is_ip_blocked(self, ip_address: str) -> tuple[bool, Optional[dict]]:
        """Check if an IP address is blocked."""
        try:
            block_key = f"security:blocked_ip:{ip_address}"
            block_data = await self.cache.get(block_key)
            return block_data is not None, block_data
        except Exception as e:
            logger.error(f"Error checking IP block status for {ip_address}: {e}")
            return False, None

    async def unblock_ip_address(self, ip_address: str) -> bool:
        """Manually unblock an IP address."""
        try:
            block_key = f"security:blocked_ip:{ip_address}"
            success = await self.cache.delete(block_key)
            if success:
                logger.info(f"IP address {ip_address} manually unblocked")
            return success
        except Exception as e:
            logger.error(f"Error unblocking IP address {ip_address}: {e}")
            return False


# Global security monitoring service instance
_security_monitoring_service: Optional[SecurityMonitoringService] = None


def get_security_monitoring_service() -> SecurityMonitoringService:
    """Get security monitoring service instance."""
    global _security_monitoring_service
    if _security_monitoring_service is None:
        _security_monitoring_service = SecurityMonitoringService()
    return _security_monitoring_service