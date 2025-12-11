# Quick Start Scripts - Cooin Platform

## 🎯 One-Command Startup

### Start Everything (Recommended)

```cmd
start-all.bat
```

This opens 3 terminal windows:
1. **Backend Server** (FastAPI on port 8000)
2. **Frontend Web App** (React Native Web on port 8083)
3. **Cloudflare Tunnel** (optional - for external access)

**What it does:**
- ✅ Checks if Docker/Redis is running
- ✅ Starts backend with virtual environment
- ✅ Starts frontend with Expo
- ✅ Asks if you want external tunnel
- ✅ Opens all in separate windows

---

## 🔧 Individual Scripts

### Backend Only
```cmd
cd cooin-backend
start-backend.bat
```

**What it does:**
- Activates Python virtual environment
- Starts FastAPI server with auto-reload
- Available at: http://localhost:8000

### Frontend Only
```cmd
cd cooin-frontend
start-frontend.bat
```

**What it does:**
- Checks for node_modules (installs if missing)
- Starts Expo web server with clear cache
- Available at: http://localhost:8083

### Backend Tunnel (Quick)
```cmd
start-tunnel-backend.bat
```

**What it does:**
- Creates temporary Cloudflare tunnel for backend
- Provides HTTPS URL (changes each restart)
- Shows URL to update in .env files

### Frontend Tunnel (Quick)
```cmd
start-tunnel-frontend.bat
```

**What it does:**
- Creates temporary Cloudflare tunnel for frontend
- Provides HTTPS URL to share with partners
- URL changes each restart

---

## 🏥 Health Check

```cmd
check-services.bat
```

**Checks:**
- ✅ Docker running
- ✅ Redis container status
- ✅ Backend server (port 8000)
- ✅ Frontend server (port 8083)
- ✅ Python virtual environment
- ✅ Cloudflared installation

**Use this to troubleshoot!**

---

## 📋 Scripts Summary

| Script | Location | Purpose | Opens Window |
|--------|----------|---------|--------------|
| **start-all.bat** | Root | Start everything | 3 windows |
| **start-backend.bat** | cooin-backend/ | Backend only | 1 window |
| **start-frontend.bat** | cooin-frontend/ | Frontend only | 1 window |
| **start-tunnel-backend.bat** | Root | Backend tunnel | 1 window |
| **start-tunnel-frontend.bat** | Root | Frontend tunnel | 1 window |
| **check-services.bat** | Root | Health check | Same window |

---

## 🚀 Typical Development Workflow

### Local Development (No External Access)

```cmd
# Just run this:
start-all.bat
# Choose option 3 (skip tunnel)
```

**URLs:**
- Backend: http://localhost:8000
- Frontend: http://localhost:8083
- API Docs: http://localhost:8000/api/v1/docs

---

### Development with Partner Testing (External Access)

```cmd
# Run this:
start-all.bat
# Choose option 1 (quick tunnel)

# Copy the tunnel URL shown in the "Cooin Tunnel - Backend" window
# Update cooin-frontend/.env with the new URL
# Restart frontend (Ctrl+C in frontend window, then r to reload)
```

**Share the frontend URL** (http://localhost:8083 or use tunnel for frontend too)

---

### Named Tunnel (Persistent URL - Advanced)

See **[SETUP-NAMED-TUNNEL.md](./SETUP-NAMED-TUNNEL.md)** for one-time setup.

After setup:
```cmd
start-all.bat
# Choose option 2 (named tunnel)
```

**Benefits:**
- ✅ Same URL every time
- ✅ No .env updates needed
- ✅ Professional setup

---

## 🛠️ Prerequisites

### Required
- ✅ Python 3.10+ (for backend)
- ✅ Node.js 18+ (for frontend)
- ✅ Docker Desktop (for Redis)

### Optional
- Cloudflared (for tunnels): `winget install cloudflare.cloudflared`

---

## 📝 First Time Setup

```cmd
# 1. Start Docker Desktop manually

# 2. Start Redis
docker-compose up -d redis

# 3. Run the all-in-one script
start-all.bat
```

The scripts will:
- ✅ Use the virtual environment (already created)
- ✅ Check for node_modules (install if needed)
- ✅ Start all services

---

## ❓ Troubleshooting

### "Virtual environment not found"
```cmd
cd cooin-backend
python -m venv venv
venv\Scripts\pip.exe install -r requirements.txt
```

### "Docker is not running"
1. Open Docker Desktop
2. Wait for it to start
3. Run: `docker-compose up -d redis`

### "Backend not responding"
```cmd
# Check if port 8000 is in use
netstat -ano | findstr :8000

# If something is using it, kill the process or use different port
```

### "Frontend won't start"
```cmd
cd cooin-frontend
rm -rf node_modules
npm install
start-frontend.bat
```

### "Cloudflared not found"
```cmd
# Install cloudflared
winget install cloudflare.cloudflared

# Or download from:
# https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
```

---

## 🎓 Tips

1. **Keep windows organized**: Each service runs in its own window for easy monitoring
2. **Check logs**: Look at each terminal window for errors
3. **Stop services**: Press Ctrl+C in each window or close the window
4. **Restart after .env changes**: Backend auto-reloads, but frontend needs manual restart (r key)
5. **Use check-services.bat**: Run this before starting if something isn't working

---

## 🔄 Quick Reference Commands

```cmd
# Start everything
start-all.bat

# Health check
check-services.bat

# Individual services
cd cooin-backend && start-backend.bat
cd cooin-frontend && start-frontend.bat

# Tunnels
start-tunnel-backend.bat
start-tunnel-frontend.bat

# Docker Redis
docker-compose up -d redis
docker-compose down
docker ps
```

---

**Created:** 2025-11-21 (Session 17)
**Purpose:** Simplify development workflow with automated scripts
**Next:** See [SETUP-NAMED-TUNNEL.md](./SETUP-NAMED-TUNNEL.md) for persistent URLs
