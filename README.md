# Cooin Platform

A peer-to-peer lending and borrowing platform with web, iOS, and mobile applications. Cooin connects lenders and borrowers through intelligent matching algorithms and provides a secure, transparent platform for financial transactions.

## 🌟 Features

- **Multi-Language Support**: Full internationalization (i18n) with English and Spanish
- **Intelligent Matching**: Algorithm-based matching between lenders and borrowers
- **Secure Authentication**: JWT-based auth with access and refresh tokens
- **Real-time Connections**: WebSocket support for instant messaging
- **Cross-Platform**: Web app, iOS app, and React Native mobile app
- **Advanced Security**: Multi-layer security middleware, rate limiting, and CORS protection
- **Caching System**: Two-tier caching (Redis + in-memory fallback)

## 📁 Project Structure

```
cooin-platform/
├── cooin-backend/          # FastAPI backend server
├── cooin-frontend/         # React Native web & mobile app
├── cooin-ios/              # Native iOS Swift app
└── TECH_STACK.md          # Comprehensive technology documentation
```

## 🚀 Quick Start

### Prerequisites

- **Backend**: Python 3.10+, PostgreSQL 14+, Redis (optional)
- **Frontend**: Node.js 18+, npm or yarn
- **iOS**: Xcode 15+, macOS 13+

### 1. Backend Setup

```bash
cd cooin-backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials and configuration

# Generate a secure SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
# Copy the output to SECRET_KEY in .env

# Create database
createdb cooin_db

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**⚠️ Windows Users:** If you get `ModuleNotFoundError`, you may have multiple Python installations. Use the full path:
```bash
"C:\Users\YOUR_USERNAME\AppData\Local\Microsoft\WindowsApps\python.exe" -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

