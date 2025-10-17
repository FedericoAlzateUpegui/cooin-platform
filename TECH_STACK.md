# Cooin Platform - Technology Stack Documentation

## Overview
This document provides a comprehensive overview of all technologies used in the Cooin platform (iOS and Web applications), including their purpose, implementation details, and how they work together.

---

## Frontend Technologies

### 1. **React Native**
- **What it is**: Cross-platform mobile framework for building native iOS and Android apps using JavaScript/TypeScript
- **Why we use it**: Write once, run on multiple platforms (iOS, Android, Web)
- **How we use it**:
  - Core framework for all UI components
  - Used in all screens: Login, Register, Matching, Connections, Messages, Profile
  - Example from `MatchingScreen.tsx`:
    ```typescript
    import { View, Text, StyleSheet, FlatList, TouchableOpacity } from 'react-native';

    export const MatchingScreen: React.FC<MatchingScreenProps> = ({ navigation }) => {
      return (
        <SafeAreaView style={styles.container}>
          <FlatList data={matches} renderItem={renderMatch} />
        </SafeAreaView>
      );
    };
    ```

### 2. **Expo**
- **What it is**: Development platform and framework built on top of React Native
- **Why we use it**: Simplifies development, provides managed workflow, and enables web deployment
- **How we use it**:
  - Runs our development server on `http://localhost:8081`
  - Provides access to native APIs through expo-localization
  - Handles build and deployment processes
  - Example: `expo-localization` for device locale detection

### 3. **TypeScript**
- **What it is**: Typed superset of JavaScript that compiles to plain JavaScript
- **Why we use it**: Type safety, better IDE support, catches errors at compile-time
- **How we use it**:
  - All React components use TypeScript interfaces
  - Type-safe API calls and data models
  - Example from `MatchingScreen.tsx`:
    ```typescript
    interface MatchingScreenProps {
      navigation: any;
    }

    interface MatchingResult {
      user_id: number;
      public_name: string;
      score: number;
      // ... more fields
    }

    const [matches, setMatches] = useState<MatchingResult[]>([]);
    ```

### 4. **i18next & react-i18next**
- **What it is**: Internationalization (i18n) framework for JavaScript applications
- **Why we use it**: Multi-language support (English and Spanish) throughout the app
- **How we use it**:
  - Translation files stored in `src/i18n/locales/en.json` and `es.json`
  - 202+ translation keys covering all screens
  - Example from `MatchingScreen.tsx`:
    ```typescript
    import { useLanguage } from '../../contexts/LanguageContext';

    const { t } = useLanguage();

    // In JSX:
    <Text style={styles.title}>{t('matching_screen.title')}</Text>

    // With parameters:
    t('matching_screen.connection_sent_message', { name: match.public_name })
    ```
  - Translation file structure:
    ```json
    {
      "matching_screen": {
        "title": "Discover Matches",
        "search_filters": "Search Filters",
        "connection_sent_message": "Your connection request has been sent to {name}."
      }
    }
    ```

### 5. **expo-localization**
- **What it is**: Expo module for detecting device locale and preferences
- **Why we use it**: Automatically detect user's preferred language on app startup
- **How we use it**:
  - Detects device locale (e.g., 'en-US', 'es-ES')
  - Sets initial language based on device settings
  - Falls back to English if locale not supported

### 6. **React Hook Form**
- **What it is**: Form state management library using React hooks
- **Why we use it**: Efficient form handling with less re-renders and better performance
- **How we use it**:
  - All forms (Login, Register, Profile Setup) use this library
  - Integrated with Zod for validation
  - Example from `RegisterScreen.tsx`:
    ```typescript
    import { useForm, Controller } from 'react-hook-form';

    const { control, handleSubmit, formState: { errors } } = useForm<RegisterFormData>({
      resolver: zodResolver(registerSchema),
      defaultValues: {
        email: '',
        password: '',
        confirmPassword: '',
      },
    });

    <Controller
      control={control}
      name="email"
      render={({ field: { onChange, onBlur, value } }) => (
        <Input
          value={value}
          onChangeText={onChange}
          onBlur={onBlur}
          error={errors.email?.message}
        />
      )}
    />
    ```

