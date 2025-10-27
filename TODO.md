# Cooin Web App - TODO List

## 🚀 Current Session Tasks (Session 6 - Complete)

### High Priority - Ngrok & Mobile Access

- [x] ✅ **Fix Backend Dependencies**
  - Fixed requirements.txt syntax error
  - Installed all dependencies successfully
  - **Status:** COMPLETED

- [x] ✅ **Resolve Python Path Issues**
  - Identified two Python installations
  - Found correct Python with packages
  - Created working backend startup command
  - **Status:** COMPLETED

- [x] ✅ **Fix Ngrok v3 Compatibility**
  - Updated ngrok.yml from `bind_tls` to `schemes`
  - Config now works with ngrok v3.24.0
  - **Status:** COMPLETED

- [x] ✅ **Resolve Ngrok Reserved Domain Conflicts**
  - Identified reserved domain issue
  - Provided solutions (delete domain / separate tunnels)
  - **Status:** COMPLETED (solution provided)

- [x] ✅ **Fix Batch Script for Spanish Windows**
  - Removed ellipsis from start-ngrok.bat
  - Works on Spanish Windows now
  - **Status:** COMPLETED

- [x] ✅ **Document Mobile Access Issue**
  - Explained localhost limitation
  - Provided 2-tunnel solution for iPhone access
  - **Status:** COMPLETED (documentation provided)

---

## 🎯 Immediate Next Steps

### High Priority - Complete Mobile Setup

- [ ] **Delete Ngrok Reserved Domain** (Recommended)
  - Go to: https://dashboard.ngrok.com/cloud-edge/domains
  - Delete: `squeakier-virgil-multicostate.ngrok-free.dev`
  - **Priority:** HIGH
  - **Effort:** 2 minutes
  - **Reason:** Prevents tunnel conflicts

- [ ] **Start Ngrok with Separate Tunnels**
  - Terminal 1: `ngrok http 8083` (frontend)
  - Terminal 2: `ngrok http 8000` (backend)
  - Get 2 different random URLs
  - **Priority:** HIGH
  - **Status:** Ready to execute

- [ ] **Update Frontend Config for Mobile**
  - File: `cooin-frontend/src/constants/config.ts`
  - Change: `BASE_URL: 'https://backend-ngrok-url.ngrok-free.app/api/v1'`
  - **Priority:** HIGH
  - **Status:** Waiting for ngrok URLs

- [ ] **Update Backend CORS for Ngrok**
  - File: `cooin-backend/.env`
  - Add: Both frontend and backend ngrok URLs
  - Example: `BACKEND_CORS_ORIGINS=["http://localhost:8083","https://frontend.ngrok-free.app","https://backend.ngrok-free.app"]`
  - **Priority:** HIGH
  - **Status:** Waiting for ngrok URLs

- [ ] **Restart Both Services**
  - Backend: Restart with Python command
  - Frontend: Ctrl+C and restart
  - **Priority:** HIGH
  - **Status:** After config updates

- [ ] **Test on iPhone**
  - Access frontend ngrok URL on iPhone Safari
  - Verify login/register works
  - Check browser console for errors
  - **Priority:** HIGH
  - **Status:** Final verification

---

## 🔧 Technical Improvements

### Python Environment Setup

- [ ] **Set Up Python Virtual Environment** (Highly Recommended)
  - Navigate to: `cooin-backend`
  - Run: `python -m venv venv`
  - Activate: `venv\Scripts\activate`
  - Install: `pip install -r requirements.txt`
  - **Priority:** Medium
  - **Effort:** 10 minutes
  - **Benefits:** Isolated dependencies, no PATH conflicts

- [ ] **Create Backend Startup Script**
  - File: `start-backend.bat`
  - Include full Python path
  - One-click backend startup
  - **Priority:** Medium
  - **Effort:** 5 minutes

- [ ] **Fix Windows PATH Order** (Alternative to venv)
  - Move Microsoft Store Python higher in PATH
  - Removes need for long Python path
  - **Priority:** Low (if using venv)
  - **Effort:** 5 minutes

---

## 🌐 Long-term Ngrok Solutions

### Choose One

- [ ] **Option 1: Delete Reserved Domain** (Simple)
  - Delete from ngrok dashboard
  - Accept random URLs each session
  - Update configs each time
  - **Best for:** Occasional testing
  - **Cost:** Free
  - **Effort:** 2 minutes

