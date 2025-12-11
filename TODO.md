# Cooin Web App - TODO (Windows 💻)

**Purpose**: Track tasks, progress, and issues specific to Windows development environment.

---

## 🚀 Current Session (Session 15) - Pydantic V2 Migration & Security Complete ✅

### ✅ Completed This Session
- [x] **Pydantic V2 Migration** - Updated schema_extra to json_schema_extra
- [x] **Full App Testing** - Complete workflow tested (registration, login, profile, notifications)
- [x] **Security Audit Complete** - Comprehensive review (SECURITY-AUDIT.md)
- [x] **Production Security Guide** - Deployment guide created
- [x] **Environment-Aware Security** - Conditional security based on ENVIRONMENT setting
- [x] **Security Middleware Enabled** - All 7 middleware now active (development mode)
- [x] **Environment Switching Guide** - ENVIRONMENT-GUIDE.md created

### ✅ Completed Previous Sessions
- [x] **System Notifications** (Session 13) - Replaced user chat with system notification center
- [x] **Educational Content** (Session 13) - 8 lending tips + 4 safety tips integrated
- [x] **Responsive Navigation** (Session 12) - Desktop sidebar + mobile tabs
- [x] **i18n Implementation** (Sessions 11) - Dynamic translation system

### 📝 Pending Work - Production Deployment (When Ready)
- [ ] **Generate Production Secrets** - Create strong SECRET_KEY and passwords
- [ ] **Setup Production Database** - PostgreSQL with restricted permissions
- [ ] **Configure Redis Password** - Secure Redis with authentication
- [ ] **Obtain SSL Certificate** - Let's Encrypt or commercial CA
- [ ] **Setup Nginx/Reverse Proxy** - HTTPS termination and routing
- [ ] **Deploy to Production Server** - AWS, DigitalOcean, or similar

---

## 🌐 Local Development (Current Mode)

### Quick Start Commands
```cmd
# Terminal 1 - Backend
cd C:\Windows\System32\cooin-app\cooin-backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd C:\Windows\System32\cooin-app\cooin-frontend
npx expo start --web --port 8083 --clear

### Access Points
- Frontend: http://localhost:8083
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs

---

## 🌍 Public Sharing Setup (When Needed)

```cmd
# Terminal 3 - Backend Tunnel
cloudflared tunnel --url http://localhost:8000

# Terminal 4 - Frontend Tunnel
cloudflared tunnel --url http://localhost:8083

# Then update config.ts and .env with new tunnel URLs
```

---

## 🐛 Known Issues

### Active Issues
- ⚠️ **Project in System32** - Permission issues
  - Solution: Move to `C:\Users\USERNAME\Documents\cooin-app` or run `fix-permissions.bat` as admin

### Resolved Issues
- ✅ **Duplicate Email Registration Error** - Clear error message displayed
- ✅ **Python Path** - Works with simple `python` command
- ✅ **Web Scrolling** - Mouse wheel scrolling fixed

---

## 📋 Technical Improvements

### Python Environment
- [ ] Set up virtual environment (prevents PATH conflicts)
  ```cmd
  cd cooin-backend
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  ```

### Cloudflare
- [ ] Consider named tunnels for persistent URLs

---

## 🔧 Future Enhancements

### UX Improvements
- [ ] Add password strength indicator
- [ ] Add email verification flow
- [ ] Implement forgot password functionality
- [ ] Add profile picture upload

### Deployment
- [ ] Move project out of System32
- [ ] Set up CI/CD pipeline
- [ ] Payment integration
- [ ] Admin dashboard

---

## 📚 Key Commands Reference

### Backend
```cmd
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```cmd
npx expo start --web --port 8083 --clear
```

### Cloudflare Tunnel
```cmd
cloudflared tunnel --url http://localhost:8000   # Backend
cloudflared tunnel --url http://localhost:8083   # Frontend
```

---

## 🐳 Docker Installation (For Reference)

### Step 1: Enable WSL 2 (PowerShell as Administrator)
```powershell
wsl --install
# Then restart computer
```

### Step 2: After Restart - Set WSL 2 as Default
```powershell
wsl --set-default-version 2
```

### Step 3: Install Docker Desktop
1. Download from: https://www.docker.com/products/docker-desktop/
2. Run installer, check "Use WSL 2 instead of Hyper-V"
3. Restart computer

### Step 4: Setup Redis
```cmd
cd C:\Windows\System32\cooin-app
docker-compose up -d redis
docker ps  # Verify running
```

---

**Last Updated**: 2025-11-19 (Session 15)
**Quick Links**: [HISTORY.md](./HISTORY.md) | [README.md](./README.md) | [HOW-TO-LAUNCH-WEB-APP.md](./HOW-TO-LAUNCH-WEB-APP.md)