### 7. **Zod**
- **What it is**: TypeScript-first schema validation library
- **Why we use it**: Type-safe validation schemas with excellent TypeScript integration
- **How we use it**:
  - Define validation schemas for all forms
  - Integrated with React Hook Form via `zodResolver`
  - Example from `RegisterScreen.tsx`:
    ```typescript
    import { z } from 'zod';
    import { zodResolver } from '@hookform/resolvers/zod';

    const getRegisterSchema = (t: (key: string) => string) => z.object({
      email: z.string().email(t('validation.invalid_email')),
      password: z.string().min(8, t('validation.password_too_short')),
      confirmPassword: z.string(),
    }).refine((data) => data.password === data.confirmPassword, {
      message: t('validation.passwords_must_match'),
      path: ["confirmPassword"],
    });

    type RegisterFormData = z.infer<typeof registerSchema>;
    ```

### 8. **React Navigation**
- **What it is**: Routing and navigation library for React Native apps
- **Why we use it**: Handle screen transitions and navigation stack management
- **How we use it**:
  - Navigate between screens (Login → Register → Dashboard)
  - Pass parameters between screens
  - Example from `MatchingScreen.tsx`:
    ```typescript
    const handleViewProfile = (match: MatchingResult) => {
      navigation.navigate('PublicProfile', { userId: match.user_id });
    };
    ```

### 9. **Axios**
- **What it is**: Promise-based HTTP client for JavaScript
- **Why we use it**: Make API requests to the backend with interceptors support
- **How we use it**:
  - Centralized API client in `src/services/api.ts`
  - Request/response interceptors for JWT token handling
  - Automatic token refresh
  - Example from `api.ts`:
    ```typescript
    import axios, { AxiosInstance } from 'axios';
    import { API_CONFIG } from '../constants/config';

    class ApiClient {
      private client: AxiosInstance;

      constructor() {
        this.client = axios.create({
          baseURL: API_CONFIG.BASE_URL, // http://127.0.0.1:8000/api/v1
          timeout: API_CONFIG.TIMEOUT,
          headers: {
            'Content-Type': 'application/json',
          },
        });
        this.setupInterceptors();
      }

      private setupInterceptors() {
        // Add JWT token to all requests
        this.client.interceptors.request.use((config) => {
          const token = getStoredToken();
          if (token) {
            config.headers.Authorization = `Bearer ${token}`;
          }
          return config;
        });

        // Handle 401 responses and refresh tokens
        this.client.interceptors.response.use(
          (response) => response,
          async (error) => {
            if (error.response?.status === 401) {
              // Attempt token refresh
            }
            return Promise.reject(error);
          }
        );
      }
    }
    ```

### 10. **@react-native-async-storage/async-storage**
- **What it is**: Persistent key-value storage for React Native
- **Why we use it**: Store user preferences (language), JWT tokens, and other data
- **How we use it**:
  - Store authentication tokens
  - Persist language preference between app sessions
  - Example usage:
    ```typescript
    import AsyncStorage from '@react-native-async-storage/async-storage';

    // Save language preference
    await AsyncStorage.setItem('user-language', 'es');

    // Load language preference
    const savedLanguage = await AsyncStorage.getItem('user-language');
    ```

### 11. **Ionicons** (from @expo/vector-icons)
- **What it is**: Icon library with thousands of pre-built icons
- **Why we use it**: Consistent, beautiful icons throughout the UI
- **How we use it**:
  - Icons for inputs (mail, lock, location)
  - Navigation icons
  - Status indicators
  - Example from `MatchingScreen.tsx`:
    ```typescript
    import { Ionicons } from '@expo/vector-icons';

    <Ionicons
      name={showFilters ? 'close' : 'filter'}
      size={24}
      color={COLORS.primary}
    />
    ```

