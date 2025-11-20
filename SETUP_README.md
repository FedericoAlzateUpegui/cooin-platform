# 🚀 Quick Setup Guide - Windows & Mac Compatible

## For First-Time Setup

### Option 1: Automated Setup (Easiest)

**On Mac:**
```bash
./setup-all.sh
```

**On Windows:**
```cmd
setup-all.bat
```

### Option 2: Manual Setup

#### Backend Setup

**Mac:**
```bash
cd cooin-backend
python3 setup_env.py
```

**Windows:**
```cmd
cd cooin-backend
python setup_env.py
```

#### Frontend Setup

**Mac/Windows:**
```bash
cd cooin-frontend
node setup-env.js
```

---

## What This Does

✅ Detects your operating system automatically
✅ Creates `.env.local` with correct settings for your OS
✅ Generates secure SECRET_KEY
✅ Sets up database connection with correct username
✅ Configures CORS for local development
✅ **Never commits your personal settings to Git**

---

## Daily Development

### Starting the App

**Mac:**
```bash
# Terminal 1 - Backend
cd cooin-backend
source venv/bin/activate
python3 start_dev.py

# Terminal 2 - Frontend
cd cooin-frontend
npx expo start --web --port 8083
```

**Windows:**
```cmd
# Terminal 1 - Backend
cd cooin-backend
venv\Scripts\activate
python start_dev.py

# Terminal 2 - Frontend
cd cooin-frontend
npx expo start --web --port 8083
```

### After Git Pull

**No reconfiguration needed!** Your `.env.local` stays intact.

---

## 🎯 Key Points

1. **`.env` and `.env.local` are never committed** - They're in .gitignore
2. **Templates are committed** - `.env.example`, `.env.mac.template`, `.env.windows.template`
3. **Each developer has their own settings** - No conflicts between Windows/Mac
4. **Pull from Git worry-free** - Your local config won't be overwritten

---

## 📚 Full Documentation

For detailed information, see:
- **[CROSS_PLATFORM_SETUP.md](./CROSS_PLATFORM_SETUP.md)** - Complete cross-platform guide
- **[HOW-TO-LAUNCH-WEB-APP.md](./HOW-TO-LAUNCH-WEB-APP.md)** - How to launch the app
- **[MAC_SETUP_INSTRUCTIONS.md](./MAC_SETUP_INSTRUCTIONS.md)** - Mac-specific setup

---

**Questions?** Check [CROSS_PLATFORM_SETUP.md](./CROSS_PLATFORM_SETUP.md) for troubleshooting.
