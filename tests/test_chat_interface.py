"""
Tests for Chat Interface Components (src/components/chat_interface.py)

This test file validates the user interface components and chat functionality.
It ensures that the visual elements work correctly and handle user interactions properly.

For non-technical users:
- These tests check that the chat interface looks and works correctly
- They test buttons, message display, and user interactions
- They ensure the app responds properly when users click things or type messages
- They validate that the visual styling and layout work as expected
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, call
import streamlit as st

# Import the interface components to test
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.components.chat_interface import (
    setup_page_config,
    apply_custom_styling,
    display_header,
    display_chat_messages,
    create_sidebar,
    handle_chat_input
)


class TestPageConfiguration:
    """
    Test the page setup and configuration functions.

    These tests ensure that the web page is configured correctly
    with the right title, icon, and layout settings.
    """

    @patch('streamlit.set_page_config')
    def test_setup_page_config(self, mock_set_page_config):
        """Test that page configuration is set up correctly."""
        setup_page_config()

        # Verify that set_page_config was called
        mock_set_page_config.assert_called_once()

        # Check the configuration parameters
        call_args = mock_set_page_config.call_args[1]
        assert 'page_title' in call_args
        assert 'page_icon' in call_args
        assert 'layout' in call_args
        assert 'initial_sidebar_state' in call_args

        # Check specific values
        assert 'AI Study Buddy' in call_args['page_title']
        assert call_args['layout'] == 'wide'

    @patch('streamlit.markdown')
    def test_apply_custom_styling(self, mock_markdown):
        """Test that custom CSS styling is applied."""
        apply_custom_styling()

        # Verify that markdown was called with CSS
        mock_markdown.assert_called_once()
        call_args = mock_markdown.call_args[0][0]

        # Check that it contains CSS
        assert '<style>' in call_args
        assert '</style>' in call_args
        assert 'unsafe_allow_html=True' in str(mock_markdown.call_args)

    @patch('streamlit.markdown')
    def test_display_header(self, mock_markdown):
        """Test that the main header is displayed correctly."""
        display_header()

        # Should call markdown twice (title and subtitle)
        assert mock_markdown.call_count == 2

        # Check that header contains app title and description
        calls = mock_markdown.call_args_list
        header_content = ' '.join([call[0][0] for call in calls])

        assert 'AI Study Buddy' in header_content
        assert 'educational' in header_content.lower()


class TestChatInterfaceStructure:
    """
    Test the structure and interface of chat components.

    These tests ensure that chat interface functions exist and have
    the correct signatures without requiring Streamlit session state.
    """

    def test_display_functions_exist(self):
        """Test that display functions exist."""
        from src.components import chat_interface

        # Test that functions exist
        required_functions = [
            'display_chat_messages',
            'create_sidebar',
            'handle_chat_input'
        ]

        for func_name in required_functions:
            assert hasattr(chat_interface, func_name), f"Missing function: {func_name}"
            assert callable(getattr(chat_interface, func_name)), f"Function not callable: {func_name}"

    def test_page_config_functions_exist(self):
        """Test that page configuration functions exist."""
        from src.components import chat_interface

        # Test that configuration functions exist
        config_functions = [
            'setup_page_config',
            'apply_custom_styling',
            'display_header'
        ]

        for func_name in config_functions:
            assert hasattr(chat_interface, func_name), f"Missing function: {func_name}"
            assert callable(getattr(chat_interface, func_name)), f"Function not callable: {func_name}"

    def test_message_display_interface(self):
        """Test message display function interface."""
        from src.components.chat_interface import display_chat_messages

        # Function should exist and be callable
        assert callable(display_chat_messages)

        # Should not raise errors when called (even with no session state)
        try:
            display_chat_messages()
        except Exception as e:
            # Expected to fail due to no session state, but should be a specific error
            assert "session_state" in str(e).lower() or "streamlit" in str(e).lower()


class TestSidebarInterface:
    """
    Test the sidebar interface and structure.

    These tests ensure that the sidebar function exists and has
    the correct interface without requiring session state.
    """

    def test_sidebar_function_exists(self):
        """Test that sidebar creation function exists."""
        from src.components.chat_interface import create_sidebar

        # Function should exist and be callable
        assert callable(create_sidebar)

    def test_sidebar_function_interface(self):
        """Test sidebar function interface."""
        from src.components.chat_interface import create_sidebar

        # Should not raise errors when called (even with no session state)
        try:
            create_sidebar()
        except Exception as e:
            # Expected to fail due to no session state, but should be a specific error
            assert "session_state" in str(e).lower() or "streamlit" in str(e).lower()






class TestChatInputInterface:
    """
    Test the chat input handling interface.

    These tests ensure that input handling functions exist and have
    the correct interface without requiring session state.
    """

    def test_chat_input_function_exists(self):
        """Test that chat input handling function exists."""
        from src.components.chat_interface import handle_chat_input

        # Function should exist and be callable
        assert callable(handle_chat_input)

    def test_chat_input_function_interface(self):
        """Test chat input function interface."""
        from src.components.chat_interface import handle_chat_input

        # Should not raise errors when called (even with no input)
        try:
            handle_chat_input()
        except Exception as e:
            # Expected to fail due to no session state or input, but should be a specific error
            assert ("session_state" in str(e).lower() or
                   "streamlit" in str(e).lower() or
                   "chat_input" in str(e).lower())

    @patch('streamlit.chat_input')
    @patch('streamlit.chat_message')
    @patch('streamlit.spinner')
    @patch('streamlit.write')
    @patch('streamlit.image')
    @patch('src.utils.helpers.validate_user_input')
    @patch('src.utils.helpers.add_message_to_history')
    @patch('src.utils.helpers.detect_image_request')
    @patch('src.services.openai_service.openai_service')
    def test_handle_image_input(self, mock_service, mock_detect_image, mock_add_message,
                               mock_validate, mock_image, mock_write, mock_spinner,
                               mock_chat_message, mock_chat_input):
        """Test handling of image generation requests."""
        # Setup mocks
        mock_chat_input.return_value = "Create an image of a sunset"
        mock_validate.return_value = (True, "")
        mock_detect_image.return_value = True
        mock_service.generate_image.return_value = {
            "type": "image",
            "url": "https://example.com/sunset.jpg",
            "text": "Generated sunset image",
            "prompt": "sunset"
        }

        # Mock context managers
        mock_chat_message.return_value.__enter__ = Mock()
        mock_chat_message.return_value.__exit__ = Mock()
        mock_spinner.return_value.__enter__ = Mock()
        mock_spinner.return_value.__exit__ = Mock()

        handle_chat_input()

        # Verify image generation was called
        mock_detect_image.assert_called_with("Create an image of a sunset")
        mock_service.generate_image.assert_called_with("Create an image of a sunset")

        # Verify both text and image were displayed
        mock_write.assert_called()
        mock_image.assert_called()



    @patch('streamlit.chat_input')
    def test_handle_no_input(self, mock_chat_input):
        """Test handling when no input is provided."""
        # Setup mock to return None (no input)
        mock_chat_input.return_value = None

        # Should not raise any errors
        handle_chat_input()

        # Function should complete without issues


class TestInterfaceIntegration:
    """
    Test integration aspects of the chat interface.

    These tests ensure that different interface components work
    together properly and can be imported and used correctly.
    """

    def test_interface_component_imports(self):
        """Test that all interface components can be imported successfully."""
        # This test ensures all imports work correctly
        from src.components.chat_interface import (
            setup_page_config,
            apply_custom_styling,
            display_header,
            display_chat_messages,
            create_sidebar,
            handle_chat_input
        )

        # All functions should be callable
        assert callable(setup_page_config)
        assert callable(apply_custom_styling)
        assert callable(display_header)
        assert callable(display_chat_messages)
        assert callable(create_sidebar)
        assert callable(handle_chat_input)

    def test_interface_module_structure(self):
        """Test that the interface module has the expected structure."""
        from src.components import chat_interface

        # Test that module can be imported
        assert chat_interface is not None

        # Test that all expected functions exist
        expected_functions = [
            'setup_page_config', 'apply_custom_styling', 'display_header',
            'display_chat_messages', 'create_sidebar', 'handle_chat_input'
        ]

        for func_name in expected_functions:
            assert hasattr(chat_interface, func_name), f"Missing function: {func_name}"
            func = getattr(chat_interface, func_name)
            assert callable(func), f"Function not callable: {func_name}"