### 12. **Zustand** (implied from useAuthStore)
- **What it is**: Small, fast state management library
- **Why we use it**: Simple global state management without Redux complexity
- **How we use it**:
  - Authentication state (user, tokens, login/logout)
  - Shared across all screens
  - Example from `MatchingScreen.tsx`:
    ```typescript
    import { useAuthStore } from '../../store/authStore';

    const { user } = useAuthStore();
    const userRole = user?.role; // 'lender' or 'borrower'
    ```

---

## Backend Technologies

### 1. **FastAPI**
- **What it is**: Modern, fast Python web framework for building APIs
- **Why we use it**: Automatic API documentation, type checking, async support, and performance
- **How we use it**:
  - RESTful API endpoints for all operations
  - Automatic request validation using Pydantic
  - Interactive API documentation at `/api/v1/docs`
  - Example from `main.py`:
    ```python
    from fastapi import FastAPI

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description="Cooin - A matching/connection platform with financial elements",
        openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.DEBUG else None,
        docs_url=f"{settings.API_V1_STR}/docs" if settings.DEBUG else None,
    )

    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "version": settings.PROJECT_VERSION
        }
    ```

### 2. **Uvicorn**
- **What it is**: Lightning-fast ASGI server for Python
- **Why we use it**: Async/await support, high performance, WebSocket support
- **How we use it**:
  - Runs the FastAPI application on port 8000
  - Hot reload during development
  - Example from `main.py`:
    ```python
    if __name__ == "__main__":
        import uvicorn
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=settings.DEBUG,
            log_level=settings.LOG_LEVEL.lower()
        )
    ```

### 3. **PostgreSQL**
- **What it is**: Powerful open-source relational database
- **Why we use it**: ACID compliance, complex queries, enum types, JSON support
- **How we use it**:
  - Store all application data (users, connections, loans)
  - Custom enum types for status fields
  - Connection string from `.env`:
    ```
    DATABASE_URL=postgresql://mariajimenez@localhost:5432/cooin_db
    ```

### 4. **SQLAlchemy**
- **What it is**: Python SQL toolkit and Object-Relational Mapping (ORM) library
- **Why we use it**: Database-agnostic code, relationship management, query building
- **How we use it**:
  - Define database models as Python classes
  - Automatic SQL generation
  - Example from `connection.py`:
    ```python
    from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
    from sqlalchemy.orm import relationship
    import enum

    class ConnectionStatus(enum.Enum):
        PENDING = "pending"
        ACCEPTED = "accepted"
        REJECTED = "rejected"
        BLOCKED = "blocked"
        EXPIRED = "expired"

    class Connection(Base):
        __tablename__ = "connections"

        id = Column(Integer, primary_key=True, index=True)
        sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
        receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
        status = Column(Enum(ConnectionStatus), default=ConnectionStatus.PENDING)
        created_at = Column(DateTime, default=datetime.utcnow)

        # Relationships
        sender = relationship("User", foreign_keys=[sender_id])
        receiver = relationship("User", foreign_keys=[receiver_id])
    ```

### 5. **Pydantic**
- **What it is**: Data validation library using Python type annotations
- **Why we use it**: Automatic request/response validation, settings management, type safety
- **How we use it**:
  - Validate incoming API requests
  - Serialize database models to JSON responses
  - Load configuration from `.env` file
  - Example request validation:
    ```python
    from pydantic import BaseModel, EmailStr, validator

    class UserRegister(BaseModel):
        email: EmailStr
        password: str
        role: UserRole

        @validator('password')
        def validate_password(cls, v):
            if len(v) < 8:
                raise ValueError('Password must be at least 8 characters')
            return v
    ```
  - Example settings management:
    ```python
    from pydantic_settings import BaseSettings

    class Settings(BaseSettings):
        DATABASE_URL: str
        SECRET_KEY: str
        BACKEND_CORS_ORIGINS: list[AnyHttpUrl]

        class Config:
            env_file = ".env"

    settings = Settings()
    ```

