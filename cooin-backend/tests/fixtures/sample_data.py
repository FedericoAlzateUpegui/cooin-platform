"""
Sample data fixtures for testing.
Provides realistic test data for loans, users, and profiles.
"""

from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Dict, Any


class SampleDataFixtures:
    """Collection of sample data for testing."""

    @staticmethod
    def sample_users() -> List[Dict[str, Any]]:
        """Sample user data for testing."""
        return [
            {
                "email": "john.borrower@example.com",
                "username": "johnb",
                "password": "BorrowerPass123!",
                "role": "borrower",
                "first_name": "John",
                "last_name": "Doe",
                "city": "San Francisco",
                "state": "California"
            },
            {
                "email": "mary.lender@example.com",
                "username": "maryl",
                "password": "LenderPass123!",
                "role": "lender",
                "first_name": "Mary",
                "last_name": "Smith",
                "city": "San Francisco",
                "state": "California"
            },
            {
                "email": "david.borrower@example.com",
                "username": "davidb",
                "password": "SecurePass123!",
                "role": "borrower",
                "first_name": "David",
                "last_name": "Johnson",
                "city": "Los Angeles",
                "state": "California"
            },
            {
                "email": "sarah.lender@example.com",
                "username": "sarahl",
                "password": "LenderSarah123!",
                "role": "lender",
                "first_name": "Sarah",
                "last_name": "Wilson",
                "city": "New York",
                "state": "New York"
            }
        ]

    @staticmethod
    def sample_loan_requests() -> List[Dict[str, Any]]:
        """Sample loan request data for testing."""
        return [
            {
                "loan_amount": 25000.00,
                "loan_purpose": "home_improvement",
                "loan_term_months": 36,
                "max_interest_rate": 8.5,
                "description": "Kitchen renovation project - updating cabinets, countertops, and appliances",
                "credit_score": 720,
                "annual_income": 85000.00,
                "employment_status": "employed_full_time"
            },
            {
                "loan_amount": 15000.00,
                "loan_purpose": "debt_consolidation",
                "loan_term_months": 24,
                "max_interest_rate": 12.0,
                "description": "Consolidating high-interest credit card debt",
                "credit_score": 650,
                "annual_income": 55000.00,
                "employment_status": "employed_full_time"
            },
            {
                "loan_amount": 40000.00,
                "loan_purpose": "education",
                "loan_term_months": 60,
                "max_interest_rate": 7.0,
                "description": "Graduate school tuition for MBA program",
                "credit_score": 780,
                "annual_income": 95000.00,
                "employment_status": "employed_full_time"
            },
            {
                "loan_amount": 10000.00,
                "loan_purpose": "small_business",
                "loan_term_months": 18,
                "max_interest_rate": 15.0,
                "description": "Startup capital for online consulting business",
                "credit_score": 690,
                "annual_income": 48000.00,
                "employment_status": "self_employed"
            },
            {
                "loan_amount": 35000.00,
                "loan_purpose": "medical",
                "loan_term_months": 48,
                "max_interest_rate": 9.0,
                "description": "Medical expenses for necessary surgery not covered by insurance",
                "credit_score": 740,
                "annual_income": 72000.00,
                "employment_status": "employed_full_time"
            }
        ]

    @staticmethod
    def sample_lending_offers() -> List[Dict[str, Any]]:
        """Sample lending offer data for testing."""
        return [
            {
                "available_amount": 100000.00,
                "min_loan_amount": 5000.00,
                "max_loan_amount": 50000.00,
                "interest_rate": 7.5,
                "preferred_loan_terms": "24,36,48",
                "lending_criteria": "Minimum 680 credit score, stable employment, debt-to-income ratio below 40%",
                "geographic_preference": "California,Nevada,Arizona",
                "loan_purposes": "home_improvement,debt_consolidation,education"
            },
            {
                "available_amount": 200000.00,
                "min_loan_amount": 10000.00,
                "max_loan_amount": 75000.00,
                "interest_rate": 6.8,
                "preferred_loan_terms": "36,48,60",
                "lending_criteria": "Minimum 700 credit score, 2+ years employment history, verified income",
                "geographic_preference": "California,New York,Texas",
                "loan_purposes": "home_improvement,education,medical"
            },
            {
                "available_amount": 50000.00,
                "min_loan_amount": 3000.00,
                "max_loan_amount": 25000.00,
                "interest_rate": 9.2,
                "preferred_loan_terms": "12,18,24",
                "lending_criteria": "Minimum 620 credit score, willing to work with debt consolidation",
                "geographic_preference": "Any",
                "loan_purposes": "debt_consolidation,small_business"
            },
            {
                "available_amount": 150000.00,
                "min_loan_amount": 15000.00,
                "max_loan_amount": 60000.00,
                "interest_rate": 8.1,
                "preferred_loan_terms": "36,48",
                "lending_criteria": "Minimum 720 credit score, professionals preferred, low risk tolerance",
                "geographic_preference": "California,Washington,Oregon",
                "loan_purposes": "home_improvement,education"
            }
        ]

    @staticmethod
    def sample_user_profiles() -> List[Dict[str, Any]]:
        """Sample user profile data for testing."""
        return [
            {
                "bio": "Software engineer looking to improve home for growing family. Stable income and good credit history.",
                "profile_image_url": None,
                "is_profile_public": True,
                "income_range": "75k_100k",
                "employment_status": "employed_full_time",
                "years_at_job": 5,
                "monthly_income": 7500.00,
                "credit_score_range": "700_750"
            },
            {
                "bio": "Experienced investor with 15+ years in peer-to-peer lending. Focus on safe, secured loans.",
                "profile_image_url": None,
                "is_profile_public": True,
                "investment_experience": "expert",
                "lending_preference": "conservative",
                "total_loans_funded": 45,
                "average_return": 8.2
            },
            {
                "bio": "Marketing professional seeking to consolidate debt and improve financial situation.",
                "profile_image_url": None,
                "is_profile_public": True,
                "income_range": "50k_75k",
                "employment_status": "employed_full_time",
                "years_at_job": 3,
                "monthly_income": 4800.00,
                "credit_score_range": "650_700"
            },
            {
                "bio": "Conservative lender focused on education and home improvement loans. Looking for reliable borrowers.",
                "profile_image_url": None,
                "is_profile_public": True,
                "investment_experience": "intermediate",
                "lending_preference": "conservative",
                "total_loans_funded": 23,
                "average_return": 7.1
            }
        ]

    @staticmethod
    def sample_connections() -> List[Dict[str, Any]]:
        """Sample connection data for testing."""
        return [
            {
                "status": "accepted",
                "message": "Hi, I'm interested in your loan request for home improvement. Let's discuss terms.",
                "connection_date": datetime.utcnow() - timedelta(days=7)
            },
            {
                "status": "pending",
                "message": "Hello, your lending offer looks interesting. I'd like to learn more about your criteria.",
                "connection_date": datetime.utcnow() - timedelta(days=3)
            },
            {
                "status": "accepted",
                "message": "Thanks for considering my loan request. Looking forward to working together.",
                "connection_date": datetime.utcnow() - timedelta(days=14)
            }
        ]

    @staticmethod
    def sample_ratings() -> List[Dict[str, Any]]:
        """Sample rating data for testing."""
        return [
            {
                "rating": 5,
                "comment": "Excellent borrower - prompt communication, transparent about finances, paid as agreed.",
                "rating_type": "lender_to_borrower",
                "transaction_amount": 25000.00
            },
            {
                "rating": 4,
                "comment": "Good lender with fair terms. Professional and helpful throughout the process.",
                "rating_type": "borrower_to_lender",
                "transaction_amount": 25000.00
            },
            {
                "rating": 5,
                "comment": "Outstanding lender - competitive rates, quick approval, smooth transaction.",
                "rating_type": "borrower_to_lender",
                "transaction_amount": 15000.00
            },
            {
                "rating": 4,
                "comment": "Reliable borrower with good financial discipline. Would lend to again.",
                "rating_type": "lender_to_borrower",
                "transaction_amount": 15000.00
            }
        ]

    @staticmethod
    def sample_analytics_events() -> List[Dict[str, Any]]:
        """Sample analytics event data for testing."""
        return [
            {
                "event_type": "page_view",
                "timestamp": datetime.utcnow().isoformat(),
                "page": "loan_request_detail",
                "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
                "session_duration": 45
            },
            {
                "event_type": "user_action",
                "timestamp": datetime.utcnow().isoformat(),
                "action": "connection_request_sent",
                "target_user_id": 2,
                "loan_request_id": 1
            },
            {
                "event_type": "search",
                "timestamp": datetime.utcnow().isoformat(),
                "search_query": "home improvement loan",
                "search_filters": {"min_amount": 20000, "max_rate": 9.0},
                "results_count": 12
            },
            {
                "event_type": "match_viewed",
                "timestamp": datetime.utcnow().isoformat(),
                "match_score": 0.87,
                "loan_request_id": 1,
                "lender_id": 2
            }
        ]

    @staticmethod
    def create_test_scenario_complete_loan() -> Dict[str, Any]:
        """
        Create a complete test scenario with borrower, lender, and successful loan.
        Returns all related data for integration testing.
        """
        return {
            "borrower": {
                "email": "complete.borrower@example.com",
                "username": "completeb",
                "password": "TestPass123!",
                "role": "borrower",
                "profile": {
                    "first_name": "Complete",
                    "last_name": "Borrower",
                    "city": "San Francisco",
                    "state_province": "California",
                    "country": "United States",
                    "bio": "Test scenario borrower for complete loan flow",
                    "income_range": "75k_100k",
                    "employment_status": "employed_full_time"
                }
            },
            "lender": {
                "email": "complete.lender@example.com",
                "username": "completel",
                "password": "TestPass123!",
                "role": "lender",
                "profile": {
                    "first_name": "Complete",
                    "last_name": "Lender",
                    "city": "San Francisco",
                    "state_province": "California",
                    "country": "United States",
                    "bio": "Test scenario lender for complete loan flow",
                    "investment_experience": "intermediate"
                }
            },
            "loan_request": {
                "loan_amount": 30000.00,
                "loan_purpose": "home_improvement",
                "loan_term_months": 36,
                "max_interest_rate": 8.0,
                "description": "Complete test scenario loan request"
            },
            "lending_offer": {
                "available_amount": 100000.00,
                "min_loan_amount": 10000.00,
                "max_loan_amount": 50000.00,
                "interest_rate": 7.2,
                "preferred_loan_terms": "24,36,48",
                "lending_criteria": "Test scenario lending criteria"
            },
            "connection": {
                "message": "Test scenario connection between borrower and lender",
                "status": "accepted"
            },
            "rating": {
                "borrower_to_lender": {
                    "rating": 5,
                    "comment": "Excellent test scenario lender"
                },
                "lender_to_borrower": {
                    "rating": 5,
                    "comment": "Excellent test scenario borrower"
                }
            }
        }