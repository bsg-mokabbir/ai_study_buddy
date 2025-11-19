"""
Integration Tests for AI Study Buddy

This test file validates how different modules work together in the restructured application.
It focuses on module structure, imports, and interfaces without requiring API keys or session state.
"""

import pytest
import sys
import os
from pathlib import Path

# Import modules for integration testing
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestModuleStructureIntegration:
    """
    Test that all modules can be imported and have the expected structure.

    These tests ensure that the restructured codebase has proper
    module organization and that all components can be imported.
    """

    def test_config_module_imports(self):
        """Test that configuration modules can be imported."""
        # Test config module imports
        from src.config import settings
        assert settings is not None

        # Test that config classes exist
        from src.config.settings import AppConfig, PromptTemplates, ExampleQuestions
        assert AppConfig is not None
        assert PromptTemplates is not None
        assert ExampleQuestions is not None

        # Test that global instances exist
        from src.config.settings import app_config, prompt_templates, example_questions
        assert app_config is not None
        assert prompt_templates is not None
        assert example_questions is not None

    def test_service_module_imports(self):
        """Test that service modules can be imported."""
        # Test service module imports
        from src.services import openai_service
        assert openai_service is not None

        # Test that service class exists
        from src.services.openai_service import OpenAIService
        assert OpenAIService is not None

        # Test that global service instance exists
        from src.services.openai_service import openai_service as service_instance
        assert service_instance is not None

    def test_utils_module_imports(self):
        """Test that utility modules can be imported."""
        # Test utils module imports
        from src.utils import helpers
        assert helpers is not None

        # Test that helper functions exist
        helper_functions = [
            'detect_image_request', 'validate_user_input', 'format_chat_message',
            'initialize_session_state', 'clear_chat_history', 'add_message_to_history'
        ]

        for func_name in helper_functions:
            assert hasattr(helpers, func_name), f"Missing helper function: {func_name}"

    def test_components_module_imports(self):
        """Test that component modules can be imported."""
        # Test components module imports
        from src.components import chat_interface
        assert chat_interface is not None

        # Test that interface functions exist
        interface_functions = [
            'setup_page_config', 'apply_custom_styling', 'display_header',
            'display_chat_messages', 'create_sidebar', 'handle_chat_input'
        ]

        for func_name in interface_functions:
            assert hasattr(chat_interface, func_name), f"Missing interface function: {func_name}"

    def test_main_module_imports(self):
        """Test that main module can be imported."""
        # Test main module imports
        from src import main
        assert main is not None

        # Test that main components exist
        from src.main import StudyBuddyApp, main as main_function
        assert StudyBuddyApp is not None
        assert main_function is not None
        assert callable(main_function)


class TestFunctionInterfaceIntegration:
    """
    Test that functions from different modules have compatible interfaces.

    These tests ensure that functions can work together properly
    without requiring complex state or API dependencies.
    """

    def test_image_detection_function_interface(self):
        """Test that image detection function has the correct interface."""
        from src.utils.helpers import detect_image_request

        # Function should exist and be callable
        assert callable(detect_image_request)

        # Should accept string input and return boolean
        result = detect_image_request("test input")
        assert isinstance(result, bool)

        # Should handle empty input
        result = detect_image_request("")
        assert isinstance(result, bool)

    def test_validation_function_interface(self):
        """Test that validation functions have the correct interface."""
        from src.utils.helpers import validate_user_input

        # Function should exist and be callable
        assert callable(validate_user_input)

        # Should return tuple of (bool, str)
        result = validate_user_input("test input")
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], bool)
        assert isinstance(result[1], str)

    def test_message_formatting_interface(self):
        """Test that message formatting has the correct interface."""
        from src.utils.helpers import format_chat_message

        # Function should exist and be callable
        assert callable(format_chat_message)

        # Should return dictionary with expected keys
        result = format_chat_message("test content", "user")
        assert isinstance(result, dict)
        assert 'role' in result
        assert 'content' in result
        assert result['role'] == "user"
        assert result['content'] == "test content"


