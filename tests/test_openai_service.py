"""
Tests for OpenAI Service Module (src/services/openai_service.py)

This test file validates the OpenAI API service functionality.
It tests API communication, error handling, and response processing using mocked API calls.

For non-technical users:
- These tests check that the app can communicate with OpenAI properly
- They test both text generation (like ChatGPT) and image generation (like DALL-E)
- They ensure errors are handled gracefully when network issues occur
- All tests use fake API calls so no real money is spent during testing
"""

import pytest
import ssl
from unittest.mock import Mock, patch, MagicMock
import streamlit as st

# Import the service to test
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.openai_service import OpenAIService


class TestOpenAIServiceStructure:
    """
    Test the structure and interface of the OpenAI service.

    These tests ensure that the service has the correct methods and
    attributes without requiring actual API keys or connections.
    """

    def test_service_class_structure(self):
        """Test that the OpenAI service class has the correct structure."""
        from src.services.openai_service import OpenAIService

        # Test that class can be imported
        assert OpenAIService is not None

        # Test that class has required methods
        required_methods = ['is_available', 'generate_text_response', 'generate_image']
        for method in required_methods:
            assert hasattr(OpenAIService, method), f"Missing method: {method}"

    def test_service_availability_method(self):
        """Test the service availability checking method."""
        from src.services.openai_service import OpenAIService

        # Create service instance
        service = OpenAIService()

        # Test that is_available method exists and returns boolean
        assert hasattr(service, 'is_available')
        assert callable(service.is_available)

        # Method should return a boolean
        result = service.is_available()
        assert isinstance(result, bool)

    def test_global_service_instance_exists(self):
        """Test that the global service instance is available."""
        from src.services.openai_service import openai_service

        assert openai_service is not None

        # Test that it has the expected interface
        assert hasattr(openai_service, 'is_available')
        assert hasattr(openai_service, 'generate_text_response')
        assert hasattr(openai_service, 'generate_image')


class TestTextGenerationInterface:
    """
    Test text generation interface and response format.

    These tests ensure that the service has the correct interface for
    text generation without requiring actual API calls.
    """

    def test_text_generation_method_exists(self):
        """Test that text generation method exists and is callable."""
        from src.services.openai_service import OpenAIService

        service = OpenAIService()

        # Test method exists
        assert hasattr(service, 'generate_text_response')
        assert callable(service.generate_text_response)

    def test_text_generation_with_mock_client(self):
        """Test text generation with a mock client."""
        from src.services.openai_service import OpenAIService

        service = OpenAIService()

        # Replace client with mock
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_response
        service.client = mock_client

        # Test text generation
        messages = [{"role": "user", "content": "Test question"}]
        result = service.generate_text_response(messages)

        # Verify result structure
        assert isinstance(result, dict)
        assert 'type' in result
        assert 'success' in result







    def test_service_unavailable_handling(self):
        """Test behavior when service is not available."""
        # Create service without client
        service = OpenAIService()
        service.client = None

        # Test text generation
        messages = [{"role": "user", "content": "Test question"}]
        result = service.generate_text_response(messages)

        # Verify unavailable response
        assert result['type'] == 'error'
        assert result['success'] is False
        assert 'not available' in result['text']


class TestImageGeneration:
    """
    Test image generation functionality (like DALL-E).

    These tests ensure that the service can generate images from text descriptions
    and handle various scenarios appropriately.
    """

    def setup_method(self):
        """Set up test fixtures for each test."""
        self.service = OpenAIService()
        self.service.client = Mock()  # Use mock client for testing

    def test_successful_image_generation(self):
        """Test successful image generation."""
        # Setup mock response
        mock_response = Mock()
        mock_response.data = [Mock()]
        mock_response.data[0].url = "https://example.com/generated_image.jpg"

        self.service.client.images.generate.return_value = mock_response

        # Test image generation
        result = self.service.generate_image("Create an image of a solar system")

        # Verify result
        assert result['type'] == 'image'
        assert result['success'] is True
        assert result['url'] == "https://example.com/generated_image.jpg"
        assert 'solar system' in result['prompt']

        # Verify API was called correctly
        self.service.client.images.generate.assert_called_once()

    def test_image_prompt_cleaning(self):
        """Test that image prompts are cleaned properly."""
        # Setup mock response
        mock_response = Mock()
        mock_response.data = [Mock()]
        mock_response.data[0].url = "https://example.com/test.jpg"

        self.service.client.images.generate.return_value = mock_response

        # Test with prompt that needs cleaning
        result = self.service.generate_image("Create an image of a beautiful sunset")

        # Verify prompt was cleaned
        call_args = self.service.client.images.generate.call_args
        cleaned_prompt = call_args[1]['prompt']

        # Should remove "create an image of" but keep "beautiful sunset"
        assert 'create an image of' not in cleaned_prompt.lower()
        assert 'beautiful sunset' in cleaned_prompt.lower()

    def test_image_generation_parameters(self):
        """Test that correct parameters are used for image generation."""
        # Setup mock response
        mock_response = Mock()
        mock_response.data = [Mock()]
        mock_response.data[0].url = "https://example.com/test.jpg"

        self.service.client.images.generate.return_value = mock_response

        # Test image generation
        self.service.generate_image("Test prompt")

        # Verify parameters
        call_args = self.service.client.images.generate.call_args
        params = call_args[1]

        assert params['model'] in ['dall-e-2', 'dall-e-3']
        assert 'x' in params['size']  # Should be format like "1024x1024"
        assert params['quality'] in ['standard', 'hd']
        assert params['n'] >= 1

    def test_image_generation_api_error_handling(self):
        """Test handling of API errors during image generation."""
        # Setup API error
        self.service.client.images.generate.side_effect = Exception("Image generation failed")

        # Test error handling
        result = self.service.generate_image("Test prompt")

        # Verify error response
        assert result['type'] == 'error'
        assert result['success'] is False
        assert 'error' in result['text'].lower()

    def test_image_generation_service_unavailable(self):
        """Test image generation when service is unavailable."""
        # Create service without client
        service = OpenAIService()
        service.client = None

        # Test image generation
        result = service.generate_image("Test prompt")

        # Verify unavailable response
        assert result['type'] == 'error'
        assert result['success'] is False
        assert 'not available' in result['text']


