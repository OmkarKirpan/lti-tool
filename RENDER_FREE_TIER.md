# 🆓 Deploying on Render Free Tier

This guide covers deploying your LTI tool on Render's **free tier** and explains the limitations.

## ⚡ Quick Deploy (Free Tier)

The current `render.yaml` is configured for **free tier** deployment. Just follow these steps:

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Deploy to Render free tier"
   git push origin main
   ```

2. **Deploy on Render:**
   - Go to [dashboard.render.com](https://dashboard.render.com)
   - Click **"New +"** → **"Blueprint"**
   - Select your repository
   - Click **"Apply"**

3. **Done!** Your app will be live in ~5-10 minutes.

## 🔍 Free Tier Characteristics

### What Works ✅
- ✅ Full LTI 1.3 functionality
- ✅ User authentication and launch
- ✅ Grade passback (AGS)
- ✅ Session management during active use
- ✅ HTTPS with free SSL certificate
- ✅ Custom domains (with manual DNS setup)
- ✅ Automatic deploys from GitHub

### Limitations ⚠️

#### 1. **Service Spin Down**
- **What:** Service goes to sleep after 15 minutes of inactivity
- **Impact:** First request after spin-down takes ~30 seconds (cold start)
- **Acceptable for:** Development, testing, low-traffic courses
- **Solution:** Upgrade to Starter ($7/month) for always-on service

#### 2. **No Persistent Disk**
- **What:** Sessions stored in ephemeral (temporary) storage
- **Impact:** Active sessions lost when service restarts or spins down
- **Why it's OK:** LTI launches create fresh sessions each time, so this is actually fine for LTI tools!
- **When to upgrade:** If you need to store user data between sessions

#### 3. **Resource Limits**
- **CPU:** Shared CPU
- **RAM:** 512 MB
- **Disk:** 512 MB ephemeral storage
- **Acceptable for:** Most LTI tools with moderate usage

## 📊 Free Tier vs Paid Plans

| Feature | Free | Starter ($7/mo) | Standard ($25/mo) |
|---------|------|-----------------|-------------------|
| **Always On** | ❌ (spins down) | ✅ | ✅ |
| **Cold Start** | ~30 seconds | None | None |
| **Persistent Disk** | ❌ | ✅ 1GB+ | ✅ 1GB+ |
| **RAM** | 512 MB | 512 MB | 2 GB |
| **CPU** | Shared | Shared | Dedicated |
| **Custom Domains** | ✅ | ✅ | ✅ |
| **SSL Certificate** | ✅ Free | ✅ Free | ✅ Free |

## 🎯 Session Management on Free Tier

### How It Works

1. **Active Usage:**
   - User launches LTI tool from OpenEdX
   - Session created and stored in ephemeral storage
   - Works perfectly during active use
   - Session timeout: 2 hours

2. **After Spin Down:**
   - Service goes to sleep (no active requests for 15 min)
   - Sessions in memory are lost
   - Next LTI launch creates a fresh session
   - **This is normal and expected for LTI tools!**

### Why This is OK for LTI

LTI tools are designed to be launched fresh each time:
- ✅ Each OpenEdX course access = new LTI launch
- ✅ New launch = new authentication = new session
- ✅ No data loss because LTI doesn't rely on persistent sessions
- ✅ User data (if needed) should be in a database, not sessions

### What Gets Lost on Restart
- ❌ Active user sessions (but LTI creates new ones on launch)
- ❌ Temporary data in `flask_session` directory
- ❌ Any data not in environment variables or code

### What Persists
- ✅ Environment variables
- ✅ Your code and configuration
- ✅ RSA keys (regenerated on each build if needed)
- ✅ LTI configuration

## 🚀 When to Upgrade

### Stick with Free If:
- ✅ Development and testing
- ✅ Small courses (< 50 students)
- ✅ Infrequent usage
- ✅ 30-second cold start is acceptable
- ✅ No need to store user data between sessions

### Upgrade to Starter ($7/month) If:
- 🎯 Production course with active students
- 🎯 Need instant response (no cold starts)
- 🎯 Want to store user data persistently
- 🎯 More than 50-100 active users
- 🎯 Course with frequent access

### Upgrade to Standard+ ($25+/month) If:
- 🎯 Large courses (500+ students)
- 🎯 High traffic
- 🎯 Need dedicated CPU
- 🎯 Multiple simultaneous users

## 🔄 Upgrading Your Plan

### To Enable Persistent Disk (Starter+)

1. **Upgrade to Starter in Render Dashboard**
   - Go to your service
   - Settings → Plan
   - Select "Starter"

2. **Uncomment disk configuration in `render.yaml`:**
   ```yaml
   disk:
     name: lti-sessions
     mountPath: /data
     sizeGB: 1
   ```

3. **Push changes:**
   ```bash
   git add render.yaml
   git commit -m "Enable persistent disk storage"
   git push
   ```

4. **Redeploy:** Render will automatically redeploy with persistent disk

### Alternative: Use Redis (Also Free!)

Render offers a **free Redis tier** that provides persistent session storage:

1. **Uncomment Redis in `render.yaml`:**
   ```yaml
   - type: redis
     name: lti-redis
     plan: free
     maxmemoryPolicy: allkeys-lru
     ipAllowList: []  # Internal connections only
   ```

2. **Update environment variables:**
   ```yaml
   - key: SESSION_TYPE
     value: redis
   
   - key: REDIS_HOST
     fromService:
       type: keyvalue
       name: lti-redis
       property: host
   
   - key: REDIS_PORT
     fromService:
       type: keyvalue
       name: lti-redis
       property: port
   ```

3. **Redis Free Tier:**
   - ✅ 25 MB storage (enough for sessions!)
   - ✅ Stays running (doesn't spin down)
   - ✅ Perfect for session storage
   - ⚠️ Limited to 25 MB

## 🧪 Testing on Free Tier

### What to Test:

1. **Cold Start Experience:**
   - Wait 15+ minutes
   - Launch LTI tool from OpenEdX
   - First request will take ~30 seconds
   - Subsequent requests will be fast

2. **LTI Launch Flow:**
   - Test initial launch
   - Test grade submission
   - Verify session works during active use

3. **After Spin Down:**
   - Verify new LTI launch works correctly
   - Confirm fresh session is created

### Known Behaviors:

- ⏰ First request after sleep: ~30 seconds
- 🚀 Active requests: < 1 second
- 💤 Spin down after: 15 minutes inactivity
- 🔄 Session lifetime: 2 hours (during active use)

## 💡 Workarounds for Free Tier Limitations

### 1. Keep Service Awake (Optional)

Use a service like [UptimeRobot](https://uptimerobot.com/) to ping your service every 14 minutes:
- ✅ Prevents spin down
- ✅ Eliminates cold starts
- ⚠️ May violate Render's Terms of Service
- ⚠️ Not officially recommended

### 2. Use Redis for Sessions

Switch to Redis (free tier available):
- ✅ Sessions persist through restarts
- ✅ Better performance
- ✅ Scales better
- See instructions above

### 3. Embrace Ephemeral

Design your tool to work without persistent sessions:
- ✅ LTI naturally creates fresh sessions
- ✅ Store critical data in environment variables
- ✅ Use external database if needed (not sessions)

## ✅ Free Tier Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Render Blueprint created
- [ ] Service deployed successfully
- [ ] Environment variables configured
- [ ] `TOOL_BASE_URL` set to your Render URL
- [ ] OpenEdX configured with LTI tool URLs
- [ ] `configs/lti_config.json` updated with credentials
- [ ] Test LTI launch from OpenEdX
- [ ] Test cold start behavior (optional)
- [ ] Test grade submission (AGS)
- [ ] Monitor logs for any issues

## 🆙 Next Steps

1. **Deploy and test on free tier**
2. **Evaluate performance with real usage**
3. **Decide if upgrade is needed**
4. **Consider Redis for better session management**

## 💰 Cost Calculator

### Development/Testing
- **Web Service:** Free
- **Redis:** Free (optional, recommended)
- **Total:** $0/month

### Production (Light Usage)
- **Web Service:** Free
- **Redis:** Free
- **Total:** $0/month
- **Users:** 50-100 students, infrequent access

### Production (Active Usage)
- **Web Service:** $7/month (Starter)
- **Redis:** Free or $7/month
- **Total:** $7-14/month
- **Users:** 100-500 students, regular access

## 📚 Resources

- [Render Free Tier Details](https://render.com/docs/free)
- [Managing Spin Down](https://render.com/docs/free#spinning-down-on-idle)
- [Upgrading Plans](https://render.com/docs/managing-your-account#changing-your-service-plan)

---

**Bottom Line:** The free tier is **perfect for development, testing, and small courses**. The session limitation is actually not a problem for LTI tools, since each launch creates a fresh session anyway! 🎉

