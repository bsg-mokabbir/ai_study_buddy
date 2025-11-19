"""
Components Package

This package contains UI components and interface elements for the application.

For non-technical users:
- Components are the visual parts of the app that users see and interact with
- They handle things like buttons, chat messages, and page layout
- The chat interface component manages the main user experience
"""

from .chat_interface import (
    setup_page_config,
    apply_custom_styling,
    display_header,
    display_chat_messages,
    create_sidebar,
    handle_chat_input
)

# Make all interface functions easily accessible
__all__ = [
    "setup_page_config",
    "apply_custom_styling",
    "display_header", 
    "display_chat_messages",
    "create_sidebar",
    "handle_chat_input"
]
