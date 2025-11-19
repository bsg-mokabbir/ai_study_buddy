"""
Utility Helper Functions

This module contains small, reusable functions that help with common tasks.
Think of these as a toolbox of handy functions that different parts of the app can use.
"""

from typing import List, Dict, Any
import streamlit as st

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.settings import app_config


def detect_image_request(user_input: str) -> bool:
    """
    Determine if the user is asking for an image to be created.

    This function looks at what the user typed and decides whether they want
    an image generated or just a text response. It's like having a smart
    assistant that can tell the difference between "explain photosynthesis"
    and "draw a picture of photosynthesis."

    Args:
        user_input: What the user typed in the chat

    Returns:
        True if they want an image, False if they want text

    Examples:
        detect_image_request("explain math") -> False
        detect_image_request("draw me a cat") -> True
        detect_image_request("create an image of a sunset") -> True
    """
    # Convert to lowercase for easier matching
    user_input_lower = user_input.lower()

    # Check if any image request keywords are in the user's message
    for keyword in app_config.IMAGE_REQUEST_KEYWORDS:
        if keyword in user_input_lower:
            return True

    return False


def format_chat_message(content: Any, role: str) -> Dict[str, Any]:
    """
    Format a message for display in the chat interface.

    This function takes raw message content and formats it properly
    for display. It's like a formatter that makes sure messages
    look good in the chat window.

    Args:
        content: The message content (text, image data, etc.)
        role: Who sent the message ('user' or 'assistant')

    Returns:
        Formatted message dictionary
    """
    return {
        'role': role,
        'content': content,
        'timestamp': st.session_state.get('current_time', None)
    }


def initialize_session_state() -> None:
    """
    Set up the app's memory for storing conversation history.

    Streamlit apps don't remember things between page refreshes by default.
    This function creates a "memory" where we can store the conversation
    history and other important information.

    Think of this as setting up a notebook where the app can write down
    what happened in previous conversations.
    """
    # Initialize chat message history if it doesn't exist
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Initialize selected AI model if it doesn't exist
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = app_config.DEFAULT_TEXT_MODEL

    # Initialize other session variables
    if 'conversation_count' not in st.session_state:
        st.session_state.conversation_count = 0

    if 'last_response_type' not in st.session_state:
        st.session_state.last_response_type = None


def clear_chat_history() -> None:
    """
    Clear all messages from the conversation history.

    This is like erasing the whiteboard to start a fresh conversation.
    It removes all previous messages but keeps other settings intact.
    """
    st.session_state.messages = []
    st.session_state.conversation_count = 0
    st.session_state.last_response_type = None


def add_message_to_history(role: str, content: Any) -> None:
    """
    Add a new message to the conversation history.

    This function saves each message (both from users and the AI) so we can
    display the full conversation and maintain context for the AI.

    Args:
        role: Who sent the message ('user' or 'assistant')
        content: The message content
    """
    # Format the message properly
    formatted_message = format_chat_message(content, role)

    # Add to conversation history
    st.session_state.messages.append(formatted_message)

    # Keep track of conversation length
    st.session_state.conversation_count += 1

    # Limit conversation history to prevent memory issues
    if len(st.session_state.messages) > app_config.MAX_CHAT_HISTORY:
        # Remove oldest messages, but keep the first few for context
        st.session_state.messages = (
            st.session_state.messages[:2] +  # Keep first 2 messages
            st.session_state.messages[-(app_config.MAX_CHAT_HISTORY-2):]  # Keep recent messages
        )


def get_conversation_for_api() -> List[Dict[str, str]]:
    """
    Prepare the conversation history for sending to OpenAI.

    This function takes our internal conversation format and converts it
    to the format that OpenAI's API expects. It's like translating between
    two different languages.

    Returns:
        List of messages formatted for OpenAI API
    """
    api_messages = []

    for message in st.session_state.messages:
        # Only include text messages in API calls
        if message['role'] in ['user', 'assistant']:
            content = message['content']

            # Handle different content types
            if isinstance(content, dict):
                if content.get('type') == 'text':
                    api_messages.append({
                        'role': message['role'],
                        'content': content['text']
                    })
                # Skip image messages for API context (they don't help with text generation)
            else:
                # Regular string content
                api_messages.append({
                    'role': message['role'],
                    'content': str(content)
                })

    return api_messages


def validate_user_input(user_input: str) -> tuple[bool, str]:
    """
    Check if the user's input is valid and safe to process.

    This function acts like a security guard, checking that the user's
    input is appropriate and safe to send to the AI.

    Args:
        user_input: What the user typed

    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if input is okay, False if there's a problem
        - error_message: Explanation of what's wrong (empty if input is valid)
    """
    # Check if input is empty or just whitespace
    if not user_input or not user_input.strip():
        return False, "Please enter a message before sending."

    # Check if input is too long
    if len(user_input) > 2000:  # Reasonable limit for chat messages
        return False, "Your message is too long. Please keep it under 2000 characters."

    # Check for potentially harmful content (basic filtering)
    harmful_patterns = [
        'hack', 'exploit', 'malware', 'virus', 'illegal'
    ]

    user_input_lower = user_input.lower()
    for pattern in harmful_patterns:
        if pattern in user_input_lower:
            return False, "Please keep your questions educational and appropriate."

    # If we get here, the input is valid
    return True, ""


def get_app_statistics() -> Dict[str, Any]:
    """
    Get statistics about the current app session.

    This function provides information about how the app is being used,
    like how many messages have been sent, what types of responses were given, etc.

    Returns:
        Dictionary containing various app statistics
    """
    total_messages = len(st.session_state.get('messages', []))
    user_messages = sum(1 for msg in st.session_state.get('messages', []) if msg['role'] == 'user')
    assistant_messages = sum(1 for msg in st.session_state.get('messages', []) if msg['role'] == 'assistant')

    return {
        'total_messages': total_messages,
        'user_messages': user_messages,
        'assistant_messages': assistant_messages,
        'current_model': st.session_state.get('selected_model', 'Unknown'),
        'conversation_count': st.session_state.get('conversation_count', 0)
    }


def format_error_message(error_type: str, details: str = "") -> str:
    """
    Create user-friendly error messages.

    This function takes technical error information and converts it into
    messages that regular users can understand and act upon.

    Args:
        error_type: Type of error that occurred
        details: Additional error details

    Returns:
        User-friendly error message
    """
    error_messages = {
        'api_key_missing': "🔑 Your OpenAI API key is missing. Please add it to your .env file.",
        'network_error': "🌐 Network connection problem. Please check your internet connection.",
        'rate_limit': "🚦 Too many requests. Please wait a moment and try again.",
        'insufficient_funds': "💳 Your OpenAI account is out of credits. Please add more credits.",
        'model_error': "🤖 The AI model encountered an error. Please try again.",
        'input_too_long': "📝 Your message is too long. Please make it shorter.",
        'unknown': "❓ An unexpected error occurred. Please try again."
    }

    base_message = error_messages.get(error_type, error_messages['unknown'])

    if details:
        return f"{base_message}\n\nDetails: {details}"

    return base_message