- [ ] **Option 2: Upgrade to Ngrok Paid** (Persistent URLs)
  - Sign up for paid plan ($8-10/month)
  - Get multiple custom subdomains
  - URLs never change
  - **Best for:** Frequent demos
  - **Cost:** $8-10/month
  - **Effort:** 10 minutes

- [ ] **Option 3: Cloudflare Tunnel** (Free Forever)
  - Download cloudflared
  - Set up free tunnel
  - Persistent URL, no limits
  - **Best for:** Production-like env
  - **Cost:** Free
  - **Effort:** 10-15 minutes
  - **See:** HISTORY.md Session 6 for details

---

## 🚀 Immediate Tasks (Session 5 - Ngrok Setup) [COMPLETED]

### High Priority - Complete Ngrok Setup

- [ ] **Start Backend Server**
  - Open terminal in VS Code
  - Navigate to: `cd C:\Windows\System32\cooin-app\cooin-backend`
  - Run: `python start_dev.py`
  - Wait for: `INFO: Uvicorn running on http://0.0.0.0:8000`
  - **Status:** ⚠️ Not running (verified via port check)

- [ ] **Start Ngrok Tunnels**
  - Open new terminal
  - Navigate to: `cd C:\Windows\System32\cooin-app`
  - Run: `start-ngrok.bat`
  - Verify 2 tunnels appear (frontend + backend)
  - Keep terminal open
  - **Status:** ⏳ Pending backend start

- [ ] **Get Public URLs and Update Config**
  - Open new terminal (PowerShell)
  - Navigate to: `cd C:\Windows\System32\cooin-app`
  - Run: `powershell -ExecutionPolicy Bypass -File .\get-ngrok-urls.ps1`
  - Type `y` when asked to update config
  - Copy the public frontend URL
  - **Status:** ⏳ Pending ngrok start

- [ ] **Update Backend CORS Configuration**
  - Open: `cooin-backend/.env`
  - Add ngrok frontend URL to CORS origins
  - Example: `BACKEND_CORS_ORIGINS=["http://localhost:8083","https://abc123.ngrok.io"]`
  - Save file
  - Restart backend server
  - **Status:** ⏳ Pending ngrok URLs

- [ ] **Restart Frontend with New Config**
  - Go to frontend terminal (port 8083)
  - Press Ctrl+C to stop
  - Run: `npx expo start --web --port 8083`
  - Wait for successful start
  - **Status:** ⏳ Pending config update

- [ ] **Test Public URL**
  - Open browser to ngrok frontend URL
  - Test login/register functionality
  - Verify API calls work (check browser console)
  - Share URL with others for testing
  - **Status:** ⏳ Pending all above steps

---

## 🔧 Optional Improvements

### Permission Management

- [ ] **Consider Moving Project** (Recommended)
  - Move from: `C:\Windows\System32\cooin-app`
  - Move to: `C:\Users\YOUR_USERNAME\Documents\cooin-app`
  - Benefits: No permission issues, safer, standard practice
  - See: `PERMISSION-FIX.md` for detailed instructions
  - **Priority:** Medium
  - **Effort:** 30 minutes
  - **Risk:** Low (if done carefully with backups)

- [ ] **OR Fix Permissions** (Alternative)
  - Right-click `fix-permissions.bat`
  - Select "Run as administrator"
  - Follow prompts
  - Close and reopen VS Code
  - **Priority:** Medium
  - **Effort:** 5 minutes
  - **Risk:** Low

---

## 📚 Documentation Tasks

### Ngrok Documentation

- [x] ✅ Create ngrok.yml configuration
- [x] ✅ Create start-ngrok.bat script
- [x] ✅ Create get-ngrok-urls.ps1 script
- [x] ✅ Write NGROK-SETUP.md (comprehensive guide)
- [x] ✅ Write NGROK-QUICKSTART.md (quick reference)
- [ ] **Update HOW-TO-LAUNCH-WEB-APP.md** with ngrok section
  - Add section: "Step 7: Expose to Public (Optional)"
  - Reference ngrok setup guides
  - **Priority:** Low
  - **Effort:** 15 minutes

### Permission Documentation

