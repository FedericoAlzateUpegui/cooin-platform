# Docker Setup Guide for Cooin App

**Session**: 14 (2025-11-17)
**Purpose**: Install Docker Desktop on Windows and configure Redis container

---

## Prerequisites

- Windows 10 64-bit (Build 19041+) or Windows 11
- Administrator access
- ~2GB free disk space for Docker Desktop

---

## Step-by-Step Installation

### Step 1: Check Windows Version
```cmd
winver
```
- Press `Win + R`, type `winver`, press Enter
- Verify you have Build 19041 or higher

### Step 2: Enable WSL 2

**Open PowerShell as Administrator** (Right-click Start → Windows PowerShell (Admin))

```powershell
wsl --install
```

**Expected output:**
```
Installing: Windows Subsystem for Linux
Installing: Virtual Machine Platform
...
The requested operation is successful. Changes will not be effective until the system is rebooted.
```

**Then restart your computer** ⚠️

### Step 3: After First Restart - Configure WSL 2

**Open PowerShell as Administrator again**

```powershell
wsl --set-default-version 2
```

**Verify WSL 2 is installed:**
```powershell
wsl --list --verbose
```

### Step 4: Download Docker Desktop

1. Open browser: https://www.docker.com/products/docker-desktop/
2. Click **"Download for Windows"**
3. Save `Docker Desktop Installer.exe`

### Step 5: Install Docker Desktop

1. **Run** `Docker Desktop Installer.exe` as Administrator
2. When prompted, **CHECK** ✅ "Use WSL 2 instead of Hyper-V"
3. Click **"OK"** and wait for installation (5-10 minutes)
4. Click **"Close and restart"** when finished

**Your computer will restart again** ⚠️

### Step 6: After Second Restart - Start Docker

1. Docker Desktop should auto-start (look for whale icon in system tray)
2. If not, search "Docker Desktop" in Start menu and launch it
3. Accept the Service Agreement
4. Skip the tutorial (optional)

### Step 7: Verify Installation

**Open Command Prompt or PowerShell** (no admin needed)

```cmd
docker --version
```
**Expected:** `Docker version 24.x.x, build xxxxxx`

```cmd
docker-compose --version
```
**Expected:** `Docker Compose version v2.x.x`

```cmd
docker run hello-world
```
**Expected:**
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

---

## Next Steps: Setup Redis for Cooin App

### Step 1: Create docker-compose.yml

Navigate to project root:
```cmd
cd C:\Windows\System32\cooin-app
```

The `docker-compose.yml` file should already be created with this content:
```yaml
version: '3.8'
services:
  redis:
    image: redis:7-alpine
    container_name: cooin-redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes
    restart: unless-stopped

volumes:
  redis-data:
```

### Step 2: Start Redis Container

```cmd
docker-compose up -d redis
```

**Expected output:**
```
[+] Running 2/2
 ✔ Network cooin-app_default  Created
 ✔ Container cooin-redis      Started
```

### Step 3: Verify Redis is Running

```cmd
docker ps
```

**Expected output:**
```
CONTAINER ID   IMAGE           COMMAND                  STATUS         PORTS                    NAMES
xxxxxxxxxx     redis:7-alpine  "docker-entrypoint.s…"   Up 5 seconds   0.0.0.0:6379->6379/tcp   cooin-redis
```

### Step 4: Test Redis Connection

```cmd
docker exec -it cooin-redis redis-cli ping
```

**Expected:** `PONG`

---

## Common Docker Commands

```cmd
# Start Redis
docker-compose up -d redis

# Stop Redis
docker-compose stop redis

# View logs
docker logs cooin-redis

# Restart Redis
docker restart cooin-redis

# Remove Redis container (data preserved in volume)
docker-compose down

# Remove Redis AND delete all data
docker-compose down -v
```

---

## Troubleshooting

### Docker Desktop won't start
- Ensure WSL 2 is installed: `wsl --list --verbose`
- Restart Docker Desktop service: Right-click Docker icon → Restart

### "WSL 2 installation is incomplete"
```powershell
# Run as Administrator
wsl --update
wsl --set-default-version 2
```

### Port 6379 already in use
```cmd
# Check what's using port 6379
netstat -ano | findstr :6379

# Stop the process or change Redis port in docker-compose.yml
```

### Cannot connect to Docker daemon
- Ensure Docker Desktop is running (check system tray for whale icon)
- Restart Docker Desktop

---

## Updated Launch Commands (After Redis Setup)

### Terminal 1 - Redis (Docker)
```cmd
cd C:\Windows\System32\cooin-app
docker-compose up -d redis
```

### Terminal 2 - Backend
```cmd
cd C:\Windows\System32\cooin-app\cooin-backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 3 - Frontend
```cmd
cd C:\Windows\System32\cooin-app\cooin-frontend
npx expo start --web --port 8083 --clear
```

---

## Files Modified for Redis Integration

After Docker setup, we'll update:
- `cooin-backend/.env` - Add `REDIS_URL=redis://localhost:6379`
- `cooin-backend/requirements.txt` - Add `redis==5.0.1`
- `cooin-backend/app/core/config.py` - Add Redis config settings
- `README.md` - Update prerequisites and setup
- `HOW-TO-LAUNCH-WEB-APP.md` - Add Docker startup step

---

**Status**: 🔄 In Progress
**Next Session**: Continue with package updates and Redis backend integration
**Questions?**: Check TODO.md or HISTORY.md for context
