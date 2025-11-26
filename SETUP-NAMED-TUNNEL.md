# Setup Cloudflare Named Tunnel (Persistent URL)

## Why Named Tunnels?

**Quick Tunnels** (what we've been using):
- ✅ Fast and easy
- ✅ No configuration needed
- ❌ URL changes every restart
- ❌ Need to update .env files each time

**Named Tunnels**:
- ✅ Same URL every time (persistent)
- ✅ No need to update .env files
- ✅ Custom domains (optional)
- ✅ Better for production/staging
- ⚠️ Requires one-time setup

---

## Setup Steps

### 1. Login to Cloudflare

```cmd
cloudflared tunnel login
```

This will open a browser window. Select your domain (or create a free Cloudflare account if needed).

### 2. Create Named Tunnel

```cmd
cloudflared tunnel create cooin-backend
```

**Output will look like:**
```
Tunnel credentials written to: C:\Users\USERNAME\.cloudflared\<TUNNEL-ID>.json
Created tunnel cooin-backend with id <TUNNEL-ID>
```

**Save the TUNNEL-ID** - you'll need it!

### 3. Configure DNS (Optional - for custom domain)

If you have a domain in Cloudflare:

```cmd
cloudflared tunnel route dns cooin-backend api.yourdomain.com
```

**Skip this step** if you just want the free `trycloudflare.com` URL.

### 4. Create Tunnel Configuration File

Create file: `C:\Users\USERNAME\.cloudflared\config.yml`

```yaml
tunnel: <TUNNEL-ID>
credentials-file: C:\Users\USERNAME\.cloudflared\<TUNNEL-ID>.json

ingress:
  # Backend API
  - hostname: api.yourdomain.com  # Or use *.trycloudflare.com
    service: http://localhost:8000

  # Catch-all rule (required)
  - service: http_status:404
```

**For free URL without custom domain:**
```yaml
tunnel: <TUNNEL-ID>
credentials-file: C:\Users\USERNAME\.cloudflared\<TUNNEL-ID>.json

ingress:
  - service: http://localhost:8000
```

### 5. Run Named Tunnel

```cmd
cloudflared tunnel run cooin-backend
```

**First time output will show:**
```
Your free tunnel URL: https://random-words.trycloudflare.com
```

This URL will **stay the same** every time you run the tunnel!

### 6. Update Environment Variables (One Time Only!)

**cooin-backend\.env:**
```env
BACKEND_CORS_ORIGINS=["https://random-words.trycloudflare.com","http://localhost:8083"]
```

**cooin-frontend\.env:**
```env
EXPO_PUBLIC_API_URL=https://random-words.trycloudflare.com/api/v1
```

### 7. Create Startup Script

Create `start-named-tunnel.bat`:

```batch
@echo off
echo Starting Cloudflare Named Tunnel: cooin-backend
cloudflared tunnel run cooin-backend
```

---

## Usage After Setup

1. Terminal 1: `start-backend.bat` (backend server)
2. Terminal 2: `start-named-tunnel.bat` (tunnel - same URL every time!)
3. Terminal 3: `start-frontend.bat` (frontend)

**URL never changes!** 🎉

---

## Multiple Tunnels (Backend + Frontend)

You can create separate tunnels:

```cmd
cloudflared tunnel create cooin-backend
cloudflared tunnel create cooin-frontend
```

**config.yml for multiple services:**
```yaml
# Run both with: cloudflared tunnel run cooin-backend
tunnel: <BACKEND-TUNNEL-ID>
credentials-file: C:\Users\USERNAME\.cloudflared\<BACKEND-TUNNEL-ID>.json

ingress:
  - hostname: api.yourdomain.com
    service: http://localhost:8000
  - hostname: app.yourdomain.com
    service: http://localhost:8083
  - service: http_status:404
```

---

## Troubleshooting

**Error: "tunnel credentials not found"**
- Make sure the credentials file path in config.yml is correct
- Check that the file exists: `dir C:\Users\USERNAME\.cloudflared\*.json`

**Error: "tunnel with that name already exists"**
- List existing tunnels: `cloudflared tunnel list`
- Delete if needed: `cloudflared tunnel delete cooin-backend`

**Tunnel URL not working:**
- Check backend is running: http://localhost:8000/health
- Verify tunnel is running: look for "Connection registered" in output
- Check CORS configuration in backend .env

---

## Quick Reference

```cmd
# List tunnels
cloudflared tunnel list

# Delete tunnel
cloudflared tunnel delete cooin-backend

# Run tunnel
cloudflared tunnel run cooin-backend

# Check tunnel info
cloudflared tunnel info cooin-backend

# Cleanup old credentials
cloudflared tunnel cleanup cooin-backend
```

---

**Benefits:**
- ✅ Set once, use forever
- ✅ No more URL updates
- ✅ Professional setup
- ✅ Ready for staging/production

**Last Updated:** 2025-11-21 (Session 17)
