"""
Custom exception classes and error handlers for the Cooin API.
Provides structured error responses with proper HTTP status codes and user-friendly messages.
"""

from typing import Any, Dict, Optional, List
from fastapi import HTTPException, status


class CooinException(HTTPException):
    """Base exception for Cooin-specific errors."""

    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: Optional[str] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.extra_data = extra_data or {}


class ValidationError(CooinException):
    """Custom validation error with detailed field information."""

    def __init__(
        self,
        detail: str = "Validation failed",
        field_errors: Optional[List[Dict[str, Any]]] = None,
        error_code: str = "VALIDATION_ERROR"
    ):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code=error_code,
            extra_data={"field_errors": field_errors or []}
        )


class AuthenticationError(CooinException):
    """Authentication-related errors."""

    def __init__(
        self,
        detail: str = "Authentication failed",
        error_code: str = "AUTH_ERROR"
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code=error_code
        )


class AuthorizationError(CooinException):
    """Authorization-related errors."""

    def __init__(
        self,
        detail: str = "Insufficient permissions",
        error_code: str = "AUTHORIZATION_ERROR"
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code=error_code
        )


class NotFoundError(CooinException):
    """Resource not found errors."""

    def __init__(
        self,
        detail: str = "Resource not found",
        error_code: str = "NOT_FOUND",
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None
    ):
        extra_data = {}
        if resource_type:
            extra_data["resource_type"] = resource_type
        if resource_id:
            extra_data["resource_id"] = resource_id

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code=error_code,
            extra_data=extra_data
        )


class ConflictError(CooinException):
    """Resource conflict errors (e.g., duplicate email)."""

    def __init__(
        self,
        detail: str = "Resource conflict",
        error_code: str = "CONFLICT_ERROR",
        conflicting_field: Optional[str] = None,
        conflicting_value: Optional[str] = None
    ):
        extra_data = {}
        if conflicting_field:
            extra_data["conflicting_field"] = conflicting_field
        if conflicting_value:
            extra_data["conflicting_value"] = conflicting_value

        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code=error_code,
            extra_data=extra_data
        )


class RateLimitError(CooinException):
    """Rate limit exceeded errors."""

    def __init__(
        self,
        detail: str = "Rate limit exceeded",
        error_code: str = "RATE_LIMIT_EXCEEDED",
        retry_after: Optional[int] = None
    ):
        extra_data = {}
        if retry_after:
            extra_data["retry_after_seconds"] = retry_after

        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            error_code=error_code,
            extra_data=extra_data
        )


class BusinessLogicError(CooinException):
    """Business logic validation errors."""

    def __init__(
        self,
        detail: str = "Business rule violation",
        error_code: str = "BUSINESS_LOGIC_ERROR"
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code=error_code
        )


class DatabaseError(CooinException):
    """Database operation errors."""

    def __init__(
        self,
        detail: str = "Database operation failed",
        error_code: str = "DATABASE_ERROR",
        operation: Optional[str] = None
    ):
        extra_data = {}
        if operation:
            extra_data["failed_operation"] = operation

        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code=error_code,
            extra_data=extra_data
        )