class TestErrorHandling:
    """
    Test comprehensive error handling across the service.

    These tests ensure that the service handles various types of errors
    gracefully and provides helpful feedback to users.
    """

    def setup_method(self):
        """Set up test fixtures for each test."""
        self.service = OpenAIService()
        self.service.client = Mock()

    @patch('streamlit.error')
    def test_ssl_error_handling(self, mock_error):
        """Test specific handling of SSL errors."""
        # Setup SSL error
        self.service.client.chat.completions.create.side_effect = ssl.SSLError("SSL Error")

        # Test error handling
        messages = [{"role": "user", "content": "Test"}]
        result = self.service.generate_text_response(messages)

        # Verify SSL-specific error handling
        mock_error.assert_called()
        error_call = mock_error.call_args[0][0]
        assert 'ssl' in error_call.lower() or 'certificate' in error_call.lower()

    @patch('streamlit.error')
    def test_permission_error_handling(self, mock_error):
        """Test handling of permission errors."""
        # Setup permission error
        self.service.client.chat.completions.create.side_effect = PermissionError("Permission denied")

        # Test error handling
        messages = [{"role": "user", "content": "Test"}]
        result = self.service.generate_text_response(messages)

        # Verify permission-specific error handling
        mock_error.assert_called()
        error_call = mock_error.call_args[0][0]
        assert 'permission' in error_call.lower()

    @patch('streamlit.error')
    def test_timeout_error_handling(self, mock_error):
        """Test handling of timeout errors."""
        # Setup timeout error
        self.service.client.chat.completions.create.side_effect = TimeoutError("Request timeout")

        # Test error handling
        messages = [{"role": "user", "content": "Test"}]
        result = self.service.generate_text_response(messages)

        # Verify timeout-specific error handling
        mock_error.assert_called()
        error_call = mock_error.call_args[0][0]
        assert 'timeout' in error_call.lower()

    def test_rate_limit_error_handling(self):
        """Test handling of rate limit errors."""
        # Setup rate limit error
        rate_limit_error = Exception("rate limit exceeded")
        self.service.client.chat.completions.create.side_effect = rate_limit_error

        # Test error handling
        messages = [{"role": "user", "content": "Test"}]
        result = self.service.generate_text_response(messages)

        # Verify rate limit handling
        assert result['type'] == 'error'
        assert result['success'] is False

    def test_insufficient_funds_error_handling(self):
        """Test handling of insufficient funds errors."""
        # Setup insufficient funds error
        funds_error = Exception("insufficient funds in your account")
        self.service.client.chat.completions.create.side_effect = funds_error

        # Test error handling
        messages = [{"role": "user", "content": "Test"}]
        result = self.service.generate_text_response(messages)

        # Verify funds error handling
        assert result['type'] == 'error'
        assert result['success'] is False


class TestServiceIntegration:
    """
    Test integration aspects of the OpenAI service.

    These tests ensure that the service works well with other parts
    of the application and handles real-world scenarios.
    """



    def test_service_availability_check(self):
        """Test the service availability checking method."""
        # Test with client
        service = OpenAIService()
        service.client = Mock()
        assert service.is_available() is True

        # Test without client
        service.client = None
        assert service.is_available() is False

    def test_response_format_consistency(self):
        """Test that all responses follow consistent format."""
        service = OpenAIService()
        service.client = Mock()

        # Setup mock responses
        mock_text_response = Mock()
        mock_text_response.choices = [Mock()]
        mock_text_response.choices[0].message.content = "Test response"
        service.client.chat.completions.create.return_value = mock_text_response

        mock_image_response = Mock()
        mock_image_response.data = [Mock()]
        mock_image_response.data[0].url = "https://example.com/test.jpg"
        service.client.images.generate.return_value = mock_image_response

        # Test text response format
        text_result = service.generate_text_response([{"role": "user", "content": "Test"}])
        assert 'type' in text_result
        assert 'success' in text_result
        assert 'text' in text_result

        # Test image response format
        image_result = service.generate_image("Test prompt")
        assert 'type' in image_result
        assert 'success' in image_result
        assert 'url' in image_result
        assert 'prompt' in image_result
