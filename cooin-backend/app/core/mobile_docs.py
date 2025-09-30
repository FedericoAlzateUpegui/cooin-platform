"""
Mobile-optimized API documentation configuration.
Provides comprehensive documentation for iOS app development.
"""

from typing import Dict, Any

# Enhanced OpenAPI tags for mobile development
MOBILE_API_TAGS = [
    {
        "name": "Authentication",
        "description": "User authentication and session management for mobile apps. "
                      "Includes login, registration, token refresh, and secure logout.",
        "externalDocs": {
            "description": "Mobile Auth Best Practices",
            "url": "https://docs.cooin.com/mobile/auth"
        }
    },
    {
        "name": "User Profile",
        "description": "User profile management with mobile-optimized responses. "
                      "Handles profile creation, updates, and image uploads.",
        "externalDocs": {
            "description": "Profile Management Guide",
            "url": "https://docs.cooin.com/mobile/profiles"
        }
    },
    {
        "name": "File Upload",
        "description": "Mobile-optimized file upload for avatars and documents. "
                      "Supports image compression and multiple formats.",
        "externalDocs": {
            "description": "Mobile Upload Guide",
            "url": "https://docs.cooin.com/mobile/uploads"
        }
    },
    {
        "name": "Connections",
        "description": "User connection and matching system. "
                      "Create connections between borrowers and lenders.",
        "externalDocs": {
            "description": "Connection System",
            "url": "https://docs.cooin.com/mobile/connections"
        }
    },
    {
        "name": "Notifications",
        "description": "Real-time notifications and push notification management. "
                      "WebSocket support for live updates.",
        "externalDocs": {
            "description": "Notification System",
            "url": "https://docs.cooin.com/mobile/notifications"
        }
    },
    {
        "name": "Search & Matching",
        "description": "Advanced search and intelligent matching algorithms. "
                      "Find compatible borrowers and lenders.",
        "externalDocs": {
            "description": "Matching Algorithm",
            "url": "https://docs.cooin.com/mobile/matching"
        }
    }
]

# Mobile-specific OpenAPI configuration
MOBILE_OPENAPI_CONFIG = {
    "title": "Cooin Mobile API",
    "version": "1.0.0",
    "description": """
# Cooin Mobile API

A comprehensive API for the Cooin mobile application, providing secure financial connection services.

## Key Features
- 🔐 **Secure Authentication** - JWT-based auth with refresh tokens
- 👤 **Profile Management** - Complete user profile system
- 🔄 **Real-time Updates** - WebSocket notifications
- 📱 **Mobile Optimized** - Designed for iOS/Android apps
- 🛡️ **Enterprise Security** - Multi-layer protection
- 📊 **Smart Matching** - AI-powered borrower/lender matching

## Getting Started

### Authentication Flow
1. Register a new account or login with existing credentials
2. Receive access and refresh tokens
3. Include access token in Authorization header: `Bearer <token>`
4. Refresh tokens before expiry using the refresh endpoint

### Mobile App Integration
- All responses are optimized for mobile consumption
- Image uploads support automatic compression
- WebSocket endpoint available for real-time features
- Push notification tokens can be registered

### Rate Limits
- Authentication endpoints: 5 requests/minute
- General API: 100 requests/minute
- File uploads: 10 requests/minute

### Error Handling
All errors follow a consistent format with error codes for easy mobile handling:
```json
{
    "error_code": "VALIDATION_ERROR",
    "detail": "Descriptive error message",
    "status_code": 422,
    "field_errors": [...]  // For validation errors
}
```
    """,
    "contact": {
        "name": "Cooin API Support",
        "url": "https://cooin.com/support",
        "email": "api-support@cooin.com"
    },
    "license": {
        "name": "Proprietary",
        "url": "https://cooin.com/license"
    },
    "servers": [
        {
            "url": "https://api.cooin.com/api/v1",
            "description": "Production server"
        },
        {
            "url": "https://staging-api.cooin.com/api/v1",
            "description": "Staging server"
        },
        {
            "url": "http://localhost:8000/api/v1",
            "description": "Development server"
        }
    ]
}

# Security schemes for mobile apps
MOBILE_SECURITY_SCHEMES = {
    "BearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "JWT access token obtained from login endpoint"
    },
    "RefreshAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "JWT refresh token for obtaining new access tokens"
    }
}

# Common response schemas for mobile
MOBILE_RESPONSE_SCHEMAS = {
    "MobileSuccessResponse": {
        "type": "object",
        "properties": {
            "success": {"type": "boolean", "example": True},
            "message": {"type": "string", "example": "Operation completed successfully"},
            "data": {"type": "object", "description": "Response data"},
            "meta": {
                "type": "object",
                "description": "Metadata for mobile apps",
                "properties": {
                    "timestamp": {"type": "string", "format": "date-time"},
                    "request_id": {"type": "string"},
                    "app_version_required": {"type": "string", "example": "1.0.0"}
                }
            }
        }
    },
    "MobileErrorResponse": {
        "type": "object",
        "properties": {
            "success": {"type": "boolean", "example": False},
            "error_code": {"type": "string", "example": "VALIDATION_ERROR"},
            "detail": {"type": "string", "example": "Invalid input data"},
            "status_code": {"type": "integer", "example": 422},
            "field_errors": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "field": {"type": "string"},
                        "message": {"type": "string"},
                        "code": {"type": "string"}
                    }
                }
            },
            "meta": {
                "type": "object",
                "properties": {
                    "timestamp": {"type": "string", "format": "date-time"},
                    "request_id": {"type": "string"}
                }
            }
        }
    }
}

# iOS-specific headers and parameters
IOS_HEADERS = {
    "X-App-Version": {
        "description": "iOS app version for compatibility checking",
        "schema": {"type": "string", "example": "1.0.0"},
        "required": False
    },
    "X-Device-ID": {
        "description": "Unique device identifier for push notifications",
        "schema": {"type": "string"},
        "required": False
    },
    "X-iOS-Version": {
        "description": "iOS system version",
        "schema": {"type": "string", "example": "17.0"},
        "required": False
    },
    "X-Device-Model": {
        "description": "iOS device model",
        "schema": {"type": "string", "example": "iPhone15,2"},
        "required": False
    }
}