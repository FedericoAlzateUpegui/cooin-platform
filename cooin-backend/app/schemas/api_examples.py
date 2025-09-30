"""
API request/response examples for enhanced Swagger documentation.
Provides comprehensive examples for all endpoints.
"""

from typing import Dict, Any

# Authentication Examples
AUTH_EXAMPLES = {
    "register": {
        "request": {
            "summary": "User Registration",
            "description": "Register a new user with email and password",
            "value": {
                "email": "john.doe@example.com",
                "username": "johndoe",
                "password": "SecurePassword123!",
                "confirm_password": "SecurePassword123!",
                "role": "BORROWER"
            }
        },
        "responses": {
            "201": {
                "summary": "Registration Successful",
                "value": {
                    "message": "User registered successfully",
                    "user": {
                        "id": 1,
                        "email": "john.doe@example.com",
                        "username": "johndoe",
                        "role": "BORROWER",
                        "is_active": True,
                        "is_verified": False,
                        "created_at": "2025-01-15T10:30:00Z"
                    },
                    "verification_sent": True
                }
            },
            "409": {
                "summary": "Email Already Exists",
                "value": {
                    "error_code": "EMAIL_ALREADY_EXISTS",
                    "detail": "User with this email already exists",
                    "status_code": 409
                }
            }
        }
    },
    "login": {
        "request": {
            "summary": "User Login",
            "description": "Authenticate user and receive access tokens",
            "value": {
                "email": "john.doe@example.com",
                "password": "SecurePassword123!"
            }
        },
        "responses": {
            "200": {
                "summary": "Login Successful",
                "value": {
                    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    "refresh_token": "def50200b5c5e8f4a8c3d2e1f0a9b8c7...",
                    "token_type": "bearer",
                    "expires_in": 1800,
                    "user": {
                        "id": 1,
                        "email": "john.doe@example.com",
                        "username": "johndoe",
                        "role": "BORROWER"
                    }
                }
            },
            "401": {
                "summary": "Invalid Credentials",
                "value": {
                    "error_code": "INVALID_CREDENTIALS",
                    "detail": "Invalid email or password",
                    "status_code": 401
                }
            }
        }
    }
}

# Profile Examples
PROFILE_EXAMPLES = {
    "get_profile": {
        "responses": {
            "200": {
                "summary": "User Profile",
                "value": {
                    "id": 1,
                    "user_id": 1,
                    "first_name": "John",
                    "last_name": "Doe",
                    "display_name": "John D.",
                    "bio": "Experienced software developer looking for business expansion loan",
                    "country": "United States",
                    "city": "New York",
                    "income_range": "$75,000 - $100,000",
                    "employment_status": "FULL_TIME",
                    "credit_score": 750,
                    "requested_loan_amount": 25000.00,
                    "loan_purpose": "Business expansion",
                    "max_acceptable_rate": 8.5,
                    "profile_completion_percentage": 85.0,
                    "identity_verified": True,
                    "avatar_url": "/uploads/profiles/avatars/user_1_avatar.jpg",
                    "created_at": "2025-01-15T10:30:00Z"
                }
            }
        }
    },
    "update_profile": {
        "request": {
            "summary": "Update Profile Information",
            "description": "Update user profile with new information",
            "value": {
                "first_name": "John",
                "last_name": "Doe",
                "display_name": "John D.",
                "bio": "Updated bio - Experienced developer seeking growth capital",
                "phone_number": "+1-555-123-4567",
                "country": "United States",
                "state_province": "New York",
                "city": "New York",
                "postal_code": "10001",
                "income_range": "$75,000 - $100,000",
                "employment_status": "FULL_TIME",
                "employer_name": "Tech Solutions Inc",
                "monthly_income": 8500.00,
                "requested_loan_amount": 30000.00,
                "loan_purpose": "Business expansion and equipment purchase",
                "max_acceptable_rate": 8.0
            }
        }
    }
}

# Search and Filtering Examples
SEARCH_EXAMPLES = {
    "search_profiles": {
        "request": {
            "summary": "Advanced Profile Search",
            "description": "Search profiles with multiple filters",
            "value": {
                "role": "LENDER",
                "min_loan_amount": 10000,
                "max_loan_amount": 50000,
                "max_interest_rate": 10.0,
                "location": "New York",
                "employment_status": ["FULL_TIME", "SELF_EMPLOYED"],
                "min_credit_score": 700,
                "verified_only": True,
                "sort_by": "credit_score",
                "sort_order": "desc",
                "page": 1,
                "limit": 20
            }
        },
        "responses": {
            "200": {
                "summary": "Search Results",
                "value": {
                    "profiles": [
                        {
                            "id": 2,
                            "display_name": "Sarah L.",
                            "role": "LENDER",
                            "min_loan_amount": 5000,
                            "max_loan_amount": 100000,
                            "preferred_interest_rate": 7.5,
                            "city": "New York",
                            "credit_score": 820,
                            "identity_verified": True,
                            "match_score": 95.5
                        }
                    ],
                    "total": 1,
                    "page": 1,
                    "limit": 20,
                    "total_pages": 1
                }
            }
        }
    }
}

