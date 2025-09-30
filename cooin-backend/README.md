# Cooin Backend API

A modern FastAPI backend for the Cooin matching/connection platform with financial elements. Built with security, scalability, and performance in mind.

## 🚀 Features

### Core Platform Features
- **User Authentication**: JWT-based auth with refresh tokens
- **User Roles**: Flexible lender/borrower/both role system
- **Profile Management**: Comprehensive user profiles with privacy controls
- **Connection System**: Matching system between lenders and borrowers
- **Rating System**: Trust and reputation management
- **Security**: Account locking, rate limiting, input validation

### Technical Features
- **FastAPI**: Modern, fast web framework with automatic OpenAPI docs
- **SQLAlchemy**: Advanced ORM with relationship management
- **PostgreSQL**: Production-ready database with migrations
- **JWT Security**: Access + refresh token pattern
- **Pydantic**: Request/response validation and serialization
- **Alembic**: Database schema migrations
- **Structured Logging**: Production-ready logging
- **CORS Support**: Configurable for frontend integration

## 📋 Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Redis (optional, for caching)

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd cooin-backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Copy the example environment file and configure it:
```bash
cp .env.example .env
```

Edit `.env` file with your settings:
```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/cooin_db

# JWT Configuration
SECRET_KEY=your-super-secret-key-min-32-chars
ALGORITHM=HS256

# API Configuration
DEBUG=True
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

### 5. Database Setup
Create PostgreSQL database:
```sql
CREATE DATABASE cooin_db;
CREATE USER cooin_user WITH ENCRYPTED PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE cooin_db TO cooin_user;
```

### 6. Run Database Migrations
```bash
alembic upgrade head
```

### 7. Start the Development Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

## 🏗️ Project Structure

```
cooin-backend/
├── app/                    # Main application package
│   ├── api/v1/            # API routes (versioned)
│   │   ├── auth.py        # Authentication endpoints
│   │   └── api.py         # Main API router
│   ├── core/              # Core configuration
│   │   ├── config.py      # Settings and environment variables
│   │   ├── security.py    # JWT and password handling
│   │   └── deps.py        # Dependency injection
│   ├── db/                # Database configuration
│   │   └── base.py        # SQLAlchemy setup
│   ├── models/            # Database models
│   │   ├── user.py        # User and RefreshToken models
│   │   ├── profile.py     # UserProfile model
│   │   ├── connection.py  # Connection and Message models
│   │   └── rating.py      # Rating model
│   ├── schemas/           # Pydantic schemas
│   │   ├── user.py        # User request/response schemas
│   │   ├── auth.py        # Authentication schemas
│   │   └── profile.py     # Profile schemas
│   ├── services/          # Business logic
│   │   └── user_service.py # User-related operations
│   ├── utils/             # Utility functions
│   └── main.py            # FastAPI application
├── alembic/               # Database migrations
├── tests/                 # Test suite
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── alembic.ini           # Alembic configuration
```

## 🔐 Authentication Endpoints

### Register
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123",
  "confirm_password": "SecurePass123",
  "role": "borrower",
  "agree_to_terms": true
}
```

### Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123",
  "remember_me": false
}
```

### Refresh Token
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Get Current User
```http
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

## 🗃️ Database Models

### User Model
- Authentication and basic user info
- Role management (lender/borrower/both)
- Account security (locking, failed attempts)
- Email verification

### UserProfile Model
- Extended personal information
- Financial details and preferences
- Privacy settings
- Profile completion tracking

### Connection Model
- Matching system between users
- Connection status tracking
- Financial request details

### Rating Model
- Trust and reputation system
- Detailed rating categories
- Review system with responses

## 🔧 Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Downgrade migration:
```bash
alembic downgrade -1
```

## 🧪 Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app
```

## 🚀 Production Deployment

### Environment Variables
Update `.env` for production:
```env
DEBUG=False
SECRET_KEY=<generate-secure-key>
DATABASE_URL=postgresql://user:pass@prod-host:5432/cooin_db
BACKEND_CORS_ORIGINS=["https://yourdomain.com"]
```

### Run with Gunicorn
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker (Optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

## 📊 API Documentation

When running in debug mode, automatic interactive documentation is available:

- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## 🔒 Security Features

### Authentication
- JWT access tokens (short-lived)
- Refresh tokens (long-lived, revokable)
- Device/session tracking
- Account locking after failed attempts

### Password Security
- Bcrypt hashing with configurable rounds
- Password strength validation
- Secure password reset flow

### Input Validation
- Pydantic schemas for all requests
- SQL injection prevention via SQLAlchemy
- XSS protection through proper serialization

### API Security
- CORS configuration
- Rate limiting (configurable)
- Security headers middleware
- HTTPS-ready configuration

## 📝 Development

### Code Style
- Follow PEP 8 style guidelines
- Use type hints throughout
- Document all functions and classes
- Keep functions focused and testable

### Adding New Features
1. Create/update database models in `app/models/`
2. Create migration: `alembic revision --autogenerate`
3. Add Pydantic schemas in `app/schemas/`
4. Implement business logic in `app/services/`
5. Create API endpoints in `app/api/v1/`
6. Add tests in `tests/`
7. Update documentation

### Environment Management
- Development: Use `.env` file
- Testing: Use separate test database
- Production: Use environment variables

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check PostgreSQL is running
sudo service postgresql status

# Check database exists
psql -h localhost -U postgres -l
```

**Migration Issues**
```bash
# Reset migrations (development only)
alembic downgrade base
alembic upgrade head
```

**Import Errors**
```bash
# Ensure you're in the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review API documentation
3. Check application logs
4. Create an issue in the repository

## 🔄 Next Steps

1. **Profile Management**: Implement profile CRUD operations
2. **Connection System**: Build matching and messaging features
3. **Rating System**: Implement review and rating endpoints
4. **Email Integration**: Add email verification and notifications
5. **File Upload**: Implement document/image upload functionality
6. **Admin Panel**: Create admin endpoints for platform management
7. **Analytics**: Add usage tracking and reporting
8. **Testing**: Expand test coverage
9. **Performance**: Add caching and optimization
10. **Monitoring**: Implement logging and error tracking