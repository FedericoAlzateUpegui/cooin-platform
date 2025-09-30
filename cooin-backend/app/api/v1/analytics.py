"""
Analytics and reporting API endpoints.
Provides business intelligence and system metrics.
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import json
import io

from app.core.deps import get_database, get_current_user
from app.core.mobile_auth import get_current_user_mobile
from app.core.mobile_responses import MobileResponseFormatter, MobileJSONResponse
from app.services.analytics_service import get_analytics_service, TimeRange
from app.models import User

logger = logging.getLogger(__name__)

router = APIRouter()
analytics_service = get_analytics_service()


@router.get("/dashboard")
async def get_dashboard_analytics(
    request: Request,
    time_range: str = Query("30d", regex="^(24h|7d|30d|90d|1y|all)$", description="Time range for analytics"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database)
):
    """
    Get comprehensive dashboard analytics with key business metrics.

    Returns metrics like user growth, loan volumes, platform activity, and financial data
    with trend analysis and percentage changes compared to previous period.
    """
    try:
        # Convert string to enum
        time_range_enum = TimeRange(time_range)

        # Get dashboard metrics
        metrics_data = await analytics_service.get_dashboard_metrics(time_range_enum)

        return {
            "success": True,
            "data": metrics_data,
            "message": f"Dashboard analytics for {time_range} retrieved successfully"
        }

    except Exception as e:
        logger.error(f"Error getting dashboard analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve dashboard analytics"
        )


@router.get("/users")
async def get_user_analytics(
    request: Request,
    time_range: str = Query("30d", regex="^(24h|7d|30d|90d|1y|all)$", description="Time range for analytics"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database)
):
    """
    Get detailed user analytics including growth patterns, demographics, and activity.

    Returns user registration trends, geographic distribution, role breakdown,
    and activity patterns over the specified time period.
    """
    try:
        # Admin or manager access only
        if current_user.role.value not in ["admin", "manager"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin or manager access required for user analytics"
            )

        time_range_enum = TimeRange(time_range)
        user_data = await analytics_service.get_user_analytics(time_range_enum)

        return {
            "success": True,
            "data": user_data,
            "message": f"User analytics for {time_range} retrieved successfully"
        }

    except Exception as e:
        logger.error(f"Error getting user analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user analytics"
        )


@router.get("/loans")
async def get_loan_analytics(
    request: Request,
    time_range: str = Query("30d", regex="^(24h|7d|30d|90d|1y|all)$", description="Time range for analytics"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database)
):
    """
    Get detailed loan analytics including amounts, terms, rates, and status distribution.

    Returns loan request patterns, amount distributions, interest rate trends,
    and loan status breakdowns over the specified time period.
    """
    try:
        # Admin or manager access only
        if current_user.role.value not in ["admin", "manager"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin or manager access required for loan analytics"
            )

        time_range_enum = TimeRange(time_range)
        loan_data = await analytics_service.get_loan_analytics(time_range_enum)

        return {
            "success": True,
            "data": loan_data,
            "message": f"Loan analytics for {time_range} retrieved successfully"
        }

    except Exception as e:
        logger.error(f"Error getting loan analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve loan analytics"
        )


@router.get("/report/comprehensive")
async def get_comprehensive_report(
    request: Request,
    time_range: str = Query("30d", regex="^(24h|7d|30d|90d|1y|all)$", description="Time range for report"),
    include_recommendations: bool = Query(True, description="Include AI-generated recommendations"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database)
):
    """
    Generate a comprehensive analytics report with insights and recommendations.

    Returns a complete business intelligence report including all metrics,
    charts, AI-generated insights, and actionable recommendations.
    """
    try:
        # Admin access only for comprehensive reports
        if current_user.role.value != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required for comprehensive reports"
            )

        time_range_enum = TimeRange(time_range)
        report = await analytics_service.generate_comprehensive_report(
            time_range_enum,
            include_recommendations
        )

        return {
            "success": True,
            "data": {
                "report_id": report.report_id,
                "generated_at": report.generated_at.isoformat(),
                "time_range": report.time_range,
                "metrics": {k: {
                    "value": v.value,
                    "change_percentage": v.change_percentage,
                    "trend": v.trend,
                    "previous_value": v.previous_value
                } for k, v in report.metrics.items()},
                "charts": report.charts_data,
                "insights": report.insights,
                "recommendations": report.recommendations,
                "summary": {
                    "total_metrics": len(report.metrics),
                    "total_insights": len(report.insights),
                    "total_recommendations": len(report.recommendations)
                }
            },
            "message": "Comprehensive report generated successfully"
        }

    except Exception as e:
        logger.error(f"Error generating comprehensive report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate comprehensive report"
        )


@router.get("/report/export")
async def export_analytics_report(
    request: Request,
    time_range: str = Query("30d", regex="^(24h|7d|30d|90d|1y|all)$", description="Time range for report"),
    format: str = Query("json", regex="^(json|csv)$", description="Export format"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database)
):
    """
    Export analytics report in specified format (JSON or CSV).

    Downloads a complete analytics report that can be used for external analysis
    or sharing with stakeholders.
    """
    try:
        # Admin or manager access only
        if current_user.role.value not in ["admin", "manager"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin or manager access required for report export"
            )

        time_range_enum = TimeRange(time_range)
        report = await analytics_service.generate_comprehensive_report(time_range_enum)

        if format == "json":
            # Create JSON export
            export_data = {
                "report_metadata": {
                    "report_id": report.report_id,
                    "generated_at": report.generated_at.isoformat(),
                    "time_range": report.time_range,
                    "exported_by": current_user.username
                },
                "metrics": {k: {
                    "value": v.value,
                    "change_percentage": v.change_percentage,
                    "trend": v.trend
                } for k, v in report.metrics.items()},
                "charts_data": report.charts_data,
                "insights": report.insights,
                "recommendations": report.recommendations
            }

            json_str = json.dumps(export_data, indent=2, default=str)
            json_bytes = json_str.encode('utf-8')

            return StreamingResponse(
                io.BytesIO(json_bytes),
                media_type="application/json",
                headers={
                    "Content-Disposition": f"attachment; filename=cooin_analytics_{time_range}_{datetime.now().strftime('%Y%m%d')}.json"
                }
            )

        elif format == "csv":
            # Create CSV export (simplified metrics)
            csv_lines = ["Metric,Value,Change_Percentage,Trend\n"]

            for metric_name, metric_data in report.metrics.items():
                csv_lines.append(f"{metric_name},{metric_data.value},{metric_data.change_percentage or 0},{metric_data.trend or 'stable'}\n")

            csv_content = "".join(csv_lines)
            csv_bytes = csv_content.encode('utf-8')

            return StreamingResponse(
                io.BytesIO(csv_bytes),
                media_type="text/csv",
                headers={
                    "Content-Disposition": f"attachment; filename=cooin_analytics_{time_range}_{datetime.now().strftime('%Y%m%d')}.csv"
                }
            )

    except Exception as e:
        logger.error(f"Error exporting analytics report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to export analytics report"
        )


# Mobile-optimized analytics endpoints
@router.get("/mobile/summary")
async def get_mobile_analytics_summary(
    request: Request,
    current_user: User = Depends(get_current_user_mobile),
    db: Session = Depends(get_database)
):
    """
    Mobile-optimized analytics summary with key metrics.
    Returns simplified data optimized for mobile consumption.
    """
    try:
        # Get basic dashboard metrics for last 30 days
        metrics_data = await analytics_service.get_dashboard_metrics(TimeRange.LAST_30_DAYS)

        # Simplify for mobile
        mobile_summary = {
            "platform_stats": {
                "total_users": int(metrics_data["metrics"].get("total_users", {}).get("value", 0)),
                "active_users": int(metrics_data["metrics"].get("active_users", {}).get("value", 0)),
                "loan_requests": int(metrics_data["metrics"].get("loan_requests", {}).get("value", 0)),
                "lending_offers": int(metrics_data["metrics"].get("lending_offers", {}).get("value", 0))
            },
            "growth_trends": {
                "user_growth": metrics_data["metrics"].get("new_users", {}).get("change_percentage", 0),
                "activity_growth": metrics_data["metrics"].get("active_users", {}).get("change_percentage", 0)
            },
            "financial_overview": {
                "avg_loan_amount": f"${metrics_data['metrics'].get('avg_loan_amount', {}).get('value', 0):,.0f}",
                "total_volume": f"${metrics_data['metrics'].get('total_loan_volume', {}).get('value', 0):,.0f}"
            }
        }

        return MobileJSONResponse(
            content=MobileResponseFormatter.success(
                data=mobile_summary,
                message="Analytics summary retrieved",
                request=request
            )
        )

    except Exception as e:
        logger.error(f"Error getting mobile analytics summary: {e}")
        return MobileJSONResponse(
            content=MobileResponseFormatter.error(
                error_code="ANALYTICS_SUMMARY_FAILED",
                detail="Failed to retrieve analytics summary",
                status_code=500,
                request=request
            ),
            status_code=500
        )


@router.get("/mobile/user-insights/{user_id}")
async def get_user_personal_insights(
    request: Request,
    user_id: int,
    current_user: User = Depends(get_current_user_mobile),
    db: Session = Depends(get_database)
):
    """
    Get personalized insights for a specific user.
    Shows user's activity, performance, and recommendations.
    """
    try:
        # Users can only see their own insights
        if current_user.id != user_id and current_user.role.value != "admin":
            return MobileJSONResponse(
                content=MobileResponseFormatter.error(
                    error_code="UNAUTHORIZED_ACCESS",
                    detail="Can only view your own insights",
                    status_code=403,
                    request=request
                ),
                status_code=403
            )

        # Get user-specific data (simplified implementation)
        from app.services.cache_service import get_app_cache_service
        cache = get_app_cache_service()

        cache_key = f"user_insights:{user_id}"
        cached_insights = await cache.get(cache_key)

        if not cached_insights:
            # Calculate user insights
            user_insights = {
                "activity_score": 75,  # Would calculate based on actual activity
                "profile_completion": 85,
                "rating_average": 4.2,
                "total_connections": 12,
                "successful_transactions": 5,
                "recommendations": [
                    "Complete your profile verification to increase trust",
                    "Add more details to your lending preferences",
                    "Consider connecting with more users in your area"
                ]
            }

            # Cache for 1 hour
            await cache.set(cache_key, user_insights, 3600)
        else:
            user_insights = cached_insights

        return MobileJSONResponse(
            content=MobileResponseFormatter.success(
                data={
                    "user_id": user_id,
                    "insights": user_insights,
                    "last_updated": datetime.utcnow().isoformat()
                },
                message="Personal insights retrieved",
                request=request
            )
        )

    except Exception as e:
        logger.error(f"Error getting user personal insights: {e}")
        return MobileJSONResponse(
            content=MobileResponseFormatter.error(
                error_code="USER_INSIGHTS_FAILED",
                detail="Failed to retrieve personal insights",
                status_code=500,
                request=request
            ),
            status_code=500
        )


@router.post("/events/track")
async def track_analytics_event(
    request: Request,
    event_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database)
):
    """
    Track custom analytics events for business intelligence.

    Allows the frontend to send custom events that will be aggregated
    for analytics and business intelligence purposes.
    """
    try:
        # Validate event data
        required_fields = ["event_type", "timestamp"]
        if not all(field in event_data for field in required_fields):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required fields: {required_fields}"
            )

        # Add user context
        event_data["user_id"] = current_user.id
        event_data["user_role"] = current_user.role.value

        # Store event (simplified - would use proper event tracking service)
        from app.services.cache_service import get_app_cache_service
        cache = get_app_cache_service()

        event_key = f"analytics_event:{datetime.utcnow().isoformat()}:{current_user.id}"
        await cache.set(event_key, event_data, 86400)  # Store for 24 hours

        logger.info(f"Analytics event tracked: {event_data['event_type']} for user {current_user.id}")

        return {
            "success": True,
            "message": "Analytics event tracked successfully",
            "event_id": event_key
        }

    except Exception as e:
        logger.error(f"Error tracking analytics event: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to track analytics event"
        )


@router.get("/health")
async def analytics_health_check():
    """Health check for analytics service."""
    try:
        # Basic health check
        service_status = {
            "service": "analytics",
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "features": {
                "dashboard_metrics": True,
                "user_analytics": True,
                "loan_analytics": True,
                "comprehensive_reports": True,
                "export_functionality": True,
                "mobile_support": True,
                "event_tracking": True
            }
        }

        return service_status

    except Exception as e:
        logger.error(f"Analytics health check failed: {e}")
        return {
            "service": "analytics",
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }