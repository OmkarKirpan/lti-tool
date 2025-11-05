"""
LTI Utility Functions
Helper functions for LTI operations and data extraction
"""

from datetime import datetime

from flask import session
from pylti1p3.launch_data_storage.session import FlaskSessionDataStorage


def get_launch_data_storage():
    """
    Get the launch data storage instance
    Uses Flask session for storing launch data
    """
    return FlaskSessionDataStorage()


def get_user_info(message_launch):
    """
    Extract user information from the LTI launch message

    Args:
        message_launch: The validated LTI message launch object

    Returns:
        dict: User information including ID, name, email, and roles
    """
    launch_data = message_launch.get_launch_data()

    # Extract basic user information
    user_info = {
        "user_id": launch_data.get("sub", "Unknown"),
        "name": launch_data.get("name", "Unknown User"),
        "given_name": launch_data.get("given_name", ""),
        "family_name": launch_data.get("family_name", ""),
        "email": launch_data.get("email", "no-email@example.com"),
        "locale": launch_data.get("locale", "en"),
        "picture": launch_data.get("picture", ""),  # Avatar URL if available
    }

    # Extract roles
    roles_claim = "https://purl.imsglobal.org/spec/lti/claim/roles"
    roles = launch_data.get(roles_claim, [])

    # Parse roles to friendly names
    user_info["roles"] = parse_roles(roles)
    user_info["raw_roles"] = roles

    # Determine primary role
    if any("Instructor" in role for role in roles):
        user_info["primary_role"] = "Instructor"
    elif any("Administrator" in role for role in roles):
        user_info["primary_role"] = "Administrator"
    elif any("ContentDeveloper" in role for role in roles):
        user_info["primary_role"] = "Content Developer"
    elif any("Learner" in role for role in roles):
        user_info["primary_role"] = "Student"
    else:
        user_info["primary_role"] = "Guest"

    # Check if user is staff/instructor
    user_info["is_instructor"] = user_info["primary_role"] in [
        "Instructor",
        "Administrator",
    ]

    return user_info


def get_course_info(message_launch):
    """
    Extract course/context information from the LTI launch message

    Args:
        message_launch: The validated LTI message launch object

    Returns:
        dict: Course information including ID, title, and label
    """
    launch_data = message_launch.get_launch_data()

    # Get context claim
    context_claim = "https://purl.imsglobal.org/spec/lti/claim/context"
    context = launch_data.get(context_claim, {})

    course_info = {
        "course_id": context.get("id", "Unknown"),
        "course_title": context.get("title", "Unknown Course"),
        "course_label": context.get("label", ""),
        "course_type": context.get("type", []),
    }

    return course_info


def get_resource_info(message_launch):
    """
    Extract resource link information from the LTI launch message

    Args:
        message_launch: The validated LTI message launch object

    Returns:
        dict: Resource information including ID, title, and description
    """
    launch_data = message_launch.get_launch_data()

    # Get resource link claim
    resource_claim = "https://purl.imsglobal.org/spec/lti/claim/resource_link"
    resource = launch_data.get(resource_claim, {})

    resource_info = {
        "resource_id": resource.get("id", "Unknown"),
        "resource_title": resource.get("title", ""),
        "resource_description": resource.get("description", ""),
    }

    return resource_info


def get_platform_info(message_launch):
    """
    Extract platform information from the LTI launch message

    Args:
        message_launch: The validated LTI message launch object

    Returns:
        dict: Platform information including name, version, and URLs
    """
    launch_data = message_launch.get_launch_data()

    # Get tool platform claim
    platform_claim = "https://purl.imsglobal.org/spec/lti/claim/tool_platform"
    platform = launch_data.get(platform_claim, {})

    platform_info = {
        "name": platform.get("name", "Unknown Platform"),
        "contact_email": platform.get("contact_email", ""),
        "description": platform.get("description", ""),
        "url": platform.get("url", ""),
        "product_family_code": platform.get("product_family_code", ""),
        "version": platform.get("version", ""),
        "guid": platform.get("guid", ""),
    }

    # Add issuer
    platform_info["issuer"] = launch_data.get("iss", "Unknown")

    return platform_info


