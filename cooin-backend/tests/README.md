# Cooin Backend Test Suite

Comprehensive testing suite for the Cooin peer-to-peer lending platform backend API.

## 📁 Test Structure

```
tests/
├── __init__.py                     # Test package initialization
├── conftest.py                     # Shared fixtures and configuration
├── pytest.ini                     # Pytest configuration
├── run_tests.py                    # Test runner script
├── README.md                       # This documentation
├── unit/                          # Unit tests
│   ├── __init__.py
│   ├── test_auth_service.py       # Authentication service tests
│   ├── test_matching_service.py   # Matching algorithm tests
│   └── ...                        # More unit tests
├── integration/                   # Integration tests
│   ├── __init__.py
│   ├── test_auth_api.py          # Authentication API tests
│   ├── test_matching_api.py      # Matching API tests
│   ├── test_analytics_api.py     # Analytics API tests
│   └── ...                       # More integration tests
└── fixtures/                     # Test data and utilities
    ├── __init__.py
    └── sample_data.py            # Sample data generators
```

## 🚀 Quick Start

### Prerequisites

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Check Test Environment**
   ```bash
   python run_tests.py check
   ```

### Running Tests

#### Basic Test Commands

```bash
# Run all tests
python run_tests.py all

# Run only unit tests
python run_tests.py unit

# Run only integration tests
python run_tests.py integration

# Run tests with coverage report
python run_tests.py coverage

# Run quick tests (exclude slow tests)
python run_tests.py quick
```

#### Test by Category

```bash
# Authentication tests only
python run_tests.py auth

# Matching algorithm tests only
python run_tests.py matching

# Analytics tests only
python run_tests.py analytics

# Search functionality tests
python run_tests.py search

# Mobile API tests
python run_tests.py mobile
```

#### Advanced Options

```bash
# Run specific test file
python run_tests.py all --file tests/unit/test_auth_service.py

# Clean test artifacts
python run_tests.py clean

# Verbose output
python run_tests.py all --verbose
```

#### Direct Pytest Commands

```bash
# Run all tests with pytest directly
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_auth_service.py

# Run tests matching a pattern
pytest -k "test_login"

# Run tests with coverage
pytest --cov=app --cov-report=html

# Run tests with specific markers
pytest -m "unit"
pytest -m "integration"
pytest -m "auth"
```

## 🏷️ Test Markers

Tests are categorized using pytest markers:

- `@pytest.mark.unit` - Unit tests (isolated component testing)
- `@pytest.mark.integration` - Integration tests (API endpoint testing)
- `@pytest.mark.auth` - Authentication related tests
- `@pytest.mark.matching` - Matching algorithm tests
- `@pytest.mark.analytics` - Analytics and reporting tests
- `@pytest.mark.search` - Search functionality tests
- `@pytest.mark.mobile` - Mobile API tests
- `@pytest.mark.slow` - Tests that take longer to run
- `@pytest.mark.cache` - Cache-related tests
- `@pytest.mark.database` - Database operation tests

## 🧪 Test Types

### Unit Tests (`tests/unit/`)

Test individual components in isolation:

- **Authentication Service** (`test_auth_service.py`)
  - Password hashing and verification
  - JWT token generation and validation
  - User authentication logic
  - Registration validation

- **Matching Service** (`test_matching_service.py`)
  - Compatibility scoring algorithms
  - Loan matching criteria
  - Geographic proximity calculations
  - Match result generation

- **Analytics Service** (`test_analytics_service.py`)
  - Metrics calculations
  - Report generation logic
  - Data aggregation functions

### Integration Tests (`tests/integration/`)

Test API endpoints and component interactions:

- **Authentication API** (`test_auth_api.py`)
  - User registration flow
  - Login/logout functionality
  - Token refresh mechanism
  - Protected endpoint access

- **Matching API** (`test_matching_api.py`)
  - Borrower match retrieval
  - Lender match generation
  - Match suggestions
  - Mobile-optimized responses

- **Analytics API** (`test_analytics_api.py`)
  - Dashboard metrics endpoints
  - Report generation and export
  - Mobile analytics summaries
  - Event tracking

## 🔧 Test Fixtures

### Database Fixtures

- `db_session` - Fresh database session for each test
- `client` - FastAPI test client with database override
- `test_user` - Pre-created test user in database
- `test_lender` - Pre-created lender user
- `test_user_profile` - Complete user profile
- `test_loan_request` - Sample loan request
- `test_lending_offer` - Sample lending offer

### Authentication Fixtures

- `authenticated_client` - Test client with valid access token
- `authenticated_lender_client` - Lender client with access token
- `test_user_data` - Sample user registration data
- `test_lender_data` - Sample lender registration data

### Data Factory Fixtures

- `test_data_factory` - Factory for generating test data
- `TestDataFactory.create_user_data()` - Generate user data
- `TestDataFactory.create_profile_data()` - Generate profile data
- `TestDataFactory.create_loan_request_data()` - Generate loan data

## 📊 Coverage Reports

### Generating Coverage Reports

```bash
# Generate HTML coverage report
python run_tests.py coverage

# View coverage report
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html  # Windows
```

