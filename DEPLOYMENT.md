# GenLaravel Deployment Guide

## Architecture

```
┌─────────────────┐     WebSocket/API     ┌─────────────────┐
│                 │ ◄──────────────────► │                 │
│  Frontend       │                       │  Backend        │
│  (Vercel)       │                       │  (Railway)      │
│                 │                       │                 │
│  - Static HTML  │                       │  - FastAPI      │
│  - JavaScript   │                       │  - AI Agents    │
│  - CSS          │                       │  - WebSocket    │
│                 │                       │                 │
└─────────────────┘                       └─────────────────┘
```

---

## 1. Backend Deployment (Railway)

### Prerequisites
- Railway account (https://railway.app)
- GitHub repository with this code

### Steps

#### Option A: Deploy from GitHub (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add deployment config"
   git push origin main
   ```

2. **Create Railway Project**
   - Go to https://railway.app/new
   - Click "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect the Dockerfile

3. **Set Environment Variables**
   In Railway dashboard → Variables:
   ```
   CEREBRAS_API_KEY=your_cerebras_api_key
   MISTRAL_API_KEY=your_mistral_api_key
   PORT=8080
   ```

4. **Generate Domain**
   - Go to Settings → Networking
   - Click "Generate Domain"
   - Copy the URL (e.g., `https://genlaravel-backend-production.up.railway.app`)

#### Option B: Deploy with Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up

# Set environment variables
railway variables set CEREBRAS_API_KEY=your_key
railway variables set MISTRAL_API_KEY=your_key
```

### Verify Backend

```bash
# Health check
curl https://your-railway-url.up.railway.app/health

# Queue status
curl https://your-railway-url.up.railway.app/api/queue/status
```

---

## 2. Frontend Deployment (Vercel)

### Prerequisites
- Vercel account (https://vercel.com)
- Backend already deployed on Railway

### Steps

1. **Update Backend URL**
   
   Edit `frontend/config.js`:
   ```javascript
   // Update this line with your Railway URL
   RAILWAY_BACKEND_URL: 'https://your-railway-url.up.railway.app',
   ```

2. **Deploy to Vercel**

   #### Option A: Vercel Dashboard
   - Go to https://vercel.com/new
   - Import your GitHub repository
   - Set **Root Directory** to `frontend`
   - Click Deploy

   #### Option B: Vercel CLI
   ```bash
   # Install Vercel CLI
   npm install -g vercel

   # Navigate to frontend
   cd frontend

   # Deploy
   vercel

   # For production
   vercel --prod
   ```

3. **Verify Frontend**
   - Open your Vercel URL
   - Check that "Backend Online" status appears
   - Try generating a page

---

## 3. Configuration Summary

### Backend (Railway)

| Variable | Description | Example |
|----------|-------------|---------|
| `CEREBRAS_API_KEY` | Cerebras AI API key | `csk-xxx` |
| `MISTRAL_API_KEY` | Mistral AI API key | `xxx` |
| `PORT` | Server port | `8080` |

### Frontend (Vercel)

Edit `frontend/config.js`:
```javascript
RAILWAY_BACKEND_URL: 'https://your-app.up.railway.app',
```

---

## 4. Testing Deployment

### Test Backend
```bash
# Health check
curl https://your-railway-url.up.railway.app/health

# Expected response:
# {"status":"healthy","timestamp":"2024-..."}
```

### Test WebSocket
Open browser console on frontend:
```javascript
CONFIG.debug();
// Should show correct URLs

const ws = new WebSocket(CONFIG.getUnifiedWebSocketUrl());
ws.onopen = () => console.log('Connected!');
ws.onerror = (e) => console.error('Error:', e);
```

---

## 5. Troubleshooting

### Backend Issues

**Problem: Railway build fails**
```bash
# Check Dockerfile syntax
docker build -t genlaravel-test .

# Check logs in Railway dashboard
```

**Problem: WebSocket connection refused**
- Ensure Railway domain is using HTTPS
- Check CORS settings in `backend/main.py`
- Verify `wss://` protocol is used (not `ws://`)

### Frontend Issues

**Problem: "Backend Offline" status**
- Check `RAILWAY_BACKEND_URL` in `config.js`
- Verify Railway deployment is running
- Check browser console for errors

**Problem: WebSocket fails to connect**
- Ensure backend URL uses `https://`
- Check Railway logs for errors
- Verify environment variables are set

---

## 6. Cost Estimation

### Railway (Backend)
- **Hobby Plan**: $5/month (500 hours)
- **Pro Plan**: Pay per usage (~$0.000463/min)
- Estimated: $5-20/month depending on usage

### Vercel (Frontend)
- **Hobby Plan**: Free (100GB bandwidth)
- **Pro Plan**: $20/month (1TB bandwidth)
- Estimated: Free for most use cases

---

## 7. Production Checklist

- [ ] Backend deployed on Railway
- [ ] Environment variables set (API keys)
- [ ] Railway domain generated
- [ ] `RAILWAY_BACKEND_URL` updated in `config.js`
- [ ] Frontend deployed on Vercel
- [ ] Health check passing
- [ ] WebSocket connection working
- [ ] Test single-page generation
- [ ] Test multi-page generation

---

## Quick Commands

```bash
# Backend (Railway)
railway up                    # Deploy
railway logs                  # View logs
railway variables            # List env vars

# Frontend (Vercel)
cd frontend
vercel                       # Deploy preview
vercel --prod               # Deploy production
vercel logs                 # View logs
```
