"""
Integration tests for analytics and reporting API endpoints.
Tests dashboard metrics, user analytics, export functionality, and mobile analytics.
"""

import pytest
import json
from fastapi.testclient import TestClient
from io import BytesIO


class TestDashboardAnalytics:
    """Test dashboard analytics endpoints."""

    def test_get_dashboard_analytics_success(self, authenticated_client):
        """Test successful dashboard analytics retrieval."""
        client, token = authenticated_client

        response = client.get("/api/v1/analytics/dashboard")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "data" in data
        assert "message" in data

        analytics_data = data["data"]
        assert "metrics" in analytics_data
        assert "charts" in analytics_data
        assert "summary" in analytics_data

    def test_dashboard_analytics_time_ranges(self, authenticated_client):
        """Test dashboard analytics with different time ranges."""
        client, token = authenticated_client

        time_ranges = ["24h", "7d", "30d", "90d", "1y", "all"]

        for time_range in time_ranges:
            response = client.get(f"/api/v1/analytics/dashboard?time_range={time_range}")

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True

    def test_dashboard_analytics_invalid_time_range(self, authenticated_client):
        """Test dashboard analytics with invalid time range."""
        client, token = authenticated_client

        response = client.get("/api/v1/analytics/dashboard?time_range=invalid")

        assert response.status_code == 422  # Validation error

    def test_dashboard_analytics_no_auth(self, client: TestClient):
        """Test dashboard analytics without authentication."""
        response = client.get("/api/v1/analytics/dashboard")

        assert response.status_code == 401


class TestUserAnalytics:
    """Test user analytics endpoints."""

    def test_get_user_analytics_admin_success(self, client: TestClient, db_session, test_data_factory):
        """Test user analytics access by admin user."""
        # Create admin user
        from app.models import User
        from app.core.security import get_password_hash

        admin_user = User(
            email="admin@example.com",
            username="admin",
            hashed_password=get_password_hash("AdminPass123!"),
            role="admin",
            is_active=True,
            is_verified=True
        )
        db_session.add(admin_user)
        db_session.commit()

        # Login as admin
        login_data = {
            "email": admin_user.email,
            "password": "AdminPass123!"
        }

        login_response = client.post("/api/v1/auth/login", json=login_data)
        tokens = login_response.json()["tokens"]
        client.headers["Authorization"] = f"Bearer {tokens['access_token']}"

        # Test user analytics
        response = client.get("/api/v1/analytics/users")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "data" in data

        user_data = data["data"]
        assert "growth_metrics" in user_data or "user_metrics" in user_data

    def test_get_user_analytics_forbidden_borrower(self, authenticated_client):
        """Test user analytics access forbidden for regular borrower."""
        client, token = authenticated_client

        response = client.get("/api/v1/analytics/users")

        assert response.status_code == 403
        data = response.json()
        assert data["success"] is False
        assert "admin" in data["detail"].lower()

    def test_user_analytics_time_range(self, client: TestClient, db_session, test_data_factory):
        """Test user analytics with time range parameter."""
        # Create and login as admin (similar to first test)
        from app.models import User
        from app.core.security import get_password_hash

        admin_user = User(
            email="admin2@example.com",
            username="admin2",
            hashed_password=get_password_hash("AdminPass123!"),
            role="admin",
            is_active=True,
            is_verified=True
        )
        db_session.add(admin_user)
        db_session.commit()

        login_data = {"email": admin_user.email, "password": "AdminPass123!"}
        login_response = client.post("/api/v1/auth/login", json=login_data)
        tokens = login_response.json()["tokens"]
        client.headers["Authorization"] = f"Bearer {tokens['access_token']}"

        # Test with specific time range
        response = client.get("/api/v1/analytics/users?time_range=7d")

        assert response.status_code == 200


class TestLoanAnalytics:
    """Test loan analytics endpoints."""

    def test_get_loan_analytics_admin_success(self, client: TestClient, db_session):
        """Test loan analytics access by admin user."""
        from app.models import User
        from app.core.security import get_password_hash

        admin_user = User(
            email="admin3@example.com",
            username="admin3",
            hashed_password=get_password_hash("AdminPass123!"),
            role="admin",
            is_active=True,
            is_verified=True
        )
        db_session.add(admin_user)
        db_session.commit()

        login_data = {"email": admin_user.email, "password": "AdminPass123!"}
        login_response = client.post("/api/v1/auth/login", json=login_data)
        tokens = login_response.json()["tokens"]
        client.headers["Authorization"] = f"Bearer {tokens['access_token']}"

        response = client.get("/api/v1/analytics/loans")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "data" in data

    def test_loan_analytics_forbidden_borrower(self, authenticated_client):
        """Test loan analytics access forbidden for regular borrower."""
        client, token = authenticated_client

        response = client.get("/api/v1/analytics/loans")

        assert response.status_code == 403