- [x] ✅ Create fix-permissions.bat script
- [x] ✅ Write PERMISSION-FIX.md guide
- [ ] **Update main README.md** with permission note
  - Add warning about System32 location
  - Reference permission fix guide
  - **Priority:** Low
  - **Effort:** 10 minutes

---

## 🔐 Security Tasks

### Ngrok Security

- [ ] **Review Ngrok URL Sharing**
  - Document who has access to URLs
  - Consider implementing ngrok authentication
  - Review free plan limitations (2-hour sessions)
  - **Priority:** Medium
  - **Effort:** 15 minutes

- [ ] **Environment Variable Management**
  - Add `.ngrok.yml` to `.gitignore` (contains auth token)
  - Verify auth token not committed to git
  - Document token rotation procedure
  - **Priority:** High
  - **Effort:** 5 minutes

- [ ] **CORS Security Review**
  - Audit all CORS origins in backend `.env`
  - Remove unnecessary origins
  - Document why each origin is needed
  - **Priority:** Medium
  - **Effort:** 10 minutes

---

## 🎯 Future Enhancements

### Ngrok Upgrades

- [ ] **Consider Ngrok Paid Plan**
  - Benefits: Persistent URLs, custom subdomains, longer sessions
  - Cost: ~$8-10/month for basic plan
  - Evaluate need vs. cost
  - **Priority:** Low
  - **Trigger:** If doing frequent demos or production testing

- [ ] **Implement Custom Subdomains**
  - Requires paid plan
  - Update ngrok.yml with subdomain config
  - Examples: `cooin-app.ngrok.io`, `cooin-api.ngrok.io`
  - **Priority:** Low
  - **Dependency:** Paid ngrok plan

- [ ] **Automate CORS Updates**
  - Create script to automatically add ngrok URLs to .env
  - Parse ngrok API response
  - Update .env file
  - Restart backend automatically
  - **Priority:** Low
  - **Effort:** 1-2 hours

### Automation Scripts

- [ ] **Create All-in-One Startup Script**
  - Single script to start: backend + frontend + ngrok
  - Automatically get URLs and update config
  - Display all URLs in organized format
  - **Priority:** Medium
  - **Effort:** 2 hours
  - **Benefits:** Faster daily workflow

- [ ] **Create Shutdown Script**
  - Gracefully stop all services
  - Kill processes on specific ports
  - Clean up temporary files
  - **Priority:** Low
  - **Effort:** 1 hour

---

## 🐛 Known Issues

### Current Issues

- ⚠️ **Backend not running on port 8000**
  - Impact: Cannot create ngrok tunnel for backend
  - Solution: Start backend server
  - Status: Identified, waiting for user action

- ⚠️ **Project in System32 folder**
  - Impact: Permission issues when editing files
  - Solutions: Run as admin, fix permissions, or move project
  - Status: Solutions provided, user to choose

### Potential Issues

- [ ] **Free Ngrok Session Expiration**
  - Issue: Sessions expire after 2 hours
  - Impact: URLs change, need to update config again
  - Mitigation: Document quick restart process
  - Long-term: Consider paid plan

- [ ] **Metro Bundler Cache Issues**
  - Issue: Config changes might not take effect immediately
  - Solution: Always hard refresh browser (Ctrl+Shift+R)
  - Solution: Use `--clear` flag when restarting
  - Status: Known limitation, documented

---

## 📊 Testing Checklist

### Pre-Launch Testing

- [ ] **Backend Health Check**
  - [ ] Backend starts without errors
  - [ ] Database connection successful
  - [ ] API docs accessible: http://localhost:8000/docs
  - [ ] Health endpoint responds: http://localhost:8000/health

- [ ] **Frontend Health Check**
  - [ ] Frontend starts on port 8083
  - [ ] No compilation errors
  - [ ] Can access: http://localhost:8083
  - [ ] Login page displays correctly

- [ ] **Ngrok Connection Test**
  - [ ] Both tunnels active
  - [ ] HTTPS URLs generated
  - [ ] Ngrok dashboard accessible: http://localhost:4040
  - [ ] Can inspect requests in dashboard

### Post-Configuration Testing

- [ ] **Frontend Config Verification**
  - [ ] Config backup created
  - [ ] BASE_URL updated to ngrok backend
  - [ ] No syntax errors in config.ts
  - [ ] Frontend restarted successfully

