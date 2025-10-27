# Ngrok Quick Start - Cooin Web App

## 🚀 Setup (One Time Only)

1. **Install ngrok:** Download from [ngrok.com/download](https://ngrok.com/download)
2. **Get auth token:** [dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
3. **Edit `ngrok.yml`:** Replace `YOUR_NGROK_AUTH_TOKEN_HERE` with your token

---

## ⚡ Quick Start (Every Session)

### Step 1: Start Services (3 Terminals)

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

**Terminal 3 - Ngrok:**
```bash
cd C:\Windows\System32\cooin-app
start-ngrok.bat
```

### Step 2: Get Public URLs

**Terminal 4 - PowerShell:**
```powershell
cd C:\Windows\System32\cooin-app
powershell -ExecutionPolicy Bypass -File .\get-ngrok-urls.ps1
```

Type `y` when asked to update config.

### Step 3: Restart Frontend

In Terminal 2, press **Ctrl+C**, then:
```bash
npx expo start --web --port 8083
```

### Step 4: Share Your App!

Share the frontend URL from the script output:
```
https://abc123.ngrok.io
```

---

## 📋 Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 8083
- [ ] Ngrok running and showing 2 tunnels
- [ ] Frontend config updated with ngrok backend URL
- [ ] Frontend restarted after config update
- [ ] Browser hard refreshed (Ctrl+Shift+R)

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't connect to server | Run `get-ngrok-urls.ps1` and update config |
| CORS errors | Add ngrok URL to `cooin-backend/.env` CORS origins |
| Ngrok not found | Add ngrok to PATH or copy to `C:\Windows\System32` |
| Session expired (2hrs) | Restart ngrok and update config again |

---

## 🌐 Important URLs

| Service | Local | Public (changes each session) |
|---------|-------|-------------------------------|
| Frontend | http://localhost:8083 | https://abc123.ngrok.io |
| Backend | http://localhost:8000 | https://xyz789.ngrok.io |
| Ngrok Dashboard | http://localhost:4040 | N/A |

---

## 💡 Pro Tips

- Keep ngrok dashboard open: [http://localhost:4040](http://localhost:4040)
- Monitor API requests in real-time
- Free plan: URLs change every restart (2 hour limit)
- Paid plan: Get permanent URLs and custom subdomains

---

**Full Guide:** See `NGROK-SETUP.md` for detailed instructions