# Connection and Matching Examples
MATCHING_EXAMPLES = {
    "get_matches": {
        "responses": {
            "200": {
                "summary": "Matching Results",
                "value": {
                    "matches": [
                        {
                            "profile_id": 2,
                            "display_name": "Sarah L.",
                            "role": "LENDER",
                            "match_score": 95.5,
                            "compatibility_factors": {
                                "loan_amount_match": 0.95,
                                "interest_rate_match": 0.90,
                                "location_proximity": 1.0,
                                "risk_profile_match": 0.85,
                                "experience_match": 0.92
                            },
                            "recommended_loan_amount": 25000,
                            "recommended_interest_rate": 7.8,
                            "risk_assessment": "LOW"
                        }
                    ],
                    "total_matches": 1,
                    "average_match_score": 95.5
                }
            }
        }
    },
    "create_connection": {
        "request": {
            "summary": "Create Connection Request",
            "description": "Send connection request to another user",
            "value": {
                "target_user_id": 2,
                "message": "Hi Sarah, I'm interested in discussing a potential loan arrangement. Your lending criteria match my needs perfectly.",
                "proposed_loan_amount": 25000,
                "proposed_interest_rate": 7.8,
                "proposed_term_months": 36
            }
        }
    }
}

# File Upload Examples
UPLOAD_EXAMPLES = {
    "upload_avatar": {
        "responses": {
            "200": {
                "summary": "Avatar Upload Successful",
                "value": {
                    "message": "Avatar uploaded successfully",
                    "file_url": "/uploads/profiles/avatars/user_1_avatar.jpg",
                    "file_size": 245760,
                    "dimensions": "400x400"
                }
            }
        }
    }
}

# Security Examples
SECURITY_EXAMPLES = {
    "security_dashboard": {
        "responses": {
            "200": {
                "summary": "Security Dashboard Data",
                "value": {
                    "dashboard": {
                        "time_range_hours": 24,
                        "total_events": 15,
                        "events_by_type": {
                            "suspicious_request": 3,
                            "rate_limit_exceeded": 2,
                            "auth_failure": 10
                        },
                        "events_by_severity": {
                            "low": 5,
                            "medium": 8,
                            "high": 2,
                            "critical": 0
                        },
                        "recent_alerts": [
                            {
                                "event_type": "rate_limit_exceeded",
                                "severity": "medium",
                                "source_ip": "192.168.1.100",
                                "timestamp": "2025-01-15T14:30:00Z"
                            }
                        ]
                    }
                }
            }
        }
    }
}

# WebSocket Examples
WEBSOCKET_EXAMPLES = {
    "notification_format": {
        "summary": "Real-time Notification Format",
        "value": {
            "type": "connection_request",
            "data": {
                "id": "notif_123",
                "user_id": 1,
                "from_user": {
                    "id": 2,
                    "display_name": "Sarah L.",
                    "avatar_url": "/uploads/profiles/avatars/user_2_avatar.jpg"
                },
                "message": "Sarah L. sent you a connection request",
                "timestamp": "2025-01-15T15:45:00Z",
                "read": False,
                "action_url": "/connections/requests"
            }
        }
    }
}

# Error Response Examples
ERROR_EXAMPLES = {
    "validation_error": {
        "summary": "Validation Error",
        "value": {
            "error_code": "VALIDATION_ERROR",
            "detail": "Please check your input data and try again",
            "status_code": 422,
            "field_errors": [
                {
                    "field": "email",
                    "message": "Invalid email format",
                    "code": "invalid_format"
                },
                {
                    "field": "password",
                    "message": "Password must be at least 8 characters long",
                    "code": "min_length"
                }
            ]
        }
    },
    "rate_limit_error": {
        "summary": "Rate Limit Exceeded",
        "value": {
            "error_code": "RATE_LIMITED",
            "detail": "Too many requests. Please slow down.",
            "status_code": 429,
            "retry_after": 60
        }
    },
    "authentication_error": {
        "summary": "Authentication Required",
        "value": {
            "error_code": "AUTHENTICATION_REQUIRED",
            "detail": "Valid authentication token required",
            "status_code": 401
        }
    }
}

# Compile all examples
ALL_EXAMPLES = {
    "auth": AUTH_EXAMPLES,
    "profile": PROFILE_EXAMPLES,
    "search": SEARCH_EXAMPLES,
    "matching": MATCHING_EXAMPLES,
    "upload": UPLOAD_EXAMPLES,
    "security": SECURITY_EXAMPLES,
    "websocket": WEBSOCKET_EXAMPLES,
    "errors": ERROR_EXAMPLES
}