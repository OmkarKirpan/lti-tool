"""
Minimal LTI 1.3 Tool for OpenEdX
Flask application with PyLTI1p3 integration
"""

import os

from flask import Flask, jsonify, render_template, request, session, url_for
from flask_session import Session
from pylti1p3.contrib.flask import FlaskMessageLaunch, FlaskOIDCLogin, FlaskRequest
from pylti1p3.exception import LtiException
from pylti1p3.tool_config import ToolConfJsonFile

from config import Config
from utils.lti_utils import get_course_info, get_launch_data_storage, get_user_info

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Configure session
Session(app)


def get_lti_config_path():
    """Get the path to the LTI configuration file"""
    return os.path.join(os.path.dirname(__file__), "configs", "lti_config.json")


@app.route("/")
def index():
    """Home page - information about the tool"""
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    OIDC Login endpoint
    Handles the OpenID Connect login initiation from the platform
    """
    try:
        tool_conf = ToolConfJsonFile(get_lti_config_path())
        flask_request = FlaskRequest()

        # Get target link URI from request
        target_link_uri = request.values.get("target_link_uri")
        if not target_link_uri:
            target_link_uri = url_for("launch", _external=True)

        # Initialize OIDC login
        oidc_login = FlaskOIDCLogin(
            flask_request, tool_conf, launch_data_storage=get_launch_data_storage()
        )

        # Redirect to platform's authentication endpoint
        return oidc_login.redirect(target_link_uri)

    except Exception as e:
        app.logger.error(f"Login error: {str(e)}")
        return render_template(
            "error.html", error_message="Failed to initiate login", error_details=str(e)
        ), 400


@app.route("/launch", methods=["POST"])
def launch():
    """
    LTI Launch endpoint
    Handles the actual LTI launch after successful authentication
    """
    try:
        tool_conf = ToolConfJsonFile(get_lti_config_path())
        flask_request = FlaskRequest()

        # Initialize and validate the message launch
        message_launch = FlaskMessageLaunch(
            flask_request, tool_conf, launch_data_storage=get_launch_data_storage()
        )

        # Get launch data
        launch_data = message_launch.get_launch_data()

        # Extract user and course information
        user_info = get_user_info(message_launch)
        course_info = get_course_info(message_launch)

        # Check if this is a resource launch
        is_resource_launch = message_launch.is_resource_launch()

        # Check if deep linking is requested
        is_deep_link = message_launch.is_deep_link_launch()

        # Get custom parameters if any
        custom_params = launch_data.get(
            "https://purl.imsglobal.org/spec/lti/claim/custom", {}
        )

        # Store important data in session for future requests
        session["user_id"] = user_info.get("user_id")
        session["course_id"] = course_info.get("course_id")
        session["is_instructor"] = "Instructor" in user_info.get("roles", [])

        # Log successful launch
        app.logger.info(
            f"Successful launch for user {user_info.get('user_id')} "
            f"in course {course_info.get('course_id')}"
        )

        return render_template(
            "launch.html",
            user_info=user_info,
            course_info=course_info,
            custom_params=custom_params,
            is_resource_launch=is_resource_launch,
            is_deep_link=is_deep_link,
            launch_id=launch_data.get("nonce", "N/A"),
        )

    except LtiException as e:
        app.logger.error(f"LTI launch error: {str(e)}")
        return render_template(
            "error.html", error_message="Invalid LTI launch", error_details=str(e)
        ), 400

    except Exception as e:
        app.logger.error(f"Unexpected launch error: {str(e)}")
        return render_template(
            "error.html", error_message="Launch failed", error_details=str(e)
        ), 500


@app.route("/jwks", methods=["GET"])
def jwks():
    """
    JWKS endpoint
    Returns the tool's public key in JWKS format for the platform to verify signatures
    """
    try:
        tool_conf = ToolConfJsonFile(get_lti_config_path())
        # Get all public keys in JWKS format
        jwks_data = tool_conf.get_jwks()
        return jsonify(jwks_data)

    except Exception as e:
        app.logger.error(f"JWKS error: {str(e)}")
        return jsonify({"error": "Failed to retrieve JWKS"}), 500


@app.route("/configure", methods=["GET"])
def configure():
    """
    Dynamic Registration endpoint
    Returns configuration for automatic tool registration
    """
    config_data = {
        "title": "Minimal LTI 1.3 Tool",
        "description": "A minimal LTI 1.3 tool for OpenEdX integration",
        "oidc_login_url": url_for("login", _external=True),
        "launch_url": url_for("launch", _external=True),
        "jwks_url": url_for("jwks", _external=True),
        "target_link_uri": url_for("launch", _external=True),
        "custom_parameters": {
            "tool_version": "1.0.0",
            "support_email": "support@example.com",
        },
        "claims": [
            "iss",
            "sub",
            "name",
            "given_name",
            "family_name",
            "email",
            "locale",
        ],
        "messages": [
            {"type": "LtiResourceLinkRequest"},
            {"type": "LtiDeepLinkingRequest"},
        ],
    }

    return jsonify(config_data)


@app.route("/api/status", methods=["GET"])
def api_status():
    """
    Status endpoint for health checks
    """
    # Check if user is authenticated
    if "user_id" not in session:
        return jsonify(
            {"status": "ok", "authenticated": False, "message": "Tool is running"}
        )

    return jsonify(
        {
            "status": "ok",
            "authenticated": True,
            "user_id": session.get("user_id"),
            "course_id": session.get("course_id"),
            "is_instructor": session.get("is_instructor", False),
        }
    )


@app.errorhandler(403)
def forbidden(error):
    """Handle 403 errors"""
    return render_template(
        "error.html",
        error_message="Access Forbidden",
        error_details="You don't have permission to access this resource.",
    ), 403


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template(
        "error.html",
        error_message="Page Not Found",
        error_details="The requested page could not be found.",
    ), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template(
        "error.html",
        error_message="Internal Server Error",
        error_details="An unexpected error occurred.",
    ), 500


# Development server
if __name__ == "__main__":
    # Check if keys exist
    if not os.path.exists("keys/private.key") or not os.path.exists("keys/public.key"):
        print("Warning: RSA keys not found. Please generate keys first.")
        print("Run: python generate_keys.py")

    # Check if config exists
    if not os.path.exists(get_lti_config_path()):
        print("Warning: LTI configuration not found at", get_lti_config_path())
        print("Please create the configuration file.")

    # Run the development server
    app.run(host="0.0.0.0", port=5000, debug=True)
