# Import all models for Alembic autodiscovery and easier imports
# Import in order to avoid circular dependencies

# Import search models first (they're referenced by user)
from app.models.search import (
    SavedSearch,
    SearchLog
)

# Import document models
from app.models.document import (
    DocumentUpload,
    DocumentType,
    DocumentStatus
)

# Import user models
from app.models.user import User, UserRole, UserStatus, RefreshToken

# Import profile models
from app.models.profile import (
    UserProfile,
    IncomeRange,
    EmploymentStatus,
    LoanPurpose
)

# Import connection models
from app.models.connection import (
    Connection,
    ConnectionStatus,
    ConnectionType,
    Message
)

# Import rating models
from app.models.rating import (
    Rating,
    RatingType,
    RatingCategory
)

# Import system message models
from app.models.system_message import (
    SystemMessage,
    SystemMessageType,
    SystemMessagePriority
)

# Export all models
__all__ = [
    # User models
    "User",
    "UserRole",
    "UserStatus",
    "RefreshToken",

    # Profile models
    "UserProfile",
    "IncomeRange",
    "EmploymentStatus",
    "LoanPurpose",

    # Connection models
    "Connection",
    "ConnectionStatus",
    "ConnectionType",
    "Message",

    # Rating models
    "Rating",
    "RatingType",
    "RatingCategory",

    # Search models
    "SavedSearch",
    "SearchLog",

    # Document models
    "DocumentUpload",
    "DocumentType",
    "DocumentStatus",

    # System message models
    "SystemMessage",
    "SystemMessageType",
    "SystemMessagePriority",
]