See [Common Issues](#common-issues--solutions) below for details.

Backend will be available at: `http://localhost:8000`
- API docs: `http://localhost:8000/api/v1/docs`
- Health check: `http://localhost:8000/health`

### 2. Frontend Setup (Web & Mobile)

```bash
cd cooin-frontend

# Install dependencies
npm install

# Start development server
# For web:
npx expo start --web

# For mobile (iOS simulator):
npx expo start --ios

# For mobile (Android):
npx expo start --android
```

Web app will be available at: `http://localhost:8081`

### 3. iOS Setup (Native Swift App)

```bash
cd cooin-ios/CooinNew

# Open in Xcode
open CooinNew.xcodeproj

# Or build from command line
xcodebuild build \
  -project CooinNew.xcodeproj \
  -scheme CooinNew \
  -destination 'platform=iOS Simulator,name=iPhone 16' \
  -configuration Debug
```

## 🔧 Configuration

### Backend Configuration

Key environment variables (see `.env.example` for complete list):

```env
# Database
DATABASE_URL=postgresql://username@localhost:5432/cooin_db

# Security
SECRET_KEY=<generated-secret-key>
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS - Add all frontend origins
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8081"]

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Frontend Configuration

Edit `cooin-frontend/src/constants/config.ts`:

```typescript
export const API_CONFIG = {
  BASE_URL: 'http://127.0.0.1:8000/api/v1',
  TIMEOUT: 10000,
  RETRY_ATTEMPTS: 3,
} as const;
```

## 🧪 Testing

### Backend Tests

```bash
cd cooin-backend
pytest
```

### Frontend Tests

```bash
cd cooin-frontend
npm test
```

### iOS Tests

```bash
cd cooin-ios/CooinNew
xcodebuild test \
  -project CooinNew.xcodeproj \
  -scheme CooinNew \
  -destination 'platform=iOS Simulator,name=iPhone 16'
```

## 🏗️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Primary database
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation
- **Redis** - Caching and sessions
- **JWT** - Authentication
- **Uvicorn** - ASGI server

### Frontend (Web & Mobile)
- **React Native** - Cross-platform framework
- **Expo** - Development platform
- **TypeScript** - Type-safe JavaScript
- **i18next** - Internationalization
- **React Hook Form** - Form management
- **Zod** - Schema validation
- **Axios** - HTTP client
- **Zustand** - State management

### iOS
- **Swift** - Native iOS development
- **SwiftUI** - Modern UI framework
- **Combine** - Reactive programming

For detailed information about the technology stack, see [TECH_STACK.md](./TECH_STACK.md).

## 🌍 Internationalization (i18n)

The platform supports multiple languages:

- **Supported Languages**: English (en), Spanish (es)
- **Translation Files**: `cooin-frontend/src/i18n/locales/`
- **202+ translation keys** covering all screens and components

### Adding a New Language

1. Create translation file: `src/i18n/locales/{language-code}.json`
2. Copy structure from `en.json` and translate all values
3. Add language to `src/i18n/config.ts`

## 📱 Platform Support

| Platform | Status | Location |
|----------|--------|----------|
| Web App | ✅ Production Ready | `cooin-frontend/` |
| iOS Native | ✅ Production Ready | `cooin-ios/` |
| Android | 🚧 In Development | `cooin-frontend/` |
| API Backend | ✅ Production Ready | `cooin-backend/` |

## 🔒 Security Features

- **Multi-layer Security Middleware**:
  - Security headers (X-Frame-Options, CSP, etc.)
  - Request validation and sanitization
  - API security checks
  - DDoS protection
  - Rate limiting (100 requests/hour per IP)

- **Authentication**:
  - JWT tokens with 30-minute access tokens
  - 7-day refresh tokens
  - Secure password hashing (bcrypt)

- **CORS Configuration**:
  - Whitelist-based origin validation
  - Automatic trailing slash handling

## 📚 API Documentation

Interactive API documentation is available when running the backend in debug mode:

- **Swagger UI**: `http://localhost:8000/api/v1/docs`
- **ReDoc**: `http://localhost:8000/api/v1/redoc`
- **OpenAPI Schema**: `http://localhost:8000/api/v1/openapi.json`

## 🐛 Common Issues & Solutions

### Backend Issues

**Problem**: CORS errors when accessing from web app
**Solution**: Add your frontend URL to `BACKEND_CORS_ORIGINS` in `.env`
```env
BACKEND_CORS_ORIGINS=["http://localhost:8081"]
```

**Problem**: Database connection failed
**Solution**: Ensure PostgreSQL is running and credentials are correct:
```bash
# Check PostgreSQL status
pg_ctl status

# Create database if it doesn't exist
createdb cooin_db
```

**Problem**: Redis connection failed
**Solution**: Redis is optional. The app will fall back to in-memory cache. To use Redis:
```bash
# Start Redis
redis-server

# Or install via Homebrew (macOS)
brew install redis
brew services start redis
```

**Problem**: `ModuleNotFoundError` - Backend can't find installed packages (Windows)
**Solution**: You likely have multiple Python installations. The packages are installed in one Python, but you're running another.

**Diagnosis:**
```bash
where python
# Shows all Python installations

pip --version
# Shows where packages are installed
```

**Fix Option 1 - Use Full Python Path** (Quick):
```bash
"C:\Users\YOUR_USERNAME\AppData\Local\Microsoft\WindowsApps\python.exe" -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Fix Option 2 - Virtual Environment** (Recommended):
```bash
cd cooin-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Fix Option 3 - Fix PATH Order**:
Move Microsoft Store Python higher in Windows PATH environment variable.

### Frontend Issues

**Problem**: Module not found errors
**Solution**: Clear cache and reinstall dependencies:
```bash
rm -rf node_modules package-lock.json
npm install
```

**Problem**: Expo server won't start
**Solution**: Clear Expo cache:
```bash
npx expo start --clear
```

### iOS Issues

**Problem**: Build fails in Xcode
**Solution**: Clean build folder and derived data:
```bash
# In Xcode: Product > Clean Build Folder (Cmd+Shift+K)
# Or via command line:
rm -rf ~/Library/Developer/Xcode/DerivedData
```

### Permission Issues (Windows)

**Problem**: Cannot edit files, "Access denied" errors
**Solution**: If project is in `C:\Windows\System32\cooin-app`:

**Option 1 - Quick Fix**: Run `fix-permissions.bat` as administrator
**Option 2 - Alternative**: Run VS Code as administrator
**Option 3 - Recommended**: Move project to user folder (e.g., `C:\Users\USERNAME\Documents\cooin-app`)

See [PERMISSION-FIX.md](./PERMISSION-FIX.md) for detailed instructions.

## 🤝 Development Workflow

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "Add feature: description"

# Push to remote
git push origin feature/your-feature-name

# Create pull request on GitHub
```

### Running All Services

Use separate terminal windows/tabs:

```bash
# Terminal 1: Backend
cd cooin-backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend Web
cd cooin-frontend
npx expo start --web

# Terminal 3: Redis (optional)
redis-server

# Terminal 4: PostgreSQL (if not running as service)
postgres -D /usr/local/var/postgres
```

## 🌐 Exposing Your App Publicly (Ngrok)

Want to share your local app with others or access it from the internet? Use ngrok to create secure tunnels.

### Quick Setup

1. **Install ngrok**: Download from [ngrok.com/download](https://ngrok.com/download)
2. **Configure auth token**: Edit `ngrok.yml` with your token from [dashboard.ngrok.com](https://dashboard.ngrok.com)
3. **Start your services**:
   ```bash
   # Backend (port 8000)
   cd cooin-backend && python start_dev.py

   # Frontend (port 8083)
   cd cooin-frontend && npx expo start --web --port 8083
   ```
4. **Start ngrok**: Run `start-ngrok.bat`
5. **Get URLs**: Run `get-ngrok-urls.ps1` and follow prompts

### Features

- ✅ Automated tunnel setup for frontend and backend
- ✅ Auto-updates frontend config with ngrok backend URL
- ✅ Creates config backups before changes
- ✅ Interactive PowerShell script with color output
- ✅ Comprehensive documentation and troubleshooting

### Documentation

- **[NGROK-QUICKSTART.md](./NGROK-QUICKSTART.md)** - One-page quick reference
- **[NGROK-SETUP.md](./NGROK-SETUP.md)** - Complete setup guide with troubleshooting

### Example URLs

After running ngrok, you'll get public URLs like:
- Frontend: `https://abc123.ngrok.io`
- Backend: `https://xyz789.ngrok.io`

**Note**: Free plan URLs change every session (2-hour limit). Consider paid plan for persistent URLs.

---

## 📊 Project Status

- ✅ Backend API - Complete
- ✅ Web Frontend - Complete with full i18n
- ✅ iOS App - Complete with full i18n
- ✅ Authentication System - Complete
- ✅ Matching Algorithm - Complete
- ✅ Real-time Messaging - Complete
- ✅ Ngrok Integration - Complete (Session 5)
- 🚧 Payment Integration - In Progress
- 🚧 Admin Dashboard - In Progress

## 📖 Additional Documentation

### Setup & Configuration
- [HOW-TO-LAUNCH-WEB-APP.md](./HOW-TO-LAUNCH-WEB-APP.md) - Detailed launch instructions for VS Code
- [TECH_STACK.md](./TECH_STACK.md) - Comprehensive technology documentation with code examples

### Ngrok Public Access
- [NGROK-QUICKSTART.md](./NGROK-QUICKSTART.md) - Quick reference for ngrok setup
- [NGROK-SETUP.md](./NGROK-SETUP.md) - Complete ngrok guide with troubleshooting

### Troubleshooting
- [PERMISSION-FIX.md](./PERMISSION-FIX.md) - Solutions for file permission issues

### Change History
- [HISTORY.md](./HISTORY.md) - Complete changelog with all sessions and fixes
- [TODO.md](./TODO.md) - Current tasks and future enhancements

### API Documentation
- [Backend API Documentation](http://localhost:8000/api/v1/docs) - Interactive Swagger UI (when running)

## 📄 License

This project is proprietary software. All rights reserved.

## 👥 Contributors

Developed with assistance from Claude AI.

---

For questions or issues, please open an issue on GitHub.
