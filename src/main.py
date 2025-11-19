"""
Main Application Entry Point

This is the heart of the AI Study Buddy application. It brings together all the different
parts (components, services, utilities) to create the complete chatbot experience.
"""

import sys
import os

# Add the src directory to Python path so we can import our modules
# This is like telling Python where to find our custom code
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all the components we need
from src.components.chat_interface import (
    setup_page_config,
    apply_custom_styling,
    display_header,
    display_chat_messages,
    create_sidebar,
    handle_chat_input
)
from src.utils.helpers import initialize_session_state
from src.services.openai_service import openai_service


class StudyBuddyApp:
    """
    Main application class for AI Study Buddy.

    This class represents the entire application. It's like a blueprint
    that defines how the app should work and what it should do.

    Following Airbnb style guidelines:
    - Clear, descriptive class and method names
    - Comprehensive documentation
    - Logical organization of functionality
    - Error handling and user feedback
    """

    def __init__(self):
        """
        Initialize the Study Buddy application.

        This sets up everything the app needs to run properly.
        It's like preparing all the ingredients before cooking a meal.
        """
        self.is_initialized = False
        self._setup_application()

    def _setup_application(self) -> None:
        """
        Set up the basic application configuration.

        This method handles all the initial setup tasks that need to happen
        before the app can start serving users.
        """
        try:
            # Initialize session state for storing conversation data
            initialize_session_state()

            # Check if OpenAI service is available
            if not openai_service.is_available():
                self._handle_service_unavailable()
                return

            self.is_initialized = True

        except Exception as error:
            self._handle_initialization_error(error)

    def _handle_service_unavailable(self) -> None:
        """
        Handle the case where OpenAI service is not available.

        This shows helpful error messages when the app can't connect to OpenAI.
        """
        import streamlit as st

        st.error("🚫 AI Study Buddy is not available")
        st.markdown("""
        **The app cannot start because:**
        - OpenAI API key is missing or invalid
        - Network connection issues
        - Service configuration problems

        **Please check:**
        1. Your `.env` file contains a valid `OPENAI_API_KEY`
        2. Your internet connection is working
        3. Your OpenAI account has sufficient credits
        """)
        st.stop()

    def _handle_initialization_error(self, error: Exception) -> None:
        """
        Handle errors that occur during app initialization.

        This provides user-friendly error messages when something goes wrong
        during startup.

        Args:
            error: The exception that occurred during initialization
        """
        import streamlit as st

        st.error(f"🚨 Failed to initialize AI Study Buddy: {str(error)}")
        st.markdown("""
        **Something went wrong during startup.**

        **Possible solutions:**
        1. Refresh the page and try again
        2. Check your internet connection
        3. Verify your OpenAI API key is correct
        4. Contact support if the problem persists
        """)
        st.stop()

    def run(self) -> None:
        """
        Run the main application.

        This is the main method that starts the app and handles user interactions.
        It's like pressing the "start" button on the application.
        """
        try:
            # MUST be first: Configure the web page settings
            setup_page_config()

            # Apply custom visual styling
            apply_custom_styling()

            if not self.is_initialized:
                return

            # Display the main header
            display_header()

            # Create the sidebar with controls and information
            create_sidebar()

            # Main content area
            self._render_main_content()

        except Exception as error:
            self._handle_runtime_error(error)

    def _render_main_content(self) -> None:
        """
        Render the main chat interface.

        This creates the central chat area where users interact with the AI.
        """
        import streamlit as st

        # Main chat section header
        st.header("💬 Chat")

        # Display existing conversation messages
        display_chat_messages()

        # Handle new user input
        handle_chat_input()

    def _handle_runtime_error(self, error: Exception) -> None:
        """
        Handle errors that occur while the app is running.

        This provides graceful error handling during normal app operation.

        Args:
            error: The exception that occurred during runtime
        """
        import streamlit as st

        st.error(f"🚨 An error occurred: {str(error)}")
        st.markdown("""
        **The app encountered an unexpected error.**

        **You can try:**
        1. Refreshing the page
        2. Clearing your chat history using the sidebar button
        3. Checking your internet connection
        4. Trying a different message

        If the problem persists, please report it to the development team.
        """)


def main() -> None:
    """
    Main entry point for the application.

    This is the function that gets called when someone runs the app.
    It creates an instance of the StudyBuddyApp and starts it running.

    Following Airbnb style guidelines:
    - Simple, clear main function
    - Proper error handling
    - Clean separation of concerns
    """
    try:
        # Create and run the application
        app = StudyBuddyApp()
        app.run()

    except KeyboardInterrupt:
        # Handle when user stops the app with Ctrl+C
        print("\n👋 AI Study Buddy stopped by user")

    except Exception as error:
        # Handle any unexpected errors
        print(f"🚨 Fatal error: {str(error)}")
        import streamlit as st
        st.error("🚨 A critical error occurred. Please restart the application.")


# This is a Python convention that ensures main() only runs when this file
# is executed directly (not when it's imported by another file)
if __name__ == "__main__":
    main()
