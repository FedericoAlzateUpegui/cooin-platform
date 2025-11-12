# Authentication Endpoints

The authentication system handles user registration, login, token management, and session control.

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register a new user |
| POST | `/api/v1/auth/login` | Authenticate user |
| POST | `/api/v1/auth/logout` | Logout user |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| GET | `/api/v1/auth/me` | Get current user info |
| GET | `/api/v1/auth/sessions` | Get user sessions |

## Register User

Register a new user account.

### Request

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123!",
  "confirm_password": "SecurePass123!",
  "role": "borrower",
  "agree_to_terms": true
}
```

### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | Yes | Valid email address |
| `username` | string | Yes | Unique username (3-50 chars) |
| `password` | string | Yes | Strong password (min 8 chars) |
| `confirm_password` | string | Yes | Must match password |
| `role` | string | Yes | User role (`borrower` or `lender`) |
| `agree_to_terms` | boolean | Yes | Must be `true` |

### Response

```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "username": "johndoe",
      "role": "borrower",
      "is_active": true,
      "is_verified": false,
      "created_at": "2024-01-15T10:30:00Z"
    }
  },
  "message": "User registered successfully"
}
```

### Error Responses

**400 Bad Request**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email already exists",
    "details": {
      "field": "email",
      "issue": "This email is already registered"
    }
  }
}
```

## Login

Authenticate a user and receive access/refresh tokens.

### Request

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "remember_me": false
}
```

### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | Yes | User's email address |
| `password` | string | Yes | User's password |
| `remember_me` | boolean | No | Extend token expiration |

### Response

```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "username": "johndoe",
      "role": "borrower"
    },
    "tokens": {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer",
      "expires_in": 1800
    }
  },
  "message": "Login successful"
}
```

### Error Responses

**401 Unauthorized**
```json
{
  "success": false,
  "error": {
    "code": "AUTHENTICATION_ERROR",
    "message": "Invalid credentials"
  }
}
```

## Get Current User

Get information about the currently authenticated user.

### Request

```http
GET /api/v1/auth/me
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Response

```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "username": "johndoe",
      "role": "borrower",
      "is_active": true,
      "is_verified": false,
      "profile_completion": 75,
      "last_login": "2024-01-15T10:30:00Z",
      "created_at": "2024-01-15T09:00:00Z"
    }
  }
}
```

## Refresh Token

Get a new access token using a refresh token.

### Request

```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Response

```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 1800
  }
}
```

## Logout

Invalidate user session and tokens.

### Request

```http
POST /api/v1/auth/logout
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "logout_all_devices": false
}
```

### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `refresh_token` | string | Yes | User's refresh token |
| `logout_all_devices` | boolean | No | Logout from all devices |

### Response

```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

## Get Sessions

Get list of active user sessions.

### Request

```http
GET /api/v1/auth/sessions
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Response

```json
{
  "success": true,
  "data": {
    "sessions": [
      {
        "id": "session_123",
        "device": "Chrome on Windows",
        "ip_address": "192.168.1.100",
        "location": "San Francisco, CA",
        "created_at": "2024-01-15T10:30:00Z",
        "last_activity": "2024-01-15T11:45:00Z",
        "is_current": true
      }
    ]
  }
}
```

## Password Requirements

Passwords must meet the following criteria:
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

## Security Features

### Rate Limiting
Authentication endpoints have stricter rate limits:
- Register: 5 attempts per IP per hour
- Login: 10 attempts per IP per minute
- General auth endpoints: 30 requests per minute

### Account Security
- Failed login attempts are logged
- Account lockout after 5 failed attempts
- Email verification required for new accounts
- Optional two-factor authentication

### Token Security
- Access tokens expire in 30 minutes
- Refresh tokens expire in 7 days
- Tokens are invalidated on logout
- JWTSecure signing with strong secret keys

## Code Examples

### JavaScript/Fetch

```javascript
// Register
const registerUser = async (userData) => {
  const response = await fetch('/api/v1/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return await response.json();
};

// Login and store tokens
const loginUser = async (email, password) => {
  const response = await fetch('/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json();

  if (data.success) {
    localStorage.setItem('access_token', data.data.tokens.access_token);
    localStorage.setItem('refresh_token', data.data.tokens.refresh_token);
  }

  return data;
};

// Make authenticated requests
const getCurrentUser = async () => {
  const token = localStorage.getItem('access_token');

  const response = await fetch('/api/v1/auth/me', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  return await response.json();
};
```

### Python/Requests

```python
import requests

class CooinAuthClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.access_token = None
        self.refresh_token = None

    def register(self, user_data):
        response = requests.post(
            f"{self.base_url}/api/v1/auth/register",
            json=user_data
        )
        return response.json()

    def login(self, email, password):
        response = requests.post(
            f"{self.base_url}/api/v1/auth/login",
            json={"email": email, "password": password}
        )

        data = response.json()
        if data.get("success"):
            self.access_token = data["data"]["tokens"]["access_token"]
            self.refresh_token = data["data"]["tokens"]["refresh_token"]

        return data

    def get_current_user(self):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(
            f"{self.base_url}/api/v1/auth/me",
            headers=headers
        )
        return response.json()

# Usage
client = CooinAuthClient()
result = client.login("user@example.com", "password")
user_info = client.get_current_user()
```

## Testing

Use these test credentials in development:

```json
{
  "email": "test.borrower@example.com",
  "password": "TestPass123!",
  "role": "borrower"
}
```

```json
{
  "email": "test.lender@example.com",
  "password": "TestPass123!",
  "role": "lender"
}
```