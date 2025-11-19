from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator


class Token(BaseModel):
    """JWT token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds until access token expires

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "token_type": "bearer",
                "expires_in": 1800
            }
        }


class TokenRefresh(BaseModel):
    """Token refresh request schema."""
    refresh_token: str

    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
            }
        }


class AccessToken(BaseModel):
    """Access token only response schema."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "token_type": "bearer",
                "expires_in": 1800
            }
        }


class LoginRequest(BaseModel):
    """User login request schema."""
    email: EmailStr
    password: str = Field(..., min_length=1)
    remember_me: bool = False  # For extended refresh token expiry

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123",
                "remember_me": False
            }
        }


class LoginResponse(BaseModel):
    """User login response schema."""
    user: dict  # UserResponse
    tokens: Token
    message: str = "Login successful"

    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "id": 1,
                    "email": "user@example.com",
                    "username": "john_doe",
                    "role": "borrower",
                    "is_active": True,
                    "is_verified": True
                },
                "tokens": {
                    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    "token_type": "bearer",
                    "expires_in": 1800
                },
                "message": "Login successful"
            }
        }


class RegisterRequest(BaseModel):
    """User registration request schema."""
    email: EmailStr = Field(..., description="Valid email address")
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Username (3-50 characters, letters, numbers, underscores, hyphens only)")
    password: str = Field(..., min_length=8, max_length=100, description="Password (min 8 chars, must include uppercase, lowercase, number)")
    confirm_password: str = Field(..., description="Must match password")
    role: str = Field("borrower", description="User role: lender, borrower, or both")
    agree_to_terms: bool = Field(..., description="Must be true - agreement to terms and conditions is required")

    @validator('username')
    def validate_username(cls, v):
        if v is not None:
            if not v.replace('_', '').replace('-', '').isalnum():
                raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        return v

    @validator('password')
    def validate_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')

        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)

        if not (has_upper and has_lower and has_digit):
            raise ValueError('Password must contain at least one uppercase letter, one lowercase letter, and one number')

        return v

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Password confirmation does not match password')
        return v

    @validator('role')
    def validate_role(cls, v):
        valid_roles = ['lender', 'borrower', 'both']
        if v.lower() not in valid_roles:
            raise ValueError(f'Role must be one of: {", ".join(valid_roles)}')
        return v.lower()

    @validator('agree_to_terms')
    def validate_terms_agreement(cls, v):
        if not v:
            raise ValueError('You must agree to the terms and conditions to create an account')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "email": "newuser@example.com",
                "username": "new_user",
                "password": "SecurePass123",
                "confirm_password": "SecurePass123",
                "role": "borrower",
                "agree_to_terms": True
            }
        }


class RegisterResponse(BaseModel):
    """User registration response schema."""
    user: dict  # UserResponse
    message: str = "Registration successful. Please check your email for verification."

    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "id": 1,
                    "email": "newuser@example.com",
                    "username": "new_user",
                    "role": "borrower",
                    "is_active": True,
                    "is_verified": False,
                    "status": "pending_verification"
                },
                "message": "Registration successful. Please check your email for verification."
            }
        }


class LogoutRequest(BaseModel):
    """User logout request schema."""
    refresh_token: Optional[str] = None  # If provided, will revoke this specific token
    logout_all_devices: bool = False  # If true, revoke all refresh tokens for user

    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "logout_all_devices": False
            }
        }


class LogoutResponse(BaseModel):
    """User logout response schema."""
    message: str = "Logout successful"
    revoked_tokens_count: int = 1

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Logout successful",
                "revoked_tokens_count": 1
            }
        }


class TokenData(BaseModel):
    """Token payload data schema (internal use)."""
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None
    token_type: Optional[str] = None


class DeviceInfo(BaseModel):
    """Device information schema for token tracking."""
    device_type: Optional[str] = None  # "mobile", "desktop", "tablet"
    device_name: Optional[str] = None  # "iPhone 12", "Chrome Browser"
    os: Optional[str] = None  # "iOS", "Android", "Windows"
    app_version: Optional[str] = None  # "1.0.0"
    ip_address: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "device_type": "mobile",
                "device_name": "iPhone 12",
                "os": "iOS",
                "app_version": "1.0.0",
                "ip_address": "192.168.1.100"
            }
        }


class ActiveSession(BaseModel):
    """Active session information schema."""
    token_id: int
    device_info: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime
    last_used: Optional[datetime] = None
    expires_at: datetime
    is_current: bool = False  # If this is the current session

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "token_id": 1,
                "device_info": "iPhone 12 - iOS",
                "ip_address": "192.168.1.100",
                "created_at": "2023-10-01T12:00:00Z",
                "last_used": "2023-10-01T15:30:00Z",
                "expires_at": "2023-10-08T12:00:00Z",
                "is_current": True
            }
        }


class SessionsResponse(BaseModel):
    """Active sessions response schema."""
    sessions: list[ActiveSession]
    total_sessions: int

    class Config:
        json_schema_extra = {
            "example": {
                "sessions": [
                    {
                        "token_id": 1,
                        "device_info": "iPhone 12 - iOS",
                        "ip_address": "192.168.1.100",
                        "created_at": "2023-10-01T12:00:00Z",
                        "expires_at": "2023-10-08T12:00:00Z",
                        "is_current": True
                    }
                ],
                "total_sessions": 1
            }
        }