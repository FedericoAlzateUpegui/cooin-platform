# Quick Start - Mac 🚀

**Last Updated**: 2025-11-16

---

## ⚡ Start Development (Daily Use)

### Option 1: Copy-Paste Commands

**Terminal 1 - Backend:**
```bash
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-backend && source venv/bin/activate && python3 start_dev.py
```

**Terminal 2 - Frontend:**
```bash
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-frontend && npx expo start --web --port 8083
```

### Option 2: Step by Step

**Terminal 1:**
```bash
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-backend
source venv/bin/activate
python3 start_dev.py
```

**Terminal 2:**
```bash
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-frontend
npx expo start --web --port 8083
```

---

## 🌐 Access the App

- **Frontend**: http://localhost:8083
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## 🔐 Login Credentials

**Test User:**
- Email: `test3@test.com`
- Password: `password123`

**Or create a new account** by clicking "Sign up" in the app!

---

## 🛑 Stop Development

Press `Ctrl+C` in both terminal windows.

---

## 🔧 Common Issues

### "Cannot connect to server"
- Make sure backend is running (Terminal 1)
- Check backend shows: `Uvicorn running on http://0.0.0.0:8000`
- Restart backend if needed

### "Port already in use"
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 8083
lsof -ti:8083 | xargs kill -9
```

### Backend won't start
```bash
# Check if PostgreSQL is running
brew services list | grep postgresql

# Start PostgreSQL if needed
brew services start postgresql@14
```

---

## 📖 More Information

- **Full Mac Setup Guide**: [MAC_SETUP_INSTRUCTIONS.md](./MAC_SETUP_INSTRUCTIONS.md)
- **All Commands**: [TODO.md](./TODO.md)
- **Change History**: [HISTORY.md](./HISTORY.md)
- **Project Overview**: [README.md](./README.md)

---

## 🆘 Troubleshooting Tool

Open in browser to diagnose connection issues:
```bash
open /Users/mariajimenez/Desktop/cooin-platform/test-connection.html
```

---

**That's it! Happy coding! 💻**
