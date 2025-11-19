# How to Launch Cooin Web App on Mac 🍎

**Purpose**: Step-by-step guide to launch all services on Mac.

**Note**: This file is ONLY edited by Claude on Mac. Windows can READ for context.

---

## 📋 Prerequisites

Before launching, ensure you have:

- ✅ Docker Desktop installed and running
- ✅ Python 3.12+ (with venv in cooin-backend)
- ✅ Node.js & npm installed
- ✅ PostgreSQL installed and running (optional, for database features)
- ✅ Project cloned at `/Users/mariajimenez/Desktop/cooin-platform`

---

## 🚀 Quick Launch (3 Simple Steps)

### Step 1: Start Docker & Redis

```bash
# Open Docker Desktop (if not running)
open -a Docker

# Wait for Docker to start (look for whale icon in menu bar)
# Then start Redis container
cd /Users/mariajimenez/Desktop/cooin-platform
docker-compose up -d redis
```

**Wait for:**
- ✅ `Container cooin-redis  Started`
- ✅ `docker ps` shows status as `healthy`

**Verify:**
```bash
docker ps
# Should show: cooin-redis with status "healthy"
```

---

### Step 2: Start Backend (Terminal 1)

```bash
# Open new terminal
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-backend

# Activate virtual environment
source venv/bin/activate

# Start FastAPI server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Wait for:**
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Access at:**
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs
- Health Check: http://localhost:8000/health

**Verify in browser:**
```
http://localhost:8000/health
# Should return: {"status":"healthy","timestamp":...}
```

---

### Step 3: Start Frontend (Terminal 2)

```bash
# Open another new terminal
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-frontend

# Start Metro bundler for web
npx expo start --web --port 8083
```

**Wait for:**
```
Web Bundled [time]ms index.ts (841 modules)
Logs will appear in the browser console
```

**Access at:**
- Web App: http://localhost:8083

**Verify:**
- Browser should automatically open
- Or manually go to: http://localhost:8083

---

## 🎯 You're Done!

All services are now running:

- ✅ **Redis**: localhost:6379 (Docker container)
- ✅ **Backend**: http://localhost:8000
- ✅ **Frontend**: http://localhost:8083
- ✅ **API Docs**: http://localhost:8000/api/v1/docs

---

## 🛑 Stopping Services

### Stop Frontend
```bash
# In frontend terminal: Press Ctrl + C
```

### Stop Backend
```bash
# In backend terminal: Press Ctrl + C
```

### Stop Redis & Docker
```bash
cd /Users/mariajimenez/Desktop/cooin-platform
docker-compose down

# Or stop Docker Desktop completely
# Click whale icon → Quit Docker Desktop
```

---

## 🔧 Troubleshooting (Mac)

### Issue: "Docker daemon not running"

**Solution:**
```bash
# Start Docker Desktop
open -a Docker

# Wait 10-20 seconds for Docker to fully start
# Look for whale icon in menu bar

# Then try again
docker ps
```

---

### Issue: "Port 8000 already in use"

**Solution:**
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process (use PID from above)
kill -9 <PID>

# Or kill all Python processes on port 8000
lsof -ti :8000 | xargs kill -9

# Then start backend again
```

---

### Issue: "Port 8083 already in use"

**Solution:**
```bash
# Find what's using port 8083
lsof -i :8083

# Kill the process
lsof -ti :8083 | xargs kill -9

# Or use different port
npx expo start --web --port 8084
```

---

### Issue: "Cannot connect to server" in frontend

**Possible Causes:**
1. Backend not running
2. Wrong API URL in config
3. CORS issue

**Solution:**
```bash
# 1. Check backend is running
curl http://localhost:8000/health

# 2. Check frontend config
cat cooin-frontend/src/constants/config.ts
# BASE_URL should be: "http://localhost:8000/api/v1"

# 3. Check backend CORS settings
cat cooin-backend/.env | grep CORS
# Should include: "http://localhost:8083"

# 4. Restart both services
# Stop backend (Ctrl+C) and restart
# Stop frontend (Ctrl+C) and restart with cache clear
npx expo start --web --port 8083 --clear
```

---

### Issue: "Module not found" in frontend

**Solution:**
```bash
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-frontend

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Metro bundler cache
npx expo start --web --port 8083 --clear
```