class TestComprehensiveReports:
    """Test comprehensive reporting endpoints."""

    def test_get_comprehensive_report_admin(self, client: TestClient, db_session):
        """Test comprehensive report generation by admin."""
        from app.models import User
        from app.core.security import get_password_hash

        admin_user = User(
            email="admin4@example.com",
            username="admin4",
            hashed_password=get_password_hash("AdminPass123!"),
            role="admin",
            is_active=True,
            is_verified=True
        )
        db_session.add(admin_user)
        db_session.commit()

        login_data = {"email": admin_user.email, "password": "AdminPass123!"}
        login_response = client.post("/api/v1/auth/login", json=login_data)
        tokens = login_response.json()["tokens"]
        client.headers["Authorization"] = f"Bearer {tokens['access_token']}"

        response = client.get("/api/v1/analytics/report/comprehensive")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "data" in data

        report_data = data["data"]
        assert "report_id" in report_data
        assert "generated_at" in report_data
        assert "metrics" in report_data
        assert "summary" in report_data

    def test_comprehensive_report_with_recommendations(self, client: TestClient, db_session):
        """Test comprehensive report with AI recommendations."""
        from app.models import User
        from app.core.security import get_password_hash

        admin_user = User(
            email="admin5@example.com",
            username="admin5",
            hashed_password=get_password_hash("AdminPass123!"),
            role="admin",
            is_active=True,
            is_verified=True
        )
        db_session.add(admin_user)
        db_session.commit()

        login_data = {"email": admin_user.email, "password": "AdminPass123!"}
        login_response = client.post("/api/v1/auth/login", json=login_data)
        tokens = login_response.json()["tokens"]
        client.headers["Authorization"] = f"Bearer {tokens['access_token']}"

        response = client.get(
            "/api/v1/analytics/report/comprehensive?include_recommendations=true"
        )

        assert response.status_code == 200
        data = response.json()

        report_data = data["data"]
        assert "recommendations" in report_data

    def test_comprehensive_report_forbidden_non_admin(self, authenticated_client):
        """Test comprehensive report access forbidden for non-admin."""
        client, token = authenticated_client

        response = client.get("/api/v1/analytics/report/comprehensive")

        assert response.status_code == 403


class TestAnalyticsExport:
    """Test analytics export functionality."""

    def test_export_analytics_json(self, client: TestClient, db_session):
        """Test analytics export in JSON format."""
        from app.models import User
        from app.core.security import get_password_hash

        admin_user = User(
            email="admin6@example.com",
            username="admin6",
            hashed_password=get_password_hash("AdminPass123!"),
            role="admin",
            is_active=True,
            is_verified=True
        )
        db_session.add(admin_user)
        db_session.commit()

        login_data = {"email": admin_user.email, "password": "AdminPass123!"}
        login_response = client.post("/api/v1/auth/login", json=login_data)
        tokens = login_response.json()["tokens"]
        client.headers["Authorization"] = f"Bearer {tokens['access_token']}"

        response = client.get("/api/v1/analytics/report/export?format=json")

        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]
        assert "attachment" in response.headers["content-disposition"]

        # Verify it's valid JSON
        content = response.content
        json_data = json.loads(content.decode('utf-8'))
        assert "report_metadata" in json_data

    def test_export_analytics_csv(self, client: TestClient, db_session):
        """Test analytics export in CSV format."""
        from app.models import User
        from app.core.security import get_password_hash

        admin_user = User(
            email="admin7@example.com",
            username="admin7",
            hashed_password=get_password_hash("AdminPass123!"),
            role="admin",
            is_active=True,
            is_verified=True
        )
        db_session.add(admin_user)
        db_session.commit()

        login_data = {"email": admin_user.email, "password": "AdminPass123!"}
        login_response = client.post("/api/v1/auth/login", json=login_data)
        tokens = login_response.json()["tokens"]
        client.headers["Authorization"] = f"Bearer {tokens['access_token']}"

        response = client.get("/api/v1/analytics/report/export?format=csv")

        assert response.status_code == 200
        assert "text/csv" in response.headers["content-type"]
        assert "attachment" in response.headers["content-disposition"]

        # Verify it's valid CSV
        content = response.content.decode('utf-8')
        lines = content.strip().split('\n')
        assert len(lines) > 0
        assert "Metric,Value,Change_Percentage,Trend" in lines[0]

    def test_export_invalid_format(self, client: TestClient, db_session):
        """Test analytics export with invalid format."""
        from app.models import User
        from app.core.security import get_password_hash

        admin_user = User(
            email="admin8@example.com",
            username="admin8",
            hashed_password=get_password_hash("AdminPass123!"),
            role="admin",
            is_active=True,
            is_verified=True
        )
        db_session.add(admin_user)
        db_session.commit()

        login_data = {"email": admin_user.email, "password": "AdminPass123!"}
        login_response = client.post("/api/v1/auth/login", json=login_data)
        tokens = login_response.json()["tokens"]
        client.headers["Authorization"] = f"Bearer {tokens['access_token']}"

        response = client.get("/api/v1/analytics/report/export?format=xml")

        assert response.status_code == 422

    def test_export_forbidden_non_admin(self, authenticated_client):
        """Test analytics export forbidden for non-admin."""
        client, token = authenticated_client

        response = client.get("/api/v1/analytics/report/export?format=json")

        assert response.status_code == 403


