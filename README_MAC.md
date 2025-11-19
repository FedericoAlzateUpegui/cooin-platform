# Cooin Platform - Mac Setup Guide 🍎

**Purpose**: Mac-specific setup instructions and configuration.

**Note**: This file is ONLY edited by Claude on Mac. Windows can READ for context.

---

## 🖥️ Mac Environment

**Machine**: MacBook Pro (Intel)
**Architecture**: x86_64
**OS**: macOS (Darwin 24.6.0)
**User**: mariajimenez

---

## 📁 Project Location

```
/Users/mariajimenez/Desktop/cooin-platform/
├── cooin-backend/          # FastAPI backend
├── cooin-frontend/         # React Native web/mobile
├── cooin-ios/             # Native iOS app
└── Documentation files
```

---

## 🚀 Quick Start (Mac)

### Prerequisites Installed ✅
- ✅ Python 3.12.1
- ✅ Node.js & npm
- ✅ Docker Desktop 25.0.3
- ✅ Homebrew (/usr/local/bin/brew)
- ✅ Git
- ✅ PostgreSQL (via backend config)

### One-Time Setup

**1. Install Homebrew** (if not installed):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**2. Install Docker Desktop** (already installed):
```bash
brew install --cask docker
# Or download from: https://www.docker.com/products/docker-desktop/
```

**3. Clone Repository** (already done):
```bash
git clone <repository-url>
cd cooin-platform
```

---

## 🏃 Running the App (Mac)

### Step 1: Start Docker Desktop
```bash
open -a Docker
# Wait for Docker to start (whale icon in menu bar)
```

### Step 2: Start Redis
```bash
cd /Users/mariajimenez/Desktop/cooin-platform
docker-compose up -d redis

# Verify Redis is running
docker ps
```

### Step 3: Start Backend
```bash
# Open new terminal
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-backend

# Activate virtual environment
source venv/bin/activate

# Start FastAPI server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will be at**: http://localhost:8000
**API Docs**: http://localhost:8000/api/v1/docs

### Step 4: Start Frontend
```bash
# Open new terminal
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-frontend

# Install dependencies (first time only)
npm install

# Start Expo web server
npx expo start --web --port 8083
```

**Frontend will be at**: http://localhost:8083

---

## 🔧 Mac-Specific Configuration

### Backend (.env)
```env
DATABASE_URL=postgresql://mariajimenez@localhost:5432/cooin_db
REDIS_URL=redis://localhost:6379/0
BACKEND_CORS_ORIGINS=["http://localhost:8083"]
```

### Frontend (config.ts)
```typescript
BASE_URL: "http://localhost:8000/api/v1"
```

### PostgreSQL Setup (Mac)
```bash
# Install PostgreSQL
brew install postgresql@14

# Start PostgreSQL service
brew services start postgresql@14

# Create database
createdb cooin_db

# Run migrations
cd cooin-backend
alembic upgrade head
```

---

## 🐳 Docker Commands (Mac)

### Docker Desktop
```bash
# Start Docker Desktop
open -a Docker

# Check if Docker is running
docker ps
```

### Redis Container
```bash
# Start Redis
docker-compose up -d redis

# Stop Redis
docker-compose down

# View Redis logs
docker logs cooin-redis

# Connect to Redis CLI
docker exec -it cooin-redis redis-cli
> PING  # Should return PONG
> SET test "hello"
> GET test
> exit
```

### Docker Troubleshooting
```bash
# If containers won't start
docker-compose down
docker system prune -a  # Clean up
docker-compose up -d redis

# View all containers
docker ps -a

# Remove all stopped containers
docker container prune
```

---

## 📦 Package Management (Mac)

### Homebrew
```bash
# Update Homebrew
brew update

# Upgrade packages
brew upgrade

# Search for package
brew search <package-name>

# Install package
brew install <package-name>
```

### Python Packages
```bash
cd cooin-backend
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Update a package
pip install --upgrade <package-name>

# List installed packages
pip list
```

### Node Packages
```bash
cd cooin-frontend

# Install dependencies
npm install

# Update packages
npm update

# Check for outdated packages
npm outdated
```

---

## 🔍 Debugging (Mac)

### Check Running Services
```bash
# Check port 8000 (Backend)
lsof -i :8000

# Check port 8083 (Frontend)
lsof -i :8083

# Check port 6379 (Redis)
lsof -i :6379

# Kill process on port
lsof -ti :8000 | xargs kill -9
```

### View Logs
```bash
# Backend logs
cd cooin-backend
tail -f app.log

# Frontend logs
# Check terminal where Metro bundler is running

# Redis logs
docker logs -f cooin-redis
```

### Test API Endpoints
```bash
# Test backend health
curl http://localhost:8000/health

# Test API v1 health
curl http://localhost:8000/api/v1/health

# Test with verbose output
curl -v http://localhost:8000/api/v1/health
```

---

## 🌐 Git Workflow (Mac)

### Before Starting Work
```bash
# Always pull latest changes from Windows
git pull origin main

# Check status
git status
```

### After Finishing Work
```bash
# Add Mac documentation files
git add HISTORY_MAC.md TODO_MAC.md README_MAC.md HOW-TO-LAUNCH-WEB-APP_MAC.md

# Commit with Mac identifier
git commit -m "docs: Session X on Mac 🍎 - [description]"

# Push to remote
git push origin main
```

### Avoid Editing Windows Files
- ❌ Don't edit: `HISTORY.md`, `TODO.md`, `README.md` (Windows only)
- ✅ Edit: `HISTORY_MAC.md`, `TODO_MAC.md`, `README_MAC.md` (Mac only)
- 👀 Read Windows files for context only

---

## 🛠️ Terminal Shortcuts (Mac)

```bash
# Open new terminal tab: Cmd + T
# Open new terminal window: Cmd + N
# Clear terminal: Cmd + K or type 'clear'
# Stop process: Ctrl + C
# Search command history: Ctrl + R

# Useful aliases (add to ~/.zshrc or ~/.bash_profile)
alias cooin='cd /Users/mariajimenez/Desktop/cooin-platform'
alias backend='cd /Users/mariajimenez/Desktop/cooin-platform/cooin-backend && source venv/bin/activate'
alias frontend='cd /Users/mariajimenez/Desktop/cooin-platform/cooin-frontend'
```

---

## 📊 Current Status (Mac)

### Services
- ✅ Docker Desktop: Running
- ✅ Redis: HEALTHY (docker container)
- ✅ Backend: Running on port 8000
- ✅ Frontend: Running on port 8083

### Installed Packages
- Backend: Python packages in venv
- Frontend: 1499 npm packages

---

## 🔗 Quick Links

**Mac Documentation**:
- [Mac History](./HISTORY_MAC.md) - Mac session history
- [Mac TODO](./TODO_MAC.md) - Mac tasks and status
- [Mac Launch Guide](./HOW-TO-LAUNCH-WEB-APP_MAC.md) - Detailed launch instructions

**Windows Documentation** (Read Only):
- [Windows History](./HISTORY.md) - What's happening on Windows
- [Windows TODO](./TODO.md) - Windows tasks
- [Windows README](./README.md) - Windows setup

**Shared Documentation**:
- [DP.md](./DP.md) - Documentation process guide
- [TECH_STACK.md](./TECH_STACK.md) - Technology stack
- [Main README](./README.md) - General project info

---

**Last Updated**: 2025-11-19 (Session 15)
**Maintained By**: Claude on Mac 🍎
