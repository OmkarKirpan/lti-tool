# 🎓 Minimal OpenEdX LTI 1.3 Tool

A production-ready, minimal LTI 1.3 tool starter project for OpenEdX integration using Python Flask and TailwindCSS.

## ✨ Features

- **Full LTI 1.3 Compliance**: OAuth 2.0 and OpenID Connect (OIDC) authentication
- **OpenEdX Ready**: Pre-configured for OpenEdX platform integration
- **Modern UI**: Beautiful, responsive interface with TailwindCSS
- **Secure**: JWT validation, CSRF protection, secure session management
- **Extensible**: Ready for AGS (grading), NRPS (roster), Deep Linking
- **Production Ready**: Includes Gunicorn configuration and Redis session support
- **⚡ Lightning Fast Setup**: Uses `uv` for 10-100x faster dependency installation
- **🚀 One-Click Deploy**: Deploy to Render.com in minutes with Blueprint config
- **💰 Free Tier Ready**: Works perfectly on Render's free tier for testing/small courses

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+ (for TailwindCSS)
- OpenSSL (for key generation)
- Redis (optional, for production sessions)
- OpenEdX instance with LTI 1.3 support

## 🚀 Quick Start

### 🌐 Option A: Deploy to Render.com (Fastest!)

**Best for:** Getting started quickly, production deployment

1. **Push your code to GitHub**
2. **Deploy in 3 clicks** - See `DEPLOYMENT_CHECKLIST.md`
3. **Configure OpenEdX** with your Render URLs
4. **Done!** - Your tool is live 🎉

**Time:** 5-10 minutes | **Cost:** Free (or $7/month for always-on)

👉 **See `DEPLOYMENT_CHECKLIST.md` for step-by-step instructions**

---

### 💻 Option B: Local Development (Using uv - Recommended)

