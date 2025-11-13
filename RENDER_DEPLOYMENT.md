# 🚀 Deploying to Render.com

This guide walks you through deploying the LTI 1.3 Tool to Render.com.

## 📋 Prerequisites

1. **GitHub Account** - Your code needs to be in a GitHub repository
2. **Render Account** - Sign up at [render.com](https://render.com)
3. **OpenEdX Instance** - Access to configure LTI tools

## 🎯 Deployment Steps

### Step 1: Prepare Your Repository

1. **Commit all changes to Git:**

   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Ensure these files are present:**
   - ✅ `render.yaml` - Render configuration
   - ✅ `build.sh` - Build script
   - ✅ `.env.example` - Environment template
   - ✅ `requirements.txt` - Python dependencies
   - ✅ `package.json` - Node dependencies

### Step 2: Deploy to Render

#### Option A: Using render.yaml (Recommended)

1. **Go to Render Dashboard:**

   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Click **"New +"** → **"Blueprint"**

2. **Connect Repository:**

   - Select your GitHub repository
   - Render will detect `render.yaml` automatically

3. **Review Configuration:**

   - Service name: `edx-lti-tool`
   - Plan: Free (or upgrade to Starter for production)
   - Environment variables will be pre-configured

4. **Click "Apply":**
   - Render will start building and deploying
   - Wait for build to complete (~5-10 minutes)

#### Option B: Manual Setup

1. **Create New Web Service:**

   - Dashboard → **"New +"** → **"Web Service"**
   - Connect your GitHub repository

2. **Configure Service:**

   ```yaml
   Name: edx-lti-tool
   Region: Oregon (or closest to your users)
   Branch: main
   Runtime: Python 3
   Build Command: ./build.sh
   Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
   Plan: Free (or Starter+)
   ```

3. **Add Environment Variables:**

   - Go to **Environment** tab
   - Add all variables from `.env.example`
   - **Important:** Set `TOOL_BASE_URL` after deployment

4. **Add Disk Storage (for filesystem sessions):**

   - Go to **Storage** tab
   - Click **"Add Disk"**
   - Name: `lti-sessions`
   - Mount Path: `/opt/render/project/src/flask_session`
   - Size: 1 GB

5. **Deploy:**
   - Click **"Create Web Service"**
   - Wait for deployment

### Step 3: Post-Deployment Configuration

1. **Get Your Render URL:**

   ```
   https://your-app-name.onrender.com
   ```

2. **Update TOOL_BASE_URL:**

   - Go to Environment tab
   - Update `TOOL_BASE_URL` to your Render URL
   - Service will auto-redeploy

3. **Make build.sh executable (if needed):**

   ```bash
   chmod +x build.sh
   git add build.sh
   git commit -m "Make build.sh executable"
   git push
   ```

4. **Download Your Public Key:**
   - Visit: `https://your-app-name.onrender.com/jwks`
   - Save the JWKS response (you'll need this for OpenEdX)

### Step 4: Configure OpenEdX

1. **Access OpenEdX Admin:**

   - Go to `https://your-openedx.com/admin`
   - Navigate to **LTI 1.3 Tool Configuration**

2. **Create New Tool:**

   ```
   Tool Name: Your LTI Tool Name
   Launch URL: https://your-app-name.onrender.com/launch
   Login URL: https://your-app-name.onrender.com/login
   JWKS URL: https://your-app-name.onrender.com/jwks
   Redirect URIs: https://your-app-name.onrender.com/launch
   ```

3. **Copy Credentials:**

   - Note the **Client ID**
   - Note the **Deployment ID**

4. **Update LTI Config:**

   - In Render, go to **Shell** tab
   - Edit `configs/lti_config.json`:

   ```json
   {
     "https://your-openedx.com": {
       "client_id": "paste-client-id-here",
       "auth_login_url": "https://your-openedx.com/api/lti/1.3/authorize/",
       "auth_token_url": "https://your-openedx.com/oauth2/token/",
       "key_set_url": "https://your-openedx.com/api/lti/1.3/jwks/",
       "private_key_file": "keys/private.key",
       "public_key_file": "keys/public.key",
       "deployment_ids": ["paste-deployment-id-here"]
     }
   }
   ```

   Or update via environment variable or use Render's file upload feature.

### Step 5: Test the Integration

1. **Add LTI Component in OpenEdX:**

   - Go to OpenEdX Studio
   - Add **LTI Consumer** XBlock
   - Configure with your tool's URLs
   - Publish the course

2. **Launch from OpenEdX:**
   - Open the course as a student
   - Click on the LTI component
   - You should see your tool's launch page! 🎉

## 🔧 Configuration Options

### Environment Variables

| Variable           | Required | Default        | Description      |
| ------------------ | -------- | -------------- | ---------------- |
| `FLASK_SECRET_KEY` | Yes      | Auto-generated | Flask secret key |
| `TOOL_BASE_URL`    | Yes      | -              | Your Render URL  |
| `OPENEDX_BASE_URL` | Yes      | -              | Your OpenEdX URL |
| `SESSION_TYPE`     | No       | filesystem     | Session backend  |
| `LOG_LEVEL`        | No       | INFO           | Logging level    |

### Session Storage Options

#### Option 1: Filesystem (Default - Free Tier)

```yaml
SESSION_TYPE=filesystem
```

- Uses Render's persistent disk
- Works with free tier
- Good for low-medium traffic

#### Option 2: Redis (Production)

```yaml
SESSION_TYPE=redis
REDIS_HOST=your-redis-host
REDIS_PORT=6379
REDIS_PASSWORD=your-password
```

- Better performance
- Supports multiple instances
- Requires Redis add-on ($7/month)

### Upgrading Plans

**Free Tier Limitations:**

- ⚠️ Spins down after 15 minutes of inactivity
- ⚠️ Cold start delay (~30 seconds)
- ✅ Good for testing/development

**Starter Tier ($7/month):**

- ✅ Always on (no spin down)
- ✅ Instant response
- ✅ Better for production

**Recommended for Production:** Starter + Redis

## 📊 Monitoring & Logs

### View Logs

```bash
# In Render Dashboard:
1. Go to your service
2. Click "Logs" tab
3. View real-time logs
```

### Health Check

- Render automatically monitors: `/api/status`
- Check manually: `https://your-app-name.onrender.com/api/status`

### Metrics

- CPU usage
- Memory usage
- Request counts
- Response times

## 🐛 Troubleshooting

### Build Fails

**Issue:** Build script fails

```bash
# Check build logs in Render
# Common fixes:
1. Make build.sh executable: chmod +x build.sh
2. Check Node.js version compatibility
3. Verify requirements.txt is correct
```

**Issue:** OpenSSL key generation fails

```bash
# Render should have OpenSSL installed
# Check build logs for specific errors
```

### Cold Start Issues (Free Tier)

**Issue:** 30-second delay on first request

```bash
# Solutions:
1. Upgrade to Starter tier ($7/month)
2. Use a service like UptimeRobot to ping every 14 minutes
3. Accept the limitation for development
```

### LTI Launch Fails

**Issue:** "Invalid LTI launch"

```bash
# Checklist:
1. ✅ TOOL_BASE_URL is correct (HTTPS)
2. ✅ configs/lti_config.json has correct credentials
3. ✅ OpenEdX has correct Launch/Login/JWKS URLs
4. ✅ SESSION_COOKIE_SECURE=True (required for HTTPS)
5. ✅ Keys exist in keys/ directory
```

**Issue:** Session issues in iframe

```bash
# Check:
1. SESSION_COOKIE_SAMESITE=None (in config.py)
2. SESSION_COOKIE_SECURE=True
3. Using HTTPS (Render provides this automatically)
```

### Configuration Issues

**Issue:** Can't update lti_config.json

```bash
# Options:
1. Use Render Shell to edit file
2. Add as environment variable (JSON string)
3. Upload via git and redeploy
4. Use Render's secret file feature
```

## 🔐 Security Best Practices

1. **Use Secret Keys:**

   - Let Render auto-generate `FLASK_SECRET_KEY`
   - Never commit `.env` to Git

2. **Protect Private Keys:**

   - Generated automatically in build
   - Never commit to repository
   - Stored in ephemeral disk

3. **HTTPS Only:**

   - Render provides free SSL
   - Always use `SESSION_COOKIE_SECURE=True`

4. **Limit Access:**
   - Configure `ALLOWED_HOSTS` for production
   - Use OpenEdX IP whitelisting if needed

## 🚀 Advanced: Custom Domain

1. **Upgrade to Starter Tier** ($7/month minimum)

2. **Add Custom Domain:**

   - Go to service settings
   - Click "Custom Domains"
   - Add your domain
   - Update DNS records

3. **Update Configuration:**
   - Change `TOOL_BASE_URL` to your domain
   - Update OpenEdX configuration
   - Redeploy

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/latest/deploying/)
- [LTI 1.3 Specification](https://www.imsglobal.org/spec/lti/v1p3)
- [OpenEdX LTI Documentation](https://edx.readthedocs.io/projects/edx-installing-configuring-and-running/en/latest/configuration/lti.html)

## 💰 Cost Estimate

### Development/Testing

- **Web Service**: Free
- **Total**: $0/month
- **Note**: Service spins down after 15 min

### Production (Recommended)

- **Web Service**: $7/month (Starter)
- **Redis**: $7/month (optional)
- **Total**: $7-14/month

### High Traffic

- **Web Service**: $25-85/month (Pro/Pro Plus)
- **Redis**: $15+/month
- **Total**: $40-100+/month

## ✅ Deployment Checklist

Before going live:

- [ ] Code pushed to GitHub
- [ ] `render.yaml` configured
- [ ] Build script is executable
- [ ] Render service created
- [ ] All environment variables set
- [ ] `TOOL_BASE_URL` updated
- [ ] Persistent disk added (for filesystem sessions)
- [ ] OpenEdX tool configured
- [ ] LTI config updated with credentials
- [ ] Test launch successful
- [ ] Health check working
- [ ] Logs reviewed
- [ ] Error handling tested
- [ ] Consider upgrading from free tier

## 🎉 Success!

Your LTI 1.3 tool should now be live at:

```
https://your-app-name.onrender.com
```

**Next Steps:**

1. Test thoroughly in OpenEdX
2. Monitor logs and performance
3. Consider upgrading for production use
4. Add custom features and content
5. Share with your team!

---

Need help? Check the [GitHub Issues](https://github.com/yourusername/edx-lti-tool/issues) or Render support.
