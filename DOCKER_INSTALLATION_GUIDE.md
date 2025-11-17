# Docker Desktop Installation Guide for Windows

Step-by-step guide to install Docker Desktop and set up Redis for Cooin.

---

## 🎯 Why Docker Desktop?

Docker Desktop provides:
- Easy Redis installation (no manual configuration)
- Isolated environment (no conflicts with other software)
- Simple start/stop controls via GUI
- Perfect for development and testing
- Easy transition to production cloud services

---

## 📋 Prerequisites

Before installing Docker Desktop, verify your system meets these requirements:

### 1. Windows Version
- **Windows 10 64-bit**: Pro, Enterprise, or Education (Build 19041 or higher)
- **Windows 11 64-bit**: Any edition

**Check Your Windows Version:**
```cmd
# Press Win + R, type: winver
# Or run in Command Prompt:
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
```

### 2. Hardware Requirements
- **64-bit processor** with Second Level Address Translation (SLAT)
- **4GB RAM minimum** (8GB recommended)
- **Virtualization enabled** in BIOS

**Check if Virtualization is Enabled:**
```cmd
# Press Win + R, type: taskmgr
# Go to Performance tab → CPU
# Look for "Virtualization: Enabled"
```

If Virtualization is **Disabled**, you'll need to enable it in BIOS:
1. Restart your PC
2. Enter BIOS (usually F2, F10, or Del during boot)
3. Find "Virtualization Technology" or "Intel VT-x" or "AMD-V"
4. Enable it
5. Save and exit

---

## 📥 Step 1: Download Docker Desktop

1. **Open your browser** and go to:
   ```
   https://www.docker.com/products/docker-desktop/
   ```

2. **Click "Download for Windows"**
   - File: `Docker Desktop Installer.exe` (~500MB)
   - Save it to your Downloads folder

---

## 🔧 Step 2: Install Docker Desktop

### Installation Steps:

1. **Locate the downloaded file**
   ```
   C:\Users\Usuario\Downloads\Docker Desktop Installer.exe
   ```

2. **Right-click** the installer → **Run as Administrator**

3. **Installation Wizard:**
   - ✅ **Check**: "Use WSL 2 instead of Hyper-V" (recommended)
   - ✅ **Check**: "Add shortcut to desktop"
   - Click **"OK"**

4. **Wait for installation** (takes 3-5 minutes)

5. **Restart your computer** when prompted

---

## 🚀 Step 3: Start Docker Desktop

1. **After restart**, Docker Desktop should auto-start
   - Look for the Docker icon in system tray (bottom-right)
   - Icon will be **blue** when running

2. **If not started**, launch manually:
   - Press **Win** key
   - Type "Docker Desktop"
   - Click to open

3. **First Launch Setup:**
   - Accept the Service Agreement
   - Optional: Sign in (you can skip this)
   - Optional: Complete tutorial (you can skip)

4. **Wait for Docker Engine to start** (~1 minute)
   - System tray icon will turn from orange/gray to **blue**
   - Status: "Docker Desktop is running"

---

## ✅ Step 4: Verify Installation

Open **Command Prompt** or **PowerShell** and run:

```cmd
# Check Docker version
docker --version
# Expected output: Docker version 24.x.x, build xxxxx

# Check Docker Compose version
docker compose version
# Expected output: Docker Compose version v2.x.x

# Test Docker is working
docker run hello-world
# Expected: Downloads and runs a test container successfully
```

If all commands work, **Docker is successfully installed!** 🎉

---

## 🐳 Step 5: Start Redis with Docker

Now that Docker is installed, let's start Redis:

### Option A: Using Docker Compose (Recommended)

1. **Open Command Prompt** or **PowerShell**

2. **Navigate to Cooin directory:**
   ```cmd
   cd C:\Windows\System32\cooin-app
   ```

3. **Start Redis:**
   ```cmd
   docker compose up -d redis
   ```

4. **Verify Redis is running:**
   ```cmd
   docker ps
   ```
   You should see `cooin-redis` container with status "Up"

5. **Test Redis connection:**
   ```cmd
   docker exec -it cooin-redis redis-cli ping
   ```
   Expected output: `PONG`

### Option B: Using Docker Desktop GUI

1. **Open Docker Desktop**
2. **Go to "Containers" tab** (left sidebar)
3. **Click "▶ Start"** button
4. **Redis should start** and show status "Running"

---

## 🎮 Step 6: Using Redis Commander (Optional GUI)

Redis Commander provides a web interface to manage Redis:

