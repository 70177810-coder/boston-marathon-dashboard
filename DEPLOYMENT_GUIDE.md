# 🚀 Deployment Guide — Boston Marathon Dashboard

This guide covers deploying the Streamlit dashboard to **Render** and **Railway**.

> **Note**: Vercel is NOT suitable for Streamlit apps (it's optimized for frontend/serverless). Use Render or Railway for persistent Python processes.

---

## 📋 Pre-Deployment Checklist

- [x] All code pushed to a GitHub repository
- [x] `requirements.txt` up to date
- [x] `.env.example` documents required environment variables
- [x] `.gitignore` excludes secrets and cache files
- [x] App runs locally with `streamlit run app.py`

---

## Option 1: Deploy on Render (Recommended)

### Step 1 — Create Account
Sign up at [render.com](https://render.com) using your GitHub account.

### Step 2 — New Web Service
Click **"New +"** → **"Web Service"** → Connect your GitHub repo.

### Step 3 — Configure Settings
| Setting | Value |
|---------|-------|
| **Runtime** | Python |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true --browser.gatherUsageStats false` |
| **Plan** | Free (spins down after 15 min idle) or Starter ($7/mo) |

### Step 4 — Environment Variables
Add these in the Render dashboard under **Environment**:
```
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### Step 5 — Deploy
Click **"Create Web Service"**. Watch logs for build progress. Your app will be live at:
```
https://boston-marathon-dashboard.onrender.com
```

### Alternative: Use render.yaml
This repo includes a `render.yaml` file. You can use **Render Blueprints** to auto-deploy:
1. Go to Render Dashboard → **Blueprints** → **New Blueprint Instance**
2. Connect the repo → Render reads `render.yaml` automatically

---

## Option 2: Deploy on Railway

### Step 1 — Create Account
Sign up at [railway.app](https://railway.app) using your GitHub account.

### Step 2 — New Project
Click **"New Project"** → **"Deploy from GitHub repo"** → Select your repo.

### Step 3 — Auto-Detection
Railway uses **Nixpacks** and will detect Python from `requirements.txt`. The included `railway.toml` and `nixpacks.toml` handle configuration automatically.

### Step 4 — Set Start Command (if not auto-detected)
Go to **Service → Settings → Deploy → Start Command**:
```
streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true --browser.gatherUsageStats false
```

### Step 5 — Generate Domain
Go to **Service → Settings → Networking → Generate Domain**.
Your app will be live at:
```
https://boston-marathon-dashboard.up.railway.app
```

### Step 6 — Add Custom Domain (Optional)
In **Networking → Add Custom Domain**, enter your domain. Add the CNAME record at your DNS provider.

---

## Option 3: Deploy with Docker (Any Platform)

This repo includes a `Dockerfile`. Build and run anywhere:

```bash
# Build image
docker build -t marathon-dashboard .

# Run locally
docker run -p 8501:8501 marathon-dashboard

# Push to any container registry
docker tag marathon-dashboard your-registry/marathon-dashboard:latest
docker push your-registry/marathon-dashboard:latest
```

Works on: Render (Docker), Railway (Docker), Google Cloud Run, AWS ECS, Azure Container Apps, etc.

---

## 🔧 Troubleshooting

| Issue | Fix |
|-------|-----|
| **App crashes with PORT error** | Ensure start command uses `$PORT` (injected by platform) |
| **Blank page on load** | Add `--server.headless true` flag |
| **Module not found** | Check all dependencies are in `requirements.txt` |
| **Render free tier slow first load** | Free services sleep after 15 min — first request takes ~30s to wake |
| **Charts not rendering** | Ensure `matplotlib` backend is set to `Agg` (headless) |

---

## 📁 Deployment Files Included

```
├── render.yaml          # Render Blueprint (Infrastructure as Code)
├── railway.toml         # Railway deployment config
├── nixpacks.toml        # Nixpacks build config for Railway
├── Dockerfile           # Docker containerization
├── Procfile             # Generic PaaS start command
├── .env.example         # Environment variable template
├── .gitignore           # Files to exclude from Git
├── .streamlit/
│   └── config.toml      # Streamlit server configuration
└── DEPLOYMENT_GUIDE.md  # This file
```
