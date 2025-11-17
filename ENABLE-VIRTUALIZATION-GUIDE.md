# Enable Virtualization Guide (VT-x / AMD-V)

**Issue**: Docker Desktop failed to start - virtualization not detected
**Status**: VirtualizationFirmwareEnabled = FALSE
**Required**: Enable virtualization in BIOS/UEFI

---

## Quick Check

Run this command to verify current status:
```cmd
wmic cpu get VirtualizationFirmwareEnabled
```

- **FALSE** = Virtualization is disabled (need to enable in BIOS)
- **TRUE** = Virtualization is enabled (Docker should work)

---

## Step-by-Step: Enable Virtualization in BIOS

### Step 1: Identify Your CPU Type

Open Command Prompt:
```cmd
wmic cpu get name
```

- If you see **"Intel"** → You need to enable **Intel VT-x**
- If you see **"AMD"** → You need to enable **AMD-V** or **SVM Mode**

### Step 2: Restart and Enter BIOS

1. **Save all your work**
2. **Restart computer**
3. **Immediately start pressing** one of these keys repeatedly during boot:

| Manufacturer | BIOS Key | Alternative Keys |
|--------------|----------|------------------|
| Dell | F2 | F12, Delete |
| HP | F10 | ESC, F2 |
| Lenovo | F1 or F2 | Enter then F1 |
| ASUS | F2 | Delete |
| Acer | F2 | Delete |
| MSI | Delete | F2 |
| Gigabyte | Delete | F2 |
| Toshiba | F2 | F12 |
| Samsung | F2 | F10 |
| Surface | Hold Volume Up | While pressing power |

**Tip**: Watch the screen during boot - it usually shows "Press [KEY] to enter Setup"

### Step 3: Navigate BIOS Menus

Use **Arrow Keys** to navigate, **Enter** to select, **ESC** to go back.

#### For Intel CPUs - Find and Enable:

**Common Location 1:**
```
Advanced → CPU Configuration → Intel Virtualization Technology → [Enabled]
```

**Common Location 2:**
```
Security → Virtualization → Intel VT-x → [Enabled]
```

**Common Location 3:**
```
Advanced → Processor Configuration → Intel VT → [Enabled]
```

**Common Location 4:**
```
Configuration → Intel Virtual Technology → [Enabled]
```

#### For AMD CPUs - Find and Enable:

**Common Location 1:**
```
Advanced → CPU Configuration → SVM Mode → [Enabled]
```

**Common Location 2:**
```
Advanced → AMD-V → [Enabled]
```

**Common Location 3:**
```
Advanced → Secure Virtual Machine → [Enabled]
```

### Step 4: Save and Exit

1. Press **F10** (common save key)
2. Or navigate to **Exit → Save Changes and Exit**
3. Confirm **"Yes"** when prompted
4. Computer will restart automatically

### Step 5: Verify After Restart

Open Command Prompt and run:
```cmd
wmic cpu get VirtualizationFirmwareEnabled
```

**Expected Result:**
```
VirtualizationFirmwareEnabled
TRUE
```

If you see **TRUE**, virtualization is now enabled! ✅

---

## Troubleshooting

### "I can't find the virtualization setting"

**Search for these names:**
- Intel Virtualization Technology
- Intel VT-x / VT-d
- Virtualization Extensions
- AMD-V
- SVM Mode (AMD)
- Secure Virtual Machine

**Check these menus systematically:**
1. Advanced
2. Advanced → CPU/Processor Configuration
3. Security
4. Configuration
5. Chipset

**Still can't find it?**
- Take photos of each BIOS menu
- Google: "[Your Computer Model] enable virtualization BIOS"
- Check your computer manual

### "The setting is grayed out"

**Possible causes:**

1. **Hyper-V is enabled** (blocks VT-x)
   ```cmd
   # Run as Administrator
   bcdedit /set hypervisorlaunchtype off
   # Restart computer
   ```

2. **Secure Boot conflict**
   - In BIOS, try disabling Secure Boot temporarily
   - Enable virtualization
   - Re-enable Secure Boot

3. **BIOS password protected**
   - Contact IT admin or computer owner
   - May need admin password to change

### "BIOS key doesn't work"

- Try pressing the key **earlier** during boot
- Try pressing it **repeatedly** (not holding)
- Try **all** the keys listed for your manufacturer
- Some laptops require holding a special button (e.g., Lenovo Novo button)

### "Still shows FALSE after enabling"

1. **Make sure you saved** before exiting BIOS
2. **Check if there are multiple virtualization options** - enable ALL of them:
   - Intel VT-x
   - Intel VT-d (if available)
   - Virtualization Technology
3. **Update BIOS** to latest version (advanced users only)
4. **Clear CMOS** (advanced users only)

---

## Alternative: Redis Without Docker

If you **cannot enable virtualization** (company computer, locked BIOS, etc.), you can use Redis without Docker:

### Option 1: Redis on WSL (Recommended)

Already have WSL installed from Docker setup attempt:

```cmd
# In Command Prompt
wsl

# Inside WSL (Ubuntu)
sudo apt update
sudo apt install redis-server -y
sudo service redis-server start
redis-cli ping  # Should respond: PONG
```

**Backend connection:**
```
REDIS_URL=redis://localhost:6379
```

### Option 2: Memurai (Redis for Windows)

Free Redis-compatible server for Windows:

1. Download: https://www.memurai.com/get-memurai
2. Install Memurai
3. Runs as Windows service on port 6379
4. No Docker needed

### Option 3: Skip Redis (Development Only)

For development, you can temporarily disable Redis features:
- Use in-memory cache instead
- Comment out Redis-dependent features
- Use file-based sessions

---

## After Enabling Virtualization

Once virtualization is enabled (shows TRUE):

### 1. Start Docker Desktop
```cmd
# Search for "Docker Desktop" in Start menu and launch
```

### 2. Verify Docker Works
```cmd
docker --version
docker run hello-world
```

### 3. Continue Cooin Setup
```cmd
cd C:\Windows\System32\cooin-app
docker-compose up -d redis
```

### 4. Next Steps
- See DOCKER-SETUP-GUIDE.md for Redis configuration
- See TODO.md for remaining session tasks

---

## Quick Reference Commands

```cmd
# Check virtualization status
wmic cpu get VirtualizationFirmwareEnabled

# Check CPU type
wmic cpu get name

# Check Hyper-V status
systeminfo | find "Hyper-V"

# Disable Hyper-V (if needed - run as Admin)
bcdedit /set hypervisorlaunchtype off

# Re-enable Hyper-V (if needed - run as Admin)
bcdedit /set hypervisorlaunchtype auto
```

---

## Still Having Issues?

**Get Your System Info:**
```cmd
wmic cpu get name,VirtualizationFirmwareEnabled
wmic computersystem get manufacturer,model
systeminfo | find "System Model"
```

**Next Steps:**
1. Google: "[Manufacturer] [Model] enable virtualization"
2. Check manufacturer support website
3. Update BIOS to latest version
4. Consider Redis alternatives (WSL, Memurai)

---

**Created**: 2025-11-17 (Session 14)
**Status**: Awaiting BIOS configuration
**Next**: After enabling virtualization, return to DOCKER-SETUP-GUIDE.md
