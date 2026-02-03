# Deployment Guide for Render

## Prerequisites
- GitHub repository: ✅ https://github.com/Namikaze-Naruto/ytrans
- Render account (free): Create at https://render.com

## Deployment Steps

### 1. Sign Up / Login to Render
- Go to: https://render.com
- Sign up with GitHub (recommended)

### 2. Create New Web Service
1. Click "New +" → "Web Service"
2. Click "Build and deploy from a Git repository"
3. Connect your GitHub account if not connected
4. Select repository: **Namikaze-Naruto/ytrans**
5. Click "Connect"

### 3. Configure Web Service

**Basic Settings:**
- **Name**: `ytrans` (or your preferred name)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

**Instance Type:**
- Select: **Free** (or upgrade if needed)

### 4. Environment Variables (Optional)
No environment variables needed for basic setup.

### 5. Deploy
- Click "Create Web Service"
- Wait 5-10 minutes for first deployment
- Render will install dependencies and start your app

### 6. Access Your App
After deployment succeeds:
- Backend API: `https://ytrans-xxxx.onrender.com`
- API Docs: `https://ytrans-xxxx.onrender.com/docs`

### 7. Update Frontend
The frontend needs to point to your Render URL instead of localhost.

**Option A: Use GitHub Pages for Frontend**
1. Push updated frontend to `gh-pages` branch
2. Update `app.js` to use your Render API URL

**Option B: Host Frontend on Same Server**
Add static file serving to FastAPI (see below)

## ⚠️ Important Notes for Free Tier

1. **Cold Starts**: Free tier spins down after 15 min of inactivity
   - First request after idle takes 30-60 seconds to wake up
   
2. **Memory Limits**: Free tier has 512MB RAM
   - Using "tiny" Whisper model (lower accuracy but fits in memory)
   - May timeout on long videos

3. **Monthly Limits**: 750 hours/month free
   - Enough for personal/demo use

4. **No Persistence**: Temporary file storage only
   - Audio files are deleted after processing (already implemented)

## Upgrade Options

If free tier is too slow:
- **Starter Plan**: $7/month - 512MB RAM, faster CPU
- **Standard Plan**: $25/month - 2GB RAM, can use "base" or "small" model

## Testing Your Deployed App

Once live, test with:
```bash
curl -X POST "https://your-app.onrender.com/transcript" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=jNQXAC9IVRw"}'
```

## Troubleshooting

**Build Fails:**
- Check build logs in Render dashboard
- Ensure all files are pushed to GitHub

**App Crashes:**
- Check logs for memory errors
- Consider upgrading to paid tier for more RAM

**Timeout Errors:**
- Free tier has request timeout limits
- Try shorter videos or upgrade tier