### 6. **JWT (JSON Web Tokens)**
- **What it is**: Compact, URL-safe token format for authentication
- **Why we use it**: Stateless authentication, secure, industry-standard
- **How we use it**:
  - Generate access tokens (30 min expiry) and refresh tokens (7 day expiry)
  - Verify tokens on protected endpoints
  - Token payload includes user ID and role
  - Example flow:
    ```python
    from jose import jwt
    from datetime import datetime, timedelta

    def create_access_token(user_id: int) -> str:
        expire = datetime.utcnow() + timedelta(minutes=30)
        payload = {
            "sub": str(user_id),
            "exp": expire,
            "type": "access"
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    # Protected endpoint
    @router.get("/me")
    async def get_current_user(token: str = Depends(oauth2_scheme)):
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        # ... fetch user from database
    ```

### 7. **Redis**
- **What it is**: In-memory data structure store used as cache and message broker
- **Why we use it**: Fast caching, session storage, rate limiting
- **How we use it**:
  - Cache frequently accessed data (analytics, user profiles)
  - Two-tier caching: Redis primary, in-memory fallback
  - Connection from `.env`:
    ```
    REDIS_URL=redis://localhost:6379/0
    ```
  - Example from `cache_service.py`:
    ```python
    class ApplicationCacheService:
        def __init__(self):
            self.cache = get_cache_service()

        async def get(self, key: str) -> Optional[Any]:
            """Get a value from cache."""
            return await self.cache.get(key)

        async def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
            """Set a value in cache with TTL."""
            return await self.cache.set(key, value, ttl)
    ```

### 8. **CORS Middleware**
- **What it is**: Cross-Origin Resource Sharing - security feature that controls which origins can access the API
- **Why we use it**: Allow our web app (localhost:8081) to communicate with backend (localhost:8000)
- **How we use it**:
  - Configured in `main.py` with allowed origins from `.env`
  - Handles preflight OPTIONS requests
  - Example from `main.py`:
    ```python
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin).rstrip('/') for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
    )
    ```
  - Configuration in `.env`:
    ```
    BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8081"]
    ```

### 9. **Security Middleware Stack**
- **What it is**: Custom middleware for security headers, request validation, and DDoS protection
- **Why we use it**: Protect against common web vulnerabilities and attacks
- **How we use it**:
  - Multiple layers of security middleware in `main.py`:
    ```python
    from app.core.security_middleware import (
        SecurityHeadersMiddleware,
        RequestValidationMiddleware,
        APISecurityMiddleware,
        RequestLoggingMiddleware,
        DDoSProtectionMiddleware
    )

    # Security middleware stack (in reverse order of execution)
    app.add_middleware(SecurityHeadersMiddleware)        # Security headers
    app.add_middleware(RequestLoggingMiddleware)         # Request logging
    app.add_middleware(APISecurityMiddleware)            # API security checks
    app.add_middleware(RequestValidationMiddleware)      # Request sanitization
    app.add_middleware(DDoSProtectionMiddleware)         # DDoS protection
    ```

### 10. **Rate Limiting Middleware**
- **What it is**: Custom middleware to limit request rates per IP address
- **Why we use it**: Prevent abuse, protect against brute force attacks
- **How we use it**:
  - Track requests per IP address
  - Periodic cleanup to prevent memory leaks
  - Example from `main.py`:
    ```python
    from app.core.rate_limiting import RateLimitMiddleware, cleanup_rate_limiter

    app.add_middleware(RateLimitMiddleware)

    # Background cleanup task
    async def periodic_cleanup():
        while True:
            await asyncio.sleep(1800)  # Every 30 minutes
            cleanup_rate_limiter()
    ```

### 11. **Python Enums**
- **What it is**: Enumeration type for defining sets of named constants
- **Why we use it**: Type-safe status values, prevent invalid data
- **How we use it**:
  - Define status enums for connections, users, etc.
  - Example from `connection.py`:
    ```python
    import enum
    from sqlalchemy import Enum

    class ConnectionStatus(enum.Enum):
        """Status of connection between users."""
        PENDING = "pending"      # Connection request sent
        ACCEPTED = "accepted"    # Connection accepted
        REJECTED = "rejected"    # Connection rejected
        BLOCKED = "blocked"      # User blocked
        EXPIRED = "expired"      # Request expired

    # Used in database model
    class Connection(Base):
        status = Column(Enum(ConnectionStatus), default=ConnectionStatus.PENDING)
    ```

