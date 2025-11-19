"""
Tests for Configuration Module (src/config/settings.py)

This test file validates the configuration and settings functionality of the AI Study Buddy.
It ensures that all configuration objects are properly initialized and contain valid values.
"""

import pytest
import os
from unittest.mock import patch, MagicMock

# Import the configuration modules to test
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.settings import AppConfig, PromptTemplates, ExampleQuestions


class TestAppConfig:
    """
    Test the main application configuration class.

    This class tests all the settings that control how the AI Study Buddy works,
    like API keys, model choices, and other important options.
    """

    def test_app_config_initialization(self):
        """Test that AppConfig initializes with default values."""
        config = AppConfig()

        # Test that basic configuration attributes exist
        assert hasattr(config, 'OPENAI_API_KEY')
        assert hasattr(config, 'AVAILABLE_TEXT_MODELS')
        assert hasattr(config, 'DEFAULT_TEXT_MODEL')
        assert hasattr(config, 'APP_TITLE')
        assert hasattr(config, 'APP_ICON')

    def test_default_text_models_list(self):
        """Test that the list of available AI models is valid."""
        config = AppConfig()

        # Check that we have a list of models
        assert isinstance(config.AVAILABLE_TEXT_MODELS, list)
        assert len(config.AVAILABLE_TEXT_MODELS) > 0

        # Check that common models are included
        expected_models = ['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo-preview']
        for model in expected_models:
            assert model in config.AVAILABLE_TEXT_MODELS

    def test_default_model_is_valid(self):
        """Test that the default model is in the available models list."""
        config = AppConfig()

        assert config.DEFAULT_TEXT_MODEL in config.AVAILABLE_TEXT_MODELS

    def test_numeric_settings_are_reasonable(self):
        """Test that numeric settings have reasonable values."""
        config = AppConfig()

        # Test token limits
        assert isinstance(config.MAX_TOKENS, int)
        assert 100 <= config.MAX_TOKENS <= 4000  # Reasonable range

        # Test temperature setting
        assert isinstance(config.TEMPERATURE, float)
        assert 0.0 <= config.TEMPERATURE <= 1.0  # Valid range for OpenAI

        # Test chat history limit
        assert isinstance(config.MAX_CHAT_HISTORY, int)
        assert config.MAX_CHAT_HISTORY > 0

        # Test port number
        assert isinstance(config.DEFAULT_PORT, int)
        assert 1000 <= config.DEFAULT_PORT <= 65535  # Valid port range

    def test_image_generation_settings(self):
        """Test that image generation settings are valid."""
        config = AppConfig()

        # Test image model
        assert config.IMAGE_MODEL in ['dall-e-2', 'dall-e-3']

        # Test image size format
        assert 'x' in config.DEFAULT_IMAGE_SIZE
        width, height = config.DEFAULT_IMAGE_SIZE.split('x')
        assert width.isdigit() and height.isdigit()

        # Test image quality
        assert config.IMAGE_QUALITY in ['standard', 'hd']

        # Test images per request
        assert isinstance(config.IMAGES_PER_REQUEST, int)
        assert config.IMAGES_PER_REQUEST >= 1

    def test_supported_subjects_list(self):
        """Test that the supported subjects list is comprehensive."""
        config = AppConfig()

        assert isinstance(config.SUPPORTED_SUBJECTS, list)
        assert len(config.SUPPORTED_SUBJECTS) > 0

        # Check for key educational subjects
        expected_subjects = ['Mathematics', 'Science', 'History', 'English']
        for subject in expected_subjects:
            # Check if subject or similar variant exists
            subject_found = any(subject.lower() in s.lower() for s in config.SUPPORTED_SUBJECTS)
            assert subject_found, f"Subject '{subject}' not found in supported subjects"

    def test_image_request_keywords(self):
        """Test that image request keywords are comprehensive."""
        config = AppConfig()

        assert isinstance(config.IMAGE_REQUEST_KEYWORDS, list)
        assert len(config.IMAGE_REQUEST_KEYWORDS) > 0

        # Check for key phrases
        expected_keywords = ['create an image', 'generate', 'draw', 'make a picture']
        for keyword in expected_keywords:
            keyword_found = any(keyword in k for k in config.IMAGE_REQUEST_KEYWORDS)
            assert keyword_found, f"Keyword '{keyword}' not found in image request keywords"

    def test_api_key_configuration_structure(self):
        """Test that API key configuration structure is correct."""
        config = AppConfig()

        # Test that API key attribute exists
        assert hasattr(config, 'OPENAI_API_KEY')

        # Test that it's a string (regardless of value)
        assert isinstance(config.OPENAI_API_KEY, str)

    def test_configuration_has_required_attributes(self):
        """Test that configuration has all required attributes."""
        config = AppConfig()

        # Test required attributes exist
        required_attrs = [
            'OPENAI_API_KEY', 'AVAILABLE_TEXT_MODELS', 'DEFAULT_TEXT_MODEL',
            'MAX_TOKENS', 'TEMPERATURE', 'IMAGE_MODEL', 'SUPPORTED_SUBJECTS'
        ]

        for attr in required_attrs:
            assert hasattr(config, attr), f"Missing required attribute: {attr}"


