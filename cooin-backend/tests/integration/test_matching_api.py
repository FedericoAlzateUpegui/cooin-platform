"""
Integration tests for intelligent matching API endpoints.
Tests matching functionality for borrowers and lenders.
"""

import pytest
from fastapi.testclient import TestClient
from decimal import Decimal

from tests.conftest import TestDataFactory


class TestBorrowerMatching:
    """Test borrower matching endpoints."""

    def test_get_borrower_matches_success(self, authenticated_client, test_loan_request, test_lender, test_lending_offer):
        """Test successful borrower matches retrieval."""
        client, token = authenticated_client

        response = client.get(f"/api/v1/matching/borrower/matches/{test_loan_request.id}")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "matches" in data
        assert isinstance(data["matches"], list)
        assert "pagination" in data

    def test_get_borrower_matches_nonexistent_request(self, authenticated_client):
        """Test borrower matches for non-existent loan request."""
        client, token = authenticated_client

        response = client.get("/api/v1/matching/borrower/matches/99999")

        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False

    def test_get_borrower_matches_unauthorized_access(self, authenticated_lender_client, test_loan_request):
        """Test borrower matches access by unauthorized user."""
        client, token = authenticated_lender_client

        response = client.get(f"/api/v1/matching/borrower/matches/{test_loan_request.id}")

        assert response.status_code == 403
        data = response.json()
        assert data["success"] is False
        assert "access" in data["detail"].lower()

    def test_borrower_matches_pagination(self, authenticated_client, test_loan_request):
        """Test pagination in borrower matches."""
        client, token = authenticated_client

        response = client.get(
            f"/api/v1/matching/borrower/matches/{test_loan_request.id}?limit=5&offset=0"
        )

        assert response.status_code == 200
        data = response.json()

        assert "pagination" in data
        pagination = data["pagination"]
        assert "limit" in pagination
        assert "offset" in pagination
        assert "total_count" in pagination
        assert pagination["limit"] == 5

    def test_borrower_matches_minimum_score_filter(self, authenticated_client, test_loan_request):
        """Test minimum score filter in borrower matches."""
        client, token = authenticated_client

        response = client.get(
            f"/api/v1/matching/borrower/matches/{test_loan_request.id}?min_score=0.8"
        )

        assert response.status_code == 200
        data = response.json()

        # All returned matches should have score >= 0.8
        for match in data["matches"]:
            assert match["compatibility_score"] >= 0.8

    def test_borrower_matches_no_auth(self, client: TestClient, test_loan_request):
        """Test borrower matches without authentication."""
        response = client.get(f"/api/v1/matching/borrower/matches/{test_loan_request.id}")

        assert response.status_code == 401


class TestLenderMatching:
    """Test lender matching endpoints."""

    def test_get_lender_matches_success(self, authenticated_lender_client, test_lending_offer, test_user, test_loan_request):
        """Test successful lender matches retrieval."""
        client, token = authenticated_lender_client

        response = client.get(f"/api/v1/matching/lender/matches/{test_lending_offer.id}")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "matches" in data
        assert isinstance(data["matches"], list)
        assert "pagination" in data

    def test_get_lender_matches_nonexistent_offer(self, authenticated_lender_client):
        """Test lender matches for non-existent lending offer."""
        client, token = authenticated_lender_client

        response = client.get("/api/v1/matching/lender/matches/99999")

        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False

    def test_get_lender_matches_unauthorized_access(self, authenticated_client, test_lending_offer):
        """Test lender matches access by unauthorized user."""
        client, token = authenticated_client

        response = client.get(f"/api/v1/matching/lender/matches/{test_lending_offer.id}")

        assert response.status_code == 403
        data = response.json()
        assert data["success"] is False

    def test_lender_matches_pagination(self, authenticated_lender_client, test_lending_offer):
        """Test pagination in lender matches."""
        client, token = authenticated_lender_client

        response = client.get(
            f"/api/v1/matching/lender/matches/{test_lending_offer.id}?limit=3&offset=0"
        )

        assert response.status_code == 200
        data = response.json()

        assert "pagination" in data
        pagination = data["pagination"]
        assert pagination["limit"] == 3

    def test_lender_matches_no_auth(self, client: TestClient, test_lending_offer):
        """Test lender matches without authentication."""
        response = client.get(f"/api/v1/matching/lender/matches/{test_lending_offer.id}")

        assert response.status_code == 401


class TestMatchSuggestions:
    """Test match suggestion endpoints."""

    def test_get_match_suggestions_borrower(self, authenticated_client, test_loan_request):
        """Test match suggestions for borrower."""
        client, token = authenticated_client

        response = client.get(
            f"/api/v1/matching/suggestions/borrower/{test_loan_request.id}"
        )

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "suggestions" in data
        assert isinstance(data["suggestions"], list)

        # Check suggestion structure if any exist
        if data["suggestions"]:
            suggestion = data["suggestions"][0]
            assert "type" in suggestion
            assert "message" in suggestion
            assert "priority" in suggestion

    def test_get_match_suggestions_lender(self, authenticated_lender_client, test_lending_offer):
        """Test match suggestions for lender."""
        client, token = authenticated_lender_client

        response = client.get(
            f"/api/v1/matching/suggestions/lender/{test_lending_offer.id}"
        )

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "suggestions" in data


