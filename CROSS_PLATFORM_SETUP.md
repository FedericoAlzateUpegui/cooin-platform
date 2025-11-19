# Cross-Platform Development Guide

## 🎯 Purpose

This guide ensures you can develop Cooin Web App on **both Windows and Mac** without configuration conflicts when committing code to Git.

---

## 🚨 The Problem We're Solving

When developing on multiple operating systems, certain settings differ:

| Setting | Windows | Mac |
|---------|---------|-----|
| **PostgreSQL Username** | Usually `postgres` | Usually your Mac username |
| **File Paths** | `C:\Users\...` | `/Users/...` |
| **Python Command** | `python` | `python3` |
| **Virtual Env Activation** | `venv\Scripts\activate` | `source venv/bin/activate` |

Previously, these differences caused issues:
- Committing `.env` with Mac username broke Windows setup
- Committing `.env` with Windows paths broke Mac setup
- Developers had to manually reconfigure after every pull

---

## ✅ The Solution

We've implemented a **multi-layered approach**:

1. **Never commit actual `.env` files** - They're gitignored
2. **Commit platform-specific templates** - `.env.mac.template` and `.env.windows.template`
3. **Auto-setup scripts** - Automatically create correct config for your OS
4. **Local overrides** - `.env.local` for personal settings (never committed)

---

## 📋 File Structure

```
cooin-platform/
├── cooin-backend/
│   ├── .env                      # ❌ Never commit (auto-generated)
│   ├── .env.local                # ❌ Never commit (your personal config)
│   ├── .env.example              # ✅ Commit (generic template)
│   ├── .env.mac.template         # ✅ Commit (Mac defaults)
│   ├── .env.windows.template     # ✅ Commit (Windows defaults)
│   └── setup_env.py              # ✅ Commit (auto-setup script)
│
├── cooin-frontend/
│   ├── .env                      # ❌ Never commit
│   ├── .env.local                # ❌ Never commit
│   ├── .env.example              # ✅ Commit
│   └── setup-env.js              # ✅ Commit (auto-setup script)
│
└── .gitignore                    # Ignores all .env* files
```

---

## 🚀 First-Time Setup on Any Machine

### Step 1: Clone the Repository

```bash
# Windows
cd C:\Users\YourUsername\Desktop
git clone <repository-url>
cd cooin-platform

# Mac
cd /Users/YourUsername/Desktop
git clone <repository-url>
cd cooin-platform
```

### Step 2: Backend Setup

#### Option A: Automated Setup (Recommended)

**On Mac:**
```bash
cd cooin-backend
python3 setup_env.py
```

**On Windows:**
```cmd
cd cooin-backend
python setup_env.py
```

The script will:
1. Detect your OS automatically
2. Ask for your PostgreSQL username (suggests correct default)
3. Ask for your PostgreSQL password
4. Generate a secure SECRET_KEY
5. Create `.env.local` with correct settings
6. Copy to `.env` if it doesn't exist

#### Option B: Manual Setup

**On Mac:**
```bash
cd cooin-backend
cp .env.mac.template .env.local

# Edit .env.local and replace:
# - your_mac_username → Your actual Mac username (e.g., mariajimenez)
# - GENERATE_ME_USING_COMMAND_ABOVE → Run: python3 -c "import secrets; print(secrets.token_urlsafe(64))"

# Then copy to .env
cp .env.local .env
```

**On Windows:**
```cmd
cd cooin-backend
copy .env.windows.template .env.local

# Edit .env.local and replace:
# - postgres (or set your PostgreSQL username)
# - your_postgres_password → Your actual password
# - GENERATE_ME_USING_COMMAND_ABOVE → Run: python -c "import secrets; print(secrets.token_urlsafe(64))"

# Then copy to .env
copy .env.local .env
```

### Step 3: Frontend Setup

**On Mac:**
```bash
cd cooin-frontend
node setup-env.js
# Follow the prompts
```

**On Windows:**
```cmd
cd cooin-frontend
node setup-env.js
# Follow the prompts
```

---

## 🔄 Daily Workflow

### Starting Development

**Mac:**
```bash
# Terminal 1 - Backend
cd cooin-platform/cooin-backend
source venv/bin/activate
python3 start_dev.py

# Terminal 2 - Frontend
cd cooin-platform/cooin-frontend
npx expo start --web --port 8083
```

**Windows:**
```cmd
# Terminal 1 - Backend
cd cooin-platform\cooin-backend
venv\Scripts\activate
python start_dev.py

# Terminal 2 - Frontend
cd cooin-platform\cooin-frontend
npx expo start --web --port 8083
```

### Making Changes

