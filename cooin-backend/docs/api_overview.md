# Cooin API Documentation

## Overview

The Cooin API is a RESTful web service that powers a peer-to-peer lending platform. It provides comprehensive functionality for user management, loan matching, analytics, and secure financial transactions.

### Base URL

```
Production: https://api.cooin.app
Development: http://localhost:8000
```

### API Version

Current Version: `v1`
All endpoints are prefixed with `/api/v1`

## Core Features

### 🔐 Authentication & Authorization
- JWT-based authentication
- Secure user registration and login
- Role-based access control (borrowers, lenders, admins)
- Session management with refresh tokens

### 👥 User & Profile Management
- Comprehensive user profiles
- Financial information tracking
- Identity verification
- Privacy controls

### 🤝 Intelligent Loan Matching
- AI-powered borrower-lender matching
- Multi-criteria scoring algorithm
- Geographic proximity matching
- Risk assessment integration

### 📊 Analytics & Reporting
- Real-time dashboard metrics
- Business intelligence reports
- Mobile-optimized analytics
- Data export capabilities

### 🔍 Advanced Search
- Loan request and offer search
- Advanced filtering options
- Personalized recommendations
- Saved search functionality

### 💬 Communication System
- User connections and messaging
- Rating and review system
- Notification management

### 📁 File Management
- Secure document uploads
- Image processing and optimization
- Document verification support

## Quick Start

### 1. Authentication

```bash
# Register a new user
curl -X POST "https://api.cooin.app/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "username",
    "password": "SecurePass123!",
    "confirm_password": "SecurePass123!",
    "role": "borrower",
    "agree_to_terms": true
  }'

# Login
curl -X POST "https://api.cooin.app/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

### 2. Create Profile

```bash
curl -X POST "https://api.cooin.app/api/v1/profiles/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "city": "San Francisco",
    "bio": "Looking for home improvement funding"
  }'
```

### 3. Find Matches

```bash
# For borrowers - find lender matches
curl -X GET "https://api.cooin.app/api/v1/matching/borrower/matches/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# For lenders - find borrower matches
curl -X GET "https://api.cooin.app/api/v1/matching/lender/matches/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Response Format

All API responses follow a consistent format:

### Success Response

```json
{
  "success": true,
  "data": {
    // Response data here
  },
  "message": "Operation completed successfully",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input provided",
    "details": {
      "field": "email",
      "issue": "Invalid email format"
    }
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Register** or **Login** to get access and refresh tokens
2. Include the access token in the `Authorization` header:
   ```
   Authorization: Bearer YOUR_ACCESS_TOKEN
   ```
3. Use the refresh token to get new access tokens when they expire

### Token Expiration
- Access tokens: 30 minutes
- Refresh tokens: 7 days

## Rate Limiting

API requests are rate-limited to ensure fair usage:

- **General endpoints**: 60 requests per minute
- **Authentication endpoints**: 10 requests per minute
- **File upload endpoints**: 5 requests per minute

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1642248600
```

## Error Codes

Common error codes and their meanings:

| Code | Description |
|------|-------------|
| `AUTHENTICATION_ERROR` | Invalid or missing authentication |
| `AUTHORIZATION_ERROR` | Insufficient permissions |
| `VALIDATION_ERROR` | Invalid input data |
| `RESOURCE_NOT_FOUND` | Requested resource doesn't exist |
| `DUPLICATE_RESOURCE` | Resource already exists |
| `RATE_LIMIT_EXCEEDED` | Too many requests |
| `SERVER_ERROR` | Internal server error |

## Data Types

### Common Data Types

- **ID**: Integer primary key
- **UUID**: String in UUID format
- **DateTime**: ISO 8601 formatted string (`2024-01-15T10:30:00Z`)
- **Money**: Decimal number with 2 decimal places
- **Email**: Valid email address string
- **URL**: Valid HTTP/HTTPS URL

### Enums

#### User Roles
- `borrower`: Individual seeking loans
- `lender`: Individual providing loans
- `admin`: Platform administrator

#### Loan Status
- `draft`: Being prepared
- `active`: Available for matching
- `matched`: Connected with counterpart
- `funded`: Loan has been funded
- `completed`: Loan fully repaid
- `cancelled`: Loan cancelled

## Pagination

List endpoints support pagination with the following parameters:

- `limit`: Number of items per page (default: 20, max: 100)
- `offset`: Number of items to skip (default: 0)

Pagination response includes:

```json
{
  "data": [...],
  "pagination": {
    "limit": 20,
    "offset": 0,
    "total_count": 150,
    "has_next": true,
    "has_previous": false
  }
}
```

## Filtering & Sorting

Many endpoints support filtering and sorting:

### Filtering
```
GET /api/v1/search/loan-requests?min_amount=10000&max_rate=8.0&purpose=home_improvement
```

### Sorting
```
GET /api/v1/profiles?sort=created_at&order=desc
```

## Webhooks

The API supports webhooks for real-time notifications:

- **User Events**: Registration, profile updates
- **Matching Events**: New matches, match actions
- **Transaction Events**: Funding, payments
- **System Events**: Maintenance, security alerts

Webhook payloads follow the standard response format with an additional `event_type` field.

## SDKs & Libraries

Official SDKs are available for:
- **JavaScript/TypeScript**: `npm install @cooin/api-client`
- **Python**: `pip install cooin-api`
- **React Native**: Included in JavaScript SDK

## Support & Resources

- **API Documentation**: [https://docs.cooin.app](https://docs.cooin.app)
- **Interactive API Explorer**: [https://api.cooin.app/api/v1/docs](https://api.cooin.app/api/v1/docs)
- **Status Page**: [https://status.cooin.app](https://status.cooin.app)
- **Developer Support**: [developers@cooin.app](mailto:developers@cooin.app)

## OpenAPI Specification

The complete OpenAPI 3.0 specification is available at:
- **JSON**: [https://api.cooin.app/api/v1/openapi.json](https://api.cooin.app/api/v1/openapi.json)
- **YAML**: [https://api.cooin.app/api/v1/openapi.yaml](https://api.cooin.app/api/v1/openapi.yaml)

---

*Last updated: January 2024*
*API Version: 1.0.0*