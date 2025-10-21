# How to Launch Cooin Web App from Visual Studio Code

## Prerequisites

Before starting, make sure you have installed:
- **Visual Studio Code** (VS Code)
- **Node.js** (version 18 or higher)
- **Python** (version 3.11 or higher)
- **Git** (for version control)

---

## Step 1: Open the Project in Visual Studio Code

### Option A: Using VS Code File Menu
1. Open **Visual Studio Code**
2. Click **File** → **Open Folder**
3. Navigate to: `C:\Windows\System32\cooin-app`
4. Click **Select Folder**

### Option B: Using Command Line
1. Open **Command Prompt** or **PowerShell**
2. Run these commands:
   ```bash
   cd C:\Windows\System32\cooin-app
   code .
   ```

---

## Step 2: Open Integrated Terminal in VS Code

1. In VS Code, press **Ctrl + `** (backtick) or go to **Terminal** → **New Terminal**
2. This opens a terminal at the bottom of VS Code
3. The terminal should be in the `C:\Windows\System32\cooin-app` directory

---

## Step 3: Start the Backend Server

### Terminal 1: Backend (FastAPI)

1. In the integrated terminal, navigate to backend folder:
   ```bash
   cd cooin-backend
   ```

2. Start the backend server:
   ```bash
   python start_dev.py
   ```

3. **Wait for the success message**:
   ```
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

4. **Do NOT close this terminal** - keep it running

### What's Happening?
- Backend API server starts on **port 8000**
- Handles all database operations, authentication, and API endpoints
- Must be running for the frontend to work

---

## Step 4: Start the Frontend Server

### Terminal 2: Frontend (React Native Web)

1. Open a **NEW terminal** in VS Code:
   - Click the **+** button in the terminal panel, OR
   - Press **Ctrl + Shift + `**

2. Navigate to frontend folder:
   ```bash
   cd cooin-frontend
   ```

3. Start the Metro bundler for web:
   ```bash
   npx expo start --web --port 8082
   ```

4. **Wait for the success message**:
   ```
   Web Bundled 9754ms index.ts (834 modules)
   Logs will appear in the browser console
   ```

5. **Do NOT close this terminal** - keep it running

### What's Happening?
- Metro bundler compiles React Native code for web
- Serves the frontend on **port 8082**
- Watches for file changes and hot-reloads automatically

---

## Step 5: Open the App in Your Browser

### Automatic Opening
- Metro bundler should **automatically open** your browser to:
  ```
  http://localhost:8082
  ```

### Manual Opening
If the browser doesn't open automatically:

1. Open your web browser (Chrome, Firefox, Edge, etc.)
2. Type in the address bar:
   ```
   http://localhost:8082
   ```
3. Press **Enter**

---

## Step 6: Using the Web App

### First Time / No Account

1. You'll see the **Login** screen
2. Click **"Sign up"** to create an account
3. Fill in the registration form:
   - Email
   - Username
   - Password
   - Select role (Borrower, Lender, or Both)
   - Agree to terms
4. Click **"Create Account"**
5. After successful registration, you'll be logged in

### Existing Account

1. Enter your **email** (e.g., `e@e.com`)
2. Enter your **password**
3. Click **"Log In"**

### After Login

- You'll be redirected to the **Dashboard/Home** screen
- Use the bottom navigation to access:
  - **Home** - Dashboard overview
  - **Matches** - Find lenders/borrowers
  - **Connections** - Your network
  - **Messages** - Chat with connections
  - **Settings** - Change language, logout, etc.

### Testing Language Switcher

1. Navigate to **Settings** (bottom navigation)
2. Tap **"Language"**
3. Select **"Español"**
4. Watch all text change to Spanish!
5. Tap **"Idioma"** → **"English"** to switch back

---

## VS Code Window Setup (Recommended)

For the best development experience:

```
┌─────────────────────────────────────────────┐
│ VS Code - C:\Windows\System32\cooin-app     │
├─────────────────────────────────────────────┤
│                                             │
│  Explorer    Code Editor                    │
│  ├── cooin-backend/     (viewing files)     │
│  ├── cooin-frontend/                        │
│  ├── history.md                             │
│  └── ...                                    │
│                                             │
├─────────────────────────────────────────────┤
│ TERMINAL 1: Backend                         │
│ C:\...\cooin-backend> python start_dev.py   │
│ INFO: Uvicorn running on http://0.0.0.0:8000│
├─────────────────────────────────────────────┤
│ TERMINAL 2: Frontend                        │
│ C:\...\cooin-frontend> npx expo start --web │
│ Web Bundled... http://localhost:8082        │
└─────────────────────────────────────────────┘
```

---

## Quick Reference: Commands

### Start Backend
```bash
cd C:\Windows\System32\cooin-app\cooin-backend
python start_dev.py
```

### Start Frontend
```bash
cd C:\Windows\System32\cooin-app\cooin-frontend
npx expo start --web --port 8082
```

### Stop Servers
- Press **Ctrl + C** in each terminal to stop the servers

---

## Troubleshooting

### Problem: "Port already in use"

**Cause**: Another process is using port 8082 or 8000

**Solution**:
1. Close any other running instances
2. In VS Code terminal:
   ```bash
   # Windows: Kill process on port 8082
   netstat -ano | findstr :8082
   taskkill /PID <PID_NUMBER> /F
   ```

### Problem: "Cannot connect to server"

**Cause**: Backend not running or CORS issue

**Solution**:
1. Make sure backend terminal shows:
   ```
   INFO: Uvicorn running on http://0.0.0.0:8000
   ```
2. Check that `cooin-backend/.env` includes port 8082:
   ```
   BACKEND_CORS_ORIGINS=["http://localhost:8082", ...]
   ```
3. Restart backend server (Ctrl + C, then run `python start_dev.py` again)

### Problem: "Blank screen" or errors after code changes

**Cause**: Metro bundler cache issues

**Solution**:
1. Stop frontend server (Ctrl + C)
2. Clear cache and restart:
   ```bash
   npx expo start --web --clear --port 8082
   ```
3. Refresh browser (Ctrl + Shift + R for hard refresh)

### Problem: Language switcher not working

**Cause**: Old cached version

**Solution**:
1. **Hard refresh** browser: **Ctrl + Shift + R** (Windows) or **Cmd + Shift + R** (Mac)
2. If still not working, clear cache:
   ```bash
   npx expo start --web --clear --port 8082
   ```
3. Open browser console (F12) and check for errors

### Problem: "Module not found" errors

**Cause**: Missing dependencies

**Solution**:
```bash
cd C:\Windows\System32\cooin-app\cooin-frontend
npm install

