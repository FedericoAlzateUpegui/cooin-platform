# Cooin Web App - TODO (Mac 🍎)

**Purpose**: Track tasks, progress, and issues specific to Mac development environment.

---

## 🚀 Current Session (Session 19) - Backend Troubleshooting & System Verification ✅

### ✅ Completed This Session
- [x] **Backend Startup Issues Resolved**
  - Fixed Docker not running issue (started Docker Desktop with `open -a Docker`)
  - Fixed port 8000 conflict (killed old Python processes: PIDs 2323, 4541)
  - Backend now running successfully with all middleware enabled
  - Redis cache connected and healthy

- [x] **Technical Education: Workers Optimization**
  - Explained `--max-workers 2` flag in detail
  - Covered context switching, memory pressure, I/O bottlenecks
  - Demonstrated cross-platform nature (Mac/Windows/Linux)
  - Explained Amdahl's Law and why 2 workers optimal

- [x] **System Verification Complete**
  - Backend API tested successfully (created user99999, 201 Created)
  - Frontend running at http://localhost:8083 (bundled in 662ms)
  - Password strength translations verified (EN & ES)
  - All services operational and ready for manual testing

### ✅ Completed Last Session (Session 18)
- [x] **Password Strength Indicator in RegisterScreen** - Matches ChangePasswordScreen
  - Added real-time password strength calculation (weak/medium/strong)
  - Visual 3-bar indicator with color-coded feedback
  - Uses existing translations (changePassword.strength_*)
  - Optimized with useMemo to prevent re-renders
  - File: `src/screens/auth/RegisterScreen.tsx`

### ✅ Completed Session 17
- [x] **Documentation Optimization Complete** - All 9 files condensed (Mac + Windows)
  - Mac files: 2,095 → 829 lines (62% reduction)
  - Windows files: 1,718 → 791 lines (54% reduction)
  - **Total**: ~2,193 lines saved (58% overall)

- [x] **Frontend Performance Optimization** - ~50% faster startup
  - Created `metro.config.js` with bundler optimizations
  - Added fast launch scripts: `npm run web:fast` (2 workers)
  - Optimized package.json scripts with EXPO_NO_DOTENV=1
  - Startup time: ~60-90s → ~30-45s
  - Memory usage: ~800MB → ~500MB (38% reduction)
  - Created `FRONTEND-PERFORMANCE.md` guide

### 📝 Pending Work
- [ ] **Test Registration Flow** - Verify password strength indicator works correctly
- [ ] **Test Change Password Flow** - ⚠️ Requires fresh login (tokens expired)
  - Issue: 401/403 errors due to JWT token expiration
  - Solution: Re-login to get fresh tokens

### ⚠️ Known Warnings (Safe to Ignore)
- Package version mismatches: react-native-screens, jest, @types/jest
- Package.json export warnings: merge-options, zustand, react-hook-form
- Update when ready: `npx expo install --fix`

---

## 🌐 Mac Local Development

### Quick Start Commands
```bash
# 1. Start Docker & Redis
open -a Docker && docker-compose up -d redis

# 2. Backend (Terminal 1)
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 3. Frontend (Terminal 2) - FAST MODE ⚡
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-frontend
npm run web:fast
# Or standard: npm run web
# Or clean cache first: npm run clean && npm run web:fast
```

### Access Points
- Frontend: http://localhost:8083
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs

### Stop Services
```bash
# Stop Redis
docker-compose down

# Stop frontend/backend: Ctrl+C in terminals
```

---

## 🐛 Known Issues (Mac)

### Active Issues
- ⚠️ **JWT Token Expiration** - Tokens expire after ~15-30 min
  - Solution: Re-login to refresh tokens

- ⚠️ **Port 8000 Conflict** - Backend fails with "Address already in use"
  - Cause: Old Python/uvicorn processes not properly terminated
  - Diagnosis: `lsof -i :8000` to find process IDs
  - Solution: `kill -9 <PID>` to terminate zombie processes

### Resolved Issues
- ✅ Docker Installation - Already installed
- ✅ npm Dependencies - Fixed with clean reinstall
- ✅ Redis Setup - Running via Docker
- ✅ node_modules Corruption - Fixed with `npm install --legacy-peer-deps`
- ✅ Docker Not Starting - Use `open -a Docker` to start Docker Desktop

---

## 📋 Environment Info

- **Python**: 3.12.1 (venv in cooin-backend)
- **Node/npm**: Installed
- **Docker**: 25.0.3
- **Architecture**: Intel (x86_64)
- **Project**: `/Users/mariajimenez/Desktop/cooin-platform`

---

## 🔧 Future Enhancements

### Development
- [ ] Update Expo packages to recommended versions
- [ ] Run full test suite on Mac
- [ ] Test iOS simulator integration

---

## 📚 Key Commands Reference

### Docker
```bash
docker ps                          # Check status
docker-compose up -d redis         # Start Redis
docker logs cooin-redis            # View logs
docker exec -it cooin-redis redis-cli  # Connect to Redis CLI
```

### Git (Mac)
```bash
git pull origin main               # Pull latest
git add HISTORY_MAC.md TODO_MAC.md README_MAC.md
git commit -m "docs: Session X on Mac 🍎"
git push origin main
```

### Backend
```bash
source venv/bin/activate           # Activate venv
curl http://localhost:8000/health  # Check health
lsof -i :8000                      # Check what's using port 8000
kill -9 <PID>                      # Kill process by ID
```

### Frontend
```bash
npm install                        # Install deps
npx expo start --web --port 8083 --clear  # Start with cache clear
```

---

**Last Updated**: 2025-12-10 (Session 19)
**Quick Links**: [Mac History](./HISTORY_MAC.md) | [Mac README](./README_MAC.md) | [Mac Launch Guide](./HOW-TO-LAUNCH-WEB-APP_MAC.md)
