"""
Unit tests for authentication service.
Tests password hashing, token generation, and validation logic.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    TokenData
)
from app.services.auth_service import AuthenticationService
from app.models import User
from app.core.exceptions import AuthenticationError, ValidationError


class TestPasswordSecurity:
    """Test password hashing and verification."""

    def test_password_hashing(self):
        """Test password is properly hashed."""
        password = "TestPass123!"
        hashed = get_password_hash(password)

        assert hashed != password
        assert len(hashed) > 0
        assert hashed.startswith("$2b$")

    def test_password_verification_success(self):
        """Test correct password verification."""
        password = "TestPass123!"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True

    def test_password_verification_failure(self):
        """Test incorrect password verification."""
        password = "TestPass123!"
        wrong_password = "WrongPass123!"
        hashed = get_password_hash(password)

        assert verify_password(wrong_password, hashed) is False

    def test_empty_password_hashing(self):
        """Test hashing empty password."""
        with pytest.raises(ValueError):
            get_password_hash("")


class TestTokenGeneration:
    """Test JWT token creation and validation."""

    def test_create_access_token(self):
        """Test access token creation."""
        data = {"sub": "test@example.com", "user_id": 1}
        token = create_access_token(data)

        assert token is not None
        assert len(token) > 0
        assert isinstance(token, str)

    def test_create_refresh_token(self):
        """Test refresh token creation."""
        data = {"sub": "test@example.com", "user_id": 1}
        token = create_refresh_token(data)

        assert token is not None
        assert len(token) > 0
        assert isinstance(token, str)

    def test_token_with_expiration(self):
        """Test token creation with custom expiration."""
        data = {"sub": "test@example.com"}
        expires_delta = timedelta(minutes=30)
        token = create_access_token(data, expires_delta=expires_delta)

        # Decode token to check expiration
        payload = decode_token(token)

        assert payload is not None
        assert "exp" in payload
        # Check expiration is approximately 30 minutes from now
        exp_time = datetime.utcfromtimestamp(payload["exp"])
        now_plus_30 = datetime.utcnow() + expires_delta
        assert abs((exp_time - now_plus_30).total_seconds()) < 60  # Within 1 minute

    def test_decode_valid_token(self):
        """Test decoding valid token."""
        data = {"sub": "test@example.com", "user_id": 1}
        token = create_access_token(data)

        payload = decode_token(token)

        assert payload is not None
        assert payload["sub"] == "test@example.com"
        assert payload["user_id"] == 1

    def test_decode_invalid_token(self):
        """Test decoding invalid token."""
        invalid_token = "invalid.token.here"

        payload = decode_token(invalid_token)

        assert payload is None

    def test_decode_expired_token(self):
        """Test decoding expired token."""
        data = {"sub": "test@example.com"}
        # Create token that expires immediately
        expires_delta = timedelta(seconds=-1)
        token = create_access_token(data, expires_delta=expires_delta)

        payload = decode_token(token)

        assert payload is None


class TestAuthenticationService:
    """Test authentication service business logic."""

    def test_validate_password_strength(self):
        """Test password strength validation."""
        service = AuthenticationService()

        # Valid passwords
        assert service.validate_password_strength("TestPass123!") is True
        assert service.validate_password_strength("MySecure@Pass1") is True

        # Invalid passwords
        assert service.validate_password_strength("weak") is False
        assert service.validate_password_strength("nouppercasepass123!") is False
        assert service.validate_password_strength("NOLOWERCASEPASS123!") is False
        assert service.validate_password_strength("NoNumber!") is False
        assert service.validate_password_strength("NoSpecialChar123") is False

    def test_validate_email_format(self):
        """Test email format validation."""
        service = AuthenticationService()

        # Valid emails
        assert service.validate_email_format("test@example.com") is True
        assert service.validate_email_format("user.name@domain.co.uk") is True
        assert service.validate_email_format("user+tag@example.org") is True

        # Invalid emails
        assert service.validate_email_format("invalid-email") is False
        assert service.validate_email_format("@example.com") is False
        assert service.validate_email_format("user@") is False
        assert service.validate_email_format("") is False

    @patch('app.services.auth_service.SessionLocal')
    def test_authenticate_user_success(self, mock_session):
        """Test successful user authentication."""
        # Setup mocks
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db

        # Create mock user
        mock_user = Mock(spec=User)
        mock_user.email = "test@example.com"
        mock_user.hashed_password = get_password_hash("TestPass123!")
        mock_user.is_active = True
        mock_user.is_verified = True

        mock_db.query.return_value.filter.return_value.first.return_value = mock_user

        service = AuthenticationService()

        # Test authentication
        result = service.authenticate_user("test@example.com", "TestPass123!")

        assert result == mock_user
        mock_db.query.assert_called_once()

    @patch('app.services.auth_service.SessionLocal')
    def test_authenticate_user_wrong_password(self, mock_session):
        """Test authentication with wrong password."""
        # Setup mocks
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db

        # Create mock user
        mock_user = Mock(spec=User)
        mock_user.email = "test@example.com"
        mock_user.hashed_password = get_password_hash("TestPass123!")
        mock_user.is_active = True
        mock_user.is_verified = True

        mock_db.query.return_value.filter.return_value.first.return_value = mock_user

        service = AuthenticationService()

        # Test authentication with wrong password
        with pytest.raises(AuthenticationError, match="Invalid credentials"):
            service.authenticate_user("test@example.com", "WrongPass123!")

    @patch('app.services.auth_service.SessionLocal')
    def test_authenticate_user_not_found(self, mock_session):
        """Test authentication with non-existent user."""
        # Setup mocks
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None

        service = AuthenticationService()

        # Test authentication
        with pytest.raises(AuthenticationError, match="Invalid credentials"):
            service.authenticate_user("nonexistent@example.com", "TestPass123!")

    @patch('app.services.auth_service.SessionLocal')
    def test_authenticate_user_inactive(self, mock_session):
        """Test authentication with inactive user."""
        # Setup mocks
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db

        # Create mock inactive user
        mock_user = Mock(spec=User)
        mock_user.email = "test@example.com"
        mock_user.hashed_password = get_password_hash("TestPass123!")
        mock_user.is_active = False
        mock_user.is_verified = True

        mock_db.query.return_value.filter.return_value.first.return_value = mock_user

        service = AuthenticationService()

        # Test authentication
        with pytest.raises(AuthenticationError, match="Account is inactive"):
            service.authenticate_user("test@example.com", "TestPass123!")

    def test_generate_user_tokens(self):
        """Test token generation for user."""
        service = AuthenticationService()

        # Create mock user
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_user.email = "test@example.com"
        mock_user.role = Mock()
        mock_user.role.value = "borrower"

        # Generate tokens
        tokens = service.generate_user_tokens(mock_user)

        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert "token_type" in tokens
        assert tokens["token_type"] == "bearer"

        # Verify access token contains user data
        access_payload = decode_token(tokens["access_token"])
        assert access_payload["sub"] == "test@example.com"
        assert access_payload["user_id"] == 1
        assert access_payload["role"] == "borrower"

    def test_validate_registration_data_success(self):
        """Test valid registration data validation."""
        service = AuthenticationService()

        valid_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "TestPass123!",
            "confirm_password": "TestPass123!",
            "role": "borrower",
            "agree_to_terms": True
        }

        # Should not raise any exception
        service.validate_registration_data(valid_data)

    def test_validate_registration_data_password_mismatch(self):
        """Test registration data validation with password mismatch."""
        service = AuthenticationService()

        invalid_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "TestPass123!",
            "confirm_password": "DifferentPass123!",
            "role": "borrower",
            "agree_to_terms": True
        }

        with pytest.raises(ValidationError, match="Passwords do not match"):
            service.validate_registration_data(invalid_data)

    def test_validate_registration_data_terms_not_agreed(self):
        """Test registration data validation without terms agreement."""
        service = AuthenticationService()

        invalid_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "TestPass123!",
            "confirm_password": "TestPass123!",
            "role": "borrower",
            "agree_to_terms": False
        }

        with pytest.raises(ValidationError, match="You must agree to the terms"):
            service.validate_registration_data(invalid_data)

    def test_validate_registration_data_weak_password(self):
        """Test registration data validation with weak password."""
        service = AuthenticationService()

        invalid_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "weak",
            "confirm_password": "weak",
            "role": "borrower",
            "agree_to_terms": True
        }

        with pytest.raises(ValidationError, match="Password does not meet security requirements"):
            service.validate_registration_data(invalid_data)


class TestTokenData:
    """Test TokenData model."""

    def test_token_data_creation(self):
        """Test TokenData creation."""
        token_data = TokenData(
            username="test@example.com",
            user_id=1,
            role="borrower"
        )

        assert token_data.username == "test@example.com"
        assert token_data.user_id == 1
        assert token_data.role == "borrower"

    def test_token_data_optional_fields(self):
        """Test TokenData with optional fields."""
        token_data = TokenData(username="test@example.com")

        assert token_data.username == "test@example.com"
        assert token_data.user_id is None
        assert token_data.role is None