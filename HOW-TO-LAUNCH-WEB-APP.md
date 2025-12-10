# How to Launch Cooin Web App (Windows 💻)

Complete guide to launching the Cooin web application for local development and sharing with partners.

---

## 📋 Prerequisites

- ✅ Python 3.10+ installed
- ✅ Node.js 18+ installed
- ✅ PostgreSQL 14+ or SQLite
- ✅ Docker Desktop (for Redis) - see [DOCKER-SETUP-GUIDE.md](./DOCKER-SETUP-GUIDE.md)
- ✅ cloudflared installed (for sharing)

---

## 🚀 Quick Launch (Local Development Only)

### Step 0: Start Redis (Docker)

**Terminal 1:**
```cmd
cd C:\Windows\System32\cooin-app
docker-compose up -d redis
docker ps  # Verify running
```

**Expected:**
```
CONTAINER ID   IMAGE            STATUS                   PORTS                    NAMES
018605d62c13   redis:7-alpine   Up 2 minutes (healthy)   0.0.0.0:6379->6379/tcp   cooin-redis
```

---

### Step 1: Start Backend

**Terminal 2:**
```cmd
cd C:\Windows\System32\cooin-app\cooin-backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Wait for:**
```
INFO: Connected to Redis cache server
INFO: Uvicorn running on http://0.0.0.0:8000
```

**Access:**
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs

---

### Step 2: Start Frontend

**Terminal 3:**
```cmd
cd C:\Windows\System32\cooin-app\cooin-frontend
npx expo start --web --port 8083
```

**Access:** http://localhost:8083

---

## 🌍 Launch with Public Access (Share with Partners)

### Step 1-2: Start Backend & Frontend (Same as Above)

---

### Step 3: Start Backend Cloudflare Tunnel

**Terminal 4:**
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

**Terminal 5:**
```cmd
cloudflared tunnel --url http://localhost:8083
```

**📋 COPY THIS URL** - This is your **Frontend Public URL** (share with partners!)

---

### Step 5: Update Configuration Files

#### 5a. Update Frontend Config

Edit `cooin-frontend\src\constants\config.ts`:
```typescript
BASE_URL: "https://YOUR-BACKEND-URL.trycloudflare.com/api/v1",
```

#### 5b. Update Backend CORS

Edit `cooin-backend\.env`:
```env
BACKEND_CORS_ORIGINS=["http://localhost:8083","https://YOUR-FRONTEND-URL.trycloudflare.com","https://YOUR-BACKEND-URL.trycloudflare.com"]
```

---

### Step 6: Restart Services

**Restart Backend (Terminal 2):**
```cmd
Ctrl+C
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Restart Frontend (Terminal 3):**
```cmd
Ctrl+C
npx expo start --web --port 8083 --clear
```

**⚠️ Keep Terminals 4 and 5 running!**

---

### Step 7: Share with Partners

Share this URL:
```
https://YOUR-FRONTEND-URL.trycloudflare.com
```

Partners can now access from any device, anywhere!

---

## 🔍 Verify Everything is Working

### Test Backend Locally
```cmd
curl http://localhost:8000/health
```
**Expected:** `{"status":"healthy"}`

### Test Backend Through Cloudflare
```cmd
curl https://YOUR-BACKEND-URL.trycloudflare.com/health
```

### Test Frontend
Open browser: `https://YOUR-FRONTEND-URL.trycloudflare.com`

---

## 🐛 Troubleshooting

### Issue: "Cannot connect to server"

**Check:**
1. Backend running? (Terminal 2 should show "Uvicorn running")
2. Backend tunnel active? (Terminal 4 shows Cloudflare URL)
3. config.ts updated with correct backend URL?

**Test:**
```cmd
curl http://localhost:8000/health
```

---

### Issue: CORS Errors in Browser

**Solution:**
1. Open `cooin-backend\.env`
2. Add both Cloudflare URLs to `BACKEND_CORS_ORIGINS`
3. Restart backend (Terminal 2)

---

### Issue: "502 Bad Gateway"

**Meaning:** Cloudflare tunnel working, but backend not responding

**Solution:**
1. Check backend running (Terminal 2)
2. Restart backend if needed
3. Wait 10 seconds, try again

---

### Issue: Frontend Loads but Can't Login

**Check:**
1. Browser console (F12) for errors
2. Verify `BASE_URL` in config.ts is correct
3. Restart frontend with `--clear` flag

---

### Issue: URLs Change Every Time

**Explanation:** Quick Cloudflare tunnels generate random URLs

**Solutions:**
1. **Accept it:** Update config files each time (5 minutes)
2. **Use Named Tunnels:** URLs never change (see [CLOUDFLARE-TUNNEL-SETUP.md](./CLOUDFLARE-TUNNEL-SETUP.md))

---

## 📝 Terminal Checklist

When running with public access, you need **5 terminals**:

- [ ] **Terminal 1:** Redis (Docker)
- [ ] **Terminal 2:** Backend server (port 8000)
- [ ] **Terminal 3:** Frontend server (port 8083)
- [ ] **Terminal 4:** Backend Cloudflare tunnel
- [ ] **Terminal 5:** Frontend Cloudflare tunnel

**All must stay open while partners use the app!**

---

## 🎯 Quick Commands Reference

### Local Development (3 Terminals)

**Terminal 1 - Redis:**
```cmd
cd C:\Windows\System32\cooin-app
docker-compose up -d redis
```

**Terminal 2 - Backend:**
```cmd
cd C:\Windows\System32\cooin-app\cooin-backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 3 - Frontend:**
```cmd
cd C:\Windows\System32\cooin-app\cooin-frontend
npx expo start --web --port 8083
```

---

### Public Sharing (+2 More Terminals)

**Terminal 4 - Backend Tunnel:**
```cmd
cloudflared tunnel --url http://localhost:8000
```

**Terminal 5 - Frontend Tunnel:**
```cmd
cloudflared tunnel --url http://localhost:8083
```

---

## 🔗 Useful URLs (When Running)

| Service | Local URL | Purpose |
|---------|-----------|---------|
| Frontend | http://localhost:8083 | Web application |
| Backend | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/api/v1/docs | Swagger UI |
| Health | http://localhost:8000/health | Backend status |

---

## ⚡ Pro Tips

1. **Use `--clear` flag** when restarting frontend to clear Metro cache
2. **Label terminals** in VS Code for easy identification
3. **Test locally first** before starting Cloudflare tunnels
4. **Save Cloudflare URLs** in a text file for easy reference
5. **Backend MUST restart** after .env changes

---

## 📚 Additional Documentation

- [CLOUDFLARE-QUICKSTART.md](./CLOUDFLARE-QUICKSTART.md) - Quick setup (5 min)
- [README.md](./README.md) - Complete project documentation
- [HISTORY.md](./HISTORY.md) - Session history
- [TODO.md](./TODO.md) - Current tasks

---

**Last Updated:** 2025-12-06 (Session 17)
**Status:** Production Ready ✅