class TestPromptTemplates:
    """
    Test the prompt templates used to guide AI behavior.

    These tests ensure that the prompts we send to the AI are well-formed
    and contain the right instructions for educational assistance.
    """

    def test_prompt_templates_initialization(self):
        """Test that PromptTemplates class initializes correctly."""
        templates = PromptTemplates()

        assert hasattr(templates, 'SYSTEM_PROMPT')
        assert hasattr(templates, 'IMAGE_GENERATION_PROMPT')

    def test_system_prompt_content(self):
        """Test that the system prompt contains educational guidance."""
        templates = PromptTemplates()

        prompt = templates.SYSTEM_PROMPT
        assert isinstance(prompt, str)
        assert len(prompt) > 100  # Should be substantial

        # Check for key educational concepts
        educational_keywords = [
            'educational', 'student', 'high school', 'tutor',
            'learning', 'explain', 'encourage'
        ]

        prompt_lower = prompt.lower()
        for keyword in educational_keywords:
            assert keyword in prompt_lower, f"Educational keyword '{keyword}' not found in system prompt"

    def test_image_generation_prompt_content(self):
        """Test that the image generation prompt is appropriate."""
        templates = PromptTemplates()

        prompt = templates.IMAGE_GENERATION_PROMPT
        assert isinstance(prompt, str)
        assert len(prompt) > 50  # Should have meaningful content

        # Check for image-specific guidance
        image_keywords = ['image', 'educational', 'clear', 'appropriate']
        prompt_lower = prompt.lower()
        for keyword in image_keywords:
            assert keyword in prompt_lower, f"Image keyword '{keyword}' not found in image prompt"

    def test_prompts_are_safe_and_appropriate(self):
        """Test that prompts don't contain inappropriate content."""
        templates = PromptTemplates()

        all_prompts = [templates.SYSTEM_PROMPT, templates.IMAGE_GENERATION_PROMPT]

        # Check that prompts don't contain problematic content
        inappropriate_terms = ['hack', 'illegal', 'harmful', 'dangerous']

        for prompt in all_prompts:
            prompt_lower = prompt.lower()
            for term in inappropriate_terms:
                assert term not in prompt_lower, f"Inappropriate term '{term}' found in prompt"


