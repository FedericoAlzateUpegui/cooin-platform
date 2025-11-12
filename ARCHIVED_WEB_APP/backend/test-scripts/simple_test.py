#!/usr/bin/env python3
"""
Simple test script to verify the Cooin backend setup.
"""

def test_imports():
    """Test that all core modules can be imported."""
    print("Testing imports...")

    try:
        import fastapi
        print("✓ FastAPI imported")
    except ImportError as e:
        print(f"✗ FastAPI import failed: {e}")
        return False

    try:
        import sqlalchemy
        print("✓ SQLAlchemy imported")
    except ImportError as e:
        print(f"✗ SQLAlchemy import failed: {e}")
        return False

    try:
        import alembic
        print("✓ Alembic imported")
    except ImportError as e:
        print(f"✗ Alembic import failed: {e}")
        return False

    try:
        import pydantic
        print("✓ Pydantic imported")
    except ImportError as e:
        print(f"✗ Pydantic import failed: {e}")
        return False

    return True

def test_app_imports():
    """Test that our app modules can be imported."""
    print("\nTesting app imports...")

    try:
        from app.core.config import settings
        print("✓ Config imported")
        print(f"  Project: {settings.PROJECT_NAME}")
        print(f"  Debug: {settings.DEBUG}")
    except Exception as e:
        print(f"✗ Config import failed: {e}")
        return False

    try:
        from app.models.user import User
        print("✓ User model imported")
    except Exception as e:
        print(f"✗ User model import failed: {e}")
        return False

    try:
        from app.schemas.auth import LoginRequest
        print("✓ Auth schemas imported")
    except Exception as e:
        print(f"✗ Auth schemas import failed: {e}")
        return False

    return True

def test_fastapi_app():
    """Test that FastAPI app can be created."""
    print("\nTesting FastAPI app creation...")

    try:
        from app.main import app
        print("✓ FastAPI app created successfully")
        print(f"  App title: {app.title}")
        return True
    except Exception as e:
        print(f"✗ FastAPI app creation failed: {e}")
        print(f"  Error details: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("=== Cooin Backend Setup Test ===")

    # Test 1: Core dependencies
    if not test_imports():
        print("\n✗ Core dependency test failed!")
        return False

    # Test 2: App imports
    if not test_app_imports():
        print("\n✗ App import test failed!")
        return False

    # Test 3: FastAPI app
    if not test_fastapi_app():
        print("\n✗ FastAPI app test failed!")
        return False

    print("\n=== All Tests Passed! ===")
    print("Your Cooin backend is ready to run!")
    print("\nNext steps:")
    print("1. Set up PostgreSQL database")
    print("2. Run: alembic upgrade head")
    print("3. Start server: uvicorn app.main:app --reload")

    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)