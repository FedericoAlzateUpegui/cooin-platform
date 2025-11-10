# Cooin Web App - Change History

## 2025-11-10 (Session 10) - Registration Error Handling & Form Validation

**Goal**: Fix duplicate email registration error handling to show specific error messages and prevent redirect to login screen.

**Problem Identified**:
- When registering with an existing email, app redirects to login screen instead of staying on register screen
- Generic "Please check your input data and try again" (422 error) shown instead of specific "An account with this email already exists"
- Form data gets cleared
- Poor user experience

**Changes/Fixes**:
1. **Form Validation Mode Change**: Updated RegisterScreen from `mode: 'onTouched'` to `mode: 'onBlur'` + added `reValidateMode: 'onBlur'`
   - Validation now triggers when user leaves a field (jumps to next field)
2. **Input Component Event Fix**: Updated Input.tsx `handleFocus` and `handleBlur` to properly pass event objects to React Hook Form
   - Changed from `props.onBlur?.({} as any)` to `props.onBlur?.(e)`
3. **Local Error State**: Added `localError` state to RegisterScreen to capture and display errors independently from authStore
   - Prevents errors from being cleared during navigation
4. **API Error Extraction Fix**: Updated `api.ts` handleError method to properly extract error messages from backend response structure
   - Backend wraps errors in `error.message` and `error.detail` via `create_error_response`
   - Now checks `responseData.error.message` and `responseData.error.detail` first
5. **Error Display Enhancement**: Improved error UI with icon and styled red box
   - Added Ionicons alert-circle icon
   - Created prominent error container with background color, border, and padding
6. **Navigation Guard**: Added useEffect to force logout if user is authenticated despite having a local error
   - Prevents accidental navigation to authenticated screens on error
7. **Comprehensive Console Logging**: Added detailed console.log statements throughout registration flow
   - RegisterScreen: Logs full error object, detail, message, status_code
   - authStore: Logs registration start, response received, authentication state changes
   - authService: Logs registration errors
8. **authStore Error Handling**: Enhanced registration method to explicitly set `isAuthenticated: false`
   - Sets false at registration start
   - Only sets true if both user and access_token exist in response
   - Guarantees false on error
9. **authService Try-Catch**: Added try-catch wrapper around registration with error detail preservation
   - Validates tokens exist before storing
   - Preserves `error.detail` as `error.message`

**Files Changed**:
- `RegisterScreen.tsx:1` - Added useEffect import
- `RegisterScreen.tsx:15` - Added Ionicons import
- `RegisterScreen.tsx:40-53` - Added localError state, isAuthenticated, logout from authStore, navigation guard useEffect
- `RegisterScreen.tsx:51-52` - Changed form validation from `mode: 'onTouched'` to `mode: 'onBlur'`, added `reValidateMode: 'onBlur'`
- `RegisterScreen.tsx:63-99` - Completely rewrote onSubmit error handling with local error state and extensive logging
- `RegisterScreen.tsx:277-284` - Updated error display to use localError with icon
- `RegisterScreen.tsx:445-464` - Enhanced error container styles (flexDirection, backgroundColor, border, icon container)
- `Input.tsx:39-47` - Fixed handleFocus and handleBlur to pass event objects properly
- `authStore.ts:52-94` - Enhanced register method with logging and explicit isAuthenticated handling
- `authService.ts:57-95` - Added try-catch wrapper with error preservation
- `api.ts:138-191` - Rewrote handleError to check nested error object first (responseData.error.message/detail)

**Pending Work**:
- [ ] **Test duplicate email registration** - Verify error message shows correctly
- [ ] **Verify no redirect** - Confirm user stays on register screen
- [ ] **Check form data persistence** - Ensure email, username, password remain filled
- [ ] **Analyze console logs** - Review [authStore] and error logs to identify any remaining issues

**Key Learning**: Backend error response structure uses nested `error` object via `create_error_response()`. Frontend must extract `responseData.error.message` or `responseData.error.detail`, not just top-level `detail`.

**Status**: Multiple fixes implemented ⚠️, needs testing with console log analysis to verify success

**Next Session**: Test duplicate email registration, review console output, and finalize error handling if needed.

---

## 2025-11-07 (Session 9) - Form Validation, Package Cleanup & Scroll Investigation

**Goal**: Enhance form UX, clean up dependencies, fix scrolling issues on web platform.

**Changes/Fixes**:
1. **Form Validation Enhancement**: Added `mode: 'onTouched'` to RegisterScreen useForm hook for real-time field validation
2. **ProfileCompletion Fix**: Fixed type error in HomeScreen - added `profileCompletion` (percentage 0-100) to ProfileState
   - Updated `profileStore.ts` to calculate completion percentage based on 10 profile fields
   - HomeScreen now displays profile completion progress bar correctly
3. **Package Cleanup**: Removed redundant `react-native-vector-icons` package (13 packages removed, no vulnerabilities)
4. **Package Validation**: Verified all required packages installed and up-to-date (React 19.1.0, Expo 54.0.22, React Native 0.81.5)
5. **Scroll Investigation**: Multiple approaches attempted for RegisterScreen and ProfileSetupScreen web scrolling (pending resolution)

**Files Changed**:
- `RegisterScreen.tsx:51` - Added `mode: 'onTouched'` to form validation
- `RegisterScreen.tsx:299,320` - Removed `flexGrow: 1`, updated scroll styles (multiple iterations)
- `ProfileSetupScreen.tsx:488` - Removed `flexGrow: 1`, updated scroll styles (multiple iterations)
- `profileStore.ts:10,25` - Added `profileCompletion: number` property
- `profileStore.ts:93-119` - Enhanced `checkProfileCompletion()` to calculate percentage (10 fields)
- `HomeScreen.tsx:26` - Updated to use both `isProfileComplete` and `profileCompletion`
- `package.json` - Removed `react-native-vector-icons` dependency

**Pending Work**:
- [ ] **CRITICAL**: Resolve web scrolling issue on Windows (mouse wheel not working on RegisterScreen/ProfileSetupScreen)
  - Attempted: SafeAreaView removal, Platform.select CSS, View with overflow, ScrollView with explicit heights
  - Status: Scrollbar visible but mouse wheel scroll range limited
- [ ] Fix `props.pointerEvents` deprecation warning (React Navigation internal - requires library update)

**Key Learning**: React Native Web ScrollView compatibility is challenging - may require custom web-specific implementation or third-party scroll library.

**Status**: Form validation improved ✅, Profile completion tracking working ✅, Web scrolling pending ⚠️

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
