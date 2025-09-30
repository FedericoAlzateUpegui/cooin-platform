# 📱 Cooin iOS App - Installation Guide

## Method 1: Direct iPhone Installation (Easiest)

### Prerequisites:
- iPhone with iOS 14.0 or later
- Mac computer with Xcode 13+
- Apple ID (free account works)

### Step-by-Step Instructions:

#### 1. **Prepare Your Mac**
```bash
# Ensure Xcode is installed
xcode-select --install

# Clone/transfer the project to your Mac
# Navigate to the project directory
cd path/to/cooin-ios
```

#### 2. **Open Project in Xcode**
```bash
open Cooin.xcodeproj
```

#### 3. **Configure Project Settings**
- Click on "Cooin" project in the navigator
- Select "Cooin" target
- Go to "Signing & Capabilities" tab
- **Team**: Select your Apple ID team
- **Bundle Identifier**: Change to `com.yourname.cooin` (must be unique)

#### 4. **Connect Your iPhone**
- Connect iPhone to Mac via USB cable
- Trust the computer on your iPhone when prompted
- In Xcode, select your iPhone from the device dropdown (top toolbar)

#### 5. **Enable Developer Mode on iPhone**
- On iPhone: Settings → Privacy & Security → Developer Mode → ON
- Restart iPhone when prompted

#### 6. **Build and Install**
- In Xcode, press **Cmd+R** (or click the Play button)
- Xcode will build and install the app on your iPhone
- First time may require trusting the developer certificate:
  - iPhone Settings → General → VPN & Device Management
  - Trust your Apple ID under "Developer App"

---

## Method 2: Archive and Distribute

### For sharing with others or creating an IPA file:

#### 1. **Archive the App**
- In Xcode: Product → Archive
- Wait for the archive to complete

#### 2. **Export IPA**
- In Organizer window → Distribute App
- Choose "Development" or "Ad Hoc"
- Export to create an IPA file

#### 3. **Install via Third-Party Tools**
- Use AltStore, Sideloadly, or similar tools
- Install the IPA file on your iPhone

---

## Method 3: TestFlight (For Beta Distribution)

#### 1. **Upload to App Store Connect**
- Requires paid Apple Developer account ($99/year)
- Archive and upload via Xcode
- Add beta testers in App Store Connect

#### 2. **Install via TestFlight**
- Beta testers download TestFlight app
- Install Cooin via TestFlight invitation

---

## Troubleshooting

### **"Untrusted Developer" Error**
- Settings → General → VPN & Device Management
- Find your Apple ID under "Developer App"
- Tap and select "Trust"

### **"Could not launch" Error**
- Ensure iPhone is unlocked
- Check that Developer Mode is enabled
- Restart both iPhone and Xcode

### **Code Signing Issues**
- Verify Apple ID is signed in to Xcode
- Change bundle identifier to something unique
- Clean build folder (Cmd+Shift+K) and retry

### **Network Issues**
- Ensure iPhone and backend server are on same network
- Check that backend is running on `http://192.168.40.34:8000`
- Test backend connectivity from iPhone Safari

---

## Backend Requirements

### **Ensure Backend is Running:**
```bash
# In your backend directory
cd cooin-backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **Network Configuration:**
- Backend must be accessible from iPhone's network
- If using different IP, update `APIClient.swift`:
  ```swift
  private let baseURL = "http://YOUR_IP_ADDRESS:8000/api/v1"
  ```

---

## Quick Start Commands

```bash
# 1. Open project
cd cooin-ios && open Cooin.xcodeproj

# 2. In Xcode:
#    - Connect iPhone
#    - Select iPhone as target
#    - Press Cmd+R to run

# 3. On iPhone:
#    - Trust developer in Settings
#    - Launch Cooin app
```

---

## App Features to Test

✅ **Authentication**
- [ ] Register new account
- [ ] Login with credentials
- [ ] Role selection (borrower/lender)

✅ **Dashboard**
- [ ] View platform statistics
- [ ] Pull to refresh data
- [ ] Navigate between tabs

✅ **Loan Matching**
- [ ] Create loan request (borrower)
- [ ] Create lending offer (lender)
- [ ] Browse opportunities
- [ ] View matches

✅ **Profile & Verification**
- [ ] Edit profile information
- [ ] Upload documents via camera
- [ ] Upload from photo library
- [ ] View verification status

✅ **Analytics**
- [ ] Platform overview
- [ ] Financial metrics
- [ ] Growth insights

---

## Need Help?

### **Common Questions:**

**Q: Do I need a paid Apple Developer account?**
A: No, a free Apple ID works for personal development and testing.

**Q: Can I install on multiple devices?**
A: Yes, but each device needs to be registered and trusted.

**Q: How long does the app stay installed?**
A: Free developer certificates expire after 7 days. Paid accounts last 1 year.

**Q: Can I distribute to friends?**
A: Yes, using Ad Hoc distribution or TestFlight (paid account required).

### **Support:**
- Check Xcode console for detailed error messages
- Ensure all file paths are correct
- Verify network connectivity to backend server