# Common error messages
class ErrorMessages:
    """Centralized error messages."""

    # Authentication
    INVALID_CREDENTIALS = "Invalid email or password"
    ACCOUNT_LOCKED = "Account is temporarily locked due to too many failed login attempts"
    ACCOUNT_INACTIVE = "Account is inactive. Please contact support"
    ACCOUNT_NOT_VERIFIED = "Account not verified. Please check your email for verification instructions"
    TOKEN_EXPIRED = "Access token has expired"
    TOKEN_INVALID = "Invalid or malformed token"
    REFRESH_TOKEN_EXPIRED = "Refresh token has expired. Please log in again"
    REFRESH_TOKEN_INVALID = "Invalid refresh token"

    # Registration
    EMAIL_ALREADY_EXISTS = "An account with this email already exists"
    USERNAME_ALREADY_EXISTS = "This username is already taken"
    PASSWORDS_DONT_MATCH = "Password and confirmation password do not match"
    WEAK_PASSWORD = "Password must contain at least 8 characters with uppercase, lowercase, and numbers"
    TERMS_NOT_AGREED = "You must agree to the terms and conditions"

    # Validation
    INVALID_EMAIL_FORMAT = "Please enter a valid email address"
    USERNAME_TOO_SHORT = "Username must be at least 3 characters long"
    USERNAME_TOO_LONG = "Username must be less than 50 characters"
    USERNAME_INVALID_CHARS = "Username can only contain letters, numbers, underscores, and hyphens"
    INVALID_ROLE = "Invalid user role specified"

    # General
    RESOURCE_NOT_FOUND = "The requested resource was not found"
    INSUFFICIENT_PERMISSIONS = "You don't have permission to perform this action"
    INTERNAL_SERVER_ERROR = "An internal server error occurred. Please try again later"
    RATE_LIMIT_EXCEEDED = "Too many requests. Please slow down and try again later"

    # Profile
    PROFILE_NOT_FOUND = "User profile not found"
    PROFILE_INCOMPLETE = "Please complete your profile before proceeding"

    # Connections
    CONNECTION_NOT_FOUND = "Connection not found"
    CONNECTION_ALREADY_EXISTS = "Connection already exists between these users"
    CANNOT_CONNECT_TO_SELF = "You cannot connect to yourself"
    CONNECTION_LIMIT_REACHED = "You have reached the maximum number of connections"

    # Ratings
    RATING_NOT_FOUND = "Rating not found"
    CANNOT_RATE_SELF = "You cannot rate yourself"
    RATING_ALREADY_EXISTS = "You have already rated this user"

    # Tickets
    TICKET_NOT_FOUND = "Ticket not found"
    TICKET_INACTIVE = "This ticket is no longer active"
    TICKET_EXPIRED = "This ticket has expired"
    CANNOT_CREATE_DEAL_WITH_OWN_TICKET = "You cannot create a deal with your own ticket"
    DEAL_ALREADY_EXISTS = "A deal already exists for this ticket between you and this user"

    # Ticket Role Restrictions
    ONLY_LENDERS_CREATE_LENDING_OFFERS = "Only lenders can create lending offers. Your account role is set to 'Borrower'. To create lending offers, please update your account role to 'Lender' or 'Both' in your profile settings."
    ONLY_BORROWERS_CREATE_BORROWING_REQUESTS = "Only borrowers can create borrowing requests. Your account role is set to 'Lender'. To create borrowing requests, please update your account role to 'Borrower' or 'Both' in your profile settings."
    ONLY_BORROWERS_RESPOND_TO_LENDING_OFFERS = "Only borrowers can respond to lending offers. Your account role is set to 'Lender'. To respond to lending offers, please update your account role to 'Borrower' or 'Both' in your profile settings."
    ONLY_LENDERS_RESPOND_TO_BORROWING_REQUESTS = "Only lenders can respond to borrowing requests. Your account role is set to 'Borrower'. To respond to borrowing requests, please update your account role to 'Lender' or 'Both' in your profile settings."


def create_error_response(
    error_code: str,
    detail: str,
    status_code: int = 400,
    field_errors: Optional[List[Dict[str, Any]]] = None,
    extra_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create a standardized error response."""

    response = {
        "error": {
            "code": error_code,
            "message": detail,
            "status_code": status_code
        }
    }

    if field_errors:
        response["error"]["field_errors"] = field_errors

    if extra_data:
        response["error"].update(extra_data)

    return response


def format_validation_errors(errors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Format pydantic validation errors into user-friendly format."""

    formatted_errors = []

    for error in errors:
        field_path = " -> ".join(str(loc) for loc in error["loc"])

        formatted_error = {
            "field": field_path,
            "message": error["msg"],
            "type": error["type"],
            "input": error.get("input")
        }

        # Create more user-friendly messages for common validation errors
        error_type = error["type"]
        field_name = error["loc"][-1] if error["loc"] else "field"

        if error_type == "value_error.email":
            formatted_error["message"] = ErrorMessages.INVALID_EMAIL_FORMAT
        elif error_type == "value_error.missing":
            formatted_error["message"] = f"{field_name.title()} is required"
        elif error_type == "value_error.any_str.min_length":
            min_length = error.get("ctx", {}).get("limit_value", "required")
            formatted_error["message"] = f"{field_name.title()} must be at least {min_length} characters"
        elif error_type == "value_error.any_str.max_length":
            max_length = error.get("ctx", {}).get("limit_value", "allowed")
            formatted_error["message"] = f"{field_name.title()} must be no more than {max_length} characters"

        formatted_errors.append(formatted_error)

    return formatted_errors