cd C:\Windows\System32\cooin-app\cooin-backend
pip install -r requirements.txt
```

---

## Development Workflow

### Making Code Changes

1. **Edit files** in VS Code
2. **Frontend changes**: Metro bundler auto-reloads in browser
3. **Backend changes**: Uvicorn auto-reloads (watch terminal for restart)
4. **Translation changes**: Hard refresh browser (Ctrl + Shift + R)

### Before Committing Changes

1. Test the changes in browser
2. Check both terminals for errors
3. Add files to git:
   ```bash
   git add <files>
   git commit -m "Description of changes"
   ```
4. **Push using GitHub Desktop** (not command line)

---

## Useful VS Code Extensions

For better development experience, install these extensions in VS Code:

1. **ES7+ React/Redux/React-Native snippets**
   - ID: `dsznajder.es7-react-js-snippets`

2. **Python**
   - ID: `ms-python.python`

3. **Prettier - Code formatter**
   - ID: `esbenp.prettier-vscode`

4. **GitLens**
   - ID: `eamodio.gitlens`

To install:
1. Press **Ctrl + Shift + X** (Extensions panel)
2. Search for extension name
3. Click **Install**

---

## URLs Reference

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend (Web App) | http://localhost:8082 | Main web application |
| Backend API | http://localhost:8000 | API endpoints |
| API Documentation | http://localhost:8000/docs | Interactive API docs (Swagger UI) |
| Alternative API Docs | http://localhost:8000/redoc | Alternative API documentation |

---

## Keyboard Shortcuts in VS Code

| Shortcut | Action |
|----------|--------|
| **Ctrl + `** | Toggle terminal |
| **Ctrl + Shift + `** | New terminal |
| **Ctrl + B** | Toggle sidebar |
| **Ctrl + P** | Quick file open |
| **Ctrl + Shift + P** | Command palette |
| **Ctrl + F** | Find in file |
| **Ctrl + Shift + F** | Find in all files |
| **F2** | Rename symbol |
| **Alt + Up/Down** | Move line up/down |

---

## Need Help?

- **Documentation**: Check `history.md` for all changes and fixes
- **API Docs**: http://localhost:8000/docs
- **Project Structure**: See `README.md` files in each folder
- **Git Issues**: Use GitHub Desktop for all push operations

---

## Summary: Quick Start

1. **Open VS Code**: `C:\Windows\System32\cooin-app`
2. **Terminal 1**:
   ```bash
   cd cooin-backend
   python start_dev.py
   ```
3. **Terminal 2** (new terminal):
   ```bash
   cd cooin-frontend
   npx expo start --web --port 8082
   ```
4. **Browser**: Open http://localhost:8082
5. **Login/Register** and start using the app!

---

**Last Updated**: 2025-10-21
**Maintainer**: Cooin Development Team
