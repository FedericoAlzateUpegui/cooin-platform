# How to Launch Cooin Web App

Complete guide to launching the Cooin web application for local development and sharing with partners.

---

## 📋 Prerequisites

Before launching, ensure you have:

- ✅ Python 3.10+ installed
- ✅ Node.js 18+ installed
- ✅ PostgreSQL 14+ or SQLite (for development)
- ✅ cloudflared installed (for sharing with partners)

---

## 🚀 Quick Launch (Local Development Only)

### Step 1: Start Backend

Open **Terminal 1** in VS Code:

```cmd
cd C:\Windows\System32\cooin-app\cooin-backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Wait for:**
```
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Application startup complete.
```

**Access backend at:** http://localhost:8000
**API Docs at:** http://localhost:8000/api/v1/docs

---

### Step 2: Start Frontend

Open **Terminal 2** in VS Code:

```cmd
cd C:\Windows\System32\cooin-app\cooin-frontend
npx expo start --web --port 8083
```

**Wait for:**
```
Metro waiting on exp://...
Compiled successfully!
```

**Access webapp at:** http://localhost:8083

---

## 🌍 Launch with Public Access (Share with Partners)

To share your webapp with partners or access it from other devices, use Cloudflare Tunnel.

### Step 1: Start Backend (Same as Above)

**Terminal 1:**
```cmd
cd C:\Windows\System32\cooin-app\cooin-backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

### Step 2: Start Frontend (Same as Above)

**Terminal 2:**
```cmd
cd C:\Windows\System32\cooin-app\cooin-frontend
npx expo start --web --port 8083
```

---

### Step 3: Start Backend Cloudflare Tunnel

Open **Terminal 3** in VS Code:

```cmd
cloudflared tunnel --url http://localhost:8000
```

**You'll see:**
```
Your quick Tunnel has been created! Visit it at:
https://random-backend-words.trycloudflare.com
```

**📋 COPY THIS URL** - This is your **Backend Public URL**

---

### Step 4: Start Frontend Cloudflare Tunnel

Open **Terminal 4** in VS Code:

```cmd
cloudflared tunnel --url http://localhost:8083
```

**You'll see:**
```
Your quick Tunnel has been created! Visit it at:
https://random-frontend-words.trycloudflare.com
```

**📋 COPY THIS URL** - This is your **Frontend Public URL** (share with partners!)

---

### Step 5: Update Configuration Files

#### 5a. Update Frontend Config

Edit `cooin-frontend\src\constants\config.ts`:

```typescript
export const API_CONFIG = {
  BASE_URL: process.env.EXPO_PUBLIC_API_URL || "https://YOUR-BACKEND-URL.trycloudflare.com/api/v1",
  //                                             ↑ Paste your backend URL here
  TIMEOUT: 10000,
  RETRY_ATTEMPTS: 3,
} as const;
```

**Replace** `YOUR-BACKEND-URL.trycloudflare.com` with the URL from Terminal 3 (Backend tunnel).

---

#### 5b. Update Backend CORS

Edit `cooin-backend\.env`:

```env
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8080","http://localhost:8081","http://localhost:8082","http://localhost:8083","http://localhost:8084","https://YOUR-FRONTEND-URL.trycloudflare.com","https://YOUR-BACKEND-URL.trycloudflare.com"]
```

**Replace:**
- `YOUR-FRONTEND-URL.trycloudflare.com` with URL from Terminal 4
- `YOUR-BACKEND-URL.trycloudflare.com` with URL from Terminal 3

---

### Step 6: Restart Services

#### Restart Backend (Terminal 1)