class TestConfigurationConsistency:
    """
    Test configuration consistency across modules.

    These tests ensure that configuration is properly shared
    and consistent across all modules in the application.
    """

    def test_configuration_accessibility(self):
        """Test that configuration is accessible from all modules."""
        # Test that configuration can be imported from different modules
        from src.config.settings import app_config
        from src.config.settings import prompt_templates
        from src.config.settings import example_questions

        # All should be accessible
        assert app_config is not None
        assert prompt_templates is not None
        assert example_questions is not None

        # Should have expected attributes
        assert hasattr(app_config, 'DEFAULT_TEXT_MODEL')
        assert hasattr(prompt_templates, 'SYSTEM_PROMPT')
        assert hasattr(example_questions, 'TEXT_EXAMPLES')

    def test_configuration_values_consistency(self):
        """Test that configuration values are consistent."""
        from src.config.settings import app_config

        # Test that default model is in available models
        assert app_config.DEFAULT_TEXT_MODEL in app_config.AVAILABLE_TEXT_MODELS

        # Test that lists are not empty
        assert len(app_config.SUPPORTED_SUBJECTS) > 0
        assert len(app_config.IMAGE_REQUEST_KEYWORDS) > 0
        assert len(app_config.AVAILABLE_TEXT_MODELS) > 0

    def test_example_questions_consistency(self):
        """Test that example questions are consistent with validation."""
        from src.config.settings import example_questions
        from src.utils.helpers import detect_image_request, validate_user_input

        # Test that text examples are not detected as image requests
        for example in example_questions.TEXT_EXAMPLES[:3]:  # Test first 3
            assert detect_image_request(example) is False
            is_valid, _ = validate_user_input(example)
            assert is_valid is True

        # Test that image examples are detected as image requests
        for example in example_questions.IMAGE_EXAMPLES[:3]:  # Test first 3
            assert detect_image_request(example) is True
            is_valid, _ = validate_user_input(example)
            assert is_valid is True


class TestModuleCompleteness:
    """
    Test that the restructured application has all required modules and components.

    These tests ensure that the codebase restructuring is complete
    and all necessary parts are in place and working.
    """

    def test_all_modules_importable(self):
        """Test that all main modules can be imported without errors."""
        # Test that all main modules can be imported
        try:
            from src.config import settings
            from src.services import openai_service
            from src.utils import helpers
            from src.components import chat_interface
            from src.templates import prompts
            from src import main

            # All imports should succeed
            assert settings is not None
            assert openai_service is not None
            assert helpers is not None
            assert chat_interface is not None
            assert prompts is not None
            assert main is not None

        except ImportError as e:
            pytest.fail(f"Failed to import module: {e}")

    def test_module_interfaces_complete(self):
        """Test that modules have complete interfaces."""
        # Test config module interface
        from src.config.settings import AppConfig, PromptTemplates, ExampleQuestions
        assert all([AppConfig, PromptTemplates, ExampleQuestions])

        # Test service module interface
        from src.services.openai_service import OpenAIService
        assert OpenAIService is not None

        # Test utils module interface
        from src.utils.helpers import detect_image_request, validate_user_input
        assert all([detect_image_request, validate_user_input])

        # Test components module interface
        from src.components.chat_interface import setup_page_config, display_chat_messages
        assert all([setup_page_config, display_chat_messages])

        # Test templates module interface
        from src.templates.prompts import EducationalPrompts
        assert EducationalPrompts is not None

        # Test main module interface
        from src.main import StudyBuddyApp, main
        assert all([StudyBuddyApp, main])

    def test_restructured_architecture_integrity(self):
        """Test that the restructured architecture maintains integrity."""
        # Test that the restructured codebase has proper separation

        # Config should be separate from services
        from src.config import settings
        from src.services import openai_service
        assert settings.__file__ != openai_service.__file__

        # Services should be separate from components
        from src.components import chat_interface
        assert openai_service.__file__ != chat_interface.__file__

        # Utils should be separate from main
        from src.utils import helpers
        from src import main
        assert helpers.__file__ != main.__file__

        # All modules should be in their proper directories
        assert 'config' in settings.__file__
        assert 'services' in openai_service.__file__
        assert 'utils' in helpers.__file__
        assert 'components' in chat_interface.__file__
