# 🚚 Transfer Cooin Project & Claude Code to Mac

## 📋 **Complete Migration Guide**

### **Part 1: Prepare Files for Transfer**

#### **Step 1: Create Transfer Package**
On your Windows machine, we need to package the project:

```bash
# Navigate to the main project directory
cd C:\Windows\System32\cooin-app

# Create a clean package (excluding unnecessary files)
# You'll copy these directories:
```

**📁 What to Transfer:**
```
cooin-app/
├── cooin-backend/          # Complete backend API
├── cooin-ios/              # Complete iOS app
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
```

---

### **Part 2: Transfer Methods (Choose One)**

#### **Method A: USB Drive (Recommended)**
1. **Insert USB drive** (needs ~500MB space)
2. **Copy entire cooin-app folder** to USB drive
3. **Safely eject** USB drive
4. **Connect to Mac** and copy to desired location

#### **Method B: Cloud Storage**
1. **Upload to Google Drive/Dropbox/OneDrive:**
   - Upload entire `cooin-app` folder
   - Wait for sync to complete
2. **Download on Mac:**
   - Install cloud service app on Mac
   - Download the `cooin-app` folder

#### **Method C: Network Transfer**
1. **Enable file sharing** on Windows
2. **Connect Mac to same network**
3. **Access Windows machine** from Mac Finder
4. **Copy cooin-app folder** directly

#### **Method D: GitHub (Advanced)**
```bash
# On Windows (if you have git)
cd C:\Windows\System32\cooin-app
git init
git add .
git commit -m "Initial Cooin project"
git remote add origin https://github.com/yourusername/cooin.git
git push -u origin main

# On Mac
git clone https://github.com/yourusername/cooin.git
```

---

### **Part 3: Set Up Mac Environment**

#### **Step 1: Install Prerequisites on Mac**
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11+
brew install python@3.11

# Install Node.js (for any future web features)
brew install node

# Verify installations
python3 --version
node --version
```

#### **Step 2: Install Xcode**
1. **Open App Store** on Mac
2. **Search for "Xcode"**
3. **Click Install** (large download ~10GB)
4. **Wait for installation** to complete
5. **Open Xcode** and accept license agreements

---

### **Part 4: Set Up Claude Code on Mac**

#### **Step 1: Install Claude Code**
```bash
# Method 1: Direct download (Recommended)
# Go to: https://claude.ai/code
# Download Mac version and install

# Method 2: Using Homebrew (if available)
brew install --cask claude-code
```

#### **Step 2: Transfer Claude Code License**
Your Claude Code license should be tied to your Anthropic account:

1. **Sign in to Claude Code** on Mac with same account
2. **License should automatically sync**
3. **If issues:** Contact Anthropic support with your license key

---

### **Part 5: Set Up Backend on Mac**

#### **Step 1: Navigate to Backend**
```bash
# After transferring files
cd ~/cooin-app/cooin-backend  # Adjust path as needed
```

#### **Step 2: Create Virtual Environment**
```bash
# Create virtual environment
python3 -m venv cooin-env

# Activate virtual environment
source cooin-env/bin/activate

# You should see (cooin-env) in your terminal prompt
```

#### **Step 3: Install Dependencies**
```bash
# Install Python packages
pip install -r requirements.txt

# Install additional packages if needed
pip install uvicorn fastapi sqlalchemy bcrypt python-multipart
```

#### **Step 4: Set Up Database**
```bash
# Initialize database
python -c "
from app.database import engine
from app.models import Base
Base.metadata.create_all(bind=engine)
print('Database initialized successfully!')
"
```

#### **Step 5: Start Backend Server**
```bash
# Start the API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# You should see:
# INFO: Uvicorn running on http://0.0.0.0:8000
```

#### **Step 6: Test Backend**
```bash
# In a new terminal, test the API
curl http://localhost:8000/api/v1/health

