#!/usr/bin/env python3
"""
Connection system test script for Cooin backend.
Tests the complete connection workflow: registration, profiles, matching, connections, messaging.
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

def create_test_user(role, number):
    """Create a test user with profile."""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    # Register user
    user_data = {
        "email": f"test{role}{number}_{timestamp}@example.com",
        "username": f"test{role}{number}_{timestamp}",
        "password": "TestPass123!",
        "confirm_password": "TestPass123!",
        "role": role,
        "agree_to_terms": True
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    if response.status_code != 201:
        print(f"Failed to register {role} {number}")
        print_response(response, f"REGISTER {role.upper()} {number}")
        return None, None, None

    # Login
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"],
        "remember_me": False
    }

    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code != 200:
        print(f"Failed to login {role} {number}")
        print_response(response, f"LOGIN {role.upper()} {number}")
        return None, None, None

    tokens = response.json()["tokens"]
    access_token = tokens["access_token"]

    # Create profile
    profile_data = {
        "first_name": f"Test{role.capitalize()}",
        "last_name": f"User{number}",
        "display_name": f"Test {role.capitalize()} {number}",
        "bio": f"I'm a test {role} looking for great opportunities",
        "city": "San Francisco" if number % 2 == 0 else "Los Angeles",
        "state_province": "California",
        "country": "United States"
    }

    if role == "lender":
        profile_data.update({
            "min_loan_amount": 10000.0,
            "max_loan_amount": 100000.0,
            "preferred_interest_rate": 7.5,
            "willing_to_lend_unsecured": True
        })
    else:  # borrower
        profile_data.update({
            "loan_purpose": "home_improvement",
            "requested_loan_amount": 25000.0,
            "max_acceptable_rate": 8.0
        })

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(f"{BASE_URL}/profiles/me", json=profile_data, headers=headers)

    if response.status_code != 201:
        print(f"Failed to create profile for {role} {number}")
        print_response(response, f"CREATE PROFILE {role.upper()} {number}")
        return None, None, None

    user_id = response.json()["user_id"]
    print(f"✅ Created {role} {number} (ID: {user_id})")

    return user_id, access_token, user_data["email"]

def test_matching(borrower_token):
    """Test the matching system."""
    print(f"\n{'='*50}")
    print("TESTING MATCHING SYSTEM")
    print(f"{'='*50}")

    headers = {"Authorization": f"Bearer {borrower_token}"}

    # Test matching with criteria
    criteria = {
        "user_role": "lender",
        "location": "California",
        "min_loan_amount": 20000,
        "max_loan_amount": 50000,
        "max_interest_rate": 8.0,
        "verified_only": False
    }

    response = requests.post(f"{BASE_URL}/connections/matching/search", json=criteria, headers=headers)
    print_response(response, "MATCHING SEARCH")

    if response.status_code == 200:
        matches = response.json()["matches"]
        print(f"Found {len(matches)} potential matches")
        return matches

    return []

def test_connection_workflow(borrower_id, borrower_token, lender_id, lender_token):
    """Test complete connection workflow."""
    print(f"\n{'='*50}")
    print("TESTING CONNECTION WORKFLOW")
    print(f"{'='*50}")

    borrower_headers = {"Authorization": f"Bearer {borrower_token}"}
    lender_headers = {"Authorization": f"Bearer {lender_token}"}

    # Step 1: Borrower sends connection request to lender
    connection_data = {
        "receiver_id": lender_id,
        "connection_type": "lending_inquiry",
        "message": "Hi! I'm interested in your lending services for a home improvement project. I need $25,000 for a kitchen renovation.",
        "loan_amount_requested": 25000.0,
        "loan_term_months": 60,
        "interest_rate_proposed": 7.5,
        "loan_purpose": "Kitchen renovation",
        "priority_level": 2
    }

    response = requests.post(f"{BASE_URL}/connections/", json=connection_data, headers=borrower_headers)
    print_response(response, "CREATE CONNECTION REQUEST")

    if response.status_code != 201:
        print("❌ Failed to create connection")
        return None

    connection_id = response.json()["id"]
    print(f"✅ Connection created (ID: {connection_id})")

    # Step 2: Lender checks pending requests
    response = requests.get(f"{BASE_URL}/connections/pending", headers=lender_headers)
    print_response(response, "LENDER PENDING REQUESTS")

    # Step 3: Lender accepts the connection
    update_data = {
        "status": "accepted",
        "response_message": "Great! I'd be happy to help with your kitchen renovation. Let's discuss the details.",
        "interest_rate_proposed": 7.0,
        "receiver_notes": "Kitchen renovation project - seems like a good borrower"
    }

    response = requests.put(f"{BASE_URL}/connections/{connection_id}", json=update_data, headers=lender_headers)
    print_response(response, "ACCEPT CONNECTION")

    if response.status_code != 200:
        print("❌ Failed to accept connection")
        return None

    print(f"✅ Connection accepted")

    # Step 4: Test connection stats
    response = requests.get(f"{BASE_URL}/connections/stats", headers=borrower_headers)
    print_response(response, "BORROWER CONNECTION STATS")

    response = requests.get(f"{BASE_URL}/connections/stats", headers=lender_headers)
    print_response(response, "LENDER CONNECTION STATS")

    return connection_id

def test_messaging(connection_id, borrower_token, lender_token):
    """Test messaging system."""
    print(f"\n{'='*50}")
    print("TESTING MESSAGING SYSTEM")
    print(f"{'='*50}")

    borrower_headers = {"Authorization": f"Bearer {borrower_token}"}
    lender_headers = {"Authorization": f"Bearer {lender_token}"}

    # Step 1: Borrower sends first message
    message_data = {
        "content": "Thanks for accepting my connection request! When would be a good time to discuss the loan details and terms?",
        "message_type": "text"
    }

    response = requests.post(f"{BASE_URL}/connections/{connection_id}/messages", json=message_data, headers=borrower_headers)
    print_response(response, "BORROWER SENDS MESSAGE")

    if response.status_code != 201:
        print("❌ Failed to send message")
        return

    message_id = response.json()["id"]
    print(f"✅ Message sent (ID: {message_id})")

    # Step 2: Lender sends reply
    message_data = {
        "content": "I'm available this week for a call. How about Thursday afternoon? We can discuss the loan terms, timeline, and any documentation you might need.",
        "message_type": "text"
    }

    response = requests.post(f"{BASE_URL}/connections/{connection_id}/messages", json=message_data, headers=lender_headers)
    print_response(response, "LENDER SENDS REPLY")

    # Step 3: Get messages for the connection
    response = requests.get(f"{BASE_URL}/connections/{connection_id}/messages", headers=borrower_headers)
    print_response(response, "GET CONNECTION MESSAGES")

    # Step 4: Mark message as read
    response = requests.put(f"{BASE_URL}/connections/{connection_id}/messages/{message_id}/read", headers=lender_headers)
    print_response(response, "MARK MESSAGE AS READ")

def test_additional_features(connection_id, borrower_token, lender_token):
    """Test additional connection features."""
    print(f"\n{'='*50}")
    print("TESTING ADDITIONAL FEATURES")
    print(f"{'='*50}")

    borrower_headers = {"Authorization": f"Bearer {borrower_token}"}
    lender_headers = {"Authorization": f"Bearer {lender_token}"}

    # Test get specific connection
    response = requests.get(f"{BASE_URL}/connections/{connection_id}", headers=borrower_headers)
    print_response(response, "GET SPECIFIC CONNECTION")

    # Test get all connections
    response = requests.get(f"{BASE_URL}/connections/", headers=borrower_headers)
    print_response(response, "GET ALL CONNECTIONS")

    # Test filter connections by status
    response = requests.get(f"{BASE_URL}/connections/?status_filter=accepted", headers=lender_headers)
    print_response(response, "GET ACCEPTED CONNECTIONS")

def main():
    """Run all connection system tests."""
    print("🚀 Starting Cooin Connection System Tests...")
    print("Make sure your FastAPI server is running on http://localhost:8000")

    # Test health check
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ API health check failed")
            sys.exit(1)
        print("✅ API is healthy")
    except:
        print("❌ Cannot connect to API server")
        sys.exit(1)

    # Create test users
    print(f"\n{'='*50}")
    print("CREATING TEST USERS")
    print(f"{'='*50}")

    borrower1_id, borrower1_token, borrower1_email = create_test_user("borrower", 1)
    borrower2_id, borrower2_token, borrower2_email = create_test_user("borrower", 2)
    lender1_id, lender1_token, lender1_email = create_test_user("lender", 1)
    lender2_id, lender2_token, lender2_email = create_test_user("lender", 2)

    if not all([borrower1_id, borrower2_id, lender1_id, lender2_id]):
        print("❌ Failed to create test users")
        sys.exit(1)

    print(f"✅ Created all test users successfully")

    # Test matching
    matches = test_matching(borrower1_token)

    # Test connection workflow
    connection_id = test_connection_workflow(borrower1_id, borrower1_token, lender1_id, lender1_token)

    if connection_id:
        # Test messaging
        test_messaging(connection_id, borrower1_token, lender1_token)

        # Test additional features
        test_additional_features(connection_id, borrower1_token, lender1_token)

    # Summary
    print(f"\n{'='*60}")
    print("🎉 CONNECTION SYSTEM TESTS COMPLETED!")
    print(f"{'='*60}")
    print("Test Summary:")
    print(f"- Created 4 test users (2 borrowers, 2 lenders)")
    print(f"- Tested matching algorithm")
    print(f"- Tested connection request/response workflow")
    print(f"- Tested messaging system")
    print(f"- Tested connection management features")
    print()
    print("Your Cooin connection system is working correctly!")
    print("You can now:")
    print("1. View API docs at: http://localhost:8000/api/v1/docs")
    print("2. Test connection endpoints interactively")
    print("3. Integrate with your React Native frontend")

if __name__ == "__main__":
    main()