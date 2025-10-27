# Cloudflare Tunnel - Quick Start (5 Minutes)

Get your Cooin app publicly accessible in 5 minutes with permanent URLs!

## 🚀 Super Quick Setup (No Domain Required)

### Step 1: Install cloudflared (1 minute)

**Windows (choose one):**
```powershell
# Option A: Using winget (recommended)
winget install cloudflare.cloudflared

# Option B: Manual download
# Visit: https://github.com/cloudflare/cloudflared/releases/latest
# Download: cloudflared-windows-amd64.exe
# Save to project folder or C:\Windows\System32
```

**Mac:**
```bash
brew install cloudflared
```

**Linux:**
```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
sudo chmod +x /usr/local/bin/cloudflared
```

### Step 2: Start Your Services (1 minute)

**Terminal 1 - Backend:**
```bash
cd C:\Windows\System32\cooin-app\cooin-backend
python start_dev.py
# Wait for: "Uvicorn running on http://0.0.0.0:8000"
```

**Terminal 2 - Frontend:**
```bash
cd C:\Windows\System32\cooin-app\cooin-frontend
npx expo start --web --port 8083
# Wait for: "Compiled successfully"
```

### Step 3: Create Quick Tunnels (2 minutes)

**Terminal 3 - Backend Tunnel:**
```bash
cloudflared tunnel --url http://localhost:8000
```

You'll see:
```
Your quick Tunnel has been created! Visit it at:
https://random-backend-words.trycloudflare.com
```

**Copy this Backend URL!** ✂️

**Terminal 4 - Frontend Tunnel:**
```bash
cloudflared tunnel --url http://localhost:8083
```

You'll see:
```
Your quick Tunnel has been created! Visit it at:
https://random-frontend-words.trycloudflare.com
```

**Copy this Frontend URL!** ✂️

### Step 4: Update Frontend Config (1 minute)

Edit `cooin-frontend/src/constants/config.ts`:

```typescript
export const API_CONFIG = {
  BASE_URL: 'https://YOUR-BACKEND-URL.trycloudflare.com/api/v1',
  //          ↑ Paste your backend URL here
  TIMEOUT: 10000,
  RETRY_ATTEMPTS: 3,
} as const;
```

### Step 5: Update Backend CORS (30 seconds)

Edit `cooin-backend/.env`:

```env
BACKEND_CORS_ORIGINS=[
  "http://localhost:8083",
  "https://YOUR-FRONTEND-URL.trycloudflare.com"
]
```

### Step 6: Restart Services (30 seconds)

1. Stop both backend and frontend (Ctrl+C)
2. Start them again (same commands as Step 2)

### Step 7: Test It! (30 seconds)

Open the frontend URL in any browser:
```
https://YOUR-FRONTEND-URL.trycloudflare.com
```

✅ Share this URL with anyone - it works worldwide!

## 📝 Important Notes

### Quick Tunnels (trycloudflare.com)

- ✅ Free forever
- ✅ Works immediately
- ⚠️ URL changes each time you restart
- ⚠️ Need to update config.ts each session

### Persistent Tunnels (Recommended)

For URLs that never change, use named tunnels:

```bash
# One-time setup
cloudflared tunnel login
cloudflared tunnel create cooin-backend
cloudflared tunnel create cooin-frontend

# Use these forever!
```

See [CLOUDFLARE-TUNNEL-SETUP.md](./CLOUDFLARE-TUNNEL-SETUP.md) for complete guide.

## 🎯 One-Command Method

After first setup, use our automated scripts:

**Windows:**
```batch
start-cloudflare.bat
```

**Mac/Linux:**
```bash
./start-cloudflare.sh
```

## 🆚 Quick Comparison

| Method | Setup Time | URL Changes | Best For |
|--------|-----------|-------------|----------|
| **Quick Tunnel** | 5 min | Every restart | Quick demos |
| **Named Tunnel** | 10 min | Never | Production use |
| **Ngrok Free** | 5 min | Every 2 hours | Short tests |

## 🐛 Common Issues

**Problem:** "Cannot connect to localhost:8000"
```bash
# Solution: Make sure backend is running!
cd cooin-backend
python start_dev.py
```

**Problem:** CORS errors in browser
```bash
# Solution: Add frontend URL to backend .env CORS origins
```

**Problem:** "cloudflared: command not found"
```bash
# Solution: Restart terminal after installation
# Or use full path: C:\path\to\cloudflared.exe
```

**Problem:** Frontend can't reach backend
```bash
# Solution: Update BASE_URL in config.ts with backend tunnel URL
```

## ✅ What You Get

After setup:
- 🌐 Public URLs accessible from anywhere
- 🔒 Automatic HTTPS/SSL
- 🚀 Cloudflare's global CDN
- 🛡️ DDoS protection included
- 💰 100% Free, no limits
- ⏰ No time restrictions

## 📚 Next Steps

1. **For Persistent URLs:** Read [CLOUDFLARE-TUNNEL-SETUP.md](./CLOUDFLARE-TUNNEL-SETUP.md)
2. **For Production:** Read [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
3. **Share with Team:** Send them your frontend URL!

---

**Questions?** Check [CLOUDFLARE-TUNNEL-SETUP.md](./CLOUDFLARE-TUNNEL-SETUP.md) for detailed guide.
