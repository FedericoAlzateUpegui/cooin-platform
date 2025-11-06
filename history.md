# Cooin Web App - Change History

## 2025-11-06 (Session 9) - Dev Branch Setup & Documentation Workflow

**Goal**: Establish dev branch workflow and streamline commit documentation process.

**Changes**:
1. **Git Workflow**: Created dev branch for all development work (main protected)
2. **Documentation Process**: Added "Auto-Documentation on Commit" quick flow section to DOCUMENTATION_PROCESS.md
3. **Session Continuity**: Captured Session 8 changes (config fixes, python path updates, documentation system)

**Files Changed**:
- `DOCUMENTATION_PROCESS.md` - Added auto-documentation workflow (lines 472-506)
- `HISTORY.md` - Added this session entry
- `TODO.md` - Updated session number and completed tasks
- `config.ts`, `package.json`, `HOW-TO-LAUNCH-WEB-APP.md` - Session 8 fixes

**Status**: Dev branch established, documentation workflow streamlined ✅

---

## 2025-11-05 (Session 8) - Documentation Cleanup & Config Fixes

**Goal**: Clean up documentation, fix connectivity issues, and improve form validation.

**Fixes**:
1. **Python Path Documentation**: Updated all docs (TODO.md, HOW-TO-LAUNCH-WEB-APP.md, HISTORY.md) to use simple `python` command instead of full path `"C:\Users\Usuario\AppData\Local\Microsoft\WindowsApps\python.exe"`
2. **Config URL Fix**: Updated `config.ts` BASE_URL from old Cloudflare tunnel to `http://localhost:8000/api/v1` - fixed "Cannot connect to server" timeout error
3. **Cache Clearing**: Identified need to restart frontend with `--clear` flag after config changes

**Educational Sessions**:
- **TECH-001**: Taught package update process (npm outdated, expo-doctor, npx expo install --fix)
- **Form Validation**: Identified need for real-time validation in RegisterScreen (onTouched mode)

**Files Changed**:
- `TODO.md` - Removed 7 occurrences of old Python path, updated Known Issues, restructured sections
- `HOW-TO-LAUNCH-WEB-APP.md` - Simplified Python commands
- `HISTORY.md` - Updated Python path documentation, added this session
- `config.ts` - Changed BASE_URL to localhost
- `README.md` - Added link to documentation process guide
- `DOCUMENTATION_PROCESS.md` - NEW: Complete documentation guide with "How to Read" section
- `SESSION_8_SUMMARY.md` - NEW: Session summary

**Pending Work**:
- [ ] Implement form validation improvements (RegisterScreen.tsx - add `mode: 'onTouched'`)
- [ ] Update Expo packages (waiting for user decision)
- [ ] Fix React Native Web deprecation warnings (shadow*, pointerEvents)

**Key Learning**: Metro bundler caches config changes - always restart with `--clear` flag!

**Status**: Connectivity fixed, local development working ✅

---

## 2025-11-03 (Session 7) - Cloudflare Tunnel Setup

**Goal**: Replace ngrok with Cloudflare Tunnel for unlimited free partner sharing.

**Changes**:
- Started Cloudflare tunnels for frontend (8083) and backend (8000)
- Generated URLs: Frontend `https://hobby-wax-option-shakira.trycloudflare.com`, Backend `https://democrat-route-among-give.trycloudflare.com`
- Updated `cooin-frontend/src/constants/config.ts` BASE_URL to Cloudflare backend
- Added Cloudflare URLs to `cooin-backend/.env` CORS_ORIGINS

**Issue Found**: Backend 502 error - server not running on port 8000

**Terminal Setup** (4 required):
```cmd
# 1. Backend: python uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# 2. Frontend: npx expo start --web --port 8083 --clear
# 3. Backend Tunnel: cloudflared tunnel --url http://localhost:8000
# 4. Frontend Tunnel: cloudflared tunnel --url http://localhost:8083
```

**Status**: Config updated, pending backend restart and testing

---

## 2025-10-25 (Session 6) - Backend & Ngrok Fixes

**Critical Fixes**:
1. **requirements.txt**: Fixed line 53 - separated merged packages `gunicorn==21.2.0user-agents==2.2.0`
2. **Python Path**: Fixed - now works with simple `python` command (Python 3.11.9)
3. **ngrok.yml**: Updated v2 syntax `bind_tls: true` → v3 syntax `schemes: [https]`
4. **Ngrok Reserved Domain**: Conflicts resolved - use separate tunnels: `ngrok http 8083` and `ngrok http 8000`
5. **start-ngrok.bat**: Removed `...` for Spanish Windows compatibility

