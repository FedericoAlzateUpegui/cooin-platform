# Ngrok Setup Guide - Cooin Web App

This guide explains how to expose your local Cooin web app to the public internet using ngrok.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Updating Frontend Config](#updating-frontend-config)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, make sure you have:

- ✅ **Ngrok account** (free or paid) - [Sign up here](https://ngrok.com/signup)
- ✅ **Cooin backend running** on port 8000
- ✅ **Cooin frontend running** on port 8083
- ✅ **Ngrok installed** on your system

---

## Installation

### Step 1: Install Ngrok

#### Option A: Download and Install
1. Go to [ngrok.com/download](https://ngrok.com/download)
2. Download the Windows version
3. Extract `ngrok.exe` to a folder (e.g., `C:\ngrok`)
4. Add to PATH or copy to `C:\Windows\System32`

#### Option B: Using Chocolatey
```powershell
choco install ngrok
```

### Step 2: Verify Installation

Open Command Prompt or PowerShell and run:
```bash
ngrok version
```

You should see output like: `ngrok version 3.x.x`

---

## Configuration

### Step 1: Get Your Auth Token

1. Go to [https://dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
2. Copy your auth token
3. Open `ngrok.yml` in the cooin-app folder
4. Replace `YOUR_NGROK_AUTH_TOKEN_HERE` with your actual token

**Example:**
```yaml
authtoken: 2abcdefGHIJKLMN1234567890_abcdefghijklmnopqrstuvwxyz
```

### Step 2: Review Configuration

The `ngrok.yml` file is already configured for both services:

```yaml
tunnels:
  frontend:
    proto: http
    addr: 8083      # Frontend port
    inspect: true
    bind_tls: true  # Use HTTPS

  backend:
    proto: http
    addr: 8000      # Backend port
    inspect: true
    bind_tls: true  # Use HTTPS
```

**Optional**: If you have a paid ngrok plan, you can use custom subdomains:
```yaml
tunnels:
  frontend:
    subdomain: my-cooin-app  # https://my-cooin-app.ngrok.io
  backend:
    subdomain: my-cooin-api  # https://my-cooin-api.ngrok.io
```

---

## Usage

### Quick Start (3 Steps)

#### Step 1: Start Backend and Frontend

Open two terminals:

**Terminal 1 - Backend:**
```bash
cd C:\Windows\System32\cooin-app\cooin-backend
python start_dev.py
```

**Terminal 2 - Frontend:**
```bash
cd C:\Windows\System32\cooin-app\cooin-frontend
npx expo start --web --port 8083
```

Wait for both to be running successfully.

#### Step 2: Start Ngrok Tunnels

**Terminal 3 - Ngrok:**

Double-click `start-ngrok.bat` or run in terminal:
```bash
cd C:\Windows\System32\cooin-app
start-ngrok.bat
```

You'll see the ngrok dashboard with your public URLs:

```
Forwarding  https://abc123.ngrok.io -> http://localhost:8083 (frontend)
Forwarding  https://xyz789.ngrok.io -> http://localhost:8000 (backend)
```

#### Step 3: Get and Share URLs

**Terminal 4 - Get URLs:**

Run the PowerShell script to retrieve the URLs:
```powershell
cd C:\Windows\System32\cooin-app
powershell -ExecutionPolicy Bypass -File .\get-ngrok-urls.ps1
```

This will:
- Display your public frontend and backend URLs
- Offer to automatically update your frontend config
- Copy the URLs for sharing

**Share the frontend URL** with anyone:
```
https://abc123.ngrok.io
```

---

## Updating Frontend Config

### Automatic Update (Recommended)

When you run `get-ngrok-urls.ps1`, it will ask:
```
Update frontend config to use ngrok backend URL? (y/n)
```

Type `y` and press Enter. The script will:
1. ✅ Backup your current config (`config.ts.backup`)
2. ✅ Update `BASE_URL` to use the ngrok backend URL
3. ✅ Show the new configuration

**After updating:**
1. Go to Terminal 2 (frontend)
2. Press **Ctrl+C** to stop Metro bundler
3. Restart: `npx expo start --web --port 8083`
4. Hard refresh browser: **Ctrl+Shift+R**

### Manual Update

If you prefer to update manually:

1. Open `cooin-frontend/src/constants/config.ts`
2. Find the `BASE_URL` line
3. Replace with your ngrok backend URL:

```typescript
export const API_CONFIG = {
  BASE_URL: 'https://xyz789.ngrok.io/api/v1',  // ← Your ngrok backend URL
  TIMEOUT: 10000,
  RETRY_ATTEMPTS: 3,
} as const;
```

4. Save the file
5. Restart frontend and hard refresh browser

---

## Architecture

When using ngrok, your setup looks like this:

```
Internet User
     ↓
https://abc123.ngrok.io (Frontend URL)
     ↓
Ngrok Cloud → Ngrok Tunnel → http://localhost:8083 (Your Frontend)
                                      ↓
                            Makes API calls to:
                                      ↓
                         https://xyz789.ngrok.io/api/v1 (Backend URL)
                                      ↓
Ngrok Cloud → Ngrok Tunnel → http://localhost:8000 (Your Backend)
                                      ↓
                              PostgreSQL Database
```

---

## Ngrok Web Interface

While ngrok is running, you can access the web interface:

**URL:** [http://localhost:4040](http://localhost:4040)

**Features:**
- 📊 See all active tunnels
- 🔍 Inspect HTTP requests and responses
- 📈 Monitor traffic
- 🐛 Debug API calls
- 📝 View request/response headers and bodies

This is incredibly useful for debugging!

---

## Troubleshooting

### Problem: "ngrok is not installed or not in PATH"

**Solution:**
1. Verify installation: `ngrok version`
2. If not found, add to PATH:
   - Right-click **This PC** → **Properties** → **Advanced system settings**
   - Click **Environment Variables**
   - Under **System variables**, find **Path**, click **Edit**
   - Click **New** and add the folder containing `ngrok.exe`
   - Click **OK**, restart terminal

### Problem: "Ngrok auth token not configured"

**Solution:**
1. Get your token: [https://dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
2. Edit `ngrok.yml`
3. Replace `YOUR_NGROK_AUTH_TOKEN_HERE` with your token
4. Save and restart ngrok

### Problem: "No active ngrok tunnels found"

**Solution:**
1. Make sure `start-ngrok.bat` is running
2. Check ngrok window for errors
3. Verify ports 8000 and 8083 are not already tunneled
4. Visit [http://localhost:4040](http://localhost:4040) to see active tunnels

### Problem: "Frontend can't connect to backend"

**Symptoms:** Login/register fails, API errors in browser console

**Solution:**
1. Run `get-ngrok-urls.ps1` and update config (choose `y`)
2. Restart frontend Metro bundler
3. Hard refresh browser (Ctrl+Shift+R)
4. Check browser console for the API URL being used
5. Verify backend ngrok URL is accessible

### Problem: CORS errors when using ngrok

**Solution:**

Update `cooin-backend/.env` to include ngrok URLs:

```env
BACKEND_CORS_ORIGINS=["http://localhost:8083","https://abc123.ngrok.io","https://xyz789.ngrok.io"]
```

Replace `abc123` and `xyz789` with your actual ngrok subdomain.

Restart backend:
```bash
cd cooin-backend
python start_dev.py
```

### Problem: Ngrok session expires

**Symptoms:** Tunnel stops working after a while

**Free Plan:** Sessions expire after 2 hours

**Solutions:**
1. **Restart ngrok:** Close and run `start-ngrok.bat` again (you'll get new URLs)
2. **Upgrade to paid plan:** Get persistent URLs and longer sessions
3. **Use ngrok Edge:** Static domain that doesn't change

---

## Tips and Best Practices

### 1. Keep Terminals Organized

```
Terminal 1: Backend  (python start_dev.py)
Terminal 2: Frontend (npx expo start --web --port 8083)
Terminal 3: Ngrok    (start-ngrok.bat)
Terminal 4: Commands (get-ngrok-urls.ps1, git, etc.)
```

### 2. Save Your URLs

After running `get-ngrok-urls.ps1`, copy the URLs somewhere safe:
- **Frontend URL:** Share this with testers
- **Backend URL:** Needed for config updates

### 3. Update Backend CORS

Every time you get new ngrok URLs (after restart), update backend CORS:

```env
BACKEND_CORS_ORIGINS=["http://localhost:8083","https://YOUR-NEW-FRONTEND.ngrok.io"]
```

### 4. Security Considerations

⚠️ **Important:**
- Don't share your ngrok URLs publicly if you have sensitive data
- Don't commit ngrok URLs to git (they change every session on free plan)
- Consider using ngrok's authentication features for extra security
- Monitor the ngrok dashboard for unexpected traffic

### 5. Free Plan Limitations

Ngrok free plan includes:
- ✅ Random URLs (changes each restart)
- ✅ 2-hour session limit
- ✅ Up to 40 connections/minute
- ❌ No custom subdomains
- ❌ No reserved domains

For production use, consider upgrading to a paid plan.

---

## Script Reference

### `start-ngrok.bat`
- **Purpose:** Start ngrok tunnels for both services
- **Usage:** Double-click or run `start-ngrok.bat`
- **What it does:**
  - Validates ngrok installation
  - Checks configuration file
  - Starts tunnels for frontend (8083) and backend (8000)
  - Shows ngrok dashboard

### `get-ngrok-urls.ps1`
- **Purpose:** Retrieve public URLs and update config
- **Usage:** `powershell -ExecutionPolicy Bypass -File .\get-ngrok-urls.ps1`
- **What it does:**
  - Queries ngrok API (localhost:4040)
  - Displays frontend and backend URLs
  - Offers to update frontend config automatically
  - Creates config backup before changes

### `ngrok.yml`
- **Purpose:** Configuration for ngrok tunnels
- **Contains:**
  - Auth token
  - Tunnel definitions (frontend, backend)
  - Port mappings
  - TLS settings

---

## Complete Workflow

Here's the complete workflow from start to finish:

### First Time Setup
```bash
# 1. Install ngrok (one time)
# Download from ngrok.com/download

# 2. Configure auth token (one time)
# Edit ngrok.yml with your token
```

### Every Session
```bash
# 1. Start backend
cd C:\Windows\System32\cooin-app\cooin-backend
python start_dev.py

# 2. Start frontend
cd C:\Windows\System32\cooin-app\cooin-frontend
npx expo start --web --port 8083

# 3. Start ngrok
cd C:\Windows\System32\cooin-app
start-ngrok.bat

# 4. Get URLs and update config
powershell -ExecutionPolicy Bypass -File .\get-ngrok-urls.ps1
# Type 'y' when asked to update config

# 5. Restart frontend (if config was updated)
# Go to frontend terminal, press Ctrl+C
npx expo start --web --port 8083

# 6. Share your frontend URL!
# https://abc123.ngrok.io
```

---

## Quick Commands

```bash
# Check if ngrok is installed
ngrok version

# Start ngrok manually (alternative to .bat script)
ngrok start --all --config=ngrok.yml

# View ngrok dashboard
# Open browser: http://localhost:4040

# Get ngrok URLs via API (curl)
curl http://localhost:4040/api/tunnels

# Stop ngrok
# Press Ctrl+C in ngrok terminal
```

---

## Need Help?

- **Ngrok Documentation:** [https://ngrok.com/docs](https://ngrok.com/docs)
- **Ngrok Dashboard:** [https://dashboard.ngrok.com](https://dashboard.ngrok.com)
- **Ngrok Status:** [https://status.ngrok.com](https://status.ngrok.com)
- **Cooin History:** See `HISTORY.md` for app-specific issues

---

**Last Updated:** 2025-10-25
**Ngrok Version:** 3.x
**Cooin Version:** Current
