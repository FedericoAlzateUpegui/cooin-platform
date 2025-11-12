# Cooin Web App - Change History

## 2025-11-12 (Session 12) - Responsive Navigation & Navigation Hook Fixes

**Goal**: Implement responsive navigation with desktop sidebar and mobile bottom tabs, fix web scrolling issues, and resolve navigation prop access problems.

**Changes/Fixes**:
1. **Responsive Navigation System**: Implemented adaptive navigation that switches between desktop sidebar and mobile bottom tabs
   - Added desktop breakpoint constant: `DESKTOP_BREAKPOINT = 768`
   - Created `DesktopSidebarNavigator` component with left sidebar navigation (240px width)
   - Created `MobileTabNavigator` component with bottom tab navigation
   - Added `MainTabNavigator` wrapper that uses `useWindowDimensions()` to detect screen size
   - Sidebar includes: Logo header, navigation items with icons/labels, active state highlighting

2. **Web Scrolling Fix**: Resolved scrolling issues on desktop by implementing proper layout hierarchy
   - Added explicit viewport units to desktop container: `width: '100vw', height: '100vh'`
   - Created `mainContent` wrapper with `flex: 1` to take remaining width after sidebar
   - Added `screenContainer` wrapper with `width: '100%', height: '100%'` for proper constraints
   - Used `Platform.select` to apply web-specific layout rules while maintaining mobile compatibility
   - Result: ScrollView components inside screens (Settings, Matching, etc.) now work properly

3. **Backend Profile Schema Fix**: Fixed 500 Internal Server Error on `/api/v1/profiles/me` endpoint
   - Issue: Pydantic V2 `from_attributes=True` doesn't automatically call `@property` methods
   - Updated `UserProfileResponse` schema to use `@computed_field` decorator with `@property`
   - Converted `age`, `location_string`, `public_name`, and `full_name` to computed fields
   - Fields now compute from other schema attributes instead of requiring ORM model properties
   - Backend restarted to apply changes

4. **Navigation Hook Migration**: Fixed navigation access issues in screens rendered directly in desktop sidebar
   - **ProfileSetupScreen**: Migrated from navigation prop to `useNavigation()` hook
     - Added `import { useNavigation } from '@react-navigation/native'`
     - Removed `ProfileSetupScreenProps` interface
     - Changed from `({ navigation })` to `const navigation = useNavigation()`
     - Fixes `navigation.goBack()` calls on lines 144 and 405
   - **HomeScreen**: Migrated from navigation prop to `useNavigation()` hook
     - Added `import { useNavigation } from '@react-navigation/native'`
     - Removed `HomeScreenProps` interface
     - Changed from `({ navigation })` to `const navigation = useNavigation()`
     - Fixes all `navigation.navigate()` calls (Profile, Matching, Connections, Messages)

**Files Changed**:
- `AppNavigator.tsx:27-33` - Added navigation items configuration array with icons and labels
- `AppNavigator.tsx:36-57` - Created `SidebarNavItem` component for desktop navigation
- `AppNavigator.tsx:60-94` - Created `DesktopSidebarNavigator` with state-based screen switching
- `AppNavigator.tsx:97-133` - Created `MobileTabNavigator` using Tab.Navigator
- `AppNavigator.tsx:136-141` - Created `MainTabNavigator` with responsive layout detection
- `AppNavigator.tsx:182-258` - Added desktop sidebar styles (sidebar, navigation items, containers)
- `AppNavigator.tsx:184-195,244-258` - Added Platform.select web-specific layout styles
- `profile.py:3,211,217,234,242` - Added `computed_field` import and decorators
- `profile.py:213-247` - Converted age, location_string, public_name, full_name to @computed_field
- `ProfileSetupScreen.tsx:16` - Added `useNavigation` import
- `ProfileSetupScreen.tsx:40-41` - Removed interface, added `const navigation = useNavigation()`
- `HomeScreen.tsx:12` - Added `useNavigation` import
- `HomeScreen.tsx:20-21` - Removed interface, added `const navigation = useNavigation()`

**Testing Results**:
- ✅ Desktop view (≥768px) shows left sidebar navigation with proper styling
- ✅ Mobile view (<768px) shows bottom tab navigation
- ✅ Scrolling works correctly on all screens (Settings, Matching, Home, etc.)
- ✅ Profile setup navigation works from HomeScreen "complete your profile" button
- ✅ All quick action navigation buttons work (Discover Matches, Connections, Messages, Profile)
- ✅ Backend `/api/v1/profiles/me` endpoint returns 200 with computed fields
- ✅ No console errors for navigation prop access

**Key Technical Decisions**:
1. **Desktop Sidebar vs Tab Navigator**: Desktop uses direct component rendering instead of Tab.Navigator to avoid navigation stack complexity
2. **useNavigation Hook**: Allows components to access navigation from React Navigation context regardless of how they're rendered
3. **Platform.select for Web**: Used web-specific CSS properties (vh, vw, boxShadow) while maintaining RN compatibility
4. **@computed_field Decorator**: Pydantic V2's recommended approach for computed properties that derive from other schema fields

