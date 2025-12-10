# Cooin Platform - Mac Setup Guide 🍎

**Purpose**: Mac-specific setup instructions and configuration.

---

## 🖥️ Mac Environment

- **Machine**: MacBook Pro (Intel x86_64)
- **OS**: macOS (Darwin 24.6.0)
- **User**: mariajimenez
- **Project Path**: `/Users/mariajimenez/Desktop/cooin-platform/`

---

## 📁 Project Structure

```
/Users/mariajimenez/Desktop/cooin-platform/
├── cooin-backend/          # FastAPI backend
├── cooin-frontend/         # React Native web/mobile
├── cooin-ios/             # Native iOS app
└── Documentation files
```

---

## 🚀 Quick Start (Mac)

### Prerequisites ✅
- Python 3.12.1
- Node.js & npm
- Docker Desktop 25.0.3
- Homebrew
- Git
- PostgreSQL

### Running the App (3 Steps)

**1. Start Docker & Redis**
```bash
open -a Docker
cd /Users/mariajimenez/Desktop/cooin-platform
docker-compose up -d redis
docker ps  # Verify status
```

**2. Start Backend**
```bash
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
→ Backend at: http://localhost:8000
→ API Docs: http://localhost:8000/api/v1/docs

**3. Start Frontend (Fast Mode)**
```bash
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-frontend
npm install  # First time only
npm run web:fast  # ~50% faster startup
```
→ Frontend at: http://localhost:8083
→ See [FRONTEND-PERFORMANCE.md](./FRONTEND-PERFORMANCE.md) for optimization details

---

## 🔧 Mac Configuration

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

### PostgreSQL Setup
```bash
brew install postgresql@14
brew services start postgresql@14
createdb cooin_db
cd cooin-backend
alembic upgrade head
```

---

## 🐳 Docker Commands (Mac)

```bash
# Start Docker Desktop
open -a Docker

# Redis
docker-compose up -d redis       # Start
docker-compose down              # Stop
docker logs cooin-redis          # View logs
docker exec -it cooin-redis redis-cli  # Connect

# Troubleshooting
docker-compose down
docker system prune -a
docker-compose up -d redis
```

---

## 🔍 Debugging (Mac)

### Check Running Services
```bash
lsof -i :8000  # Backend
lsof -i :8083  # Frontend
lsof -i :6379  # Redis

# Kill process on port
lsof -ti :8000 | xargs kill -9
```

### Test API Endpoints
```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/health
```

---

## 🌐 Git Workflow (Mac)

### Before Starting Work
```bash
git pull origin main
git status
```

### After Finishing Work
```bash
git add HISTORY_MAC.md TODO_MAC.md README_MAC.md HOW-TO-LAUNCH-WEB-APP_MAC.md
git commit -m "docs: Session X on Mac 🍎 - [description]"
git push origin main
```

### Important
- ❌ Don't edit: `HISTORY.md`, `TODO.md`, `README.md` (Windows only)
- ✅ Edit: `HISTORY_MAC.md`, `TODO_MAC.md`, `README_MAC.md` (Mac only)

---

## 🛠️ Terminal Shortcuts (Mac)

```bash
# Useful aliases (add to ~/.zshrc or ~/.bash_profile)
alias cooin='cd /Users/mariajimenez/Desktop/cooin-platform'
alias backend='cd /Users/mariajimenez/Desktop/cooin-platform/cooin-backend && source venv/bin/activate'
alias frontend='cd /Users/mariajimenez/Desktop/cooin-platform/cooin-frontend'
```

---

## 📊 Current Status

- ✅ Docker Desktop: Running
- ✅ Redis: HEALTHY (docker container)
- ✅ Backend: Running on port 8000
- ✅ Frontend: Running on port 8083
- ✅ Installed: 1499 npm packages, Python packages in venv

---

## 🔗 Quick Links

**Mac Documentation**:
- [Mac History](./HISTORY_MAC.md) - Session history
- [Mac TODO](./TODO_MAC.md) - Tasks and status
- [Mac Launch Guide](./HOW-TO-LAUNCH-WEB-APP_MAC.md) - Launch instructions

**Windows Documentation** (Read Only):
- [Windows History](./HISTORY.md)
- [Windows TODO](./TODO.md)
- [Windows README](./README.md)

**Shared Documentation**:
- [DP.md](./DP.md) - Documentation process guide
- [TECH_STACK.md](./TECH_STACK.md) - Technology stack

---

**Last Updated**: 2025-12-06 (Session 18)
**Maintained By**: Claude on Mac 🍎
