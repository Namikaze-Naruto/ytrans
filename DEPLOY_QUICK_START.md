# 🚀 Deploy to Render - Quick Start

## Step 1: Sign Up / Login
1. Go to: https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (easiest option)

## Step 2: Create New Web Service
1. From Dashboard, click "New +" button (top right)
2. Select "Web Service"
3. Click "Build and deploy from a Git repository"
4. Click "Next"

## Step 3: Connect Repository
1. Click "Connect account" if GitHub not connected
2. Find and select: **Namikaze-Naruto/ytrans**
3. Click "Connect"

## Step 4: Configure Settings

Copy these settings exactly:

**Name**: `ytrans`

**Region**: Select closest to you (e.g., Oregon USA)

**Branch**: `main`

**Root Directory**: (leave empty)

**Runtime**: `Python 3`

**Build Command**: 
```
pip install -r requirements.txt
```

**Start Command**:
```
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

**Instance Type**: `Free`

## Step 5: Deploy
1. Scroll down
2. Click "Create Web Service" button
3. Wait 5-10 minutes (first deployment is slow)
4. Watch the logs - you'll see:
   - Installing dependencies
   - Downloading Whisper model
   - Starting server

## Step 6: Test Your Deployment
Once "Live" appears:

1. Copy your app URL (looks like: `https://ytrans-xxxx.onrender.com`)
2. Open it in browser - you'll see your UI!
3. Try a short video: `https://www.youtube.com/watch?v=jNQXAC9IVRw`

## ⚠️ Important: Free Tier Limitations

1. **Cold Starts**: App sleeps after 15min of inactivity
   - First request after sleep: 30-60 seconds to wake up
   
2. **Processing Time**: Using "tiny" Whisper model
   - Faster than "base" but slightly less accurate
   - Good for short videos (< 5 minutes)

3. **Monthly Limit**: 750 hours/month free

## 🎯 Your App URLs

After deployment:
- **Web Interface**: `https://ytrans-xxxx.onrender.com/`
- **API Docs**: `https://ytrans-xxxx.onrender.com/docs`
- **API Endpoint**: `https://ytrans-xxxx.onrender.com/transcript`

## 💡 Upgrade If Needed

If free tier is too slow:
- Click "Settings" in Render dashboard
- Change Instance Type to "Starter" ($7/month)
- Better CPU + can use "base" model (more accurate)

## 🐛 Troubleshooting

**Build Failed?**
- Check "Logs" tab for errors
- Make sure GitHub repo is updated

**App Crashes?**
- Free tier has 512MB RAM limit
- Try shorter videos
- Consider upgrading

**Takes Forever?**
- Cold start is normal (30-60 sec first request)
- Processing long videos takes time
- Use shorter videos for testing

## ✅ Done!

Share your URL with friends! 🎉
