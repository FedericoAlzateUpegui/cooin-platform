"""
Pytest configuration and shared fixtures for the test suite.
Provides database setup, client fixtures, and test data.
"""

import pytest
import asyncio
from typing import Generator, AsyncGenerator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base, get_database
from app.core.config import settings
from app.models import User, UserProfile, LoanRequest, LendingOffer
from app.core.security import get_password_hash
from app.services.cache_service import get_app_cache_service


# Test database configuration
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
test_engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Create a fresh database session for each test.
    All changes are rolled back after the test.
    """
    # Create all tables
    Base.metadata.create_all(bind=test_engine)

    # Create session
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    Create a test client with database dependency override.
    """
    def override_get_database():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_database] = override_get_database

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "TestPass123!",
        "confirm_password": "TestPass123!",
        "role": "borrower",
        "agree_to_terms": True
    }


@pytest.fixture
def test_lender_data():
    """Sample lender data for testing."""
    return {
        "email": "lender@example.com",
        "username": "testlender",
        "password": "TestPass123!",
        "confirm_password": "TestPass123!",
        "role": "lender",
        "agree_to_terms": True
    }


@pytest.fixture
def test_user(db_session: Session) -> User:
    """Create a test user in the database."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("TestPass123!"),
        role="borrower",
        is_active=True,
        is_verified=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_lender(db_session: Session) -> User:
    """Create a test lender in the database."""
    user = User(
        email="lender@example.com",
        username="testlender",
        hashed_password=get_password_hash("TestPass123!"),
        role="lender",
        is_active=True,
        is_verified=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_user_profile(db_session: Session, test_user: User) -> UserProfile:
    """Create a test user profile."""
    profile = UserProfile(
        user_id=test_user.id,
        first_name="John",
        last_name="Doe",
        display_name="JohnD",
        bio="Test user bio",
        city="San Francisco",
        state_province="California",
        country="United States",
        is_profile_public=True,
        profile_completion_percentage=75.0
    )
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(profile)
    return profile


@pytest.fixture
def test_loan_request(db_session: Session, test_user: User) -> LoanRequest:
    """Create a test loan request."""
    loan_request = LoanRequest(
        user_id=test_user.id,
        loan_amount=25000.00,
        loan_purpose="home_improvement",
        loan_term_months=36,
        max_interest_rate=8.5,
        description="Need funds for kitchen renovation",
        status="active"
    )
    db_session.add(loan_request)
    db_session.commit()
    db_session.refresh(loan_request)
    return loan_request


@pytest.fixture
def test_lending_offer(db_session: Session, test_lender: User) -> LendingOffer:
    """Create a test lending offer."""
    lending_offer = LendingOffer(
        user_id=test_lender.id,
        available_amount=50000.00,
        min_loan_amount=10000.00,
        max_loan_amount=100000.00,
        interest_rate=7.5,
        preferred_loan_terms="24,36,48",
        lending_criteria="Stable income, good credit history",
        status="active"
    )
    db_session.add(lending_offer)
    db_session.commit()
    db_session.refresh(lending_offer)
    return lending_offer


@pytest.fixture
def authenticated_client(client: TestClient, test_user: User) -> tuple[TestClient, str]:
    """
    Create an authenticated test client with access token.
    Returns tuple of (client, access_token).
    """
    # Login to get access token
    login_data = {
        "email": test_user.email,
        "password": "TestPass123!"
    }

    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200

    tokens = response.json()["tokens"]
    access_token = tokens["access_token"]

    # Set authorization header for subsequent requests
    client.headers["Authorization"] = f"Bearer {access_token}"

    return client, access_token


@pytest.fixture
def authenticated_lender_client(client: TestClient, test_lender: User) -> tuple[TestClient, str]:
    """
    Create an authenticated lender test client with access token.
    Returns tuple of (client, access_token).
    """
    # Login to get access token
    login_data = {
        "email": test_lender.email,
        "password": "TestPass123!"
    }

    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200

    tokens = response.json()["tokens"]
    access_token = tokens["access_token"]

    # Set authorization header for subsequent requests
    client.headers["Authorization"] = f"Bearer {access_token}"

    return client, access_token


@pytest.fixture(scope="function")
async def cache_service():
    """Get cache service for testing."""
    cache = get_app_cache_service()
    yield cache
    # Clean up cache after each test
    await cache.clear()


class TestDataFactory:
    """Factory for creating test data."""

    @staticmethod
    def create_user_data(
        email: str = "user@example.com",
        username: str = "testuser",
        role: str = "borrower"
    ) -> dict:
        """Create user registration data."""
        return {
            "email": email,
            "username": username,
            "password": "TestPass123!",
            "confirm_password": "TestPass123!",
            "role": role,
            "agree_to_terms": True
        }

    @staticmethod
    def create_profile_data(
        first_name: str = "John",
        last_name: str = "Doe"
    ) -> dict:
        """Create profile data."""
        return {
            "first_name": first_name,
            "last_name": last_name,
            "display_name": f"{first_name}{last_name[0]}",
            "bio": "Test user profile",
            "city": "San Francisco",
            "state_province": "California",
            "country": "United States"
        }

    @staticmethod
    def create_loan_request_data(
        loan_amount: float = 25000.0,
        loan_term_months: int = 36
    ) -> dict:
        """Create loan request data."""
        return {
            "loan_amount": loan_amount,
            "loan_purpose": "home_improvement",
            "loan_term_months": loan_term_months,
            "max_interest_rate": 8.5,
            "description": "Need funds for renovation"
        }

    @staticmethod
    def create_lending_offer_data(
        available_amount: float = 50000.0,
        interest_rate: float = 7.5
    ) -> dict:
        """Create lending offer data."""
        return {
            "available_amount": available_amount,
            "min_loan_amount": 10000.0,
            "max_loan_amount": 100000.0,
            "interest_rate": interest_rate,
            "preferred_loan_terms": "24,36,48",
            "lending_criteria": "Stable income required"
        }


@pytest.fixture
def test_data_factory():
    """Provide test data factory."""
    return TestDataFactory


# Test configuration overrides
@pytest.fixture(autouse=True)
def override_settings():
    """Override settings for testing."""
    # Override any settings needed for testing
    settings.TESTING = True
    settings.DEBUG = True
    yield
    # Restore settings if needed