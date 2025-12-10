# How to Launch Cooin Web App on Mac 🍎

**Purpose**: Step-by-step guide to launch all services on Mac.

---

## 📋 Prerequisites

- ✅ Docker Desktop installed
- ✅ Python 3.12+ (with venv in cooin-backend)
- ✅ Node.js & npm installed
- ✅ Project at `/Users/mariajimenez/Desktop/cooin-platform`

---

## 🚀 Quick Launch (3 Steps)

### Step 1: Start Docker & Redis

```bash
# Open Docker Desktop
open -a Docker

# Wait for Docker to start (whale icon in menu bar)
# Then start Redis
cd /Users/mariajimenez/Desktop/cooin-platform
docker-compose up -d redis
```

**Verify:**
```bash
docker ps
# Should show: cooin-redis with status "healthy"
```

---

### Step 2: Start Backend (Terminal 1)

```bash
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Wait for:**
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Access:**
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs
- Health Check: http://localhost:8000/health

---

### Step 3: Start Frontend (Terminal 2) - Fast Mode ⚡

```bash
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-frontend
npm run web:fast
```

**Alternative modes:**
```bash
# Standard mode
npm run web

# Clean cache first (if issues)
npm run clean && npm run web:fast
```

**Wait for:**
```
Web Bundled [time]ms index.ts (841 modules)
```

**Access:**
- Web App: http://localhost:8083

**Note**: `web:fast` reduces startup time by ~50% (30-45s vs 60-90s)
See [FRONTEND-PERFORMANCE.md](./FRONTEND-PERFORMANCE.md) for details

---

## 🎯 All Services Running!

- ✅ **Redis**: localhost:6379
- ✅ **Backend**: http://localhost:8000
- ✅ **Frontend**: http://localhost:8083
- ✅ **API Docs**: http://localhost:8000/api/v1/docs

---

## 🛑 Stopping Services

```bash
# Frontend/Backend: Ctrl + C in terminals

# Redis & Docker
cd /Users/mariajimenez/Desktop/cooin-platform
docker-compose down
```

---

## 🔧 Troubleshooting (Mac)

### Issue: "Docker daemon not running"

```bash
open -a Docker
# Wait 10-20 seconds for whale icon in menu bar
docker ps
```

---

### Issue: "Port 8000 already in use"

```bash
lsof -ti :8000 | xargs kill -9
# Then restart backend
```

---

### Issue: "Port 8083 already in use"

```bash
lsof -ti :8083 | xargs kill -9
# Then restart frontend
```

---

### Issue: "Cannot connect to server" in frontend

```bash
# 1. Check backend is running
curl http://localhost:8000/health

# 2. Check frontend config
cat cooin-frontend/src/constants/config.ts
# BASE_URL should be: "http://localhost:8000/api/v1"

# 3. Restart both services
# Stop backend (Ctrl+C) and restart
# Stop frontend (Ctrl+C) and restart with cache clear:
npx expo start --web --port 8083 --clear
```

---

### Issue: "Module not found" in frontend

```bash
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
npx expo start --web --port 8083 --clear
```

---

### Issue: Redis container won't start

```bash
docker-compose down
docker rm -f cooin-redis
docker volume rm cooin-platform_redis-data
docker-compose up -d redis
docker logs cooin-redis
```

---

## 🔍 Verification Checklist

```bash
# ✅ Docker running
docker ps

# ✅ Redis responding
docker exec -it cooin-redis redis-cli PING
# Should return: PONG

# ✅ Backend health
curl http://localhost:8000/health

# ✅ Frontend accessible
curl http://localhost:8083
```

---

## 📚 Additional Resources

- [Mac README](./README_MAC.md) - Mac setup & config
- [Mac TODO](./TODO_MAC.md) - Current tasks
- [Mac History](./HISTORY_MAC.md) - Session history
- [DP.md](./DP.md) - Documentation process

---

**Last Updated**: 2025-12-06 (Session 17)
**Platform**: macOS (Intel)
**Maintained By**: Claude on Mac 🍎