**Key Learning**:
- When rendering React Navigation screens outside of Stack/Tab navigators, they lose navigation prop access
- `useNavigation()` hook provides universal navigation access from React Navigation context
- React Native Web layout requires explicit viewport constraints (vh/vw) for proper scrolling
- Pydantic V2 requires `@computed_field` decorator to compute fields from schema attributes vs ORM model properties

**Status**: All features working ✅ - Responsive navigation implemented, scrolling fixed, navigation hooks working

---

## 2025-11-11 (Session 11) - Internationalization & Bug Fixes

**Goal**: Fix registration navigation bug, implement dynamic translation system for error messages, and resolve TypeScript errors.

**Changes/Fixes**:
1. **Navigation Bug Fixed**: Resolved issue where registration errors caused redirect to login screen
   - Root cause: `isLoading` state change caused AppNavigator to unmount/remount auth flow
   - Solution: Added separate `isInitializing` flag for app startup authentication checks
   - Updated AppNavigator to use `isInitializing` instead of `isLoading` for LoadingScreen
   - Now `isLoading` only controls button states, preventing navigation unmounts
2. **Dynamic Translation System**: Implemented comprehensive internationalization for form validation
   - Added 20+ validation error messages to both `en.json` and `es.json` translation files
   - Updated RegisterScreen to use `useMemo` for dynamic zod schema creation with `t()` function
   - Schema recreates automatically when language changes
   - Created `getTranslatedErrorMessage()` helper function to map backend errors to translation keys
   - Supports both exact matches and fuzzy matching for error messages
3. **Error Message Improvements**: Enhanced error extraction and display in `api.ts`
   - Updated field error handling to combine multiple validation errors
   - Shows all field errors when multiple exist (e.g., "username: invalid; email: already exists")
   - Single field errors display message only
4. **ProfileSetupScreen TypeScript Fix**: Resolved style prop type error on line 434
   - Button component accepts `ViewStyle` (single object), not `ViewStyle[]` (array)
   - Changed from conditional array to merged style object using spread operator
5. **ProfileSetupScreen Internationalization**: Replaced all hardcoded English strings with translations
   - All 4 steps now fully translatable (Basic Info, Photo/Bio, Location, Financial Info)
   - Converted static zod schema to dynamic `useMemo` schema with translated validation messages
   - Updated employment status options to use translation keys
   - Translated all UI elements: header, progress label, buttons, alerts, placeholders

**Files Changed**:
- `authStore.ts:9,25` - Added `isInitializing` state flag
- `authStore.ts:98-111` - Removed isLoading from logout (unnecessary)
- `authStore.ts:114-140` - Updated checkAuth to use isInitializing instead of isLoading
- `AppNavigator.tsx:110,116` - Changed from isLoading to isInitializing in LoadingScreen check
- `i18n/locales/en.json:262-282` - Added comprehensive validation error messages
- `i18n/locales/es.json:262-282` - Added Spanish translations for all validation errors
- `RegisterScreen.tsx:1` - Added useMemo import
- `RegisterScreen.tsx:23-29` - Moved RegisterFormData type definition before component
- `RegisterScreen.tsx:43-60` - Created dynamic registerSchema with useMemo and translations
- `RegisterScreen.tsx:86-133` - Added getTranslatedErrorMessage helper function with mapping logic
- `RegisterScreen.tsx:135-158` - Updated onSubmit to use translated errors
- `api.ts:161-178` - Enhanced field error extraction to combine multiple errors
- `ProfileSetupScreen.tsx:1` - Added useMemo import
- `ProfileSetupScreen.tsx:25-37` - Moved ProfileFormData type, removed static schema
- `ProfileSetupScreen.tsx:53-68` - Created dynamic profileSchema with useMemo and translations
- `ProfileSetupScreen.tsx:98-134` - Translated all Alert messages
- `ProfileSetupScreen.tsx:150-380` - Replaced all hardcoded strings in steps 1-4 with t() function
- `ProfileSetupScreen.tsx:393,400,423,432,441` - Translated header, progress, and button text
- `ProfileSetupScreen.tsx:434` - Fixed TypeScript error with style prop (merged object vs array)

**Testing Results**:
- ✅ Duplicate email registration now stays on register screen
- ✅ Shows translated error: "An account with this email already exists" (English)
- ✅ Shows translated error: "Ya existe una cuenta con este correo electrónico" (Spanish)
- ✅ Username validation errors properly translated in both languages
- ✅ ProfileSetupScreen displays correctly in Spanish when selected
- ✅ All form validation errors translate dynamically on language change

**Key Learning**:
- Separating `isLoading` (UI state) from `isInitializing` (app startup state) prevents navigation unmounts
- Using `useMemo` with `t()` function enables dynamic schema recreation on language changes
- Backend error messages need intelligent mapping to translation keys for proper i18n support

**Status**: All features working ✅

---

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