[uv](https://github.com/astral-sh/uv) is an extremely fast Python package manager written in Rust.

#### 1. Install uv and Setup

```bash
# Install uv (one-time setup)
curl -LsSf https://astral.sh/uv/install.sh | sh
# On Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Navigate to project
cd edxLTI

# Create virtual environment with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies (super fast! 🚀)
uv pip install -r requirements.txt

# Install Node dependencies
npm install
```

#### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

Update the following in `.env`:
- `FLASK_SECRET_KEY`: Generate with `uv run python -c "import secrets; print(secrets.token_hex(32))"`
- `TOOL_BASE_URL`: Your tool's URL (e.g., `https://yourtool.com`)
- `OPENEDX_BASE_URL`: Your OpenEdX instance URL

#### 3. Build TailwindCSS

```bash
# Development (with watch mode)
npm run dev

# Production (minified)
npm run build
```

#### 4. Configure OpenEdX Platform

Edit `configs/lti_config.json` with your OpenEdX platform details:

```json
{
  "https://your-openedx-domain.com": {
    "client_id": "YOUR_CLIENT_ID",
    "auth_login_url": "https://your-openedx-domain.com/api/lti/1.3/authorize/",
    "auth_token_url": "https://your-openedx-domain.com/oauth2/token/",
    "key_set_url": "https://your-openedx-domain.com/api/lti/1.3/jwks/",
    "private_key_file": "../keys/private.key",
    "public_key_file": "../keys/public.key",
    "deployment_ids": ["YOUR_DEPLOYMENT_ID"]
  }
}
```

#### 5. Run the Application

```bash
# Development
uv run flask run

# Or with debug mode
uv run python app.py

# Production with Gunicorn
uv run gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Or run without activating venv (uv detects it automatically)
uv run python app.py
```

### 💻 Option C: Local Development (Using pip)

<details>
<summary>Click to expand pip installation instructions</summary>

#### 1. Clone and Setup

```bash
# Navigate to project
cd edxLTI

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies
npm install
```

#### 2. Configure Environment

Same as Option A above.

#### 3. Build TailwindCSS

Same as Option A above.

#### 4. Configure OpenEdX Platform

Same as Option A above.

#### 5. Run the Application

```bash
# Development
flask run

# Or with debug mode
python app.py

# Production with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

</details>

The tool will be available at `http://localhost:5000`

## ⚡ Why uv?

Using `uv` instead of `pip` provides significant benefits:

- **Speed**: 10-100x faster package installation
- **Reliability**: Better dependency resolution using PubGrub algorithm
- **Disk Space**: Global cache reduces duplicate downloads
- **Convenience**: Built-in virtual environment management
- **Compatibility**: Works with existing `requirements.txt` files

**Performance Example**: Installing this project's dependencies:
- `pip`: ~30-60 seconds
- `uv`: ~2-5 seconds (first run), ~1 second (cached)

## 🔧 OpenEdX Configuration

### Platform Registration

1. Access OpenEdX Django Admin: `https://your-openedx.com/admin`
2. Navigate to **LTI 1.3 Tool Configuration**
3. Create a new tool configuration with:
   - **Tool Name**: Minimal LTI 1.3 Tool
   - **Launch URL**: `https://yourtool.com/launch`
   - **Login URL**: `https://yourtool.com/login`
   - **JWKS URL**: `https://yourtool.com/jwks`
4. Note the generated **Client ID** and **Deployment ID**
5. Update `configs/lti_config.json` with these values

### Course Integration

1. In OpenEdX Studio, go to your course
2. Navigate to **Advanced Settings**
3. Add an LTI Consumer XBlock
4. Configure with your tool's URLs
5. Save and publish

## 📁 Project Structure

```
edxLTI/
├── app.py                        # Main Flask application
├── config.py                     # Configuration management
├── requirements.txt              # Python dependencies
├── pyproject.toml               # Modern Python project config
├── package.json                 # Node dependencies
├── tailwind.config.js           # TailwindCSS configuration
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
│
├── 🚀 Deployment Files
├── render.yaml                 # Render Blueprint config
├── build.sh                    # Build script for Render
├── DEPLOYMENT_CHECKLIST.md     # Quick deployment guide
├── RENDER_FREE_TIER.md         # Free tier setup guide
├── RENDER_DEPLOYMENT.md        # Complete deployment guide
│
├── configs/
│   └── lti_config.json        # LTI platform configurations
├── keys/
│   ├── private.key            # RSA private key (generated)
│   └── public.key             # RSA public key (generated)
├── templates/
│   ├── base.html             # Base template
│   ├── index.html            # Home page
│   ├── launch.html           # Launch success page
│   └── error.html            # Error page
├── static/
│   ├── css/
│   │   ├── input.css         # TailwindCSS input
│   │   └── output.css        # Compiled CSS
│   └── js/
│       └── main.js           # JavaScript (optional)
└── utils/
    └── lti_utils.py          # LTI helper functions
```

## 🔑 Key Generation

The RSA keys have already been generated, but if you need new ones:

```bash
# Generate new RSA key pair
openssl genrsa -out keys/private.key 2048
openssl rsa -in keys/private.key -pubout -out keys/public.key
```

**Important**: Never commit private keys to version control!

## 🌐 Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with tool information |
| `/login` | GET/POST | OIDC login initiation |
| `/launch` | POST | LTI launch handler |
| `/jwks` | GET | Public keys in JWKS format |
| `/configure` | GET | Dynamic registration config |
| `/api/status` | GET | Health check endpoint |

## 🔒 Security Features

- **JWT Validation**: Validates all LTI launch tokens
- **CSRF Protection**: Enabled by default
- **Secure Cookies**: HttpOnly, Secure, SameSite=None
- **Session Security**: Encrypted sessions with timeout
- **HTTPS Enforcement**: Required in production
- **Key Rotation**: Supports multiple keys

## 🌐 Deployment Options

This project supports multiple deployment methods:

| Platform | Difficulty | Cost | Setup Time | Best For |
|----------|-----------|------|------------|----------|
| **Render.com** | ⭐ Easy | Free-$7/mo | 5 min | **Recommended** - Quick deploy |
| **Docker** | ⭐⭐ Medium | Varies | 15 min | Container environments |
| **VPS/Server** | ⭐⭐⭐ Hard | Varies | 30+ min | Full control needed |

### 📋 Deployment Files Included

- `render.yaml` - Render Blueprint configuration (auto-deploy)
- `build.sh` - Build script for Render
- `DEPLOYMENT_CHECKLIST.md` - Quick deployment guide
- `RENDER_FREE_TIER.md` - Free tier setup and limitations  
- `RENDER_DEPLOYMENT.md` - Complete Render deployment guide
- `.env.example` - Environment variables template

## 🚢 Production Deployment

### 🎯 Deploy to Render.com (Recommended - Easiest!)

The fastest way to deploy this LTI tool is using [Render.com](https://render.com) with our Blueprint configuration.

#### Free Tier Deployment (Perfect for testing!)

```bash
# 1. Push to GitHub
git add .
git commit -m "Deploy to Render"
git push origin main

# 2. Deploy on Render
# - Go to https://dashboard.render.com
# - Click "New +" → "Blueprint"
# - Select your repository
# - Click "Apply"
# 
# Done! Your tool will be live in ~5-10 minutes 🎉
```

**📚 Deployment Guides:**
- **Quick Start:** See `DEPLOYMENT_CHECKLIST.md` for step-by-step instructions
- **Free Tier:** See `RENDER_FREE_TIER.md` for free tier details and limitations
- **Complete Guide:** See `RENDER_DEPLOYMENT.md` for advanced configuration

**✨ Why Render?**
- ✅ Free tier available (perfect for dev/testing)
- ✅ Automatic HTTPS with free SSL certificates
- ✅ Auto-deploy from GitHub
- ✅ Built-in persistent disk support (Starter tier+)
- ✅ One-click deployment with Blueprint
- ✅ No credit card required for free tier

**Free Tier Notes:**
- Service spins down after 15 min inactivity (~30s cold start)
- No persistent disk (but sessions work fine for LTI!)
- Perfect for development, testing, and small courses
- Upgrade to Starter ($7/month) for always-on service

### Using Gunicorn (Traditional Deployment)

```bash
# With uv (recommended)
uv run gunicorn -w 4 -b 0.0.0.0:5000 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  app:app

# Or with traditional pip
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  app:app
```

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

# Install uv for faster builds
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies with uv (much faster!)
RUN uv pip install --system -r requirements.txt

# Copy application code
COPY . .

# Build TailwindCSS
RUN apt-get update && apt-get install -y nodejs npm && \
    npm install && npm run build && \
    apt-get remove -y nodejs npm && apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

<details>
<summary>Alternative Dockerfile using pip</summary>

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Build TailwindCSS
RUN apt-get update && apt-get install -y nodejs npm
RUN npm install && npm run build

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

</details>

Build and run:

```bash
docker build -t lti-tool .
docker run -p 5000:5000 --env-file .env lti-tool
```

### Environment Variables for Production

```bash
FLASK_ENV=production
FLASK_SECRET_KEY=<strong-secret-key>
SESSION_TYPE=redis
REDIS_HOST=redis-server
REDIS_PORT=6379
SESSION_COOKIE_SECURE=True
TOOL_BASE_URL=https://yourtool.com
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourtool.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourtool.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🧪 Testing & Code Quality

```bash
# With uv and ruff (lightning fast! ⚡)
uv run pytest
uv run pytest --cov=.
uv run ruff check .          # Lint code
uv run ruff format . --check # Check formatting
uv run ruff format .         # Auto-format code

# Or use uvx to run without installing
uvx pytest
uvx ruff check .
uvx ruff format .

# With pip
pytest
pytest --cov=.
ruff check .
ruff format .
```

### Ruff Commands (Replaces black + flake8 + isort)

```bash
# Check for linting issues
uv run ruff check .

# Auto-fix linting issues
uv run ruff check . --fix

# Check formatting
uv run ruff format . --check

# Auto-format code
uv run ruff format .

# Watch mode for automatic fixes
uv run ruff check . --watch
```

## 📝 Development Tips

### Using uv for Development

```bash
# Install a new package
uv pip install package-name

# Update dependencies
uv pip install --upgrade package-name

# Sync environment with requirements.txt
uv pip sync requirements.txt

# Generate updated requirements.txt
uv pip freeze > requirements.txt

# Run any Python command with uv
uv run python script.py
uv run flask --app app.py --debug run
```

### TailwindCSS Development

```bash
# Watch for CSS changes
npm run dev

# The CSS will auto-rebuild when you modify templates
```

### Flask Debug Mode

```bash
# Enable debug mode in .env
FLASK_ENV=development

# Run with auto-reload (using uv)
uv run flask run --debug

# Or traditional method
flask run --debug
```

### Testing Locally with ngrok

```bash
# Install ngrok
brew install ngrok  # macOS
# or download from https://ngrok.com

# Expose local server
ngrok http 5000

# Use the generated HTTPS URL in OpenEdX configuration
```

## 📦 uv Command Reference

Quick reference for common uv commands used in this project:

```bash
# Virtual Environment
uv venv                          # Create venv
source .venv/bin/activate        # Activate (same as before)

# Package Management
uv pip install -r requirements.txt     # Install deps
uv pip install package               # Install package
uv pip uninstall package             # Remove package
uv pip list                          # List installed
uv pip freeze > requirements.txt    # Export deps
uv pip sync requirements.txt        # Sync exact deps

# Running Commands
uv run python app.py            # Run script
uv run flask run                # Run Flask
uv run pytest                   # Run tests
uvx ruff check .                # Run tool without installing
```

## 🔄 Extending the Tool

### Adding Grade Passback (AGS)

```python
# In app.py launch endpoint
if message_launch.has_ags():
    ags = message_launch.get_ags()
    # Send grades back to OpenEdX
```

### Adding Roster Access (NRPS)

```python
# In app.py launch endpoint
if message_launch.has_nrps():
    nrps = message_launch.get_nrps()
    # Get course roster
```

### Adding Deep Linking

```python
# Check for deep linking launch
if message_launch.is_deep_link_launch():
    # Handle content selection
```

## 🐛 Troubleshooting

### Common Issues

1. **"Invalid LTI launch"**
   - Check if cookies are enabled
   - Verify clock synchronization
   - Ensure HTTPS in production
   - Check session configuration

2. **"Failed to initiate login"**
   - Verify platform URLs in config
   - Check client ID and deployment ID
   - Ensure tool is registered in OpenEdX

3. **Session issues in iframe**
   - Ensure `SESSION_COOKIE_SAMESITE='None'`
   - Use HTTPS in production
   - Check browser third-party cookie settings

4. **CSS not loading**
   - Run `npm run build`
   - Check that `output.css` exists
   - Verify static file serving

5. **uv not found**
   - Ensure uv is installed: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Restart terminal or run `source ~/.bashrc` (or `~/.zshrc`)
   - Check PATH includes `~/.cargo/bin`

6. **Render deployment issues**
   - See `RENDER_DEPLOYMENT.md` troubleshooting section
   - Check build logs in Render dashboard
   - Verify `TOOL_BASE_URL` is set correctly
   - Ensure `configs/lti_config.json` has correct credentials

### Debug Mode

Enable debug logging:

```python
# In .env
FLASK_ENV=development
LOG_LEVEL=DEBUG
```

Check logs:
```bash
tail -f lti_tool.log
```

## 🔄 Migrating from pip to uv

If you have an existing environment with pip:

```bash
# Deactivate current venv
deactivate

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Remove old venv
rm -rf venv

# Create new venv with uv
uv venv

# Activate and install
source .venv/bin/activate
uv pip install -r requirements.txt
```

That's it! Your project now uses uv for faster dependency management.

## 📚 Resources

### Documentation
- **Quick Deploy:** `DEPLOYMENT_CHECKLIST.md` - Fast deployment to Render
- **Free Tier Guide:** `RENDER_FREE_TIER.md` - Free tier setup and limitations
- **Complete Guide:** `RENDER_DEPLOYMENT.md` - Advanced deployment options

### External Resources
- [LTI 1.3 Specification](https://www.imsglobal.org/spec/lti/v1p3)
- [PyLTI1p3 Documentation](https://github.com/dmitry-viskov/pylti1.3)
- [OpenEdX LTI Documentation](https://edx.readthedocs.io/projects/edx-installing-configuring-and-running/en/latest/configuration/lti.html)
- [Render Documentation](https://render.com/docs)
- [uv Documentation](https://github.com/astral-sh/uv)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙋 Support

For issues or questions:
- Email: support@example.com
- GitHub Issues: [Create an issue](https://github.com/yourusername/lti-tool/issues)

---

Built with ❤️ and ⚡ for the OpenEdX community