def parse_roles(roles):
    """
    Parse LTI roles into friendly names

    Args:
        roles: List of LTI role URIs

    Returns:
        list: List of friendly role names
    """
    friendly_roles = []

    for role in roles:
        if "Instructor" in role:
            friendly_roles.append("Instructor")
        elif "Learner" in role:
            friendly_roles.append("Student")
        elif "Administrator" in role:
            friendly_roles.append("Administrator")
        elif "ContentDeveloper" in role:
            friendly_roles.append("Content Developer")
        elif "Mentor" in role:
            friendly_roles.append("Mentor")
        elif "TeachingAssistant" in role:
            friendly_roles.append("Teaching Assistant")
        else:
            # Extract the last part of the role URI as fallback
            role_parts = role.split("#")
            if len(role_parts) > 1:
                friendly_roles.append(role_parts[-1])

    return list(set(friendly_roles))  # Remove duplicates


def get_custom_params(message_launch):
    """
    Extract custom parameters from the LTI launch message

    Args:
        message_launch: The validated LTI message launch object

    Returns:
        dict: Custom parameters passed by the platform
    """
    launch_data = message_launch.get_launch_data()
    custom_claim = "https://purl.imsglobal.org/spec/lti/claim/custom"
    return launch_data.get(custom_claim, {})


def get_launch_presentation(message_launch):
    """
    Extract launch presentation information

    Args:
        message_launch: The validated LTI message launch object

    Returns:
        dict: Launch presentation details
    """
    launch_data = message_launch.get_launch_data()
    presentation_claim = "https://purl.imsglobal.org/spec/lti/claim/launch_presentation"
    presentation = launch_data.get(presentation_claim, {})

    return {
        "document_target": presentation.get(
            "document_target", "window"
        ),  # iframe, window, etc.
        "return_url": presentation.get("return_url", ""),
        "locale": presentation.get("locale", "en"),
        "height": presentation.get("height", 600),
        "width": presentation.get("width", 800),
    }


def format_launch_data_for_display(message_launch):
    """
    Format all launch data for display/debugging

    Args:
        message_launch: The validated LTI message launch object

    Returns:
        dict: Formatted launch data
    """
    return {
        "user": get_user_info(message_launch),
        "course": get_course_info(message_launch),
        "resource": get_resource_info(message_launch),
        "platform": get_platform_info(message_launch),
        "custom_params": get_custom_params(message_launch),
        "presentation": get_launch_presentation(message_launch),
        "timestamp": datetime.now().isoformat(),
    }


def check_ags_availability(message_launch):
    """
    Check if Assignment and Grade Services (AGS) is available

    Args:
        message_launch: The validated LTI message launch object

    Returns:
        bool: True if AGS is available
    """
    try:
        return message_launch.has_ags()
    except Exception:
        return False


def check_nrps_availability(message_launch):
    """
    Check if Names and Role Provisioning Services (NRPS) is available

    Args:
        message_launch: The validated LTI message launch object

    Returns:
        bool: True if NRPS is available
    """
    try:
        return message_launch.has_nrps()
    except Exception:
        return False


def validate_session():
    """
    Validate that the current session has required LTI data

    Returns:
        tuple: (is_valid, error_message)
    """
    if "user_id" not in session:
        return False, "No user session found. Please launch from your LMS."

    if "course_id" not in session:
        return False, "No course context found. Please launch from a course."

    return True, None


def get_session_info():
    """
    Get current session information

    Returns:
        dict: Current session data
    """
    return {
        "user_id": session.get("user_id"),
        "course_id": session.get("course_id"),
        "is_instructor": session.get("is_instructor", False),
        "session_active": "user_id" in session,
    }


def clear_session():
    """Clear all LTI session data"""
    session.pop("user_id", None)
    session.pop("course_id", None)
    session.pop("is_instructor", None)
    session.clear()