- [ ] **CORS Testing**
  - [ ] No CORS errors in browser console
  - [ ] API requests succeed from ngrok URL
  - [ ] Login/register works via public URL
  - [ ] Backend accepts requests from ngrok frontend

### End-to-End Testing

- [ ] **Public Access Test**
  - [ ] Can access app from ngrok frontend URL
  - [ ] Can create new account
  - [ ] Can log in
  - [ ] Can navigate all screens
  - [ ] API calls work correctly

- [ ] **External Access Test**
  - [ ] Share URL with another device/person
  - [ ] Verify they can access the app
  - [ ] Verify functionality works for them
  - [ ] Check ngrok dashboard for their requests

---

## 📱 Platform-Specific Tasks

### Web App (Current Focus)

- [x] ✅ Ngrok integration setup
- [ ] ⏳ Complete ngrok setup and testing
- [ ] Test on different browsers (Chrome, Firefox, Edge)
- [ ] Test responsive design on mobile browsers
- [ ] Performance testing on public URL

### Mobile App (Future)

- [ ] Configure Expo tunnel for mobile testing
- [ ] Test ngrok backend with mobile app
- [ ] Configure API endpoint switching (local vs. ngrok)
- [ ] Test on physical devices

### iOS App (Separate)

- [ ] Document iOS app setup with ngrok backend
- [ ] Update API configuration in Swift code
- [ ] Test with ngrok backend URL

---

## 🔄 Regular Maintenance

### Daily (If Using Ngrok)

- [ ] Start backend server
- [ ] Start frontend server
- [ ] Start ngrok tunnels
- [ ] Update frontend config with new URLs
- [ ] Verify CORS configuration

### Weekly

- [ ] Review ngrok usage/logs
- [ ] Clean up old config backups
- [ ] Update documentation if workflow changes
- [ ] Check for ngrok client updates

### Monthly

- [ ] Review ngrok plan (free vs. paid)
- [ ] Audit security settings
- [ ] Review and update documentation
- [ ] Check for breaking changes in dependencies

---

## 📖 Documentation Review

### Files to Keep Updated

- [ ] `README.md` - Main project overview
- [ ] `HISTORY.md` - Change log (updated this session)
- [ ] `TODO.md` - This file (keep current)
- [ ] `HOW-TO-LAUNCH-WEB-APP.md` - Launch instructions
- [ ] `NGROK-SETUP.md` - Ngrok setup guide
- [ ] `NGROK-QUICKSTART.md` - Quick reference

### Documentation Quality Checks

- [ ] All code examples are tested and working
- [ ] All file paths are accurate
- [ ] All commands are copy-paste ready
- [ ] Screenshots/diagrams are up to date (if any)
- [ ] Links to external resources are valid

---

## 🎓 Learning Resources

### For Team Members

- [ ] Create video walkthrough of ngrok setup
- [ ] Document common troubleshooting scenarios
- [ ] Create FAQ section
- [ ] Set up knowledge base

### External Resources

- **Ngrok Documentation:** https://ngrok.com/docs
- **FastAPI CORS Guide:** https://fastapi.tiangolo.com/tutorial/cors/
- **React Native Web:** https://necolas.github.io/react-native-web/
- **Expo Documentation:** https://docs.expo.dev/

---

## ✅ Completed This Session

- [x] Created ngrok.yml configuration file
- [x] Created start-ngrok.bat startup script
- [x] Created get-ngrok-urls.ps1 URL retrieval script
- [x] Wrote comprehensive NGROK-SETUP.md guide
- [x] Wrote quick NGROK-QUICKSTART.md reference
- [x] Created fix-permissions.bat script
- [x] Wrote PERMISSION-FIX.md guide
- [x] Configured ngrok auth token
- [x] Verified ngrok installation
- [x] Verified frontend running on port 8083
- [x] Updated HISTORY.md with session 5 details
- [x] Created this TODO.md file

---

## 🎯 Next Session Goals

1. Complete ngrok setup (start backend, tunnels, test)
2. Test public URL access end-to-end
3. Consider moving project out of System32
4. Create all-in-one startup script
5. Add ngrok section to HOW-TO-LAUNCH-WEB-APP.md

---

**Last Updated:** 2025-10-25
**Session:** 5 - Ngrok Integration & Permission Fix
**Status:** Setup complete, testing pending
