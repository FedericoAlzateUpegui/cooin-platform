"""
Integration tests for authentication API endpoints.
Tests complete authentication flow including registration, login, token refresh, and logout.
"""

import pytest
from fastapi.testclient import TestClient

from tests.conftest import TestDataFactory


class TestUserRegistration:
    """Test user registration endpoint."""

    def test_successful_registration(self, client: TestClient, test_data_factory: TestDataFactory):
        """Test successful user registration."""
        user_data = test_data_factory.create_user_data(
            email="newuser@example.com",
            username="newuser"
        )

        response = client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == 201
        data = response.json()

        assert data["success"] is True
        assert data["message"] == "User registered successfully"
        assert "user" in data
        assert data["user"]["email"] == user_data["email"]
        assert data["user"]["username"] == user_data["username"]
        assert data["user"]["role"] == user_data["role"]
        assert "id" in data["user"]

    def test_registration_with_existing_email(self, client: TestClient, test_user_data, test_user):
        """Test registration with already existing email."""
        response = client.post("/api/v1/auth/register", json=test_user_data)

        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "already exists" in data["detail"].lower()

    def test_registration_with_invalid_email(self, client: TestClient, test_data_factory: TestDataFactory):
        """Test registration with invalid email format."""
        user_data = test_data_factory.create_user_data(
            email="invalid-email-format",
            username="testuser"
        )

        response = client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == 422  # Validation error

    def test_registration_password_mismatch(self, client: TestClient, test_data_factory: TestDataFactory):
        """Test registration with password mismatch."""
        user_data = test_data_factory.create_user_data()
        user_data["confirm_password"] = "DifferentPassword123!"

        response = client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == 400
        data = response.json()
        assert "password" in data["detail"].lower()

    def test_registration_weak_password(self, client: TestClient, test_data_factory: TestDataFactory):
        """Test registration with weak password."""
        user_data = test_data_factory.create_user_data()
        user_data["password"] = "weak"
        user_data["confirm_password"] = "weak"

        response = client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == 400
        data = response.json()
        assert "password" in data["detail"].lower()

    def test_registration_terms_not_agreed(self, client: TestClient, test_data_factory: TestDataFactory):
        """Test registration without agreeing to terms."""
        user_data = test_data_factory.create_user_data()
        user_data["agree_to_terms"] = False

        response = client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == 400
        data = response.json()
        assert "terms" in data["detail"].lower()

    def test_registration_invalid_role(self, client: TestClient, test_data_factory: TestDataFactory):
        """Test registration with invalid role."""
        user_data = test_data_factory.create_user_data()
        user_data["role"] = "invalid_role"

        response = client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == 422  # Validation error


