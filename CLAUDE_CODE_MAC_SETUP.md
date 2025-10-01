# 🍎 Claude Code Setup Guide for Mac

## 🎯 **Complete Step-by-Step Setup for Mac**

---

## **Step 1: Download Claude Code for Mac**

### **Method A: Direct Download (Recommended)**
1. **Open Safari** on your Mac
2. **Go to:** https://claude.ai/code
3. **Click "Download"** or look for Mac download button
4. **Select "Download for Mac"** (will download .dmg file)
5. **Wait for download** to complete

### **Method B: Alternative Download**
If direct link doesn't work:
1. **Visit:** https://anthropic.com/claude-code
2. **Look for Mac version** download link
3. **Download the .dmg installer**

---

## **Step 2: Install Claude Code**

### **Installation Process:**
1. **Locate downloaded file** (usually in Downloads folder)
   - File name: `Claude-Code-Mac.dmg` (or similar)

2. **Double-click the .dmg file** to mount it

3. **Drag Claude Code** to Applications folder
   - You'll see Claude Code icon and Applications folder
   - Drag Claude Code → Applications

4. **Eject the .dmg** (right-click → Eject)

### **First Launch:**
1. **Open Applications** folder (Cmd+Space → "Applications")
2. **Find Claude Code** and double-click to open
3. **Allow app to run** if macOS asks for permission:
   - Click "Open" when prompted
   - If blocked: System Preferences → Security & Privacy → "Open Anyway"

---

## **Step 3: Sign In & Activate License**

### **Account Setup:**
1. **Launch Claude Code** from Applications
2. **Sign in** with your Anthropic account:
   - Same email/password you used on Windows
   - Click "Sign In" or "Get Started"

3. **License Transfer:**
   - Your license should **automatically sync** with your account
   - If prompted, use the same login credentials

### **If License Issues:**
1. **Check your account** at https://claude.ai
2. **Contact Anthropic Support:**
   - Go to: https://support.anthropic.com
   - Subject: "Claude Code License Transfer to Mac"
   - Include: Your account email and license details

---

## **Step 4: Configure Claude Code for Development**

### **Basic Configuration:**
1. **Open Claude Code Preferences:**
   - Claude Code → Preferences (or Cmd+,)

2. **Set up workspace:**
   - Choose default project directory
   - Configure coding preferences

3. **Enable extensions/plugins** if available

### **Terminal Integration:**
1. **Open Terminal** (Cmd+Space → "Terminal")
2. **Test Claude Code CLI** (if available):
   ```bash
   claude-code --version
   ```
3. **Add to PATH** if needed (follow app instructions)

---

## **Step 5: Open Your Cooin Project**

### **After Cloning from GitHub:**
```bash
# Navigate to your project
cd ~/Documents/cooin-platform

# Open in Claude Code (if CLI available)
claude-code .

# Or manually:
# 1. Open Claude Code app
# 2. File → Open → Navigate to cooin-platform folder
# 3. Select the folder and open
```

### **Project Structure in Claude Code:**
You should see:
```
cooin-platform/
├── cooin-backend/     # FastAPI backend
├── cooin-ios/         # SwiftUI iOS app
├── README.md          # Documentation
└── .gitignore         # Git ignore rules
```

---

## **Step 6: Test Claude Code Features**

### **Essential Features to Test:**
1. **File Navigation:**
   - Browse project files
   - Search across files (Cmd+Shift+F)

2. **Code Editing:**
   - Open a .swift or .py file
   - Test syntax highlighting
   - Try code completion

3. **AI Features:**
   - Ask Claude about your code
   - Request code explanations
   - Get development suggestions

4. **Git Integration:**
   - View git status
   - Make commits
   - Push/pull changes

---

## **Step 7: Useful Mac Shortcuts**

### **Claude Code Shortcuts:**
- **Open file:** Cmd+O
- **Quick search:** Cmd+P
- **Find in files:** Cmd+Shift+F
- **Command palette:** Cmd+Shift+P
- **New file:** Cmd+N
- **Save:** Cmd+S
- **Preferences:** Cmd+,

### **Mac System Shortcuts:**
- **Spotlight search:** Cmd+Space
- **App switcher:** Cmd+Tab
- **Force quit:** Cmd+Option+Esc
- **Screenshot:** Cmd+Shift+4

---

## **Step 8: Troubleshooting Common Issues**

### **App Won't Open:**
```bash
# Check if app is in Applications
ls /Applications/ | grep -i claude

# Reset app permissions
sudo xattr -rd com.apple.quarantine /Applications/Claude\ Code.app
```

### **License Not Recognized:**
1. **Sign out and back in:**
   - Claude Code → Account → Sign Out
   - Restart app and sign in again

2. **Clear app data:**
   - Quit Claude Code completely
   - Delete: `~/Library/Application Support/Claude Code`
   - Restart and sign in

3. **Check internet connection:**
   - License verification requires internet
   - Try different network if needed

### **Can't Open Project:**
1. **Check file permissions:**
   ```bash
   # Make sure you own the project folder
   sudo chown -R $(whoami) ~/Documents/cooin-platform
   ```

2. **Project not showing:**
   - File → Open Folder
   - Navigate to exact project location
   - Select entire `cooin-platform` folder

---

## **Step 9: Optimize for Development**

### **Performance Settings:**
1. **Close unnecessary apps** to free RAM
2. **Enable/disable** features you don't need
3. **Set up** file watchers for auto-reload

### **Workspace Setup:**
1. **Pin frequently used files**
2. **Set up** split screen with Terminal
3. **Configure** color themes for better visibility

### **Integration with Other Tools:**
- **Xcode** for iOS development
- **Terminal** for command line tasks
- **Safari** for testing web features
- **Git** for version control

---

## **Step 10: Verify Everything Works**

### **✅ Final Checklist:**

**Claude Code Installation:**
- [ ] App installed in Applications folder
- [ ] App launches without errors
- [ ] Successfully signed into account
- [ ] License activated and working

**Project Access:**
- [ ] Can open cooin-platform folder
- [ ] File tree shows all project files
- [ ] Can edit .swift files (iOS)
- [ ] Can edit .py files (backend)
- [ ] Syntax highlighting works

**AI Features:**
- [ ] Can ask Claude questions about code
- [ ] Code suggestions work
- [ ] File search and navigation work
- [ ] Git integration functional

**Development Ready:**
- [ ] Can open Terminal from Claude Code
- [ ] Project files are editable
- [ ] Ready to continue Cooin development

---

## **🎉 Success! You're Ready to Develop**

### **What You Can Do Now:**
1. **Continue iOS development** with full Claude Code support
2. **Enhance backend features** with AI assistance
3. **Get code explanations** and suggestions
4. **Maintain version control** with integrated Git
5. **Collaborate** and document your platform

### **Next Steps:**
1. **Clone your Cooin project** from GitHub
2. **Open in Claude Code** for development
3. **Set up backend** on Mac
4. **Build iOS app** with Xcode
5. **Continue platform development**

---

## **🆘 Need Help?**

### **Resources:**
- **Claude Code Documentation:** https://docs.claude.com/code
- **Anthropic Support:** https://support.anthropic.com
- **Community:** https://discord.gg/anthropic (if available)

### **Common Commands:**
```bash
# Open project in Claude Code
claude-code ~/Documents/cooin-platform

# Check Claude Code version
claude-code --version

# Open current directory
claude-code .
```

**Your Mac is now ready for professional Cooin development with Claude Code!** 🚀