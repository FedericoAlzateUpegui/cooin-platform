# Cooin Web App - TODO

## 🚀 Current Session (Session 9) - Dev Branch & Workflow Setup

### 🔨 In Progress
- [ ] **Form Validation Enhancement** - Add `mode: 'onTouched'` to RegisterScreen.tsx useForm hook
- [ ] **Package Updates (TECH-001)** - Update @expo/vector-icons, expo, react-native

### ✅ Completed This Session
- [x] **Git Workflow** - Created dev branch for development (main protected)
- [x] **Documentation Workflow** - Added auto-documentation process to DOCUMENTATION_PROCESS.md
- [x] **Session 8 Capture** - Documented config fixes, python path updates in HISTORY.md

### 🌐 Local Development (Current Mode)
```cmd
# Terminal 1 - Backend
cd C:\Windows\System32\cooin-app\cooin-backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd C:\Windows\System32\cooin-app\cooin-frontend
npx expo start --web --port 8083 --clear
```

### 🌍 Public Sharing Setup (When Needed)
```cmd
# Terminal 3 - Backend Tunnel
cloudflared tunnel --url http://localhost:8000

# Terminal 4 - Frontend Tunnel
cloudflared tunnel --url http://localhost:8083

# Then update config.ts and .env with new tunnel URLs
```

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
- [ ] Create backend startup script (`start-backend.bat`)

### Cloudflare
- [ ] Consider named tunnels for persistent URLs (vs random URLs that change)
- [ ] Optional: Custom domain configuration

---

## 🐛 Known Issues

- ⚠️ **Project in System32** - Permission issues. Solution: Move to `C:\Users\USERNAME\Documents\cooin-app` or run `fix-permissions.bat` as admin
- ✅ **Python Path** - FIXED: Now works with simple `python` command (Python 3.11.9)
- ⚠️ **Ngrok Reserved Domain** - Delete from https://dashboard.ngrok.com/cloud-edge/domains if using ngrok

---

## 🐞 Technical Debt

### Code Quality
- [ ] Fix React Native Web deprecation warnings:
  - `shadow*` props → Use `boxShadow` (MatchCard.tsx:145)
  - `props.pointerEvents` → Use `style.pointerEvents` (AppNavigator.tsx:122)
- [ ] Implement error boundary for better error handling
- [ ] Add loading states for all async operations

### Testing
- [ ] Add unit tests for form validation
- [ ] Add integration tests for auth flow
- [ ] Test Cloudflare tunnel configuration

---

## 🔧 Future Enhancements

### UX Improvements
- [ ] Add password strength indicator
- [ ] Add email verification flow
- [ ] Implement forgot password functionality
- [ ] Add profile picture upload

### Automation
- [ ] All-in-one startup script (backend + frontend + tunnels)
- [ ] Auto-update config with tunnel URLs

### Deployment
- [ ] Move project out of System32
- [ ] Implement automated deployment workflow
- [ ] Set up CI/CD pipeline
- [ ] Payment integration
- [ ] Admin dashboard

---

## 📚 Key Commands Reference

### Backend
```cmd
# Simple Python command
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# With venv
venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
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

### Ngrok (Alternative)
```cmd
ngrok http 8000   # Backend
ngrok http 8083   # Frontend
```

---

**Last Updated**: 2025-11-06 (Session 9)

**Quick Links**: [HISTORY.md](./HISTORY.md) | [README.md](./README.md) | [HOW-TO-LAUNCH-WEB-APP.md](./HOW-TO-LAUNCH-WEB-APP.md)
