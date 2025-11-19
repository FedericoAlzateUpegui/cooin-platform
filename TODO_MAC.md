# Cooin Web App - TODO (Mac 🍎)

**Purpose**: Track tasks, progress, and issues specific to Mac development environment.

**Note**: This file is ONLY edited by Claude on Mac. Windows can READ for context.

---

## 🚀 Current Session (Session 15) - Docker & Redis Running ✅

### ✅ Completed This Session
- [x] **Frontend Dependencies Installed** - All npm packages installed successfully
- [x] **Metro Bundler Started** - Web server running on port 8083
- [x] **Backend Verified** - FastAPI healthy on port 8000
- [x] **Docker Desktop Started** - Daemon running (v25.0.3)
- [x] **Redis Container Running** - Healthy on port 6379
- [x] **Multi-Machine Documentation Created** - Mac-specific files created

### 📝 Pending Work (Mac)
- [ ] **Restart Backend with Redis** - Backend currently running without Redis connection
- [ ] **Test Full Application** - Test complete app workflow with all services
- [ ] **Verify Frontend-Backend Connection** - Fix "Cannot connect to server" error if persists

### 🔄 Context from Windows
- Windows is on Session 14
- Latest Windows work: System notifications, Redis setup, Docker configuration
- See `TODO.md` for Windows-specific pending tasks

---

## 🌐 Mac Local Development

### Current Services Running
```bash
# Frontend - Already Running
# Port: 8083
# Status: ✅ Running (PID in background Bash 90f140)

# Backend - Already Running
# Port: 8000
# Status: ✅ Running (PID 56223, 56228)

# Redis - Docker Container
docker ps  # Check status
# Port: 6379
# Container: cooin-redis
# Status: ✅ HEALTHY
```

### Quick Start Commands (Mac)
```bash
# Terminal 1 - Frontend (if not running)
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-frontend
npx expo start --web --port 8083

# Terminal 2 - Backend (if not running)
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 3 - Redis (Docker)
cd /Users/mariajimenez/Desktop/cooin-platform
docker-compose up -d redis

# Check Redis status
docker ps
```

### Stop Services
```bash
# Stop Redis
docker-compose down

# Stop frontend/backend: Ctrl+C in their terminals
```

---

## 🐛 Known Issues (Mac)

### Active Issues
- ⚠️ **Frontend "Cannot connect to server"** - May need browser refresh or backend restart
  - Frontend is on port 8083
  - Backend is on port 8000
  - CORS configured for localhost:8083
  - Next: Restart backend to ensure Redis connection

### Resolved Issues
- ✅ **Docker Installation** - Was already installed, just needed to start
- ✅ **npm Dependencies** - Fixed by running `npm install`
- ✅ **Redis Setup** - Successfully running via Docker

---

## 📋 Mac-Specific Technical Notes

### Environment Setup
- **Python**: 3.12.1 (via venv in cooin-backend)
- **Node/npm**: Installed and working
- **Docker**: 25.0.3 (Docker Desktop)
- **Homebrew**: /usr/local/bin/brew
- **Architecture**: Intel (x86_64)

### File Paths
- Project: `/Users/mariajimenez/Desktop/cooin-platform`
- Frontend: `/Users/mariajimenez/Desktop/cooin-platform/cooin-frontend`
- Backend: `/Users/mariajimenez/Desktop/cooin-platform/cooin-backend`

### Package Versions (Mac)
- expo: 54.0.23
- @types/jest: 30.0.0 (warning: expects 29.5.14)
- jest: 30.2.0 (warning: expects ~29.7.0)
- Total npm packages: 1499

---

## 🔧 Future Enhancements (Mac-Specific)

### Development Environment
- [ ] Update Expo packages to recommended versions
- [ ] Configure VS Code settings for Mac
- [ ] Set up git aliases for Mac terminal

### Testing
- [ ] Run full test suite on Mac
- [ ] Test iOS simulator integration
- [ ] Verify cross-platform compatibility

---

## 📚 Key Commands Reference (Mac)

### Docker
```bash
# Start Docker Desktop
open -a Docker

# Check Docker status
docker ps

# Start Redis
docker-compose up -d redis

# Stop all containers
docker-compose down

# View Redis logs
docker logs cooin-redis

# Connect to Redis CLI
docker exec -it cooin-redis redis-cli
```

### Git (Mac)
```bash
# Pull latest changes from Windows
git pull origin main

# Commit Mac documentation
git add HISTORY_MAC.md TODO_MAC.md README_MAC.md
git commit -m "docs: Session X on Mac 🍎"
git push origin main
```

### Backend
```bash
# Activate venv
source venv/bin/activate

# Start backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Check backend health
curl http://localhost:8000/health
```

### Frontend
```bash
# Install dependencies
npm install

# Start web
npx expo start --web --port 8083

# Clear cache
npx expo start --web --port 8083 --clear
```

---

**Last Updated**: 2025-11-19 (Session 15)

**Quick Links**:
- [Mac History](./HISTORY_MAC.md)
- [Mac README](./README_MAC.md)
- [Mac Launch Guide](./HOW-TO-LAUNCH-WEB-APP_MAC.md)
- [Windows TODO](./TODO.md) (Read Only)
- [Windows History](./HISTORY.md) (Read Only)