class TestExampleQuestions:
    """
    Test the example questions provided to users.

    These tests ensure that the pre-written questions are educational,
    appropriate, and cover a good range of subjects.
    """

    def test_example_questions_initialization(self):
        """Test that ExampleQuestions class initializes correctly."""
        examples = ExampleQuestions()

        assert hasattr(examples, 'TEXT_EXAMPLES')
        assert hasattr(examples, 'IMAGE_EXAMPLES')

    def test_text_examples_are_educational(self):
        """Test that text examples are educational and appropriate."""
        examples = ExampleQuestions()

        assert isinstance(examples.TEXT_EXAMPLES, list)
        assert len(examples.TEXT_EXAMPLES) > 0

        # Check that examples cover different subjects
        all_examples = ' '.join(examples.TEXT_EXAMPLES).lower()

        educational_topics = [
            'math', 'science', 'history', 'english', 'geography',
            'equation', 'photosynthesis', 'war', 'theorem'
        ]

        topics_found = sum(1 for topic in educational_topics if topic in all_examples)
        assert topics_found >= 3, "Text examples should cover multiple educational topics"

    def test_image_examples_are_appropriate(self):
        """Test that image examples are appropriate for education."""
        examples = ExampleQuestions()

        assert isinstance(examples.IMAGE_EXAMPLES, list)
        assert len(examples.IMAGE_EXAMPLES) > 0

        # Check that image examples contain creation keywords
        for example in examples.IMAGE_EXAMPLES:
            assert isinstance(example, str)
            assert len(example) > 10  # Should be meaningful

            # Should contain image creation keywords
            creation_keywords = ['create', 'generate', 'draw', 'make', 'show']
            example_lower = example.lower()
            has_creation_keyword = any(keyword in example_lower for keyword in creation_keywords)
            assert has_creation_keyword, f"Image example '{example}' should contain creation keyword"

    def test_examples_are_age_appropriate(self):
        """Test that all examples are appropriate for high school students."""
        examples = ExampleQuestions()

        all_examples = examples.TEXT_EXAMPLES + examples.IMAGE_EXAMPLES

        # Check that examples don't contain inappropriate content
        inappropriate_terms = [
            'adult', 'violence', 'weapon', 'drug', 'alcohol',
            'inappropriate', 'mature', 'explicit'
        ]

        for example in all_examples:
            example_lower = example.lower()
            for term in inappropriate_terms:
                assert term not in example_lower, f"Inappropriate term '{term}' found in example: {example}"

    def test_examples_have_variety(self):
        """Test that examples show variety in subjects and complexity."""
        examples = ExampleQuestions()

        # Text examples should have variety
        assert len(examples.TEXT_EXAMPLES) >= 5, "Should have multiple text examples"
        assert len(set(examples.TEXT_EXAMPLES)) == len(examples.TEXT_EXAMPLES), "Text examples should be unique"

        # Image examples should have variety
        assert len(examples.IMAGE_EXAMPLES) >= 4, "Should have multiple image examples"
        assert len(set(examples.IMAGE_EXAMPLES)) == len(examples.IMAGE_EXAMPLES), "Image examples should be unique"


class TestConfigurationIntegration:
    """
    Test how different configuration components work together.

    These tests ensure that all the configuration pieces fit together
    properly and don't have conflicting settings.
    """

    def test_global_config_instances_exist(self):
        """Test that global configuration instances are available."""
        from src.config.settings import app_config, prompt_templates, example_questions

        assert app_config is not None
        assert prompt_templates is not None
        assert example_questions is not None

        # Test that they have the expected attributes
        assert hasattr(app_config, 'DEFAULT_TEXT_MODEL')
        assert hasattr(prompt_templates, 'SYSTEM_PROMPT')
        assert hasattr(example_questions, 'TEXT_EXAMPLES')

    def test_configuration_consistency(self):
        """Test that configuration settings are consistent with each other."""
        from src.config.settings import app_config, example_questions

        # Test that default model is actually available
        assert app_config.DEFAULT_TEXT_MODEL in app_config.AVAILABLE_TEXT_MODELS

        # Test that image examples use keywords from the config
        image_keywords = app_config.IMAGE_REQUEST_KEYWORDS
        image_examples = example_questions.IMAGE_EXAMPLES

        # At least some image examples should use the configured keywords
        examples_using_keywords = 0
        for example in image_examples:
            example_lower = example.lower()
            if any(keyword in example_lower for keyword in image_keywords):
                examples_using_keywords += 1

        assert examples_using_keywords > 0, "Image examples should use configured keywords"

    def test_configuration_values_are_production_ready(self):
        """Test that configuration values are suitable for production use."""
        from src.config.settings import app_config

        # Test reasonable defaults
        assert app_config.MAX_TOKENS >= 500, "Max tokens should be sufficient for educational responses"
        assert app_config.TEMPERATURE <= 0.8, "Temperature should not be too high for educational content"
        assert len(app_config.SUPPORTED_SUBJECTS) >= 4, "Should support multiple subjects"
        assert app_config.APP_TITLE, "App should have a title"
        assert app_config.APP_ICON, "App should have an icon"