1. **Start Redis Commander:**
   ```cmd
   cd C:\Windows\System32\cooin-app
   docker compose --profile dev up -d
   ```

2. **Open in browser:**
   ```
   http://localhost:8081
   ```

3. **You can now:**
   - View all keys
   - See values
   - Monitor memory usage
   - Execute commands via GUI

---

## 🔄 Daily Usage Commands

### Starting Redis
```cmd
# From cooin-app directory
docker compose up -d redis
```

### Stopping Redis
```cmd
docker compose down redis
```

### Restarting Redis
```cmd
docker compose restart redis
```

### View Redis Logs
```cmd
docker logs -f cooin-redis
```

### Access Redis CLI
```cmd
docker exec -it cooin-redis redis-cli
```

### Stop All Containers
```cmd
docker compose down
```

---

## 📊 Step 7: Verify Backend Connects to Redis

1. **Make sure Redis is running:**
   ```cmd
   docker ps | findstr redis
   ```

2. **Start your backend:**
   ```cmd
   cd C:\Windows\System32\cooin-app\cooin-backend
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Check backend logs:**
   Look for:
   ```
   INFO - Connected to Redis cache server (attempt 1/3)
   ```

   Instead of the old warning:
   ```
   WARNING - Failed to connect to Redis. Using in-memory cache fallback.
   ```

4. **Test the cache:**
   - Open your app in browser: http://localhost:8083
   - Navigate through the app
   - Redis is now caching data in the background!

---

## 🐛 Troubleshooting

### Issue 1: "Docker Desktop requires Windows 10 Pro/Enterprise"

**Solution for Windows 10 Home users:**
1. Upgrade to Windows 10 Pro (or)
2. Use WSL 2 with Docker Engine (more complex)
3. Alternative: Use Memurai (Redis for Windows) - See REDIS_SETUP.md

### Issue 2: "Virtualization is not enabled"

**Solution:**
1. Restart PC and enter BIOS
2. Enable Intel VT-x or AMD-V
3. Save and restart

**Check in Windows:**
```cmd
systeminfo | findstr /C:"Hyper-V Requirements"
```

### Issue 3: "Docker Desktop is slow to start"

**Solution:**
- Give it 2-3 minutes on first start
- Check if antivirus is blocking
- Disable unnecessary Docker extensions in Settings

### Issue 4: "Cannot connect to Redis from backend"

**Solution:**
```cmd
# Check Redis is running
docker ps | findstr redis

# Check Redis logs
docker logs cooin-redis

# Test Redis directly
docker exec -it cooin-redis redis-cli ping
# Should return: PONG

# Check backend .env file
# Should have: REDIS_URL=redis://localhost:6379/0
```

### Issue 5: "Port 6379 is already in use"

**Solution:**
```cmd
# Check what's using port 6379
netstat -ano | findstr :6379

# Stop any existing Redis
docker compose down

# Or kill the process using the port
taskkill /F /PID <PID_NUMBER>
```

---

## 🎯 Success Checklist

After completing this guide, you should have:

- [x] Docker Desktop installed and running
- [x] Redis container running via docker-compose
- [x] Backend connecting to Redis successfully
- [x] No more "in-memory cache fallback" warnings
- [x] (Optional) Redis Commander accessible at http://localhost:8081

---

## 📚 Next Steps

1. **Restart your backend** to connect to Redis
2. **Test the application** - cache is now active
3. **Monitor Redis** with Redis Commander
4. **Read REDIS_SETUP.md** for production configuration

---

## 🔗 Useful Resources

- Docker Desktop Documentation: https://docs.docker.com/desktop/windows/
- Docker Compose Documentation: https://docs.docker.com/compose/
- Redis Documentation: https://redis.io/documentation
- WSL 2 Setup: https://docs.microsoft.com/en-us/windows/wsl/install

---

## 💡 Tips

1. **Docker Desktop Auto-Start**
   - Settings → General → "Start Docker Desktop when you log in"

2. **Resource Management**
   - Settings → Resources
   - Adjust CPU, Memory, Disk based on your system

3. **Keep Docker Updated**
   - Docker Desktop → Check for updates regularly

4. **Backup Redis Data**
   - Data is stored in Docker volume: `cooin-app_redis-data`
   - Automatic backups via RDB and AOF (configured in redis.conf)

---

**Installation Time**: ~15 minutes
**Difficulty**: Beginner-friendly
**Last Updated**: 2025-11-17 (Session 14)

🎉 **You're all set! Redis is now ready for production-scale caching!**