**Mobile Access Solution**:
- Issue: `localhost` doesn't work on iPhone
- Fix: Use ngrok for both frontend AND backend
- Update `config.ts` BASE_URL to backend ngrok URL
- Add ngrok URLs to backend CORS `.env`

**Cloudflare Tunnel Alternative**: Free forever, unlimited sessions, persistent URLs vs ngrok's 2hr limit

**Files**: `requirements.txt`, `ngrok.yml`, `start-ngrok.bat`, `config.ts`, `.env`

---

## 2025-10-25 (Session 5) - Ngrok Integration

**Created Files**:
- `ngrok.yml` - Dual tunnel config (frontend 8083, backend 8000)
- `start-ngrok.bat` - Automated tunnel startup with validation
- `get-ngrok-urls.ps1` - URL extraction + auto-config update
- `NGROK-SETUP.md` & `NGROK-QUICKSTART.md` - Documentation
- `fix-permissions.bat` - Permission fix for System32 location
- `PERMISSION-FIX.md` - Permission troubleshooting guide

**Permission Issue**: Project in `C:\Windows\System32\cooin-app` requires admin rights
**Solutions**: Run `fix-permissions.bat` as admin OR move to `C:\Users\USERNAME\Documents\cooin-app`

---

## 2025-10-24 (Session 4) - Language Selector UX Upgrade

**Changed**: `SettingsScreen.tsx` - Replaced `window.prompt("1 or 2")` with modal dialog
**Added**: Language modal with flags (🇺🇸 🇪🇸), checkmarks, native names. Lines 248-320 (UI), 451-532 (styles)

---

## 2025-10-24 (Session 3) - HomeScreen Display Name Fix

**Bug**: Greeting showed "Good morning y" instead of "Good morning Testy"
**Fix**: `HomeScreen.tsx` line 91 - Added `user?.username` to fallback chain
**Before**: `profile?.display_name || user?.email?.split('@')[0] || 'User'`
**After**: `profile?.display_name || user?.username || user?.email?.split('@')[0] || 'User'`

---

## 2025-10-24 (Session 2) - Registration Username Field (Critical)

**Bug**: Registration failing - username not sent to backend
**Fixes**:
- `api.ts`: Added `username`, `confirm_password`, `agree_to_terms` to RegisterRequest
- `RegisterScreen.tsx`: Added username input field with validation (3-30 chars)
- `authStore.ts`: Added username parameter to register()
- Added translations: `en.json` & `es.json`

---

## 2025-10-24 (Session 1) - Backend Bcrypt Compatibility

**Error**: 500 on auth endpoints - bcrypt 5.0 incompatible with passlib 1.7.4
**Fixes**:
- Installed `user-agents==2.2.0`
- Downgraded `bcrypt==5.0.0` → `bcrypt==4.0.1`
- `security.py`: Added password length validation (72-byte limit)

---

## 2025-10-23 (Sessions 1-2) - Full i18n Implementation

**Completed**: Entire app multilingual (English/Spanish) across all 6 screens
**Changes**:
- `AppNavigator.tsx`: Navigation titles use `t('navigation.*')`
- `LanguageContext.tsx`: Added interpolation support
- `SettingsScreen.tsx`: Platform-specific dialogs (web: `window.confirm/prompt`, mobile: `Alert.alert`)
- All screens: Added `useLanguage` hook - HomeScreen, ConnectionsScreen, MessagesScreen, MatchingScreen, ProfileSetupScreen, VerificationScreen
- Translation files: 275+ keys in `en.json` & `es.json`

**Storage Fix**: `secureStorage.ts` & `authService.ts` - Auto-clear corrupted localStorage entries

---

## 2025-10-21 (Multiple Sessions) - i18n Infrastructure Setup

**Component Created**: `LanguageSwitcher.tsx` (3 variants: icon/button/dropdown)

**Critical Fixes**:
1. **App.tsx**: Added `LanguageProvider` wrapper + `import './src/i18n/i18n.config'`
2. **LanguageContext.tsx**: Async i18n initialization with `isI18nInitialized` state
3. **SettingsScreen.tsx**: Connected to LanguageContext (was using local state)
4. **LoginScreen & RegisterScreen**: Added translations for all text
5. **config.ts**: Fixed BASE_URL port 8003 → 8000
6. **api.ts**: Skip token refresh on auth endpoints
7. **.env**: Added port 8082 to CORS origins

**Fixes**: JSX syntax errors, Metro bundler caching, login scroll issues

**Git Strategy**: Always use GitHub Desktop for pushing (credential manager issues)
