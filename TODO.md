# Cooin Web App - TODO

## 🚀 Current Session (Session 7) - Cloudflare Tunnel

### Pending Actions
- [ ] **Restart Backend** - `"C:\Users\Usuario\AppData\Local\Microsoft\WindowsApps\python.exe" -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- [ ] **Restart Frontend** - `npx expo start --web --port 8083 --clear`
- [ ] **Test** - `https://hobby-wax-option-shakira.trycloudflare.com`
- [ ] **Share URL** with partners

### Terminal Setup (4 required)
```cmd
# 1. Backend: python uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# 2. Frontend: npx expo start --web --port 8083 --clear
# 3. Backend Tunnel: cloudflared tunnel --url http://localhost:8000
# 4. Frontend Tunnel: cloudflared tunnel --url http://localhost:8083
```

---

## 📋 Technical Improvements

### Python Environment
- [ ] Set up virtual environment (prevents PATH conflicts)
  ```cmd
  cd cooin-backend
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  ```
- [ ] Create backend startup script (`start-backend.bat`)

### Cloudflare
- [ ] Consider named tunnels for persistent URLs (vs random URLs that change)
- [ ] Optional: Custom domain configuration

---

## 🐛 Known Issues

- ⚠️ **Project in System32** - Permission issues. Solution: Move to `C:\Users\USERNAME\Documents\cooin-app` or run `fix-permissions.bat` as admin
- ⚠️ **Multiple Python Installations** - Use full path or virtual environment
- ⚠️ **Ngrok Reserved Domain** - Delete from https://dashboard.ngrok.com/cloud-edge/domains if using ngrok

---

## 🔧 Future Enhancements

### Automation
- [ ] All-in-one startup script (backend + frontend + tunnels)
- [ ] Auto-update config with tunnel URLs

### Deployment
- [ ] Move project out of System32
- [ ] Implement automated deployment workflow
- [ ] Payment integration
- [ ] Admin dashboard

---

## 📚 Key Commands Reference

### Backend
```cmd
# With full Python path
"C:\Users\Usuario\AppData\Local\Microsoft\WindowsApps\python.exe" -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# With venv
venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```cmd
npx expo start --web --port 8083 --clear
```

### Cloudflare Tunnel
```cmd
cloudflared tunnel --url http://localhost:8000   # Backend
cloudflared tunnel --url http://localhost:8083   # Frontend
```

### Ngrok (Alternative)
```cmd
ngrok http 8000   # Backend
ngrok http 8083   # Frontend
```

---

**Last Updated**: 2025-11-03 (Session 7)
