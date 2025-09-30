# 🐙 Transfer Cooin Project to Mac via GitHub

## 🎯 **Perfect Choice!** GitHub is the cleanest way to transfer your project.

---

## **Part 1: Prepare Git Repository on Windows**

### **Step 1: Install Git (if not installed)**
```bash
# Download from: https://git-scm.com/downloads
# Or use Windows Package Manager
winget install Git.Git
```

### **Step 2: Navigate to Project Directory**
```bash
# Open Command Prompt or PowerShell
cd C:\Windows\System32\cooin-app
```

### **Step 3: Create .gitignore File**
```bash
# Create .gitignore to exclude unnecessary files
echo "# Python
__pycache__/
*.py[cod]
*.so
env/
venv/
cooin-env/
*.egg-info/
dist/
build/

# Database
*.db
*.sqlite
*.sqlite3

# Environment variables
.env

# Logs
*.log

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Xcode
xcuserdata/
DerivedData/
*.xcworkspace/
*.xccheckout

# Temporary files
tmp/
temp/" > .gitignore
```

### **Step 4: Initialize Git Repository**
```bash
# Initialize git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: Complete Cooin peer-to-peer lending platform

- Backend API with FastAPI, SQLAlchemy, JWT auth
- iOS app with SwiftUI, camera integration, real-time analytics
- Complete loan matching system for borrowers and lenders
- Document verification with file upload
- Mobile analytics dashboard
- Ready for production deployment"
```

---

## **Part 2: Create GitHub Repository**

### **Step 1: Create Repository on GitHub**
1. **Go to** https://github.com
2. **Sign in** to your account (or create one)
3. **Click "+" → "New repository"**
4. **Repository name:** `cooin-platform`
5. **Description:** `Peer-to-peer lending platform with iOS app and FastAPI backend`
6. **Set as:** Public (recommended) or Private
7. **Don't** initialize with README (we already have files)
8. **Click "Create repository"**

### **Step 2: Connect Local Repository to GitHub**
```bash
# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/cooin-platform.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**🎉 Your code is now on GitHub!**

---

## **Part 3: Clone on Mac**

### **Step 1: Install Prerequisites on Mac**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Git (usually pre-installed)
git --version

# Install Python 3.11
brew install python@3.11

# Verify installation
python3 --version
```

### **Step 2: Clone Repository**
```bash
# Navigate to desired directory (e.g., Documents)
cd ~/Documents

# Clone your repository
git clone https://github.com/YOUR_USERNAME/cooin-platform.git

# Navigate to project
cd cooin-platform

# Verify files transferred
ls -la
# You should see: cooin-backend/, cooin-ios/, README.md, etc.
```

---

## **Part 4: Set Up Backend on Mac**

### **Step 1: Set Up Python Environment**
```bash
cd cooin-backend

# Create virtual environment
python3 -m venv cooin-env

# Activate environment
source cooin-env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **Step 2: Initialize Database**
```bash
# Create new database
python -c "
from app.database import engine
from app.models import Base
Base.metadata.create_all(bind=engine)
print('✅ Database initialized on Mac!')
"
```

### **Step 3: Start Backend**
```bash
# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Test in new terminal
curl http://localhost:8000/api/v1/health
```

---

## **Part 5: Set Up iOS App**

### **Step 1: Install Xcode**
1. **Open App Store** on Mac
2. **Search "Xcode"** and install (free, ~10GB)
3. **Launch Xcode** and accept licenses

### **Step 2: Open iOS Project**
```bash
cd ~/Documents/cooin-platform/cooin-ios
open Cooin.xcodeproj
```

### **Step 3: Configure Project**
1. **Sign in to Xcode:**
   - Xcode → Preferences → Accounts → Add Apple ID

2. **Set Development Team:**
   - Select "Cooin" project in sidebar
   - Choose "Cooin" target
   - Signing & Capabilities → Team → Select your Apple ID

3. **Change Bundle Identifier:**
   - Change to `com.yourname.cooin` (must be unique)

### **Step 4: Update API URL (if needed)**
```bash
# Find your Mac's IP address
ifconfig | grep "inet " | grep -v 127.0.0.1
# Example output: inet 192.168.1.100

# If different from 192.168.40.34, update APIClient.swift:
# Edit cooin-ios/Cooin/Services/APIClient.swift
# Change: private let baseURL = "http://YOUR_MAC_IP:8000/api/v1"
```

---

## **Part 6: Install on iPhone**

### **Step 1: Connect iPhone**
1. **Connect iPhone** to Mac via USB
2. **Trust computer** on iPhone
3. **Enable Developer Mode** (iOS 16+): Settings → Privacy & Security → Developer Mode

### **Step 2: Build and Install**
1. **Select iPhone** as target in Xcode (top toolbar)
2. **Press Cmd+R** to build and install
3. **Trust developer** on iPhone: Settings → General → VPN & Device Management

### **Step 3: Test App**
- **Launch Cooin** on iPhone
- **Register/login** to test authentication
- **Explore all features**: dashboard, matching, camera upload, analytics

---

## **Part 7: Set Up Claude Code on Mac**

### **Step 1: Install Claude Code**
```bash
# Download from: https://claude.ai/code
# Install the Mac version
```

### **Step 2: Transfer License**
- **Sign in** with same Anthropic account
- **License should sync automatically**
- **If issues:** Contact Anthropic support

### **Step 3: Open Project in Claude Code**
```bash
# Open the project
claude-code ~/Documents/cooin-platform
```

---

## **🎉 Success Checklist**

### **✅ Verify Everything Works:**
- [ ] **Git repository** created and synced
- [ ] **Project cloned** to Mac successfully
- [ ] **Backend running** at http://localhost:8000
- [ ] **Database initialized** and responding
- [ ] **iOS app opens** in Xcode without errors
- [ ] **App builds** and installs on iPhone
- [ ] **App connects** to backend and loads data
- [ ] **Claude Code** installed and licensed
- [ ] **All features working:** auth, matching, camera, analytics

---

## **🚀 Benefits of Using GitHub:**

### **✅ Advantages:**
- ✅ **Version control** - Track all changes
- ✅ **Backup** - Code safely stored in cloud
- ✅ **Collaboration** - Easy to share with others
- ✅ **History** - See what changed and when
- ✅ **Branching** - Work on features separately
- ✅ **Documentation** - README, issues, wiki

### **📈 Future Development:**
```bash
# Continue development with Git workflow
git add .
git commit -m "Add new feature"
git push origin main

# Pull updates on any machine
git pull origin main
```

---

## **🔧 Troubleshooting**

### **Git Issues:**
```bash
# If authentication fails
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# If push fails (large files)
git lfs track "*.db"
git add .gitattributes
```

### **Network Issues:**
```bash
# Check Mac IP address
ifconfig | grep "inet "

# Test backend from iPhone's network
# Open Safari on iPhone: http://YOUR_MAC_IP:8000/api/v1/health
```

---

## **📞 Next Steps**

### **You Now Have:**
1. ✅ **Complete project** transferred to Mac via GitHub
2. ✅ **Working backend** API server
3. ✅ **iOS app** ready for iPhone installation
4. ✅ **Claude Code** for continued development
5. ✅ **Version control** for future development

### **Ready to:**
- 📱 **Install and test** the iOS app
- 💻 **Continue development** with Claude Code
- 🔄 **Make updates** and sync via Git
- 🚀 **Deploy to production** when ready

**Your complete peer-to-peer lending platform is now ready on Mac!** 🎊