### 12. **Python asyncio**
- **What it is**: Python's built-in library for asynchronous programming
- **Why we use it**: Handle concurrent requests efficiently, background tasks
- **How we use it**:
  - All FastAPI endpoints are async
  - Background cleanup tasks
  - Example from `main.py`:
    ```python
    import asyncio

    @app.on_event("startup")
    async def startup_event():
        await init_cache()
        asyncio.create_task(periodic_cleanup())

    async def periodic_cleanup():
        while True:
            await asyncio.sleep(1800)
            cleanup_rate_limiter()
            cache_service = get_app_cache_service()
            await cache_service.cleanup_expired_entries()
    ```

---

## Configuration & Environment

### 1. **Environment Variables (.env file)**
- **What it is**: Configuration file storing sensitive data and settings
- **Why we use it**: Keep secrets out of version control, environment-specific config
- **How we use it**:
  - All configuration loaded via Pydantic Settings
  - Example `.env` structure:
    ```env
    # Database
    DATABASE_URL=postgresql://user@localhost:5432/cooin_db

    # Security
    SECRET_KEY=your-secret-key-here
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30

    # Application
    DEBUG=false

    # CORS
    BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8081"]

    # Redis
    REDIS_URL=redis://localhost:6379/0

    # Email
    SMTP_HOST=smtp.gmail.com
    SMTP_PORT=587
    SMTP_USER=your-email@gmail.com
    SMTP_PASSWORD=your-app-password
    ```

---

## Data Flow Example

### User Login Flow:
1. **Frontend (React Native)**:
   - User enters email/password in `LoginScreen.tsx`
   - React Hook Form validates input using Zod schema
   - Axios sends POST request to `/api/v1/auth/login`

2. **Network Layer**:
   - Browser sends OPTIONS preflight request (CORS)
   - Backend responds with CORS headers allowing request
   - POST request proceeds with credentials

3. **Backend (FastAPI)**:
   - CORS middleware validates origin
   - Security middleware stack processes request
   - Request hits authentication endpoint
   - Pydantic validates request body
   - SQLAlchemy queries PostgreSQL for user
   - Password verified using bcrypt
   - JWT tokens generated (access + refresh)
   - Response sent with tokens

4. **Frontend Storage**:
   - Tokens stored in AsyncStorage
   - User object stored in Zustand state
   - Navigation redirects to Dashboard
   - Axios interceptor adds token to future requests

### Matching Flow:
1. **Frontend**: User opens `MatchingScreen.tsx`
2. **API Call**: `matchingService.findMatches()` called via Axios
3. **Backend**:
   - JWT token verified
   - Matching algorithm runs (database query)
   - Results cached in Redis
4. **Response**: Matching results with scores returned
5. **Frontend**:
   - Results displayed in FlatList
   - User can filter using search criteria
   - Connection request sent when user taps "Connect"

---

## Architecture Patterns

### Frontend Patterns:
- **Component-based architecture**: Reusable components (Input, Button, MatchCard)
- **Custom hooks**: `useLanguage()`, `useAuthStore()` for shared logic
- **Controller pattern**: React Hook Form Controller for form inputs
- **Service layer**: Separate service files (`matchingService.ts`, `authService.ts`)
- **Type safety**: TypeScript interfaces for all data structures

### Backend Patterns:
- **Layered architecture**:
  - API routes → Services → Models → Database
- **Dependency injection**: FastAPI's dependency system for auth
- **Repository pattern**: SQLAlchemy models abstract database access
- **Middleware pipeline**: Security → Validation → Logging → Rate Limiting
- **Error handling**: Custom exception classes with structured responses

---

## Security Implementations

