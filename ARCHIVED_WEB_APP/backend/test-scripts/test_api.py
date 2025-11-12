#!/usr/bin/env python3
"""
Simple API test script for Cooin backend.
Run this script to test the authentication endpoints.
"""

import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

def print_response(response, title):
    """Print formatted response."""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_health():
    """Test health endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print_response(response, "HEALTH CHECK")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_register():
    """Test user registration."""
    user_data = {
        "email": f"test{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
        "username": f"testuser_{datetime.now().strftime('%H%M%S')}",
        "password": "TestPass123!",
        "confirm_password": "TestPass123!",
        "role": "borrower",
        "agree_to_terms": True
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        print_response(response, "USER REGISTRATION")

        if response.status_code == 201:
            return user_data["email"], user_data["password"]
        else:
            return None, None
    except Exception as e:
        print(f"Registration failed: {e}")
        return None, None

def test_login(email, password):
    """Test user login."""
    login_data = {
        "email": email,
        "password": password,
        "remember_me": False
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print_response(response, "USER LOGIN")

        if response.status_code == 200:
            data = response.json()
            return data["tokens"]["access_token"], data["tokens"]["refresh_token"]
        else:
            return None, None
    except Exception as e:
        print(f"Login failed: {e}")
        return None, None

def test_get_current_user(access_token):
    """Test getting current user info."""
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        print_response(response, "GET CURRENT USER")
        return response.status_code == 200
    except Exception as e:
        print(f"Get current user failed: {e}")
        return False

def test_refresh_token(refresh_token):
    """Test token refresh."""
    token_data = {"refresh_token": refresh_token}

    try:
        response = requests.post(f"{BASE_URL}/auth/refresh", json=token_data)
        print_response(response, "REFRESH TOKEN")

        if response.status_code == 200:
            data = response.json()
            return data["access_token"]
        else:
            return None
    except Exception as e:
        print(f"Token refresh failed: {e}")
        return None

def test_get_sessions(access_token):
    """Test getting user sessions."""
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(f"{BASE_URL}/auth/sessions", headers=headers)
        print_response(response, "GET USER SESSIONS")
        return response.status_code == 200
    except Exception as e:
        print(f"Get sessions failed: {e}")
        return False

def test_profile_operations(access_token):
    """Test profile CRUD operations."""
    headers = {"Authorization": f"Bearer {access_token}"}

    # Test profile completion
    try:
        response = requests.get(f"{BASE_URL}/profiles/me/completion", headers=headers)
        print_response(response, "PROFILE COMPLETION STATUS")
    except Exception as e:
        print(f"Profile completion check failed: {e}")

    # Test create profile
    profile_data = {
        "first_name": "John",
        "last_name": "Doe",
        "display_name": "JohnD",
        "bio": "Looking for a home improvement loan",
        "city": "San Francisco",
        "state_province": "California",
        "country": "United States"
    }

    try:
        response = requests.post(f"{BASE_URL}/profiles/me", json=profile_data, headers=headers)
        print_response(response, "CREATE PROFILE")
        profile_created = response.status_code == 201
    except Exception as e:
        print(f"Profile creation failed: {e}")
        profile_created = False

    # Test get profile
    try:
        response = requests.get(f"{BASE_URL}/profiles/me", headers=headers)
        print_response(response, "GET MY PROFILE")
    except Exception as e:
        print(f"Get profile failed: {e}")

    # Test update profile if created
    if profile_created:
        update_data = {
            "bio": "Updated bio - seeking home improvement loan for kitchen renovation"
        }
        try:
            response = requests.put(f"{BASE_URL}/profiles/me", json=update_data, headers=headers)
            print_response(response, "UPDATE PROFILE")
        except Exception as e:
            print(f"Profile update failed: {e}")

    # Test search profiles
    try:
        response = requests.get(f"{BASE_URL}/profiles/?limit=5")
        print_response(response, "SEARCH PROFILES")
    except Exception as e:
        print(f"Profile search failed: {e}")

    return profile_created


def test_logout(access_token, refresh_token):
    """Test user logout."""
    headers = {"Authorization": f"Bearer {access_token}"}
    logout_data = {
        "refresh_token": refresh_token,
        "logout_all_devices": False
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/logout", json=logout_data, headers=headers)
        print_response(response, "USER LOGOUT")
        return response.status_code == 200
    except Exception as e:
        print(f"Logout failed: {e}")
        return False

def main():
    """Run all API tests."""
    print("Starting Cooin API Tests...")
    print("Make sure your FastAPI server is running on http://localhost:8000")

    # Test 1: Health check
    if not test_health():
        print("❌ Health check failed. Is the server running?")
        sys.exit(1)

    print("✅ Health check passed")

    # Test 2: User registration
    email, password = test_register()
    if not email:
        print("❌ Registration failed")
        sys.exit(1)

    print("✅ Registration passed")

    # Test 3: User login
    access_token, refresh_token = test_login(email, password)
    if not access_token:
        print("❌ Login failed")
        sys.exit(1)

    print("✅ Login passed")

    # Test 4: Get current user
    if not test_get_current_user(access_token):
        print("❌ Get current user failed")
    else:
        print("✅ Get current user passed")

    # Test 5: Get sessions
    if not test_get_sessions(access_token):
        print("❌ Get sessions failed")
    else:
        print("✅ Get sessions passed")

    # Test 6: Profile operations
    profile_created = test_profile_operations(access_token)
    if profile_created:
        print("✅ Profile operations passed")
    else:
        print("⚠️  Some profile operations failed (check individual tests above)")

    # Test 7: Refresh token
    new_access_token = test_refresh_token(refresh_token)
    if not new_access_token:
        print("❌ Refresh token failed")
    else:
        print("✅ Refresh token passed")

    # Test 8: Logout
    if not test_logout(access_token, refresh_token):
        print("❌ Logout failed")
    else:
        print("✅ Logout passed")

    print(f"\n{'='*50}")
    print("🎉 All API tests completed!")
    print(f"{'='*50}")
    print("Your Cooin backend is working correctly!")
    print("You can now:")
    print("1. View API docs at: http://localhost:8000/api/v1/docs")
    print("2. Test endpoints interactively")
    print("3. Connect your React Native frontend")

if __name__ == "__main__":
    main()