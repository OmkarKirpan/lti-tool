# 🚀 Render.com Deployment - Quick Checklist

## Before You Start

- [ ] Code is committed to a GitHub repository
- [ ] You have a Render.com account (free tier is fine for testing)
- [ ] You have access to OpenEdX admin panel

## Deployment Steps

### 1️⃣ Push to GitHub

```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### 2️⃣ Deploy on Render

1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will detect `render.yaml` automatically
5. Click **"Apply"**
6. Wait for deployment (~5-10 minutes)

### 3️⃣ Configure Environment

After deployment, update these environment variables in Render dashboard:

**Required:**

- `TOOL_BASE_URL` → Your Render URL (e.g., `https://your-app.onrender.com`)

**Optional but Recommended:**

- `OPENEDX_BASE_URL` → Your OpenEdX instance URL
- `TOOL_NAME` → Your tool's display name

### 4️⃣ Get Your URLs

After deployment, note these URLs:

```
Your App:     https://your-app-name.onrender.com
Login URL:    https://your-app-name.onrender.com/login
Launch URL:   https://your-app-name.onrender.com/launch
JWKS URL:     https://your-app-name.onrender.com/jwks
Status Check: https://your-app-name.onrender.com/api/status
```

### 5️⃣ Configure OpenEdX

1. Go to OpenEdX Admin → **LTI 1.3 Tool Configuration**
2. Create new tool with your URLs from step 4
3. Copy the **Client ID** and **Deployment ID**
4. Update `configs/lti_config.json` in your repository:
   ```json
   {
     "https://your-openedx.com": {
       "client_id": "PASTE_CLIENT_ID_HERE",
       "deployment_ids": ["PASTE_DEPLOYMENT_ID_HERE"]
     }
   }
   ```
5. Commit and push (will trigger auto-redeploy)

### 6️⃣ Test

1. Add LTI component in OpenEdX course
2. Launch from student view
3. You should see the launch success page! 🎉

## ⚠️ Important Notes

### Free Tier Limitations

- ⏰ Service spins down after 15 minutes of inactivity
- 🐌 First request after spin-down takes ~30 seconds (cold start)
- 💾 No persistent disk (sessions stored in ephemeral storage)
  - **This is OK!** LTI launches create fresh sessions each time
- ✅ Perfect for development/testing/small courses
- 💰 Upgrade to Starter ($7/month) for production (always on + persistent disk)

> **Note:** Session storage limitation doesn't affect LTI functionality since each OpenEdX launch creates a new session. See `RENDER_FREE_TIER.md` for complete details.

### Common Issues

**Build fails?**

```bash
# Ensure build.sh is executable:
chmod +x build.sh
git add build.sh
git commit -m "Make build script executable"
git push
```

**LTI launch fails?**

- ✅ Check `TOOL_BASE_URL` is correct (HTTPS)
- ✅ Verify `configs/lti_config.json` has correct credentials
- ✅ Confirm OpenEdX has all three URLs configured
- ✅ Wait for cold start (30s) on free tier

**Session issues?**

- Already configured correctly for HTTPS and iframes
- `SESSION_COOKIE_SECURE=True`
- `SESSION_COOKIE_SAMESITE=None` (in config.py)

## 📚 Full Documentation

For detailed instructions, troubleshooting, and advanced configuration:
→ See `RENDER_DEPLOYMENT.md`

## 💰 Pricing

- **Free**: $0/month (spins down, perfect for dev/test)
- **Starter**: $7/month (always on, recommended for production)
- **Pro**: $25/month (for high traffic)

## ✅ Success Indicators

Your deployment is successful when:

- [ ] Build completes without errors
- [ ] `/api/status` returns 200 OK
- [ ] `/jwks` returns JSON with public keys
- [ ] Home page loads correctly
- [ ] LTI launch from OpenEdX works

---

**Need Help?** Check `RENDER_DEPLOYMENT.md` for detailed troubleshooting!
