"""
Comprehensive analytics and reporting service.
Tracks business metrics, user behavior, and system performance.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import json

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc, text

from app.models import (
    User, UserProfile, LoanRequest, LendingOffer, Connection,
    UserRating, LoanTransaction, SecurityEvent
)
from app.core.config import settings
from app.services.cache_service import get_app_cache_service

logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of metrics we track."""
    USER_REGISTRATION = "user_registration"
    USER_ACTIVITY = "user_activity"
    LOAN_REQUESTS = "loan_requests"
    LENDING_OFFERS = "lending_offers"
    MATCHES_GENERATED = "matches_generated"
    CONNECTIONS_MADE = "connections_made"
    TRANSACTIONS_COMPLETED = "transactions_completed"
    SECURITY_EVENTS = "security_events"
    API_USAGE = "api_usage"
    MOBILE_USAGE = "mobile_usage"


class TimeRange(Enum):
    """Time ranges for analytics."""
    LAST_24_HOURS = "24h"
    LAST_7_DAYS = "7d"
    LAST_30_DAYS = "30d"
    LAST_90_DAYS = "90d"
    LAST_YEAR = "1y"
    ALL_TIME = "all"


@dataclass
class MetricData:
    """Container for metric data."""
    value: float
    change_percentage: Optional[float] = None
    trend: Optional[str] = None  # "up", "down", "stable"
    previous_value: Optional[float] = None


@dataclass
class AnalyticsReport:
    """Container for analytics report data."""
    report_id: str
    generated_at: datetime
    time_range: str
    metrics: Dict[str, MetricData]
    charts_data: Dict[str, List[Dict]]
    insights: List[str]
    recommendations: List[str]