---

### Issue: Redis container won't start

**Solution:**
```bash
# Stop all containers
docker-compose down

# Remove Redis container and volume
docker rm -f cooin-redis
docker volume rm cooin-platform_redis-data

# Restart Redis
docker-compose up -d redis

# Check logs
docker logs cooin-redis
```

---

## 🔍 Verification Checklist

Use this checklist to verify everything is working:

```bash
# ✅ Docker is running
docker ps
# Should show cooin-redis with status "healthy"

# ✅ Redis is responding
docker exec -it cooin-redis redis-cli PING
# Should return: PONG

# ✅ Backend health check
curl http://localhost:8000/health
# Should return: {"status":"healthy",...}

# ✅ Backend API health
curl http://localhost:8000/api/v1/health
# Should return: {"status":"healthy","version":"v1",...}

# ✅ Frontend is accessible
curl http://localhost:8083
# Should return HTML

# ✅ API docs accessible
# Open browser: http://localhost:8000/api/v1/docs
# Should show Swagger UI
```

---

## 📊 Service Status Check

### Check All Services at Once
```bash
#!/bin/bash
echo "🔍 Checking Cooin Services on Mac..."
echo ""

# Check Docker
echo "1. Docker:"
if docker ps &> /dev/null; then
    echo "   ✅ Docker is running"
else
    echo "   ❌ Docker is not running"
fi

# Check Redis
echo "2. Redis:"
if docker ps | grep -q cooin-redis; then
    echo "   ✅ Redis container is running"
else
    echo "   ❌ Redis container is not running"
fi

# Check Backend
echo "3. Backend (port 8000):"
if lsof -i :8000 &> /dev/null; then
    echo "   ✅ Backend is running"
else
    echo "   ❌ Backend is not running"
fi

# Check Frontend
echo "4. Frontend (port 8083):"
if lsof -i :8083 &> /dev/null; then
    echo "   ✅ Frontend is running"
else
    echo "   ❌ Frontend is not running"
fi

echo ""
echo "📝 Open terminals: $(ps aux | grep -c [t]erminal)"
```

Save this as `check-services-mac.sh` and run:
```bash
chmod +x check-services-mac.sh
./check-services-mac.sh
```

---

## ⚡ Advanced: Using Scripts

### Create Startup Script

Create `start-all-mac.sh`:
```bash
#!/bin/bash
echo "🚀 Starting all Cooin services on Mac..."

# Start Docker if not running
if ! docker ps &> /dev/null; then
    echo "Starting Docker Desktop..."
    open -a Docker
    sleep 10
fi

# Start Redis
echo "Starting Redis..."
cd /Users/mariajimenez/Desktop/cooin-platform
docker-compose up -d redis

# Start backend in background
echo "Starting Backend..."
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &

# Wait for backend
sleep 5

# Start frontend
echo "Starting Frontend..."
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-frontend
npx expo start --web --port 8083

echo "✅ All services started!"
```

Make it executable:
```bash
chmod +x start-all-mac.sh
./start-all-mac.sh
```

---

## 🌐 Access Points Summary

Once all services are running:

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend Web App | http://localhost:8083 | Main application UI |
| Backend API | http://localhost:8000 | REST API server |
| API Documentation | http://localhost:8000/api/v1/docs | Swagger UI |
| Alternative API Docs | http://localhost:8000/redoc | ReDoc UI |
| Health Check | http://localhost:8000/health | Server health status |
| API v1 Health | http://localhost:8000/api/v1/health | API health status |
| Redis | localhost:6379 | Cache server (internal) |

---

## 📚 Additional Resources

**Mac-Specific Documentation:**
- [Mac README](./README_MAC.md) - Mac setup and config
- [Mac TODO](./TODO_MAC.md) - Current tasks
- [Mac History](./HISTORY_MAC.md) - Session history

**Windows Documentation** (Read Only):
- [Windows Launch Guide](./HOW-TO-LAUNCH-WEB-APP.md)
- [Windows TODO](./TODO.md)

**General Documentation:**
- [DP.md](./DP.md) - Documentation process
- [TECH_STACK.md](./TECH_STACK.md) - Technology details

---

**Last Updated**: 2025-11-19 (Session 15)
**Platform**: macOS (Intel)
**Maintained By**: Claude on Mac 🍎
