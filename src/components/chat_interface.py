"""
Chat Interface Components

This module contains all the visual components for the chat interface.
Think of this as the "face" of the application - everything users see and interact with.
"""

import streamlit as st
from typing import Dict, Any, List

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.settings import app_config, example_questions
from src.utils.helpers import get_app_statistics


def setup_page_config() -> None:
    """
    Configure the basic settings for the web page.

    This sets up how the page looks in the browser - the title, icon,
    and overall layout. It's like setting up the window dressing for a store.
    """
    st.set_page_config(
        page_title=app_config.APP_TITLE,
        page_icon=app_config.APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded"
    )


def apply_custom_styling() -> None:
    """
    Apply custom visual styling to make the app look professional.

    This function adds custom colors, fonts, and spacing to make the app
    more visually appealing. It's like interior decorating for the app.
    """
    st.markdown("""
    <style>
        /* Main header styling */
        .main-header {
            text-align: center;
            color: #2E86AB;
            margin-bottom: 2rem;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        /* Sidebar styling */
        .sidebar .element-container {
            margin-bottom: 1rem;
        }

        /* Chat message styling */
        .chat-message {
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
            border-left: 4px solid #2196F3;
        }

        /* Button styling */
        .stButton > button {
            width: 100%;
            border-radius: 0.5rem;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        /* Info boxes */
        .info-box {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }

        /* Statistics display */
        .stats-container {
            background-color: #ffffff;
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid #e0e0e0;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)


def display_header() -> None:
    """
    Show the main title and description at the top of the page.

    This creates the welcoming header that users see when they first visit the app.
    """
    st.markdown(
        f'<h1 class="main-header">{app_config.APP_ICON} {app_config.APP_TITLE}</h1>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p style="text-align: center; color: #666; font-size: 1.1em;">Your AI-powered educational assistant with text and image generation</p>',
        unsafe_allow_html=True
    )


def display_chat_messages() -> None:
    """
    Show all the messages in the conversation history.

    This function goes through all the saved messages and displays them
    in the chat interface. It handles both text messages and images.
    """
    # Display each message in the conversation
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            content = message["content"]

            # Handle different types of content
            if isinstance(content, dict):
                # Handle structured content (like image responses)
                if content.get("type") == "image":
                    # Display image response
                    st.write(content["text"])
                    st.image(
                        content["url"],
                        caption=f"Generated image: {content['prompt']}",
                        use_column_width=True
                    )
                elif content.get("type") == "text":
                    # Display text response
                    st.write(content["text"])
                elif content.get("type") == "error":
                    # Display error message
                    st.error(content["text"])
                else:
                    # Fallback for unknown content types
                    st.write(str(content))
            else:
                # Handle simple text content
                st.write(content)


def create_sidebar() -> None:
    """
    Create the sidebar with controls and information.

    The sidebar contains model selection, example questions, and other controls.
    It's like a control panel for the app.
    """
    with st.sidebar:
        st.header("🎯 Settings")

        # Model selection dropdown
        st.session_state.selected_model = st.selectbox(
            "Choose AI Model:",
            app_config.AVAILABLE_TEXT_MODELS,
            index=app_config.AVAILABLE_TEXT_MODELS.index(
                st.session_state.get('selected_model', app_config.DEFAULT_TEXT_MODEL)
            ),
            help="Different models have different capabilities and costs"
        )

        st.markdown("---")

        # App information section
        _display_app_info()

        st.markdown("---")

        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            from src.utils.helpers import clear_chat_history
            clear_chat_history()
            st.rerun()

        st.markdown("---")

        # Example questions section
        _display_example_questions()

        st.markdown("---")

        # App statistics
        _display_app_statistics()


def _display_app_info() -> None:
    """
    Show information about what the app can do.

    This displays a list of subjects and capabilities to help users
    understand what they can ask about.
    """
    st.header("📖 About")
    st.write("AI Study Buddy helps with:")

    # Display supported subjects
    for subject in app_config.SUPPORTED_SUBJECTS:
        st.write(f"• {subject}")

    # Highlight image generation capability
    st.write("• 🎨 **Image Generation** (DALL-E)")

    st.info("💡 **New!** Ask me to create, generate, or draw images and I'll use DALL-E to make them for you!")


def _display_example_questions() -> None:
    """
    Show clickable example questions to help users get started.

    This creates buttons for common questions that users can click
    instead of typing them out.
    """
    st.header("💡 Try asking:")

    # Text-based questions
    st.subheader("📝 Text Questions:")
    for question in example_questions.TEXT_EXAMPLES[:4]:  # Show first 4 examples
        if st.button(f"💬 {question}", key=f"text_{hash(question)}", use_container_width=True):
            _handle_example_question(question, is_image=False)

    # Image generation examples
    st.subheader("🎨 Image Generation:")
    for question in example_questions.IMAGE_EXAMPLES[:4]:  # Show first 4 examples
        if st.button(f"🎨 {question}", key=f"image_{hash(question)}", use_container_width=True):
            _handle_example_question(question, is_image=True)


def _handle_example_question(question: str, is_image: bool = False) -> None:
    """
    Handle when a user clicks an example question button.

    This adds the question to the chat and triggers the AI response.

    Args:
        question: The example question that was clicked
        is_image: Whether this is an image generation request
    """
    from src.utils.helpers import add_message_to_history
    from src.services.openai_service import openai_service
    from src.utils.helpers import get_conversation_for_api

    # Add the question to chat history
    add_message_to_history("user", question)

    # Generate response
    spinner_text = "Generating image..." if is_image else "Thinking..."

    with st.spinner(spinner_text):
        if is_image:
            response = openai_service.generate_image(question)
        else:
            conversation = get_conversation_for_api()
            response = openai_service.generate_text_response(conversation, st.session_state.selected_model)

    # Add response to chat history
    add_message_to_history("assistant", response)

    # Refresh the page to show the new messages
    st.rerun()


def _display_app_statistics() -> None:
    """
    Show statistics about the current session.

    This displays information like how many messages have been sent,
    which model is being used, etc.
    """
    st.header("📊 Session Stats")

    stats = get_app_statistics()

    # Create a nice-looking stats display
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Messages", stats['total_messages'])
        st.metric("Model", stats['current_model'])

    with col2:
        st.metric("User Messages", stats['user_messages'])
        st.metric("AI Responses", stats['assistant_messages'])


def handle_chat_input() -> None:
    """
    Handle new messages from the user.

    This function processes what the user types in the chat input box
    and generates an appropriate response.
    """
    # Get user input from the chat input widget
    if prompt := st.chat_input("Ask me anything about your studies..."):
        from src.utils.helpers import (
            validate_user_input,
            add_message_to_history,
            detect_image_request,
            get_conversation_for_api
        )
        from src.services.openai_service import openai_service

        # Validate the user's input
        is_valid, error_message = validate_user_input(prompt)
        if not is_valid:
            st.error(error_message)
            return

        # Add user message to chat history
        add_message_to_history("user", prompt)

        # Display user message immediately
        with st.chat_message("user"):
            st.write(prompt)

        # Determine if this is an image request
        is_image_request = detect_image_request(prompt)

        # Generate AI response
        with st.chat_message("assistant"):
            spinner_text = "Generating image..." if is_image_request else "Thinking..."

            with st.spinner(spinner_text):
                if is_image_request:
                    response = openai_service.generate_image(prompt)
                else:
                    conversation = get_conversation_for_api()
                    response = openai_service.generate_text_response(
                        conversation,
                        st.session_state.selected_model
                    )

            # Display the response
            if isinstance(response, dict):
                if response.get("type") == "image":
                    st.write(response["text"])
                    st.image(
                        response["url"],
                        caption=f"Generated image: {response['prompt']}",
                        use_column_width=True
                    )
                elif response.get("type") == "text":
                    st.write(response["text"])
                elif response.get("type") == "error":
                    st.error(response["text"])
                else:
                    st.write(str(response))
            else:
                st.write(response)

        # Add AI response to chat history
        add_message_to_history("assistant", response)
