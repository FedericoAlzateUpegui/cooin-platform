# Cloudflare Tunnel Setup - Complete Guide

Replace ngrok with Cloudflare Tunnel for free, permanent public URLs with no time limits!

## 🌟 Why Cloudflare Tunnel?

**Advantages over ngrok:**
- ✅ **100% Free** - No paid plan needed
- ✅ **Persistent URLs** - Same URL every time
- ✅ **No Time Limits** - Works forever, not just 2 hours
- ✅ **Custom Domains** - Use your own domain (optional)
- ✅ **Better Performance** - Cloudflare's global network
- ✅ **Built-in DDoS Protection**
- ✅ **No session limits** - Keep running 24/7

## 📋 Prerequisites

- Cloudflare account (free): https://dash.cloudflare.com/sign-up
- Backend running on port 8000
- Frontend running on port 8083

## 🚀 Quick Setup (5 minutes)

### Step 1: Install cloudflared

**Windows:**
```powershell
# Download cloudflared
# Visit: https://github.com/cloudflare/cloudflared/releases/latest
# Download: cloudflared-windows-amd64.exe
# Rename to: cloudflared.exe
# Move to: C:\Windows\System32\ or project folder
```

**Or use winget:**
```powershell
winget install --id Cloudflare.cloudflared
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

### Step 2: Login to Cloudflare

```bash
cloudflared tunnel login
```

This will:
1. Open your browser
2. Ask you to select a domain (or create one for free)
3. Authorize the tunnel
4. Save credentials to `~/.cloudflared/cert.pem`

### Step 3: Create Your Tunnels

```bash
# Create tunnel for backend API
cloudflared tunnel create cooin-backend

# Create tunnel for frontend
cloudflared tunnel create cooin-frontend
```

You'll see output like:
```
Tunnel credentials written to: C:\Users\YourName\.cloudflared\UUID.json
Created tunnel cooin-backend with id: abc123...
```

**💾 SAVE THE TUNNEL IDs** - You'll need them!

### Step 4: Create Configuration File

Create `cloudflare-config.yml` in your project root:

```yaml
# Cloudflare Tunnel Configuration for Cooin Platform
# DO NOT commit this file to git - contains tunnel credentials

# Backend API Tunnel
tunnel: YOUR_BACKEND_TUNNEL_ID
credentials-file: C:\Users\YOUR_USERNAME\.cloudflared\YOUR_BACKEND_UUID.json

ingress:
  # Route backend API
  - hostname: cooin-api.YOUR_DOMAIN.com
    service: http://localhost:8000

  # Catch-all rule (required)
  - service: http_status:404
```

Create another for frontend `cloudflare-frontend-config.yml`:

```yaml
# Frontend Web App Tunnel
tunnel: YOUR_FRONTEND_TUNNEL_ID
credentials-file: C:\Users\YOUR_USERNAME\.cloudflared\YOUR_FRONTEND_UUID.json

ingress:
  # Route frontend web app
  - hostname: cooin-app.YOUR_DOMAIN.com
    service: http://localhost:8083

  # Catch-all rule (required)
  - service: http_status:404
```

### Step 5: Configure DNS

```bash
# Add DNS records for backend
cloudflared tunnel route dns cooin-backend cooin-api.YOUR_DOMAIN.com

# Add DNS records for frontend
cloudflared tunnel route dns cooin-frontend cooin-app.YOUR_DOMAIN.com
```

### Step 6: Start Your Tunnels

**Terminal 1 - Backend:**
```bash
cd cooin-backend
# Start backend server first
python start_dev.py
```

**Terminal 2 - Frontend:**
```bash
cd cooin-frontend
# Start frontend
npx expo start --web --port 8083
```

**Terminal 3 - Backend Tunnel:**
```bash
cloudflared tunnel --config cloudflare-config.yml run cooin-backend
```

**Terminal 4 - Frontend Tunnel:**
```bash
cloudflared tunnel --config cloudflare-frontend-config.yml run cooin-frontend
```

## 🎯 Simplified Setup (Without Custom Domain)

If you don't have a domain, use quick tunnels (similar to ngrok):

```bash
# Backend - Terminal 1
cloudflared tunnel --url http://localhost:8000

# Frontend - Terminal 2
cloudflared tunnel --url http://localhost:8083
```

You'll get random URLs like:
- `https://random-words.trycloudflare.com`

**Note:** Quick tunnels change each session, like ngrok free.

## ⚡ One-Command Startup (Advanced)

Create `start-cloudflare.bat` for Windows:

```batch
@echo off
echo Starting Cloudflare Tunnels for Cooin Platform...
echo.

REM Start Backend Tunnel
start "Cooin Backend Tunnel" cloudflared tunnel --config cloudflare-config.yml run cooin-backend

REM Wait 2 seconds
timeout /t 2 /nobreak > nul

REM Start Frontend Tunnel
start "Cooin Frontend Tunnel" cloudflared tunnel --config cloudflare-frontend-config.yml run cooin-frontend

echo.
echo ✅ Tunnels started!
echo.
echo Backend:  https://cooin-api.YOUR_DOMAIN.com
echo Frontend: https://cooin-app.YOUR_DOMAIN.com
echo.
echo Press any key to stop tunnels...
pause > nul

REM Kill cloudflared processes
taskkill /F /IM cloudflared.exe
echo Tunnels stopped.
```

## 🔧 Configuration for Production

### Update Frontend Config

Edit `cooin-frontend/src/constants/config.ts`:

```typescript
export const API_CONFIG = {
  BASE_URL: 'https://cooin-api.YOUR_DOMAIN.com/api/v1',
  TIMEOUT: 10000,
  RETRY_ATTEMPTS: 3,
} as const;
```