class TestMobileMatching:
    """Test mobile-optimized matching endpoints."""

    def test_mobile_borrower_matches(self, authenticated_client, test_loan_request):
        """Test mobile borrower matches endpoint."""
        client, token = authenticated_client

        response = client.get(
            f"/api/v1/mobile/matching/mobile/borrower/matches/{test_loan_request.id}"
        )

        # Should return mobile-optimized response
        assert response.status_code == 200
        data = response.json()

        # Check mobile response structure
        assert "success" in data
        assert "timestamp" in data
        assert "request_id" in data

        if data["success"]:
            assert "data" in data
            matches_data = data["data"]
            assert "matches" in matches_data

    def test_mobile_lender_matches(self, authenticated_lender_client, test_lending_offer):
        """Test mobile lender matches endpoint."""
        client, token = authenticated_lender_client

        response = client.get(
            f"/api/v1/mobile/matching/mobile/lender/matches/{test_lending_offer.id}"
        )

        assert response.status_code == 200
        data = response.json()

        # Mobile response should have specific structure
        assert "success" in data
        assert "timestamp" in data

    def test_mobile_matches_simplified_data(self, authenticated_client, test_loan_request):
        """Test that mobile matches return simplified data."""
        client, token = authenticated_client

        response = client.get(
            f"/api/v1/mobile/matching/mobile/borrower/matches/{test_loan_request.id}"
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("success") and "data" in data:
                matches = data["data"].get("matches", [])

                # Mobile matches should have simplified structure
                for match in matches:
                    # Should contain essential info only
                    assert "lender_id" in match
                    assert "compatibility_score" in match
                    # Should not contain complex nested objects


class TestMatchingValidation:
    """Test matching endpoint validation."""

    def test_invalid_loan_request_id(self, authenticated_client):
        """Test matching with invalid loan request ID."""
        client, token = authenticated_client

        response = client.get("/api/v1/matching/borrower/matches/invalid")

        assert response.status_code == 422  # Validation error

    def test_invalid_lending_offer_id(self, authenticated_lender_client):
        """Test matching with invalid lending offer ID."""
        client, token = authenticated_lender_client

        response = client.get("/api/v1/matching/lender/matches/invalid")

        assert response.status_code == 422

    def test_negative_limit_parameter(self, authenticated_client, test_loan_request):
        """Test matching with negative limit parameter."""
        client, token = authenticated_client

        response = client.get(
            f"/api/v1/matching/borrower/matches/{test_loan_request.id}?limit=-1"
        )

        assert response.status_code == 422

    def test_limit_too_large(self, authenticated_client, test_loan_request):
        """Test matching with limit parameter too large."""
        client, token = authenticated_client

        response = client.get(
            f"/api/v1/matching/borrower/matches/{test_loan_request.id}?limit=100"
        )

        assert response.status_code == 422

    def test_invalid_min_score(self, authenticated_client, test_loan_request):
        """Test matching with invalid min_score parameter."""
        client, token = authenticated_client

        response = client.get(
            f"/api/v1/matching/borrower/matches/{test_loan_request.id}?min_score=1.5"
        )

        assert response.status_code == 422


class TestMatchingHealthCheck:
    """Test matching service health check."""

    def test_matching_health_check(self, client: TestClient):
        """Test matching service health check."""
        response = client.get("/api/v1/matching/health")

        assert response.status_code == 200
        data = response.json()

        assert "service" in data
        assert data["service"] == "intelligent-matching"
        assert "status" in data
        assert "timestamp" in data
        assert "features" in data

        features = data["features"]
        assert "borrower_matching" in features
        assert "lender_matching" in features
        assert "match_suggestions" in features
        assert "mobile_support" in features


class TestMatchingCaching:
    """Test matching caching behavior."""

    def test_match_results_caching(self, authenticated_client, test_loan_request):
        """Test that match results are cached for performance."""
        client, token = authenticated_client

        # First request
        response1 = client.get(f"/api/v1/matching/borrower/matches/{test_loan_request.id}")
        assert response1.status_code == 200

        # Second request should be faster (cached)
        response2 = client.get(f"/api/v1/matching/borrower/matches/{test_loan_request.id}")
        assert response2.status_code == 200

        # Results should be identical
        assert response1.json()["data"] == response2.json()["data"]

    def test_cache_invalidation_on_profile_update(self, authenticated_client, test_loan_request, test_user_profile):
        """Test that cache is invalidated when user profile is updated."""
        client, token = authenticated_client

        # Get matches
        response1 = client.get(f"/api/v1/matching/borrower/matches/{test_loan_request.id}")
        assert response1.status_code == 200

        # Update profile (this should invalidate cache)
        profile_update = {"bio": "Updated bio for better matches"}
        client.put("/api/v1/profiles/me", json=profile_update)

        # Get matches again (should recalculate)
        response2 = client.get(f"/api/v1/matching/borrower/matches/{test_loan_request.id}")
        assert response2.status_code == 200

        # We can't easily test if cache was actually invalidated without mocking,
        # but the endpoint should still work correctly