### Frontend Security:
- **No sensitive data in code**: All secrets in environment variables
- **Secure token storage**: AsyncStorage for JWT tokens
- **Input validation**: Zod schemas prevent malformed data
- **Password strength indicators**: Real-time feedback for users
- **HTTPS only in production**: Enforced at network level

### Backend Security:
- **Password hashing**: bcrypt for all passwords
- **JWT authentication**: Stateless auth with short-lived tokens
- **Rate limiting**: Prevent brute force attacks
- **CORS protection**: Only allowed origins can access API
- **Security headers**: X-Frame-Options, X-Content-Type-Options, etc.
- **Request sanitization**: Middleware validates and cleans inputs
- **SQL injection protection**: SQLAlchemy ORM parameterized queries
- **DDoS protection**: Request throttling and IP tracking

---

## Performance Optimizations

### Frontend:
- **React Hook Form**: Reduces re-renders during form input
- **FlatList**: Efficient rendering of large lists with virtualization
- **AsyncStorage**: Fast local storage for tokens and preferences
- **Axios interceptors**: Automatic token refresh without user interaction
- **Memoization**: React.memo for expensive components

### Backend:
- **Redis caching**: Frequently accessed data cached in-memory
- **Two-tier cache**: Redis primary, in-memory fallback
- **Database indexing**: Primary keys and foreign keys indexed
- **Connection pooling**: SQLAlchemy manages database connections
- **Async endpoints**: Non-blocking I/O for concurrent requests
- **Background tasks**: Periodic cleanup runs independently

---

## Development Tools

### Frontend:
- **Expo CLI**: Development server and build tools
- **TypeScript compiler**: Type checking before runtime
- **ESLint**: Code quality and consistency
- **React DevTools**: Component inspection and debugging

### Backend:
- **Uvicorn**: Fast ASGI server with hot reload
- **FastAPI docs**: Interactive API testing at `/api/v1/docs`
- **Pydantic validation**: Automatic request validation
- **Python logging**: Structured logging for debugging

---

## Study Resources

### Frontend Learning:
- **React Native**: https://reactnative.dev/docs/getting-started
- **TypeScript**: https://www.typescriptlang.org/docs/
- **React Hook Form**: https://react-hook-form.com/get-started
- **i18next**: https://react.i18next.com/
- **Zod**: https://zod.dev/

### Backend Learning:
- **FastAPI**: https://fastapi.tiangolo.com/tutorial/
- **SQLAlchemy**: https://docs.sqlalchemy.org/en/20/tutorial/
- **Pydantic**: https://docs.pydantic.dev/latest/
- **JWT**: https://jwt.io/introduction
- **PostgreSQL**: https://www.postgresql.org/docs/

---

## Common Issues & Solutions

### Issue 1: CORS Errors
**Problem**: Web app can't connect to backend
**Solution**:
- Add origin to `BACKEND_CORS_ORIGINS` in `.env`
- Strip trailing slashes in CORS middleware
- Ensure preflight OPTIONS requests succeed

### Issue 2: Token Expiration
**Problem**: User logged out unexpectedly
**Solution**:
- Axios interceptor handles 401 responses
- Automatically refreshes access token using refresh token
- Redirects to login only when refresh token expires

### Issue 3: Translation Missing
**Problem**: Text showing key instead of translation
**Solution**:
- Add key to both `en.json` and `es.json`
- Ensure key path matches usage (e.g., `matching_screen.title`)
- Check for typos in translation keys

### Issue 4: Database Connection
**Problem**: Backend can't connect to PostgreSQL
**Solution**:
- Verify PostgreSQL is running: `pg_ctl status`
- Check `DATABASE_URL` in `.env`
- Ensure database exists: `createdb cooin_db`

---

## Conclusion

This technology stack provides a robust, scalable, and maintainable platform with:
- **Type safety** throughout (TypeScript + Pydantic)
- **Security** at multiple layers
- **Performance** through caching and async operations
- **User experience** with multi-language support
- **Developer experience** with automatic validation and documentation

All technologies work together to create a seamless lending/borrowing platform with focus on matching users based on their financial needs and preferences.
