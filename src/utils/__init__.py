"""
Utilities Package

This package contains utility functions and helper tools used throughout the application.

For non-technical users:
- Utilities are like a toolbox of handy functions
- They perform common tasks that multiple parts of the app need
- Helper functions make the main code cleaner and easier to understand
"""

from .helpers import (
    detect_image_request,
    format_chat_message,
    initialize_session_state,
    clear_chat_history,
    add_message_to_history,
    get_conversation_for_api,
    validate_user_input,
    get_app_statistics,
    format_error_message
)

# Make all helper functions easily accessible
__all__ = [
    "detect_image_request",
    "format_chat_message", 
    "initialize_session_state",
    "clear_chat_history",
    "add_message_to_history",
    "get_conversation_for_api",
    "validate_user_input",
    "get_app_statistics",
    "format_error_message"
]