class AnalyticsService:
    """Comprehensive analytics and reporting service."""

    def __init__(self):
        self.cache = get_app_cache_service()

    async def get_dashboard_metrics(
        self,
        time_range: TimeRange = TimeRange.LAST_30_DAYS,
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get key dashboard metrics with trend analysis."""

        cache_key = f"dashboard_metrics:{time_range.value}:{user_id or 'all'}"
        cached_data = await self.cache.get(cache_key)
        if cached_data:
            return cached_data

        # Calculate date range
        end_date = datetime.utcnow()
        start_date = self._get_start_date(end_date, time_range)
        previous_start_date = start_date - (end_date - start_date)

        metrics = {}

        # User metrics
        metrics.update(await self._get_user_metrics(start_date, end_date, previous_start_date))

        # Loan metrics
        metrics.update(await self._get_loan_metrics(start_date, end_date, previous_start_date))

        # Platform metrics
        metrics.update(await self._get_platform_metrics(start_date, end_date, previous_start_date))

        # Financial metrics
        metrics.update(await self._get_financial_metrics(start_date, end_date, previous_start_date))

        result = {
            "time_range": time_range.value,
            "generated_at": datetime.utcnow().isoformat(),
            "metrics": metrics
        }

        # Cache for 15 minutes
        await self.cache.set(cache_key, result, 900)
        return result

    async def _get_user_metrics(
        self,
        start_date: datetime,
        end_date: datetime,
        previous_start_date: datetime
    ) -> Dict[str, MetricData]:
        """Calculate user-related metrics."""

        from app.db.base import get_database_session

        metrics = {}

        with get_database_session() as db:
            # Total users
            total_users = db.query(User).count()

            # New users in period
            new_users = db.query(User).filter(
                User.created_at.between(start_date, end_date)
            ).count()

            previous_new_users = db.query(User).filter(
                User.created_at.between(previous_start_date, start_date)
            ).count()

            # Active users (logged in during period)
            active_users = db.query(User).filter(
                User.last_login.between(start_date, end_date)
            ).count()

            previous_active_users = db.query(User).filter(
                User.last_login.between(previous_start_date, start_date)
            ).count()

            # Verified users
            verified_users = db.query(User).filter(User.is_verified == True).count()

            # Profile completion rate
            profiles_with_completion = db.query(UserProfile.profile_completion_percentage).all()
            avg_completion = sum(p[0] or 0 for p in profiles_with_completion) / len(profiles_with_completion) if profiles_with_completion else 0

        metrics["total_users"] = MetricData(
            value=total_users,
            change_percentage=self._calculate_percentage_change(new_users, previous_new_users),
            trend=self._get_trend(new_users, previous_new_users)
        )

        metrics["new_users"] = MetricData(
            value=new_users,
            change_percentage=self._calculate_percentage_change(new_users, previous_new_users),
            trend=self._get_trend(new_users, previous_new_users),
            previous_value=previous_new_users
        )

        metrics["active_users"] = MetricData(
            value=active_users,
            change_percentage=self._calculate_percentage_change(active_users, previous_active_users),
            trend=self._get_trend(active_users, previous_active_users),
            previous_value=previous_active_users
        )

        metrics["verified_users"] = MetricData(value=verified_users)
        metrics["avg_profile_completion"] = MetricData(value=round(avg_completion, 1))

        return metrics

    async def _get_loan_metrics(
        self,
        start_date: datetime,
        end_date: datetime,
        previous_start_date: datetime
    ) -> Dict[str, MetricData]:
        """Calculate loan-related metrics."""

        from app.db.base import get_database_session

        metrics = {}

        with get_database_session() as db:
            # Loan requests
            loan_requests = db.query(LoanRequest).filter(
                LoanRequest.created_at.between(start_date, end_date)
            ).count()

            previous_loan_requests = db.query(LoanRequest).filter(
                LoanRequest.created_at.between(previous_start_date, start_date)
            ).count()

            # Lending offers
            lending_offers = db.query(LendingOffer).filter(
                LendingOffer.created_at.between(start_date, end_date)
            ).count()

            previous_lending_offers = db.query(LendingOffer).filter(
                LendingOffer.created_at.between(previous_start_date, start_date)
            ).count()

            # Average loan amount requested
            avg_loan_amount = db.query(func.avg(LoanRequest.amount)).filter(
                LoanRequest.created_at.between(start_date, end_date)
            ).scalar() or 0

            # Most common loan purposes
            loan_purposes = db.query(
                LoanRequest.purpose,
                func.count(LoanRequest.purpose).label('count')
            ).filter(
                LoanRequest.created_at.between(start_date, end_date)
            ).group_by(LoanRequest.purpose).order_by(desc('count')).limit(5).all()

        metrics["loan_requests"] = MetricData(
            value=loan_requests,
            change_percentage=self._calculate_percentage_change(loan_requests, previous_loan_requests),
            trend=self._get_trend(loan_requests, previous_loan_requests),
            previous_value=previous_loan_requests
        )

        metrics["lending_offers"] = MetricData(
            value=lending_offers,
            change_percentage=self._calculate_percentage_change(lending_offers, previous_lending_offers),
            trend=self._get_trend(lending_offers, previous_lending_offers),
            previous_value=previous_lending_offers
        )

        metrics["avg_loan_amount"] = MetricData(value=round(avg_loan_amount, 2))
        metrics["top_loan_purposes"] = MetricData(value=dict(loan_purposes))

        return metrics

    async def _get_platform_metrics(
        self,
        start_date: datetime,
        end_date: datetime,
        previous_start_date: datetime
    ) -> Dict[str, MetricData]:
        """Calculate platform usage metrics."""

        from app.db.base import get_database_session

        metrics = {}

        with get_database_session() as db:
            # Connections made
            connections = db.query(Connection).filter(
                Connection.created_at.between(start_date, end_date),
                Connection.status == "accepted"
            ).count()

            previous_connections = db.query(Connection).filter(
                Connection.created_at.between(previous_start_date, start_date),
                Connection.status == "accepted"
            ).count()

            # Ratings given
            ratings = db.query(UserRating).filter(
                UserRating.created_at.between(start_date, end_date)
            ).count()

            # Average rating
            avg_rating = db.query(func.avg(UserRating.rating)).scalar() or 0

            # Security events
            security_events = 0  # Would implement if SecurityEvent model exists

        metrics["connections_made"] = MetricData(
            value=connections,
            change_percentage=self._calculate_percentage_change(connections, previous_connections),
            trend=self._get_trend(connections, previous_connections),
            previous_value=previous_connections
        )

        metrics["ratings_given"] = MetricData(value=ratings)
        metrics["avg_platform_rating"] = MetricData(value=round(avg_rating, 2))
        metrics["security_events"] = MetricData(value=security_events)

        return metrics

    async def _get_financial_metrics(
        self,
        start_date: datetime,
        end_date: datetime,
        previous_start_date: datetime
    ) -> Dict[str, MetricData]:
        """Calculate financial metrics."""

        from app.db.base import get_database_session

        metrics = {}

        with get_database_session() as db:
            # Total loan volume requested
            total_loan_volume = db.query(func.sum(LoanRequest.amount)).filter(
                LoanRequest.created_at.between(start_date, end_date)
            ).scalar() or 0

            previous_loan_volume = db.query(func.sum(LoanRequest.amount)).filter(
                LoanRequest.created_at.between(previous_start_date, start_date)
            ).scalar() or 0

            # Total lending capacity
            total_lending_capacity = db.query(func.sum(LendingOffer.max_amount)).filter(
                LendingOffer.created_at.between(start_date, end_date)
            ).scalar() or 0

            # Average interest rates
            avg_borrower_rate = db.query(func.avg(LoanRequest.max_interest_rate)).filter(
                LoanRequest.created_at.between(start_date, end_date)
            ).scalar() or 0

            avg_lender_rate = db.query(func.avg(LendingOffer.min_interest_rate)).filter(
                LendingOffer.created_at.between(start_date, end_date)
            ).scalar() or 0

        metrics["total_loan_volume"] = MetricData(
            value=total_loan_volume,
            change_percentage=self._calculate_percentage_change(total_loan_volume, previous_loan_volume),
            trend=self._get_trend(total_loan_volume, previous_loan_volume),
            previous_value=previous_loan_volume
        )

        metrics["total_lending_capacity"] = MetricData(value=total_lending_capacity)
        metrics["avg_borrower_interest_rate"] = MetricData(value=round(avg_borrower_rate or 0, 2))
        metrics["avg_lender_interest_rate"] = MetricData(value=round(avg_lender_rate or 0, 2))

        return metrics

    async def get_user_analytics(
        self,
        time_range: TimeRange = TimeRange.LAST_30_DAYS
    ) -> Dict[str, Any]:
        """Get detailed user analytics."""

        cache_key = f"user_analytics:{time_range.value}"
        cached_data = await self.cache.get(cache_key)
        if cached_data:
            return cached_data

        from app.db.base import get_database_session

        end_date = datetime.utcnow()
        start_date = self._get_start_date(end_date, time_range)

        with get_database_session() as db:
            # User growth over time
            user_growth = []
            days_back = (end_date - start_date).days

            for i in range(days_back, -1, -1):
                day = end_date - timedelta(days=i)
                daily_signups = db.query(User).filter(
                    func.date(User.created_at) == day.date()
                ).count()

                user_growth.append({
                    "date": day.strftime("%Y-%m-%d"),
                    "signups": daily_signups
                })

            # User roles distribution
            role_distribution = db.query(
                User.role,
                func.count(User.role).label('count')
            ).group_by(User.role).all()

            # Geographic distribution
            geo_distribution = db.query(
                UserProfile.country,
                func.count(UserProfile.country).label('count')
            ).filter(
                UserProfile.country.isnot(None)
            ).group_by(UserProfile.country).order_by(desc('count')).limit(10).all()

            # User activity patterns
            hourly_activity = db.query(
                func.extract('hour', User.last_login).label('hour'),
                func.count(User.id).label('count')
            ).filter(
                User.last_login.between(start_date, end_date)
            ).group_by('hour').order_by('hour').all()

        result = {
            "time_range": time_range.value,
            "generated_at": datetime.utcnow().isoformat(),
            "charts": {
                "user_growth": user_growth,
                "role_distribution": [{"role": r[0], "count": r[1]} for r in role_distribution],
                "geo_distribution": [{"country": g[0], "count": g[1]} for g in geo_distribution],
                "hourly_activity": [{"hour": int(h[0] or 0), "count": h[1]} for h in hourly_activity]
            }
        }

        # Cache for 1 hour
        await self.cache.set(cache_key, result, 3600)
        return result

    async def get_loan_analytics(
        self,
        time_range: TimeRange = TimeRange.LAST_30_DAYS
    ) -> Dict[str, Any]:
        """Get detailed loan analytics."""

        cache_key = f"loan_analytics:{time_range.value}"
        cached_data = await self.cache.get(cache_key)
        if cached_data:
            return cached_data

        from app.db.base import get_database_session

        end_date = datetime.utcnow()
        start_date = self._get_start_date(end_date, time_range)

        with get_database_session() as db:
            # Loan amount distribution
            loan_amounts = db.query(LoanRequest.amount).filter(
                LoanRequest.created_at.between(start_date, end_date)
            ).all()

            # Categorize loan amounts
            amount_ranges = {
                "0-5000": 0,
                "5000-15000": 0,
                "15000-50000": 0,
                "50000-100000": 0,
                "100000+": 0
            }

            for amount in loan_amounts:
                val = amount[0]
                if val <= 5000:
                    amount_ranges["0-5000"] += 1
                elif val <= 15000:
                    amount_ranges["5000-15000"] += 1
                elif val <= 50000:
                    amount_ranges["15000-50000"] += 1
                elif val <= 100000:
                    amount_ranges["50000-100000"] += 1
                else:
                    amount_ranges["100000+"] += 1

            # Loan terms distribution
            term_distribution = db.query(
                LoanRequest.term_months,
                func.count(LoanRequest.term_months).label('count')
            ).filter(
                LoanRequest.created_at.between(start_date, end_date)
            ).group_by(LoanRequest.term_months).order_by(LoanRequest.term_months).all()

            # Interest rate trends
            rate_trends = db.query(
                func.date(LoanRequest.created_at).label('date'),
                func.avg(LoanRequest.max_interest_rate).label('avg_rate')
            ).filter(
                LoanRequest.created_at.between(start_date, end_date),
                LoanRequest.max_interest_rate.isnot(None)
            ).group_by(func.date(LoanRequest.created_at)).order_by('date').all()

            # Loan status distribution
            status_distribution = db.query(
                LoanRequest.status,
                func.count(LoanRequest.status).label('count')
            ).group_by(LoanRequest.status).all()

        result = {
            "time_range": time_range.value,
            "generated_at": datetime.utcnow().isoformat(),
            "charts": {
                "amount_distribution": [{"range": k, "count": v} for k, v in amount_ranges.items()],
                "term_distribution": [{"months": t[0], "count": t[1]} for t in term_distribution],
                "rate_trends": [{"date": r[0].strftime("%Y-%m-%d"), "avg_rate": float(r[1] or 0)} for r in rate_trends],
                "status_distribution": [{"status": s[0], "count": s[1]} for s in status_distribution]
            }
        }

        # Cache for 1 hour
        await self.cache.set(cache_key, result, 3600)
        return result

    async def generate_comprehensive_report(
        self,
        time_range: TimeRange = TimeRange.LAST_30_DAYS,
        include_recommendations: bool = True
    ) -> AnalyticsReport:
        """Generate a comprehensive analytics report."""

        report_id = f"report_{int(datetime.utcnow().timestamp())}"

        # Get all analytics data
        dashboard_metrics = await self.get_dashboard_metrics(time_range)
        user_analytics = await self.get_user_analytics(time_range)
        loan_analytics = await self.get_loan_analytics(time_range)

        # Generate insights
        insights = self._generate_insights(dashboard_metrics, user_analytics, loan_analytics)

        # Generate recommendations
        recommendations = []
        if include_recommendations:
            recommendations = self._generate_recommendations(dashboard_metrics, insights)

        return AnalyticsReport(
            report_id=report_id,
            generated_at=datetime.utcnow(),
            time_range=time_range.value,
            metrics=dashboard_metrics["metrics"],
            charts_data={
                "user_charts": user_analytics["charts"],
                "loan_charts": loan_analytics["charts"]
            },
            insights=insights,
            recommendations=recommendations
        )

    def _get_start_date(self, end_date: datetime, time_range: TimeRange) -> datetime:
        """Calculate start date based on time range."""
        if time_range == TimeRange.LAST_24_HOURS:
            return end_date - timedelta(hours=24)
        elif time_range == TimeRange.LAST_7_DAYS:
            return end_date - timedelta(days=7)
        elif time_range == TimeRange.LAST_30_DAYS:
            return end_date - timedelta(days=30)
        elif time_range == TimeRange.LAST_90_DAYS:
            return end_date - timedelta(days=90)
        elif time_range == TimeRange.LAST_YEAR:
            return end_date - timedelta(days=365)
        else:  # ALL_TIME
            return datetime(2020, 1, 1)  # Platform start date

    def _calculate_percentage_change(self, current: float, previous: float) -> Optional[float]:
        """Calculate percentage change between two values."""
        if previous == 0:
            return 100.0 if current > 0 else 0.0
        return round(((current - previous) / previous) * 100, 2)

    def _get_trend(self, current: float, previous: float) -> str:
        """Determine trend direction."""
        if current > previous:
            return "up"
        elif current < previous:
            return "down"
        else:
            return "stable"

    def _generate_insights(
        self,
        dashboard_metrics: Dict[str, Any],
        user_analytics: Dict[str, Any],
        loan_analytics: Dict[str, Any]
    ) -> List[str]:
        """Generate business insights from analytics data."""

        insights = []
        metrics = dashboard_metrics["metrics"]

        # User growth insights
        if "new_users" in metrics:
            new_users = metrics["new_users"]
            if new_users.change_percentage and new_users.change_percentage > 20:
                insights.append(f"User growth is accelerating with {new_users.change_percentage}% increase in new registrations")
            elif new_users.change_percentage and new_users.change_percentage < -10:
                insights.append(f"User growth is slowing with {abs(new_users.change_percentage)}% decrease in new registrations")

        # Loan demand insights
        if "loan_requests" in metrics and "lending_offers" in metrics:
            loan_requests = metrics["loan_requests"].value
            lending_offers = metrics["lending_offers"].value

            if loan_requests > lending_offers * 2:
                insights.append("High loan demand detected - consider incentivizing more lenders to join the platform")
            elif lending_offers > loan_requests * 2:
                insights.append("High lending supply detected - consider marketing to attract more borrowers")
            else:
                insights.append("Balanced supply and demand between borrowers and lenders")

        # Financial insights
        if "avg_borrower_interest_rate" in metrics and "avg_lender_interest_rate" in metrics:
            borrower_rate = metrics["avg_borrower_interest_rate"].value
            lender_rate = metrics["avg_lender_interest_rate"].value

            if borrower_rate - lender_rate > 5:
                insights.append("Large interest rate spread indicates good matching opportunity")
            elif borrower_rate - lender_rate < 2:
                insights.append("Narrow interest rate spread may indicate competitive pricing")

        # Platform engagement insights
        if "connections_made" in metrics:
            connections = metrics["connections_made"]
            if connections.change_percentage and connections.change_percentage > 30:
                insights.append("Platform engagement is strong with increasing user connections")

        return insights

    def _generate_recommendations(
        self,
        dashboard_metrics: Dict[str, Any],
        insights: List[str]
    ) -> List[str]:
        """Generate actionable recommendations based on data."""

        recommendations = []
        metrics = dashboard_metrics["metrics"]

        # User acquisition recommendations
        if "new_users" in metrics:
            new_users = metrics["new_users"]
            if new_users.change_percentage and new_users.change_percentage < 0:
                recommendations.append("Consider launching user acquisition campaigns to boost registration growth")

        # Profile completion recommendations
        if "avg_profile_completion" in metrics:
            completion = metrics["avg_profile_completion"].value
            if completion < 70:
                recommendations.append("Implement profile completion incentives to improve user onboarding")

        # Verification recommendations
        if "verified_users" in metrics and "total_users" in metrics:
            verification_rate = (metrics["verified_users"].value / metrics["total_users"].value) * 100
            if verification_rate < 50:
                recommendations.append("Streamline verification process to increase user trust and platform safety")

        # Matching optimization recommendations
        for insight in insights:
            if "High loan demand" in insight:
                recommendations.append("Implement lender referral programs and targeted marketing")
            elif "High lending supply" in insight:
                recommendations.append("Focus marketing efforts on attracting quality borrowers")

        return recommendations


# Global analytics service instance
_analytics_service: Optional[AnalyticsService] = None


def get_analytics_service() -> AnalyticsService:
    """Get analytics service instance."""
    global _analytics_service
    if _analytics_service is None:
        _analytics_service = AnalyticsService()
    return _analytics_service