import secrets
from typing import List, Union
from pydantic import AnyHttpUrl, EmailStr, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Cooin API"
    PROJECT_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Environment Configuration
    ENVIRONMENT: str = "development"  # development, staging, production

    # Security Configuration
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    BCRYPT_ROUNDS: int = 12

    # Database Configuration
    DATABASE_URL: str
    DATABASE_HOSTNAME: str
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return self.DATABASE_URL

    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"

    # Email Configuration
    SMTP_TLS: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: str = ""
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    FRONTEND_URL: str = "http://localhost:3000"  # Frontend application URL

    # File Upload Configuration
    MAX_UPLOAD_SIZE: int = 5242880  # 5MB
    UPLOAD_FOLDER: str = "uploads/"
    ALLOWED_IMAGE_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "gif"]
    ALLOWED_DOCUMENT_EXTENSIONS: List[str] = ["pdf", "doc", "docx"]

    # Session Configuration
    SESSION_COOKIE_SECURE: bool = True
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "lax"

    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    # Pagination Configuration
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # Rate Limiting Configuration
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 3600  # 1 hour in seconds

    # Security Middleware Configuration (Environment-aware)
    ENABLE_SECURITY_HEADERS: bool = True
    ENABLE_RATE_LIMITING: bool = True
    ENABLE_DDOS_PROTECTION: bool = True
    ENABLE_REQUEST_VALIDATION: bool = True
    ENABLE_SECURITY_LOGGING: bool = True

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT == "development"

    @property
    def security_enabled(self) -> bool:
        """Security features should be fully enabled in production."""
        return self.is_production or self.ENVIRONMENT == "staging"

    # External API Configuration
    EXTERNAL_API_KEY: str = ""
    EXTERNAL_API_URL: str = ""

    # Mobile & Push Notification Configuration
    APNS_KEY_ID: str = ""  # Apple Push Notification Service Key ID
    APNS_TEAM_ID: str = ""  # Apple Developer Team ID
    APNS_BUNDLE_ID: str = "com.cooin.app"  # iOS App Bundle ID
    APNS_KEY_PATH: str = ""  # Path to .p8 key file (optional)

    # Mobile File Upload Settings
    MOBILE_AVATAR_MAX_SIZE: int = 10485760  # 10MB
    MOBILE_BANNER_MAX_SIZE: int = 15728640  # 15MB
    MOBILE_DOCUMENT_MAX_SIZE: int = 52428800  # 50MB

    # WebSocket Configuration
    WEBSOCKET_HEARTBEAT_INTERVAL: int = 30  # seconds
    WEBSOCKET_MAX_CONNECTIONS_PER_USER: int = 5

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()