"""
Configuration module for the LTI 1.3 Tool
Manages all application settings and environment variables
"""

from datetime import timedelta
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class"""

    # Flask Configuration
    SECRET_KEY = (
        os.environ.get("FLASK_SECRET_KEY") or "dev-secret-key-change-in-production"
    )
    DEBUG = os.environ.get("FLASK_ENV") == "development"

    # Session Configuration
    SESSION_TYPE = os.environ.get(
        "SESSION_TYPE", "filesystem"
    )  # Options: filesystem, redis, memcached
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

    # Session Cookie Configuration (Required for LTI in iframes)
    SESSION_COOKIE_NAME = "lti_session"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "False").lower() in ("true", "1", "yes")
    SESSION_COOKIE_SAMESITE = "None"  # Required for iframe embedding
    SESSION_COOKIE_DOMAIN = os.environ.get("SESSION_COOKIE_DOMAIN", None)

    # Redis Configuration (if using Redis for sessions)
    if SESSION_TYPE == "redis":
        SESSION_REDIS = {
            "host": os.environ.get("REDIS_HOST", "localhost"),
            "port": int(os.environ.get("REDIS_PORT", 6379)),
            "db": int(os.environ.get("REDIS_DB", 0)),
            "password": os.environ.get("REDIS_PASSWORD", None),
        }

    # Tool Configuration
    TOOL_NAME = os.environ.get("TOOL_NAME", "Minimal LTI 1.3 Tool")
    TOOL_DESCRIPTION = os.environ.get(
        "TOOL_DESCRIPTION", "A minimal LTI 1.3 tool for OpenEdX"
    )
    TOOL_VERSION = "1.0.0"
    TOOL_SUPPORT_EMAIL = os.environ.get("TOOL_SUPPORT_EMAIL", "support@example.com")

    # URLs (for production deployment)
    TOOL_BASE_URL = os.environ.get("TOOL_BASE_URL", "http://localhost:5000")

    # OpenEdX Platform URLs (default values)
    OPENEDX_BASE_URL = os.environ.get("OPENEDX_BASE_URL", "https://courses.edx.org")

    # Logging Configuration
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    LOG_FILE = os.environ.get("LOG_FILE", "lti_tool.log")

    # Security
    ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")
    CSRF_ENABLED = True

    # File Upload Configuration (if needed in future)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")

    # Database Configuration (if needed in future)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///lti_tool.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        # Create necessary directories
        os.makedirs("logs", exist_ok=True)
        os.makedirs("uploads", exist_ok=True)
        os.makedirs("configs", exist_ok=True)

        # Set up logging
        import logging
        from logging.handlers import RotatingFileHandler

        if not app.debug:
            file_handler = RotatingFileHandler(
                Config.LOG_FILE,
                maxBytes=10240000,  # 10MB
                backupCount=10,
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
                )
            )
            file_handler.setLevel(getattr(logging, Config.LOG_LEVEL))
            app.logger.addHandler(file_handler)
            app.logger.setLevel(getattr(logging, Config.LOG_LEVEL))
            app.logger.info("LTI Tool startup")


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    SESSION_COOKIE_SECURE = False  # Allow HTTP in development
    TOOL_BASE_URL = "http://localhost:5000"


class ProductionConfig(Config):
    """Production configuration"""

    DEBUG = False
    SESSION_COOKIE_SECURE = True  # Enforce HTTPS
    SESSION_TYPE = "redis"  # Use Redis in production

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # Production-specific initialization
        # Log to syslog
        import logging
        from logging.handlers import SysLogHandler

        syslog = SysLogHandler()
        syslog.setLevel(logging.WARNING)
        app.logger.addHandler(syslog)


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
    SESSION_TYPE = "filesystem"
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}


def get_config():
    """Get configuration based on environment"""
    env = os.environ.get("FLASK_ENV", "development")
    return config.get(env, config["default"])
