# 🚀 Cooin App - Deployment Guide for Web Testing

## Overview
This guide will help you deploy your Cooin app so your partners can test it from anywhere.

---

## Part 1: Setup ngrok (Make Backend Accessible) ⚙️

### Step 1: Install ngrok
1. Go to https://ngrok.com/download
2. Download ngrok for Windows
3. Extract it to a folder (e.g., `C:\ngrok`)

### Step 2: Setup ngrok Account
1. Sign up at https://dashboard.ngrok.com/signup (it's free!)
2. Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken
3. Run in terminal:
```bash
ngrok config add-authtoken YOUR_TOKEN_HERE
```

### Step 3: Start Backend with ngrok
1. Make sure your backend is running (you should already have it running on port 8000)
2. Open a **NEW terminal window**
3. Run:
```bash
ngrok http 8000
```

4. You'll see output like:
```
Forwarding    https://abc123-xx-xxx.ngrok-free.app -> http://localhost:8000
```

5. **COPY** that https URL (e.g., `https://abc123-xx-xxx.ngrok-free.app`)
   - This is your public backend URL!
   - **IMPORTANT**: Keep this terminal window open while testing

---

## Part 2: Deploy Frontend to Vercel 🌐

### Step 1: Install Vercel CLI
Open a terminal and run:
```bash
npm install -g vercel
```

### Step 2: Login to Vercel
```bash
vercel login
```
- Choose your preferred login method (GitHub, GitLab, Bitbucket, or Email)
- Follow the authentication steps

### Step 3: Build the Frontend
```bash
cd C:\Windows\System32\cooin-app\cooin-frontend
npm run build:web
```

### Step 4: Deploy to Vercel
```bash
vercel
```

When prompted:
1. **"Set up and deploy?"** → Press **Y** (Yes)
2. **"Which scope?"** → Choose your account
3. **"Link to existing project?"** → Press **N** (No, create new)
4. **"What's your project's name?"** → Type: `cooin-frontend` (or any name)
5. **"In which directory is your code?"** → Press Enter (current directory)
6. **"Want to override settings?"** → Press **N** (No)

Wait for deployment to complete...

### Step 5: Set Environment Variable
After deployment, set the API URL:
```bash
vercel env add EXPO_PUBLIC_API_URL
```
- When prompted, paste your ngrok URL + `/api/v1`
- Example: `https://abc123-xx-xxx.ngrok-free.app/api/v1`
- Select: **Production**, **Preview**, and **Development**

### Step 6: Redeploy with Environment Variable
```bash
vercel --prod
```

### Step 7: Get Your App URL
After deployment completes, you'll see:
```
✅ Production: https://cooin-frontend.vercel.app
```

**🎉 DONE! Share this URL with your partners!**

---

## Part 3: Share with Your Partners 📱

### For PC/Mac Users:
Simply share the Vercel URL:
```
https://cooin-frontend.vercel.app
```
They can open it in any browser!

### For iOS Users:
1. Send them the same Vercel URL
2. They can open it in Safari on their iPhone
3. For a native app feel:
   - Open the URL in Safari
   - Tap the Share button
   - Tap "Add to Home Screen"
   - Now it looks like a real app!

---

## Important Notes ⚠️

### Keep Backend Running
- Your PC must be ON with backend running
- Keep the ngrok terminal window OPEN
- If you close ngrok or restart your PC:
  1. Start backend again
  2. Run `ngrok http 8000` again
  3. Update the EXPO_PUBLIC_API_URL in Vercel with new ngrok URL
  4. Run `vercel --prod` again

### ngrok Free Tier Limitations
- URL changes every time you restart ngrok
- Sessions expire after 2 hours (need to restart)
- Consider upgrading to ngrok paid plan for stable URL

### Better Long-term Solution
For production, deploy backend to:
- **Render** (https://render.com) - Free tier available
- **Railway** (https://railway.app) - Free tier available
- **Heroku** (https://heroku.com) - Paid

---

## Troubleshooting 🔧

### "Cannot connect to API"
1. Check if backend is running
2. Check if ngrok is running
3. Verify the ngrok URL in Vercel environment variables
4. Redeploy: `vercel --prod`

### "Page not found" on Vercel
1. Check if build succeeded
2. Check vercel.json is present
3. Try rebuilding: `npm run build:web && vercel --prod`

### Partners see old version
1. Ask them to hard refresh: Ctrl+Shift+R (PC) or Cmd+Shift+R (Mac)
2. Or clear browser cache

---

## Quick Commands Summary 📝

```bash
# 1. Start backend (in terminal 1)
cd C:\Windows\System32\cooin-app\cooin-backend
source venv/Scripts/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 2. Start ngrok (in terminal 2)
ngrok http 8000

# 3. Deploy frontend (in terminal 3)
cd C:\Windows\System32\cooin-app\cooin-frontend
npm run build:web
vercel --prod
```

---

## Need Help?
If you encounter any issues, check:
1. Backend is running on port 8000
2. ngrok is running and showing forwarding URL
3. Vercel environment variable has correct ngrok URL
4. All services are running simultaneously