Press `Ctrl+C` to stop, then run:
```cmd
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Restart Frontend (Terminal 2)

Press `Ctrl+C` to stop, then run:
```cmd
npx expo start --web --port 8083 --clear
```

**⚠️ Keep Terminals 3 and 4 running!**

---

### Step 7: Share with Partners

Once both services restart successfully, share this URL with your partners:

```
https://YOUR-FRONTEND-URL.trycloudflare.com
```

Your partners can now:
- ✅ Access from **any device** (phone, laptop, tablet)
- ✅ Access from **anywhere in the world**
- ✅ Register accounts
- ✅ Login and use all features
- ✅ **No installation required!**

---

## 🔍 Verify Everything is Working

### Test Backend Locally

```cmd
curl http://localhost:8000/health
```

**Expected:** `{"status":"healthy"}`

---

### Test Backend Through Cloudflare

```cmd
curl https://YOUR-BACKEND-URL.trycloudflare.com/health
```

**Expected:** `{"status":"healthy"}`

---

### Test Frontend

Open your browser to:
```
https://YOUR-FRONTEND-URL.trycloudflare.com
```

**Expected:**
- Login page loads correctly
- Can create account
- Can login
- No CORS errors in browser console (F12)

---

## 🐛 Troubleshooting

### Issue: "Cannot connect to server"

**Check:**
1. Is backend running? (Terminal 1 should show "Uvicorn running")
2. Is backend tunnel active? (Terminal 3 should show Cloudflare URL)
3. Is config.ts updated with correct backend URL?

**Test:**
```cmd
curl http://localhost:8000/health
```

**If this fails:** Backend is not running. Restart Terminal 1.

---

### Issue: CORS Errors in Browser Console

**Symptoms:**
```
Access to fetch at 'https://...' from origin 'https://...' has been blocked by CORS policy
```

**Solution:**
1. Open `cooin-backend\.env`
2. Add both Cloudflare URLs to `BACKEND_CORS_ORIGINS`
3. Restart backend (Terminal 1)

---

### Issue: "502 Bad Gateway"

**Meaning:** Cloudflare tunnel is working, but backend is not responding.

**Solution:**
1. Check if backend is running (Terminal 1)
2. Restart backend if needed
3. Wait 10 seconds for backend to fully start
4. Try again

---

### Issue: Frontend Loads but Can't Login

**Check:**
1. Open browser console (F12)
2. Look for network errors
3. Verify `BASE_URL` in config.ts is correct
4. Restart frontend with `--clear` flag

---

### Issue: "Module not found" Error (Backend)

**Problem:** Python not in PATH or wrong Python version.

**Solution:** Use simple Python command:
```cmd
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

See [README.md](./README.md) Common Issues section for more details.

---

### Issue: URLs Change Every Time

**Explanation:** Quick Cloudflare tunnels generate random URLs each restart.

**Solution Options:**
1. **Accept it:** Update config files each time (5 minutes)
2. **Use Named Tunnels:** URLs never change (see [CLOUDFLARE-TUNNEL-SETUP.md](./CLOUDFLARE-TUNNEL-SETUP.md))
3. **Use Custom Domain:** Professional URLs (requires Cloudflare account)

---

## 📝 Terminal Checklist

When running with public access, you need **4 terminals**:

- [ ] **Terminal 1:** Backend server running (port 8000)
- [ ] **Terminal 2:** Frontend server running (port 8083)
- [ ] **Terminal 3:** Backend Cloudflare tunnel active
- [ ] **Terminal 4:** Frontend Cloudflare tunnel active

**All 4 must stay open while partners use the app!**

---

## 🎯 Quick Commands Reference

### Start Everything

**Terminal 1 - Backend:**
```cmd
cd C:\Windows\System32\cooin-app\cooin-backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```cmd
cd C:\Windows\System32\cooin-app\cooin-frontend
npx expo start --web --port 8083
```

**Terminal 3 - Backend Tunnel:**
```cmd
cloudflared tunnel --url http://localhost:8000
```

**Terminal 4 - Frontend Tunnel:**
```cmd
cloudflared tunnel --url http://localhost:8083
```

---

### Stop Everything

Press `Ctrl+C` in each terminal to stop all services.

---

## 📚 Additional Documentation

- [CLOUDFLARE-QUICKSTART.md](./CLOUDFLARE-QUICKSTART.md) - Quick Cloudflare setup (5 minutes)
- [README.md](./README.md) - Complete project documentation
- [HISTORY.md](./HISTORY.md) - Session history and troubleshooting
- [TODO.md](./TODO.md) - Current tasks and next steps

---

## 🔗 Useful URLs (When Running)

| Service | Local URL | Purpose |
|---------|-----------|---------|
| Frontend | http://localhost:8083 | Web application |
| Backend | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/api/v1/docs | Swagger UI |
| Health Check | http://localhost:8000/health | Backend status |

---

## ⚡ Pro Tips

1. **Use `--clear` flag** when restarting frontend to clear Metro cache
2. **Keep terminals organized** - label them in VS Code
3. **Test locally first** before starting Cloudflare tunnels
4. **Save Cloudflare URLs** in a text file for easy reference
5. **Backend MUST restart** after .env changes (--reload doesn't watch .env)

---

**Last Updated:** 2025-11-03 (Session 7)
**Status:** Production Ready ✅
