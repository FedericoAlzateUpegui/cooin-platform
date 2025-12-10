# Cooin Web App - Mac Setup Instructions

**Last Updated**: 2025-11-16 (Session 14)
**Platform**: macOS
**Project Location**: `/Users/mariajimenez/Desktop/cooin-platform`

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start (First Time Setup)](#quick-start-first-time-setup)
3. [Daily Development Workflow](#daily-development-workflow)
4. [Public Sharing Setup](#public-sharing-setup)
5. [Troubleshooting](#troubleshooting)
6. [Common Commands Reference](#common-commands-reference)

---

## 🔧 Prerequisites

### Required Software

#### 1. **Python 3.11+**
```bash
# Check if installed
python3 --version

# If not installed, download from python.org or use Homebrew
brew install python@3.11
```

#### 2. **Node.js 18+ and npm**
```bash
# Check if installed
node --version
npm --version

# If not installed, use Homebrew
brew install node
```

#### 3. **PostgreSQL 14+**
```bash
# Install PostgreSQL
brew install postgresql@14

# Start PostgreSQL service
brew services start postgresql@14

# Verify it's running
psql --version
```

#### 4. **Cloudflare Tunnel** (Optional - for public sharing)
```bash
# Install cloudflared
brew install cloudflare/cloudflare/cloudflared

# Verify installation
cloudflared --version
```

---

## 🚀 Quick Start (First Time Setup)

### Step 1: Database Setup

```bash
# Create the database
createdb cooin_db

# Verify database was created
psql -l | grep cooin_db
```

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-backend
# Create Python virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
cp .env.example .env

# Edit .env file with your settings
nano .env
```

**Important .env settings to configure:**
```env
DATABASE_URL=postgresql://YOUR_USERNAME@localhost:5432/cooin_db
SECRET_KEY=your-generated-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_CORS_ORIGINS=["http://localhost:8083","http://localhost:19006"]
REDIS_URL=redis://localhost:6379/0
```

**Generate a secure SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Find your PostgreSQL username:**
```bash
whoami  # This is usually your PostgreSQL username on Mac
```

```bash
# Run database migrations
alembic upgrade head

# Verify migrations completed
alembic current
```

### Step 3: Frontend Setup

```bash
# Open a new terminal tab/window
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-frontend

# Install dependencies
npm install

# Create .env file (optional - defaults work for local development)
echo "EXPO_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env
```

### Step 4: Start the Application

**Terminal 1 - Backend:**
```bash
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-backend
source venv/bin/activate
python3 start_dev.py
```

**Wait for:** `Uvicorn running on http://0.0.0.0:8000`

**Terminal 2 - Frontend:**
```bash
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-frontend
npx expo start --web --port 8083 --clear
```

**Wait for:** `Metro waiting on exp://localhost:19000`

### Step 5: Access the Application

**Open in browser:**
- Frontend: http://localhost:8083
- Backend API Docs: http://localhost:8000/docs

---

## 💻 Daily Development Workflow

Once you've completed the first-time setup, use this simplified workflow:

### Terminal 1 - Backend
```bash
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-backend
source venv/bin/activate
python3 start_dev.py
```

### Terminal 2 - Frontend
```bash
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-frontend
npx expo start --web --port 8083
```

**Access at:** http://localhost:8083

---

## 🌍 Public Sharing Setup

When you need to share your app with partners/testers via the internet:

### Step 1: Start Backend and Frontend (as above)

Follow the [Daily Development Workflow](#daily-development-workflow) to start both services.

### Step 2: Start Cloudflare Tunnels

**Terminal 3 - Backend Tunnel:**
```bash
cloudflared tunnel --url http://localhost:8000
```

**Look for output like:**
```
Your quick Tunnel has been created! Visit it at:
https://random-string-1234.trycloudflare.com
```

**Terminal 4 - Frontend Tunnel:**
```bash
cloudflared tunnel --url http://localhost:8083
```

**Look for output like:**
```
Your quick Tunnel has been created! Visit it at:
https://random-string-5678.trycloudflare.com
```

### Step 3: Update Frontend Configuration

```bash
# Edit the frontend config file
nano /Users/mariajimenez/Desktop/cooin-platform/cooin-frontend/src/constants/config.ts
```

**Update the API_URL:**
```typescript
export const API_CONFIG = {
  BASE_URL: "https://random-string-1234.trycloudflare.com/api/v1",  // Your backend tunnel URL
  TIMEOUT: 10000,
  RETRY_ATTEMPTS: 3,
} as const;
```

**Or set environment variable:**
```bash
# In cooin-frontend directory
echo "EXPO_PUBLIC_API_URL=https://random-string-1234.trycloudflare.com/api/v1" > .env
```

### Step 4: Restart Frontend

Stop the frontend (Ctrl+C in Terminal 2) and restart:
```bash
npx expo start --web --port 8083 --clear
```

### Step 5: Share the Frontend URL

Share the **frontend tunnel URL** with your partners:
```
https://random-string-5678.trycloudflare.com
```

⚠️ **Important Notes:**
- Cloudflare tunnel URLs change each time you restart the tunnel
- You need to update the config and restart frontend each time tunnel URLs change
- Keep all 4 terminals running while sharing

---

## 🐛 Troubleshooting

### Backend Issues

#### "Command not found: python3"
```bash
# Install Python
brew install python@3.11

# Or create an alias in ~/.zshrc
echo 'alias python=python3' >> ~/.zshrc
source ~/.zshrc
```

#### "Could not connect to database"
```bash
# Check if PostgreSQL is running
brew services list | grep postgresql

# Start PostgreSQL if stopped
brew services start postgresql@14

# Check database exists
psql -l | grep cooin_db

# If database doesn't exist, create it
createdb cooin_db
```

#### "ModuleNotFoundError: No module named 'X'"
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### "Alembic migration failed"
```bash
# Check current migration version
alembic current

# Reset database (WARNING: Deletes all data)
dropdb cooin_db
createdb cooin_db
alembic upgrade head
```

### Frontend Issues

#### "Cannot find module 'expo'"
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

#### "Metro bundler error"
```bash
# Clear Metro cache
npx expo start --web --port 8083 --clear

# Or manually clear cache
rm -rf .expo
npm start -- --reset-cache
```

#### "Cannot connect to API"
```bash
# Check backend is running
curl http://localhost:8000/api/v1/health

# Check frontend .env file
cat .env

# Verify config.ts uses correct URL
cat src/constants/config.ts | grep BASE_URL
```

#### "Port 8083 already in use"
```bash
# Find and kill process using port 8083
lsof -ti:8083 | xargs kill -9

# Or use a different port
npx expo start --web --port 8084
```

### Cloudflare Tunnel Issues

#### "Command not found: cloudflared"
```bash
# Install cloudflared
brew install cloudflare/cloudflare/cloudflared
```

#### "Tunnel disconnects frequently"
- This is normal for free Cloudflare tunnels
- Consider upgrading to a named tunnel for stable URLs
- See: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/

---

## 📚 Common Commands Reference

### Backend Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Deactivate virtual environment
deactivate

# Start development server
python3 start_dev.py

# Alternative: Start with uvicorn directly
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Check database connection
psql cooin_db
```

### Frontend Commands

```bash
# Install dependencies
npm install

# Start development server (web)
npx expo start --web --port 8083

# Clear cache and restart
npx expo start --web --port 8083 --clear

# Run on iOS simulator (requires Xcode)
npx expo start --ios

# Run on Android emulator
npx expo start --android

# Type checking
npx tsc --noEmit

# Lint
npm run lint
```

### Database Commands

```bash
# Create database
createdb cooin_db

# Drop database (WARNING: Deletes all data)
dropdb cooin_db

# List databases
psql -l

# Connect to database
psql cooin_db

# Backup database
pg_dump cooin_db > backup.sql

# Restore database
psql cooin_db < backup.sql
```

### Cloudflare Tunnel Commands

```bash
# Start tunnel for backend
cloudflared tunnel --url http://localhost:8000

# Start tunnel for frontend
cloudflared tunnel --url http://localhost:8083

# Check cloudflared version
cloudflared --version

# Login to Cloudflare account
cloudflared tunnel login
```

### Git Commands (For Development)

```bash
# Check status
git status

# Create feature branch
git checkout -b feature/your-feature-name

# Add changes
git add .

# Commit changes
git commit -m "Description of changes"

# Push to remote
git push origin feature/your-feature-name

# Pull latest changes
git pull origin main
```

---

## 📁 Important File Locations

### Backend Files
- **Main app**: `/Users/mariajimenez/Desktop/cooin-platform/cooin-backend/app/main.py`
- **Config**: `/Users/mariajimenez/Desktop/cooin-platform/cooin-backend/app/core/config.py`
- **Environment**: `/Users/mariajimenez/Desktop/cooin-platform/cooin-backend/.env`
- **Dependencies**: `/Users/mariajimenez/Desktop/cooin-platform/cooin-backend/requirements.txt`
- **Migrations**: `/Users/mariajimenez/Desktop/cooin-platform/cooin-backend/alembic/versions/`

### Frontend Files
- **App entry**: `/Users/mariajimenez/Desktop/cooin-platform/cooin-frontend/App.tsx`
- **API config**: `/Users/mariajimenez/Desktop/cooin-platform/cooin-frontend/src/constants/config.ts`
- **Environment**: `/Users/mariajimenez/Desktop/cooin-platform/cooin-frontend/.env`
- **Dependencies**: `/Users/mariajimenez/Desktop/cooin-platform/cooin-frontend/package.json`

### Documentation
- **Main README**: `/Users/mariajimenez/Desktop/cooin-platform/README.md`
- **This guide**: `/Users/mariajimenez/Desktop/cooin-platform/MAC_SETUP_INSTRUCTIONS.md`
- **Todo list**: `/Users/mariajimenez/Desktop/cooin-platform/TODO.md`
- **History**: `/Users/mariajimenez/Desktop/cooin-platform/HISTORY.md`

---

## 🎯 Quick Reference Card

**For Local Development:**
```bash
# Terminal 1 - Backend
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-backend
source venv/bin/activate
python3 start_dev.py

# Terminal 2 - Frontend
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-frontend
npx expo start --web --port 8083

# Access: http://localhost:8083
```

**For Public Sharing:**
```bash
# Start local development first (above), then:

# Terminal 3 - Backend Tunnel
cloudflared tunnel --url http://localhost:8000

# Terminal 4 - Frontend Tunnel
cloudflared tunnel --url http://localhost:8083

# Update config.ts with backend tunnel URL
# Restart frontend
# Share frontend tunnel URL
```

---

## 📞 Need Help?

- **Project Documentation**: Check `/Users/mariajimenez/Desktop/cooin-platform/README.md`
- **Known Issues**: Check `/Users/mariajimenez/Desktop/cooin-platform/TODO.md` - Known Issues section
- **Change History**: Check `/Users/mariajimenez/Desktop/cooin-platform/HISTORY.md`
- **API Documentation**: http://localhost:8000/docs (when backend is running)

---

## ✅ Setup Checklist

Use this checklist for your first-time setup:

- [ ] Python 3.11+ installed (`python3 --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] PostgreSQL 14+ installed (`psql --version`)
- [ ] PostgreSQL service running (`brew services list | grep postgresql`)
- [ ] Database created (`createdb cooin_db`)
- [ ] Backend virtual environment created (`python3 -m venv venv`)
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Backend .env file configured (copied from .env.example)
- [ ] SECRET_KEY generated and added to .env
- [ ] Database migrations run (`alembic upgrade head`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Backend starts successfully (`python3 start_dev.py`)
- [ ] Frontend starts successfully (`npx expo start --web --port 8083`)
- [ ] Can access app at http://localhost:8083
- [ ] Can access API docs at http://localhost:8000/docs
- [ ] (Optional) Cloudflare installed for public sharing

---

**Happy Coding! 🚀**
