"""
OpenAI Service Module

This module handles all communication with OpenAI's API services.
Think of this as the "translator" that converts our app's requests into
language that OpenAI's servers can understand.
"""

import ssl
import httpx
import streamlit as st
from typing import Dict, List, Union, Optional
from openai import OpenAI

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.settings import app_config, prompt_templates


class OpenAIService:
    """
    Service class for handling OpenAI API interactions.

    This class is like a specialized assistant that knows how to talk to OpenAI's servers.
    It handles both text generation (like ChatGPT) and image generation (like DALL-E).
    """

    def __init__(self):
        """
        Initialize the OpenAI service.

        This sets up the connection to OpenAI when the app starts.
        It's like dialing a phone number to connect to OpenAI's services.
        """
        self.client: Optional[OpenAI] = None
        self._initialize_client()

    def _initialize_client(self) -> None:
        """
        Set up the connection to OpenAI's servers.

        This method tries different ways to connect to OpenAI, starting with
        the most secure method and falling back to alternatives if needed.
        """
        # Check if we have an API key
        if not app_config.OPENAI_API_KEY:
            self._show_api_key_error()
            return

        # Try to connect with standard security settings
        try:
            self.client = OpenAI(
                api_key=app_config.OPENAI_API_KEY,
                organization=app_config.OPENAI_ORG_ID if app_config.OPENAI_ORG_ID else None
            )
            return

        except Exception as ssl_error:
            # If there's a security certificate problem, try alternative connection
            st.warning("⚠️ SSL certificate issue detected. Trying alternative connection...")
            self._initialize_with_relaxed_ssl()

    def _initialize_with_relaxed_ssl(self) -> None:
        """
        Set up connection with relaxed security settings.

        Sometimes corporate networks or antivirus software block secure connections.
        This method tries a less secure but more compatible connection method.
        """
        try:
            # Create a custom connection that's more permissive
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            # Create HTTP client with relaxed security
            http_client = httpx.Client(
                verify=False,
                timeout=30.0
            )

            # Initialize OpenAI client with custom settings
            self.client = OpenAI(
                api_key=app_config.OPENAI_API_KEY,
                organization=app_config.OPENAI_ORG_ID if app_config.OPENAI_ORG_ID else None,
                http_client=http_client
            )

            st.info("✅ Connected with relaxed SSL settings")

        except Exception as error:
            self._show_connection_error(str(error))

    def _show_api_key_error(self) -> None:
        """
        Display helpful instructions when API key is missing.

        This shows users exactly how to set up their OpenAI API key.
        """
        st.error("🔑 OpenAI API key not found!")
        st.markdown("""
        **To use this chatbot, you need to set up your OpenAI API key:**

        1. **Get an API key** from [OpenAI](https://platform.openai.com/api-keys)
        2. **Create a `.env` file** in the project directory
        3. **Add your key** to the `.env` file:
           ```
           OPENAI_API_KEY=your_actual_api_key_here
           ```
        4. **Restart the application**

        📝 **Note:** You can copy `.env.example` to `.env` and edit it with your key.
        """)
        st.stop()

    def _show_connection_error(self, error_message: str) -> None:
        """
        Display helpful error message when connection fails.

        This gives users specific steps to fix connection problems.
        """
        st.error(f"❌ Failed to connect to OpenAI: {error_message}")
        st.markdown("""
        **Possible solutions:**
        1. **Check your internet connection**
        2. **Try running as administrator** (Windows)
        3. **Check corporate firewall/proxy settings**
        4. **Try a different network** (mobile hotspot)
        5. **Contact your IT department** if on corporate network
        """)
        st.stop()

    def is_available(self) -> bool:
        """
        Check if the OpenAI service is ready to use.

        Returns True if we can talk to OpenAI, False if there's a problem.
        """
        return self.client is not None

    def generate_text_response(
        self,
        messages: List[Dict[str, str]],
        model: str = None
    ) -> Dict[str, Union[str, bool]]:
        """
        Generate a text response using OpenAI's chat models.

        This is like having a conversation with ChatGPT. We send a list of messages
        (the conversation history) and get back a response.

        Args:
            messages: List of conversation messages (user and assistant)
            model: Which AI model to use (defaults to app setting)

        Returns:
            Dictionary containing the response and success status
        """
        if not self.is_available():
            return {
                'type': 'error',
                'text': 'OpenAI service is not available. Please check your connection.',
                'success': False
            }

        # Use default model if none specified
        if model is None:
            model = app_config.DEFAULT_TEXT_MODEL

        try:
            # Prepare the conversation for OpenAI
            # Add the system prompt that defines the AI's personality
            api_messages = [
                {
                    'role': 'system',
                    'content': prompt_templates.SYSTEM_PROMPT
                }
            ] + messages

            # Send request to OpenAI
            response = self.client.chat.completions.create(
                model=model,
                messages=api_messages,
                max_tokens=app_config.MAX_TOKENS,
                temperature=app_config.TEMPERATURE
            )

            # Extract the AI's response
            response_text = response.choices[0].message.content.strip()

            return {
                'type': 'text',
                'text': response_text,
                'success': True
            }

        except Exception as error:
            return self._handle_api_error(error)

    def generate_image(self, prompt: str) -> Dict[str, Union[str, bool]]:
        """
        Generate an image using OpenAI's DALL-E model.

        This takes a text description and creates an image based on it.
        It's like having an AI artist draw a picture from your description.

        Args:
            prompt: Text description of the image to create

        Returns:
            Dictionary containing the image URL and success status
        """
        if not self.is_available():
            return {
                'type': 'error',
                'text': 'OpenAI service is not available. Please check your connection.',
                'success': False
            }

        try:
            # Clean up the prompt for better image generation
            cleaned_prompt = self._clean_image_prompt(prompt)

            # Generate image using DALL-E
            response = self.client.images.generate(
                model=app_config.IMAGE_MODEL,
                prompt=cleaned_prompt,
                size=app_config.DEFAULT_IMAGE_SIZE,
                quality=app_config.IMAGE_QUALITY,
                n=app_config.IMAGES_PER_REQUEST,
            )

            # Get the image URL from the response
            image_url = response.data[0].url

            return {
                'type': 'image',
                'url': image_url,
                'prompt': cleaned_prompt,
                'text': f"I've created an image based on your request: '{cleaned_prompt}'",
                'success': True
            }

        except Exception as error:
            return self._handle_api_error(error)

    def _clean_image_prompt(self, prompt: str) -> str:
        """
        Clean up the user's prompt for better image generation.

        This removes common phrases like "create an image of" to make
        the prompt more focused on the actual content.
        """
        # Remove common request phrases
        phrases_to_remove = [
            'create an image of', 'generate an image of', 'make an image of',
            'draw an image of', 'show me an image of', 'create a picture of',
            'generate a picture of', 'make a picture of', 'draw a picture of',
            'show me a picture of', 'visualize', 'illustrate'
        ]

        cleaned = prompt.lower()
        for phrase in phrases_to_remove:
            cleaned = cleaned.replace(phrase, '')

        return cleaned.strip()

    def _handle_api_error(self, error: Exception) -> Dict[str, Union[str, bool]]:
        """
        Handle errors from OpenAI API calls.

        This converts technical error messages into user-friendly explanations.
        """
        error_message = str(error)

        # Provide specific error messages for common problems
        if 'ssl' in error_message.lower() or 'certificate' in error_message.lower():
            user_message = "🔒 SSL/Certificate error. Please check your network settings."
        elif 'permission' in error_message.lower():
            user_message = "🚫 Permission error. Try running as administrator or check firewall settings."
        elif 'timeout' in error_message.lower():
            user_message = "⏱️ Request timeout. Please check your internet connection."
        elif 'rate limit' in error_message.lower():
            user_message = "🚦 Rate limit exceeded. Please wait a moment and try again."
        elif 'insufficient funds' in error_message.lower():
            user_message = "💳 Insufficient OpenAI credits. Please check your account balance."
        else:
            user_message = f"❌ Error communicating with OpenAI: {error_message}"

        # Show error in the app
        st.error(user_message)

        return {
            'type': 'error',
            'text': 'I encountered an error. Please try again or check your connection.',
            'success': False
        }


# Create a global instance that other parts of the app can use
openai_service = OpenAIService()