### Coverage Targets

- **Overall Coverage**: ≥ 80%
- **Critical Components**: ≥ 90%
  - Authentication services
  - Security functions
  - Matching algorithms
  - Payment processing

### Coverage Configuration

Coverage settings in `pytest.ini`:

```ini
addopts = --cov=app --cov-report=html --cov-report=term-missing --cov-fail-under=80
```

## 🔍 Test Data

### Sample Data Generators

The `tests/fixtures/sample_data.py` provides realistic test data:

- **Sample Users**: Borrowers and lenders with varied profiles
- **Loan Requests**: Different purposes, amounts, and terms
- **Lending Offers**: Various criteria and preferences
- **Complete Scenarios**: End-to-end loan flow data

### Using Sample Data

```python
from tests.fixtures.sample_data import SampleDataFixtures

# Get sample users
users = SampleDataFixtures.sample_users()

# Get sample loan requests
loan_requests = SampleDataFixtures.sample_loan_requests()

# Create complete test scenario
scenario = SampleDataFixtures.create_test_scenario_complete_loan()
```

## 🚨 Testing Best Practices

### Test Organization

1. **One test class per feature/component**
2. **Descriptive test method names**
3. **Arrange-Act-Assert pattern**
4. **Independent tests** (no dependencies between tests)

### Test Data Management

1. **Use fixtures for reusable test data**
2. **Clean database state between tests**
3. **Use factories for dynamic test data**
4. **Avoid hard-coded values in tests**

### Mock Usage

```python
from unittest.mock import Mock, patch, AsyncMock

# Mock external services
@patch('app.services.external_api.call')
def test_with_external_mock(mock_call):
    mock_call.return_value = {"status": "success"}
    # Test logic here

# Mock async functions
@patch('app.services.cache_service.get', new_callable=AsyncMock)
async def test_with_async_mock(mock_get):
    mock_get.return_value = cached_data
    # Test logic here
```

### Error Testing

```python
def test_authentication_with_invalid_credentials(client):
    """Test authentication failure with wrong password."""
    response = client.post("/api/v1/auth/login", json={
        "email": "user@example.com",
        "password": "wrong_password"
    })

    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]
```

## 🐛 Debugging Tests

### Verbose Test Output

```bash
# Run tests with maximum verbosity
pytest -vvv

# Show local variables on failure
pytest --tb=long

# Show only short traceback
pytest --tb=short

# Stop on first failure
pytest -x
```

### Test Debugging

```python
def test_with_debugging(client):
    response = client.post("/api/v1/auth/login", json=login_data)

    # Debug response
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # Use debugger
    import pdb; pdb.set_trace()

    assert response.status_code == 200
```

### Common Issues

1. **Database State**: Tests failing due to leftover data
   ```bash
   python run_tests.py clean  # Clean artifacts
   ```

2. **Import Errors**: Module path issues
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

3. **Async Test Issues**: Use `pytest-asyncio`
   ```python
   @pytest.mark.asyncio
   async def test_async_function():
       result = await async_function()
       assert result is not None
   ```

## 📈 Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run tests
      run: |
        python run_tests.py coverage

    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

## 📝 Writing New Tests

### Unit Test Template

```python
"""
Unit tests for [component_name].
Tests [brief_description].
"""

import pytest
from unittest.mock import Mock, patch

from app.services.your_service import YourService


class TestYourService:
    """Test YourService functionality."""

    @pytest.fixture
    def service(self):
        """Create service instance for testing."""
        return YourService()

    def test_basic_functionality(self, service):
        """Test basic service functionality."""
        # Arrange
        input_data = {"key": "value"}

        # Act
        result = service.process_data(input_data)

        # Assert
        assert result is not None
        assert result["processed"] is True

    @patch('app.services.your_service.external_call')
    def test_with_external_dependency(self, mock_external, service):
        """Test service with mocked external dependency."""
        # Arrange
        mock_external.return_value = {"status": "success"}

        # Act
        result = service.method_with_external_call()

        # Assert
        assert result["external_result"] == "success"
        mock_external.assert_called_once()
```

### Integration Test Template

```python
"""
Integration tests for [API_name] endpoints.
Tests [brief_description].
"""

import pytest
from fastapi.testclient import TestClient


class TestYourAPI:
    """Test Your API endpoints."""

    def test_successful_request(self, authenticated_client):
        """Test successful API request."""
        client, token = authenticated_client

        request_data = {"field": "value"}

        response = client.post("/api/v1/your-endpoint", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_validation_error(self, client: TestClient):
        """Test API validation error handling."""
        invalid_data = {"invalid": "data"}

        response = client.post("/api/v1/your-endpoint", json=invalid_data)

        assert response.status_code == 422

    def test_authentication_required(self, client: TestClient):
        """Test endpoint requires authentication."""
        response = client.post("/api/v1/your-endpoint", json={})

        assert response.status_code == 401
```

## 📚 Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [Factory Boy](https://factoryboy.readthedocs.io/)

---

For questions or issues with the test suite, please check the troubleshooting section or create an issue in the project repository.