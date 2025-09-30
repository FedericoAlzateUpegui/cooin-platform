#!/usr/bin/env python3
"""
Debug script to test user registration directly
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User, UserRole, UserStatus
from app.services.user_service import UserService
from app.schemas.user import UserCreate
from app.core.config import settings

# Create database session
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_registration():
    """Test user registration directly"""
    db = SessionLocal()

    try:
        # Create user data
        user_data = UserCreate(
            email="debug@example.com",
            username="debuguser",
            password="TestPass123!",
            confirm_password="TestPass123!",
            role="borrower"
        )

        print(f"Attempting to create user: {user_data.email}")

        # Try to create user
        user = UserService.create_user(db, user_data)
        print(f"User created successfully: {user.id} - {user.email}")

    except Exception as e:
        print(f"Error creating user: {e}")
        import traceback
        traceback.print_exc()

    finally:
        db.close()

if __name__ == "__main__":
    test_registration()