### Update Backend CORS

Edit `cooin-backend/.env`:

```env
BACKEND_CORS_ORIGINS=[
  "http://localhost:8083",
  "https://cooin-app.YOUR_DOMAIN.com",
  "https://cooin-api.YOUR_DOMAIN.com"
]
```

Restart both servers after changes.

## 📱 Using Free Cloudflare Subdomain

Don't have a domain? Get a free `.pages.dev` subdomain:

1. Go to: https://pages.cloudflare.com/
2. Create a Pages project (can be empty)
3. You get: `your-project.pages.dev`
4. Use this domain for tunnels!

Or use the temporary `trycloudflare.com` URLs (change each session).

## 🔒 Security Best Practices

### 1. Protect Configuration Files

Add to `.gitignore`:
```
cloudflare-config.yml
cloudflare-frontend-config.yml
.cloudflared/
*.cloudflared/
```

### 2. Secure Tunnel Credentials

```bash
# Credentials are stored in:
# Windows: C:\Users\YourName\.cloudflared\
# Mac/Linux: ~/.cloudflared/

# Keep these files secure!
# Never commit to git
# Never share publicly
```

### 3. Access Control

Cloudflare can add authentication:

```yaml
ingress:
  - hostname: cooin-api.YOUR_DOMAIN.com
    service: http://localhost:8000
    originRequest:
      # Add Cloudflare Access for authentication
      noTLSVerify: false
```

Enable Cloudflare Access in dashboard: https://dash.cloudflare.com/

## 🐛 Troubleshooting

### "tunnel credentials file not found"

```bash
# Check if you logged in:
ls ~/.cloudflared/cert.pem

# If missing, login again:
cloudflared tunnel login
```

### "failed to sufficiently increase receive buffer size"

This is a warning, not an error. Tunnel still works.

To fix:
```bash
# Windows (as Admin):
netsh int ipv4 set subinterface "Ethernet" mtu=1500 store=persistent

# Mac:
sudo sysctl -w net.inet.tcp.recvspace=65536

# Linux:
sudo sysctl -w net.core.rmem_max=2500000
```

### "no such host"

DNS not configured. Run:
```bash
cloudflared tunnel route dns TUNNEL_NAME HOSTNAME
```

### Tunnel disconnects

Check your internet connection. Cloudflare tunnels auto-reconnect.

### "tunnel already exists"

```bash
# List existing tunnels:
cloudflared tunnel list

# Delete old tunnel if needed:
cloudflared tunnel delete TUNNEL_NAME

# Create new one:
cloudflared tunnel create TUNNEL_NAME
```

## 📊 Tunnel Management

### List All Tunnels
```bash
cloudflared tunnel list
```

### View Tunnel Info
```bash
cloudflared tunnel info TUNNEL_NAME
```

### Delete Tunnel
```bash
# First, delete DNS routes
cloudflared tunnel route dns --delete TUNNEL_NAME

# Then delete tunnel
cloudflared tunnel delete TUNNEL_NAME
```

### Cleanup Old Tunnels
```bash
cloudflared tunnel cleanup TUNNEL_NAME
```

## 🎓 Advanced Features

### Run as Service (Background)

**Windows Service:**
```bash
# Install as service
cloudflared service install

# Start service
cloudflared service start
```

**Linux Systemd:**
```bash
# Create systemd service
sudo cloudflared service install
sudo systemctl start cloudflared
sudo systemctl enable cloudflared
```

### Multiple Services (Single Tunnel)

One tunnel can route multiple ports:

```yaml
tunnel: YOUR_TUNNEL_ID
credentials-file: /path/to/UUID.json

ingress:
  - hostname: api.YOUR_DOMAIN.com
    service: http://localhost:8000

  - hostname: app.YOUR_DOMAIN.com
    service: http://localhost:8083

  - hostname: admin.YOUR_DOMAIN.com
    service: http://localhost:3000

  - service: http_status:404
```

### Load Balancing

```yaml
ingress:
  - hostname: api.YOUR_DOMAIN.com
    service: http://localhost:8000
    originRequest:
      connectTimeout: 30s
      noTLSVerify: false
      # Add more origin servers for load balancing
```

## 📚 Resources

- **Official Docs**: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/
- **Tunnel Guide**: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/tunnel-guide/
- **GitHub**: https://github.com/cloudflare/cloudflared
- **Community**: https://community.cloudflare.com/

## 🆚 Cloudflare vs Ngrok Comparison

| Feature | Cloudflare Tunnel | Ngrok (Free) |
|---------|-------------------|--------------|
| **Price** | Free forever | Free (limited) |
| **Session Time** | Unlimited | 2 hours |
| **Persistent URL** | Yes | No (random) |
| **Custom Domain** | Yes (free) | Paid only |
| **Speed** | Very fast | Fast |
| **DDoS Protection** | Included | Basic |
| **Bandwidth** | Unlimited | Limited |
| **SSL/TLS** | Automatic | Automatic |
| **Web Interface** | Yes (dashboard) | Yes (local) |

**Winner: Cloudflare Tunnel** for production use and long-term development.

## ✅ Quick Reference

```bash
# Install
winget install cloudflare.cloudflared

# Login
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create my-tunnel

# Configure DNS
cloudflared tunnel route dns my-tunnel subdomain.domain.com

# Run tunnel
cloudflared tunnel --config config.yml run my-tunnel

# Quick tunnel (no domain)
cloudflared tunnel --url http://localhost:8000

# List tunnels
cloudflared tunnel list

# Delete tunnel
cloudflared tunnel delete my-tunnel
```

---

**Ready to switch from ngrok to Cloudflare? Follow the Quick Setup section above!**

For questions, see the Troubleshooting section or visit the Cloudflare Community.