# Should return: {"status": "healthy", "version": "1.0.0"}
```

---

### **Part 6: Set Up iOS App**

#### **Step 1: Open iOS Project**
```bash
# Navigate to iOS project
cd ~/cooin-app/cooin-ios

# Open in Xcode
open Cooin.xcodeproj
```

#### **Step 2: Configure Xcode Project**
1. **In Xcode:**
   - Click "Cooin" project in left sidebar
   - Select "Cooin" target
   - Go to "Signing & Capabilities" tab

2. **Set Development Team:**
   - Add your Apple ID: Xcode → Preferences → Accounts → +
   - Select your Apple ID from "Team" dropdown

3. **Change Bundle Identifier:**
   - Change from `com.yourcompany.cooin`
   - To something unique like `com.yourname.cooin`

#### **Step 3: Update API URL (if needed)**
If your Mac has a different IP address:

1. **Find Mac IP address:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

2. **Update APIClient.swift:**
   - Open `Cooin/Services/APIClient.swift`
   - Change the baseURL to your Mac's IP:
```swift
private let baseURL = "http://YOUR_MAC_IP:8000/api/v1"
```

---

### **Part 7: Install on iPhone**

#### **Step 1: Connect iPhone**
1. **Connect iPhone** to Mac via USB cable
2. **Unlock iPhone** and trust computer when prompted
3. **Enable Developer Mode** (iOS 16+):
   - Settings → Privacy & Security → Developer Mode → ON

#### **Step 2: Build and Install**
1. **In Xcode:**
   - Select your iPhone from device dropdown (top toolbar)
   - Press **Cmd+R** or click ▶️ Play button
   - Wait for build to complete

2. **Trust Developer on iPhone:**
   - Settings → General → VPN & Device Management
   - Find your Apple ID under "Developer App"
   - Tap "Trust" and confirm

#### **Step 3: Test the App**
1. **Launch Cooin app** on iPhone
2. **Register new account** or login
3. **Test features:**
   - Dashboard with live data
   - Loan matching
   - Document upload with camera
   - Analytics screens

---

### **Part 8: Verification Checklist**

#### **✅ Backend Working:**
- [ ] Server running on Mac at port 8000
- [ ] Health endpoint responding
- [ ] Database initialized
- [ ] Can register/login users

#### **✅ iOS App Working:**
- [ ] Project opens in Xcode without errors
- [ ] Builds successfully
- [ ] Installs on iPhone
- [ ] Connects to backend API
- [ ] All features functional

#### **✅ Claude Code Working:**
- [ ] Installed on Mac
- [ ] License activated
- [ ] Can open project files
- [ ] All features accessible

---

### **🚨 Troubleshooting Common Issues**

#### **Backend Issues:**
```bash
# If port 8000 is in use
lsof -ti:8000 | xargs kill -9

# If database errors
rm -f cooin.db  # Remove old database
python -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"
```

#### **iOS Build Issues:**
- **Clean build folder:** Cmd+Shift+K in Xcode
- **Reset derived data:** Xcode → Preferences → Locations → Derived Data → Delete
- **Check bundle identifier:** Must be unique

#### **Network Issues:**
- **Firewall:** Allow port 8000 in Mac firewall settings
- **WiFi:** Ensure iPhone and Mac on same network
- **IP address:** Update APIClient.swift with correct Mac IP

---

### **📞 Support**

#### **If You Need Help:**
1. **Claude Code Issues:** Check https://docs.claude.com/code
2. **Xcode Issues:** Apple Developer Documentation
3. **Network Issues:** Check firewall and network settings
4. **Backend Issues:** Review console logs for errors

---

### **🎉 Success!**

Once everything is transferred and running, you'll have:
- ✅ **Full development environment** on Mac
- ✅ **Claude Code** for continued development
- ✅ **Working iOS app** on your iPhone
- ✅ **Live backend API** serving real data
- ✅ **Complete peer-to-peer lending platform**

**Ready to continue developing and using your Cooin app!**