1. **Code your feature** (in any OS)
2. **Test locally** (on your OS)
3. **Commit changes**:
   ```bash
   git add .
   git commit -m "feat: your feature description"
   git push
   ```

**Important:** `.env` and `.env.local` are automatically ignored by Git, so your OS-specific settings will NEVER be committed!

### Switching Between Computers

**On Mac** (after pulling from Windows):
```bash
git pull
# Your .env.local stays intact - no reconfiguration needed!
# If you need to update settings, run: python3 setup_env.py
```

**On Windows** (after pulling from Mac):
```cmd
git pull
# Your .env.local stays intact - no reconfiguration needed!
# If you need to update settings, run: python setup_env.py
```

---

## 📝 What Gets Committed vs What Doesn't

### ✅ Always Committed (Safe for Git)

- `.env.example` - Generic template with placeholder values
- `.env.mac.template` - Mac-specific defaults (no real credentials)
- `.env.windows.template` - Windows-specific defaults (no real credentials)
- `setup_env.py` / `setup-env.js` - Auto-setup scripts
- Source code files
- Documentation

### ❌ Never Committed (Gitignored)

- `.env` - Your actual environment file
- `.env.local` - Your personal overrides
- `.env.production` - Production settings
- `.env.development` - Development settings
- `.env.mac` - Mac-specific settings
- `.env.windows` - Windows-specific settings
- Secret keys, passwords, tokens

---

## 🔧 Advanced: Updating Templates

If you add a new environment variable that should be available on all platforms:

1. **Update `.env.example`** with the new variable
2. **Update `.env.mac.template`** with Mac-specific default (if different)
3. **Update `.env.windows.template`** with Windows-specific default (if different)
4. **Commit all three files**:
   ```bash
   git add cooin-backend/.env.example
   git add cooin-backend/.env.mac.template
   git add cooin-backend/.env.windows.template
   git commit -m "docs: add NEW_VARIABLE to environment templates"
   git push
   ```

5. **Notify team** to update their local `.env.local`:
   - "Hey team, I added NEW_VARIABLE. Run setup_env.py again or manually add it to your .env.local"

---

## 🐛 Troubleshooting

### Issue: "Database connection failed" after pulling

**Cause:** Someone committed their `.env` file (shouldn't happen, but if it does)

**Solution:**
```bash
# Regenerate your .env.local
python3 setup_env.py  # Mac
python setup_env.py   # Windows
```

### Issue: "SECRET_KEY not set" error

**Cause:** `.env` file is missing or incomplete

**Solution:**
```bash
# Run the setup script
python3 setup_env.py  # Mac
python setup_env.py   # Windows
```

### Issue: Changes to .env not taking effect

**Cause:** Backend caches environment variables

**Solution:**
1. Restart the backend server
2. Clear any cached processes

### Issue: Git is trying to commit my .env file

**Cause:** `.env` might have been tracked before .gitignore was updated

**Solution:**
```bash
# Remove from Git tracking (but keep local file)
git rm --cached cooin-backend/.env
git rm --cached cooin-frontend/.env
git commit -m "chore: remove .env from tracking"
git push
```

---

## 📊 Quick Reference

### Check Current Configuration

**Backend:**
```bash
python3 setup_env.py  # Choose option 2
```

**Frontend:**
```bash
node setup-env.js     # Choose option 2
```

### Regenerate Configuration

**Backend:**
```bash
python3 setup_env.py  # Choose option 1
```

**Frontend:**
```bash
node setup-env.js     # Choose option 1
```

### Verify .gitignore is Working

```bash
git status
# .env and .env.local should NOT appear in the list
# Only .env.example and templates should be tracked
```

---

## 🎯 Benefits of This Approach

✅ **No Configuration Conflicts** - Each developer has their own settings
✅ **No Manual Reconfiguration** - Pull from Git without changing .env
✅ **Security** - Secrets never committed to Git
✅ **Cross-Platform** - Works seamlessly on Windows, Mac, Linux
✅ **Easy Onboarding** - New developers run one script
✅ **Maintainable** - Templates document all available settings

---

## 📚 Related Documentation

- [HOW-TO-LAUNCH-WEB-APP.md](./HOW-TO-LAUNCH-WEB-APP.md) - How to start the app
- [MAC_SETUP_INSTRUCTIONS.md](./MAC_SETUP_INSTRUCTIONS.md) - Mac-specific setup
- [README.md](./README.md) - Project overview
- [DOCUMENTATION_PROCESS.md](./DOCUMENTATION_PROCESS.md) - How to document changes

---

**Last Updated**: 2025-11-17 (Session 15)
**Maintained By**: Development Team
