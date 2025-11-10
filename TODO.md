# Cooin Web App - TODO

## 🚀 Current Session (Session 10) - Registration Error Handling & Form Validation

### 🔨 In Progress
- [ ] **CRITICAL: Duplicate Email Registration** - Fix error handling when registering with existing email
  - Issue: App redirects to login screen on error instead of staying on register screen
  - Issue: Generic 422 error shown instead of specific "email already exists" message
  - Status: Multiple fixes implemented, needs testing with console logs
  - Next: Test with duplicate email and review console output

### ✅ Completed This Session
- [x] **Form Validation on Blur** - Changed RegisterScreen from `mode: 'onTouched'` to `mode: 'onBlur'` + fixed Input component event handling
- [x] **Local Error State** - Added `localError` state in RegisterScreen to capture and display errors without relying on authStore
- [x] **Error Extraction Fix** - Updated api.ts handleError to properly extract nested error messages from backend `error.message` and `error.detail`
- [x] **Error Display Enhancement** - Added error icon and prominent red box styling for better error visibility
- [x] **Navigation Guard** - Added useEffect to force logout if user is authenticated despite local error
- [x] **Comprehensive Logging** - Added console.log statements throughout registration flow for debugging
- [x] **authStore Error Handling** - Explicitly set `isAuthenticated: false` on registration start and error
- [x] **authService Try-Catch** - Added error handling to preserve error.detail as error.message

### 📝 Completed Previous Sessions (Session 9)
- [x] **Form Validation Enhancement** - Added `mode: 'onTouched'` to RegisterScreen.tsx useForm hook (line 51)
- [x] **ProfileCompletion Fix** - Fixed HomeScreen type error, added percentage calculation to profileStore
- [x] **Package Cleanup** - Removed redundant react-native-vector-icons package (13 packages removed)
- [x] **Package Validation** - Verified all required packages up-to-date (React 19.1.0, Expo 54.0.22, RN 0.81.5)
- [x] **Web Scrolling** - Confirmed working (issue resolved from previous session)

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

- 🔴 **CRITICAL: Duplicate Email Registration Error** - App redirects to login screen when registering with existing email
  - Issue: Generic 422 error message instead of specific "An account with this email already exists"
  - Status: Multiple fixes implemented (local error state, error extraction, navigation guard, logging)
  - Next: Test with duplicate email registration and analyze console logs
  - Impact: Poor UX - users don't know why registration failed and lose form data
- ⚠️ **Project in System32** - Permission issues. Solution: Move to `C:\Users\USERNAME\Documents\cooin-app` or run `fix-permissions.bat` as admin
- ✅ **Python Path** - FIXED: Now works with simple `python` command (Python 3.11.9)
- ✅ **Web Scrolling** - FIXED: Mouse wheel scrolling now working on RegisterScreen/ProfileSetupScreen
- ⚠️ **Ngrok Reserved Domain** - Delete from https://dashboard.ngrok.com/cloud-edge/domains if using ngrok

---

## 🐞 Technical Debt

### Code Quality
- [ ] Fix React Native Web deprecation warnings:
  - `shadow*` props → Use `boxShadow` (MatchCard.tsx:145)
  - `props.pointerEvents` → Use `style.pointerEvents` (AppNavigator.tsx:122) - Note: This is from React Navigation library, requires library update
- [ ] Implement error boundary for better error handling
- [ ] Add loading states for all async operations
- [ ] Resolve web scrolling compatibility (consider react-native-web-scroll-view or custom implementation)

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

**Last Updated**: 2025-11-10 (Session 10)

**Quick Links**: [HISTORY.md](./HISTORY.md) | [README.md](./README.md) | [HOW-TO-LAUNCH-WEB-APP.md](./HOW-TO-LAUNCH-WEB-APP.md)
