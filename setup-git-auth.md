# GitHub Authentication Setup

Your push failed because GitHub requires authentication. Choose one option:

## Option 1: Personal Access Token (PAT) - Recommended

### Step 1: Create Token
1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Token name: `Cooin Platform`
4. Expiration: Choose duration (90 days recommended)
5. Select scopes:
   - ✅ `repo` (Full control of private repositories)
6. Click **"Generate token"**
7. **COPY THE TOKEN NOW** - You won't see it again!

### Step 2: Push with Token
```bash
cd "C:\Windows\System32\cooin-app"

# Replace YOUR_TOKEN with the token you copied
git push https://YOUR_TOKEN@github.com/FedericoAlzateUpegui/cooin-platform.git main
```

### Step 3: Store Credentials (Optional)
To avoid entering token each time:
```bash
# Store credentials in Windows Credential Manager
git config --global credential.helper manager

# Next push will ask for credentials once, then remember them
git push origin main
# Username: FedericoAlzateUpegui
# Password: [paste your token]
```

## Option 2: SSH Key (More Secure)

### Step 1: Generate SSH Key
```bash
# Generate new SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Press Enter to accept default location
# Enter a passphrase (or press Enter for none)
```

### Step 2: Add SSH Key to GitHub
```bash
# Copy the public key
cat ~/.ssh/id_ed25519.pub

# Or on Windows:
type %USERPROFILE%\.ssh\id_ed25519.pub
```

1. Copy the entire output
2. Go to: https://github.com/settings/keys
3. Click **"New SSH key"**
4. Title: `Cooin Windows PC`
5. Paste the key
6. Click **"Add SSH key"**

### Step 3: Update Remote URL
```bash
cd "C:\Windows\System32\cooin-app"

# Change from HTTPS to SSH
git remote set-url origin git@github.com:FedericoAlzateUpegui/cooin-platform.git

# Test connection
ssh -T git@github.com

# Push
git push origin main
```

## Quick Test After Setup

```bash
cd "C:\Windows\System32\cooin-app"
git push origin main
```

## Troubleshooting

### "Authentication failed"
- Make sure you're using the token as password, not your GitHub password
- Check the token hasn't expired
- Verify the token has `repo` scope

### "Permission denied (publickey)"
- Make sure you added the SSH public key to GitHub
- Test connection: `ssh -T git@github.com`
- Should see: "Hi FedericoAlzateUpegui! You've successfully authenticated"

## Current Status

- ✅ Project cleaned up
- ✅ All files committed locally
- ⏳ Waiting to push to GitHub
- 2 commits ready to push (1 previous + 1 new deployment commit)