class TestUserLogin:
    """Test user login endpoint."""

    def test_successful_login(self, client: TestClient, test_user):
        """Test successful user login."""
        login_data = {
            "email": test_user.email,
            "password": "TestPass123!",
            "remember_me": False
        }

        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "tokens" in data
        assert "access_token" in data["tokens"]
        assert "refresh_token" in data["tokens"]
        assert data["tokens"]["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["id"] == test_user.id

    def test_login_with_wrong_password(self, client: TestClient, test_user):
        """Test login with incorrect password."""
        login_data = {
            "email": test_user.email,
            "password": "WrongPassword123!",
            "remember_me": False
        }

        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False
        assert "credentials" in data["detail"].lower()

    def test_login_with_nonexistent_user(self, client: TestClient):
        """Test login with non-existent user."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "TestPass123!",
            "remember_me": False
        }

        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False

    def test_login_with_invalid_email_format(self, client: TestClient):
        """Test login with invalid email format."""
        login_data = {
            "email": "invalid-email",
            "password": "TestPass123!",
            "remember_me": False
        }

        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 422  # Validation error

    def test_login_remember_me_option(self, client: TestClient, test_user):
        """Test login with remember_me option."""
        login_data = {
            "email": test_user.email,
            "password": "TestPass123!",
            "remember_me": True
        }

        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        # With remember_me, tokens might have longer expiration


class TestCurrentUser:
    """Test current user endpoint."""

    def test_get_current_user_success(self, authenticated_client):
        """Test successful current user retrieval."""
        client, token = authenticated_client

        response = client.get("/api/v1/auth/me")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "user" in data
        assert "id" in data["user"]
        assert "email" in data["user"]
        assert "role" in data["user"]

    def test_get_current_user_no_token(self, client: TestClient):
        """Test current user endpoint without authentication token."""
        response = client.get("/api/v1/auth/me")

        assert response.status_code == 401

    def test_get_current_user_invalid_token(self, client: TestClient):
        """Test current user endpoint with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/auth/me", headers=headers)

        assert response.status_code == 401


class TestTokenRefresh:
    """Test token refresh endpoint."""

    def test_successful_token_refresh(self, client: TestClient, test_user):
        """Test successful token refresh."""
        # First login to get tokens
        login_data = {
            "email": test_user.email,
            "password": "TestPass123!",
            "remember_me": False
        }

        login_response = client.post("/api/v1/auth/login", json=login_data)
        tokens = login_response.json()["tokens"]

        # Refresh tokens
        refresh_data = {"refresh_token": tokens["refresh_token"]}
        response = client.post("/api/v1/auth/refresh", json=refresh_data)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_token_refresh_invalid_token(self, client: TestClient):
        """Test token refresh with invalid refresh token."""
        refresh_data = {"refresh_token": "invalid_refresh_token"}
        response = client.post("/api/v1/auth/refresh", json=refresh_data)

        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False

    def test_token_refresh_missing_token(self, client: TestClient):
        """Test token refresh without providing refresh token."""
        response = client.post("/api/v1/auth/refresh", json={})

        assert response.status_code == 422  # Validation error


class TestUserSessions:
    """Test user sessions endpoint."""

    def test_get_user_sessions(self, authenticated_client):
        """Test getting user sessions."""
        client, token = authenticated_client

        response = client.get("/api/v1/auth/sessions")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "sessions" in data
        assert isinstance(data["sessions"], list)

    def test_get_sessions_no_auth(self, client: TestClient):
        """Test getting sessions without authentication."""
        response = client.get("/api/v1/auth/sessions")

        assert response.status_code == 401


class TestUserLogout:
    """Test user logout endpoint."""

    def test_successful_logout(self, client: TestClient, test_user):
        """Test successful user logout."""
        # First login
        login_data = {
            "email": test_user.email,
            "password": "TestPass123!",
            "remember_me": False
        }

        login_response = client.post("/api/v1/auth/login", json=login_data)
        tokens = login_response.json()["tokens"]

        # Set authorization header
        client.headers["Authorization"] = f"Bearer {tokens['access_token']}"

        # Logout
        logout_data = {
            "refresh_token": tokens["refresh_token"],
            "logout_all_devices": False
        }

        response = client.post("/api/v1/auth/logout", json=logout_data)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_logout_all_devices(self, client: TestClient, test_user):
        """Test logout from all devices."""
        # First login
        login_data = {
            "email": test_user.email,
            "password": "TestPass123!",
            "remember_me": False
        }

        login_response = client.post("/api/v1/auth/login", json=login_data)
        tokens = login_response.json()["tokens"]

        # Set authorization header
        client.headers["Authorization"] = f"Bearer {tokens['access_token']}"

        # Logout from all devices
        logout_data = {
            "refresh_token": tokens["refresh_token"],
            "logout_all_devices": True
        }

        response = client.post("/api/v1/auth/logout", json=logout_data)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_logout_no_auth(self, client: TestClient):
        """Test logout without authentication."""
        logout_data = {
            "refresh_token": "some_token",
            "logout_all_devices": False
        }

        response = client.post("/api/v1/auth/logout", json=logout_data)

        assert response.status_code == 401

    def test_logout_invalid_refresh_token(self, authenticated_client):
        """Test logout with invalid refresh token."""
        client, token = authenticated_client

        logout_data = {
            "refresh_token": "invalid_token",
            "logout_all_devices": False
        }

        response = client.post("/api/v1/auth/logout", json=logout_data)

        # Should still succeed but log warning
        assert response.status_code == 200


class TestAuthenticationFlow:
    """Test complete authentication flow."""

    def test_complete_auth_flow(self, client: TestClient, test_data_factory: TestDataFactory):
        """Test complete authentication flow from registration to logout."""
        # 1. Register new user
        user_data = test_data_factory.create_user_data(
            email="flowtest@example.com",
            username="flowtest"
        )

        register_response = client.post("/api/v1/auth/register", json=user_data)
        assert register_response.status_code == 201

        # 2. Login
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"],
            "remember_me": False
        }

        login_response = client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == 200

        tokens = login_response.json()["tokens"]
        client.headers["Authorization"] = f"Bearer {tokens['access_token']}"

        # 3. Access protected endpoint
        me_response = client.get("/api/v1/auth/me")
        assert me_response.status_code == 200

        # 4. Refresh token
        refresh_data = {"refresh_token": tokens["refresh_token"]}
        refresh_response = client.post("/api/v1/auth/refresh", json=refresh_data)
        assert refresh_response.status_code == 200

        new_tokens = refresh_response.json()
        client.headers["Authorization"] = f"Bearer {new_tokens['access_token']}"

        # 5. Access protected endpoint with new token
        me_response2 = client.get("/api/v1/auth/me")
        assert me_response2.status_code == 200

        # 6. Logout
        logout_data = {
            "refresh_token": new_tokens["refresh_token"],
            "logout_all_devices": False
        }

        logout_response = client.post("/api/v1/auth/logout", json=logout_data)
        assert logout_response.status_code == 200

        # 7. Try to access protected endpoint after logout (should fail)
        me_response3 = client.get("/api/v1/auth/me")
        assert me_response3.status_code == 401