class TestMobileAnalytics:
    """Test mobile-optimized analytics endpoints."""

    def test_mobile_analytics_summary(self, authenticated_client):
        """Test mobile analytics summary endpoint."""
        client, token = authenticated_client

        response = client.get("/api/v1/analytics/mobile/summary")

        assert response.status_code == 200
        data = response.json()

        # Mobile response structure
        assert "success" in data
        assert "timestamp" in data
        assert "request_id" in data

        if data["success"]:
            assert "data" in data
            summary_data = data["data"]
            assert "platform_stats" in summary_data
            assert "growth_trends" in summary_data
            assert "financial_overview" in summary_data

    def test_mobile_user_insights_own_data(self, authenticated_client, test_user):
        """Test mobile user insights for own data."""
        client, token = authenticated_client

        response = client.get(f"/api/v1/analytics/mobile/user-insights/{test_user.id}")

        assert response.status_code == 200
        data = response.json()

        assert "success" in data
        if data["success"]:
            assert "data" in data
            insights_data = data["data"]
            assert "user_id" in insights_data
            assert "insights" in insights_data

    def test_mobile_user_insights_other_user_forbidden(self, authenticated_client):
        """Test mobile user insights for other user (should be forbidden)."""
        client, token = authenticated_client

        # Try to access insights for user ID 99999 (not the authenticated user)
        response = client.get("/api/v1/analytics/mobile/user-insights/99999")

        assert response.status_code == 403
        data = response.json()
        assert data["success"] is False

    def test_mobile_analytics_no_auth(self, client: TestClient):
        """Test mobile analytics without authentication."""
        response = client.get("/api/v1/analytics/mobile/summary")

        assert response.status_code == 401


class TestEventTracking:
    """Test analytics event tracking."""

    def test_track_analytics_event_success(self, authenticated_client):
        """Test successful analytics event tracking."""
        client, token = authenticated_client

        event_data = {
            "event_type": "user_action",
            "timestamp": "2024-01-15T10:30:00Z",
            "action": "profile_view",
            "details": {
                "page": "profile_detail",
                "duration": 45
            }
        }

        response = client.post("/api/v1/analytics/events/track", json=event_data)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "event_id" in data
        assert "message" in data

    def test_track_analytics_event_missing_fields(self, authenticated_client):
        """Test analytics event tracking with missing required fields."""
        client, token = authenticated_client

        # Missing timestamp
        event_data = {
            "event_type": "user_action",
            "action": "profile_view"
        }

        response = client.post("/api/v1/analytics/events/track", json=event_data)

        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False

    def test_track_analytics_event_no_auth(self, client: TestClient):
        """Test analytics event tracking without authentication."""
        event_data = {
            "event_type": "user_action",
            "timestamp": "2024-01-15T10:30:00Z"
        }

        response = client.post("/api/v1/analytics/events/track", json=event_data)

        assert response.status_code == 401


class TestAnalyticsHealthCheck:
    """Test analytics service health check."""

    def test_analytics_health_check(self, client: TestClient):
        """Test analytics service health check."""
        response = client.get("/api/v1/analytics/health")

        assert response.status_code == 200
        data = response.json()

        assert "service" in data
        assert data["service"] == "analytics"
        assert "status" in data
        assert "timestamp" in data
        assert "features" in data

        features = data["features"]
        assert "dashboard_metrics" in features
        assert "user_analytics" in features
        assert "comprehensive_reports" in features
        assert "export_functionality" in features
        assert "mobile_support" in features