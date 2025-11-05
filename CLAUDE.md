# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a minimal LTI 1.3 (Learning Tools Interoperability) tool starter project for OpenEdX integration. It implements the full OAuth 2.0/OIDC authentication flow required by LTI 1.3 specification using Flask and PyLTI1p3.

## Essential Commands

### Development Setup & Running

```bash
# Install dependencies (using uv - 10-100x faster than pip)
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
npm install

# Build TailwindCSS
npm run dev     # Watch mode for development
npm run build   # Production minified build

# Run the application
uv run python app.py              # Debug mode on port 5000
uv run flask run                  # Flask CLI
uv run gunicorn -w 4 -b 0.0.0.0:5000 app:app  # Production
```

### Code Quality & Testing

```bash
# Linting and formatting with Ruff (replaces black+flake8+isort)
uv run ruff check .               # Check for issues
uv run ruff check . --fix         # Auto-fix issues
uv run ruff format .              # Format code
uv run ruff check . --watch       # Watch mode

# Testing
uv run pytest                     # Run all tests
uv run pytest -v path/to/test.py # Run specific test
uv run pytest --cov=.            # With coverage

# Type checking
uv run mypy app.py config.py utils/
```

### Installation Options

```bash
# Install all extras (dev + test + docs)
uv pip install -e ".[all]"

# Install specific groups
uv pip install -e ".[dev]"
uv pip install -e ".[test]"
```

## Architecture & Key Components

### LTI 1.3 Flow Implementation

The application implements a three-step LTI 1.3 launch flow:

1. **Login Initiation** (`/login` endpoint in `app.py`):
   - Receives OIDC login request from platform (OpenEdX)
   - Validates issuer and login hint
   - Redirects to platform's authentication endpoint

2. **Authentication** (handled by OpenEdX):
   - Platform authenticates user
   - Creates signed JWT with user/course claims

3. **Resource Launch** (`/launch` endpoint in `app.py`):
   - Receives and validates JWT using PyLTI1p3
   - Extracts user and course context
   - Stores session data for subsequent requests
   - Renders tool content

### Critical Configuration Files

- **`configs/lti_config.json`**: Platform registration data
  - Must contain correct client_id and deployment_ids from OpenEdX
  - Points to RSA key files for JWT signing/verification
  - Each platform (issuer) has its own configuration block

- **`keys/private.key` & `keys/public.key`**: RSA 2048-bit keypair
  - Private key signs tool's responses
  - Public key exposed via `/jwks` endpoint for platform verification
  - Never commit private key (already in .gitignore)

### Session Management

- Uses Flask-Session with configurable backend (filesystem/Redis)
- Session cookies configured with `SameSite=None` for iframe compatibility
- Required for maintaining state between LTI launch and subsequent requests

### Key Utility Functions (`utils/lti_utils.py`)

- `get_user_info()`: Extracts user claims from JWT (name, email, roles)
- `get_course_info()`: Extracts course context (course_id, title)
- `get_launch_data_storage()`: Manages PyLTI1p3's launch state
- Role parsing distinguishes Instructor/Student/Administrator roles

## OpenEdX Integration Specifics

### Platform URLs Pattern
```
OIDC Auth: https://{domain}/api/lti/1.3/authorize/
Token URL: https://{domain}/oauth2/token/
JWKS URL: https://{domain}/api/lti/1.3/jwks/
```

### Required Endpoints for Registration
- Launch URL: `https://yourtool.com/launch`
- Login URL: `https://yourtool.com/login`
- JWKS URL: `https://yourtool.com/jwks`

## Development Workflow with uv + Ruff

This project uses two Rust-based tools for exceptional performance:
- **uv**: Package manager (10-100x faster than pip)
- **ruff**: Linter/formatter (10-30x faster than black+flake8)

When modifying Python code:
1. Use `uv run ruff check . --watch` for real-time feedback
2. Before committing: `uv run ruff check . --fix && uv run ruff format .`

## Environment Variables (.env)

Critical settings that must be configured:
- `FLASK_SECRET_KEY`: Session encryption key
- `FLASK_ENV`: development/production
- `SESSION_TYPE`: filesystem/redis
- `SESSION_COOKIE_SECURE`: True in production (HTTPS required)
- `TOOL_BASE_URL`: Public URL of the tool

## Testing Locally with ngrok

For OpenEdX integration testing:
```bash
ngrok http 5000
# Use the HTTPS URL provided by ngrok in OpenEdX tool configuration
```

## Extension Points

The codebase is designed to be extended with:
- **AGS (Assignment and Grade Services)**: Check with `message_launch.has_ags()`
- **NRPS (Names and Role Provisioning)**: Check with `message_launch.has_nrps()`
- **Deep Linking**: Check with `message_launch.is_deep_link_launch()`

These are stubbed but not implemented in the minimal version.