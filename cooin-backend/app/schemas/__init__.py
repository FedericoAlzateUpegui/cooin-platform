# Import all schemas for easier access
from app.schemas.user import (
    UserRoleSchema,
    UserStatusSchema,
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserPublicResponse,
    PasswordChange,
    PasswordReset,
    PasswordResetConfirm,
    EmailVerification,
    UserStats
)

from app.schemas.auth import (
    Token,
    TokenRefresh,
    AccessToken,
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    LogoutRequest,
    LogoutResponse,
    TokenData,
    DeviceInfo,
    ActiveSession,
    SessionsResponse
)

from app.schemas.profile import (
    IncomeRangeSchema,
    EmploymentStatusSchema,
    LoanPurposeSchema,
    UserProfileBase,
    UserProfileCreate,
    UserProfileUpdate,
    FinancialInfoBase,
    FinancialInfoUpdate,
    LendingPreferencesBase,
    LendingPreferencesUpdate,
    BorrowingPreferencesBase,
    BorrowingPreferencesUpdate,
    UserProfileResponse,
    UserProfilePublicResponse,
    ProfileCompletionResponse,
    ProfileStats
)

from app.schemas.ticket import (
    TicketBase,
    TicketCreate,
    TicketUpdate,
    TicketResponse,
    TicketWithUser,
    TicketListResponse,
    TicketFilter,
    CreateDealFromTicket,
    TicketStats
)

# Export all schemas
__all__ = [
    # User schemas
    "UserRoleSchema",
    "UserStatusSchema",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserPublicResponse",
    "PasswordChange",
    "PasswordReset",
    "PasswordResetConfirm",
    "EmailVerification",
    "UserStats",

    # Auth schemas
    "Token",
    "TokenRefresh",
    "AccessToken",
    "LoginRequest",
    "LoginResponse",
    "RegisterRequest",
    "RegisterResponse",
    "LogoutRequest",
    "LogoutResponse",
    "TokenData",
    "DeviceInfo",
    "ActiveSession",
    "SessionsResponse",

    # Profile schemas
    "IncomeRangeSchema",
    "EmploymentStatusSchema",
    "LoanPurposeSchema",
    "UserProfileBase",
    "UserProfileCreate",
    "UserProfileUpdate",
    "FinancialInfoBase",
    "FinancialInfoUpdate",
    "LendingPreferencesBase",
    "LendingPreferencesUpdate",
    "BorrowingPreferencesBase",
    "BorrowingPreferencesUpdate",
    "UserProfileResponse",
    "UserProfilePublicResponse",
    "ProfileCompletionResponse",
    "ProfileStats",

    # Ticket schemas
    "TicketBase",
    "TicketCreate",
    "TicketUpdate",
    "TicketResponse",
    "TicketWithUser",
    "TicketListResponse",
    "TicketFilter",
    "CreateDealFromTicket",
    "TicketStats",
]