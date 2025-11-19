"""
Pytest Configuration and Fixtures for AI Study Buddy

This file contains shared test configuration and fixtures for the AI Study Buddy test suite.
It provides proper isolation and mocking to ensure tests pass reliably.
"""

import pytest
import os
import sys
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class MockSessionState:
    """Mock Streamlit session state that behaves like a dictionary."""

    def __init__(self):
        self._state = {}

    def __getitem__(self, key):
        return self._state[key]

    def __setitem__(self, key, value):
        self._state[key] = value

    def __contains__(self, key):
        return key in self._state

    def __getattr__(self, name):
        if name.startswith('_'):
            return super().__getattribute__(name)
        return self._state.get(name)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            if not hasattr(self, '_state'):
                super().__setattr__('_state', {})
            self._state[name] = value

    def get(self, name, default=None):
        return self._state.get(name, default)

    def clear(self):
        self._state.clear()

    def keys(self):
        return self._state.keys()

    def values(self):
        return self._state.values()

    def items(self):
        return self._state.items()


@pytest.fixture
def mock_streamlit_session_state():
    """Provide a properly mocked Streamlit session state."""
    mock_state = MockSessionState()
    mock_state.messages = []
    mock_state.selected_model = "gpt-3.5-turbo"
    mock_state.conversation_count = 0
    mock_state.last_response_type = None
    return mock_state


@pytest.fixture
def isolated_environment():
    """Provide completely isolated environment variables."""
    # Store original environment
    original_env = os.environ.copy()

    # Clear all environment variables
    os.environ.clear()

    yield os.environ

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def test_environment():
    """Provide test environment with API key."""
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key_123'}, clear=False):
        yield


@pytest.fixture
def mock_openai_client():
    """Provide a mock OpenAI client for testing."""
    mock_client = Mock()

    # Mock text generation response
    mock_text_response = Mock()
    mock_text_response.choices = [Mock()]
    mock_text_response.choices[0].message.content = "This is a test response from the AI."
    mock_client.chat.completions.create.return_value = mock_text_response

    # Mock image generation response
    mock_image_response = Mock()
    mock_image_response.data = [Mock()]
    mock_image_response.data[0].url = "https://example.com/test_image.jpg"
    mock_client.images.generate.return_value = mock_image_response

    return mock_client


@pytest.fixture
def sample_messages():
    """Provide sample chat messages for testing."""
    return [
        {"role": "user", "content": "What is photosynthesis?"},
        {"role": "assistant", "content": "Photosynthesis is the process by which plants convert sunlight into energy."},
        {"role": "user", "content": "Can you explain it in more detail?"}
    ]


@pytest.fixture
def mock_streamlit():
    """Mock all Streamlit functions used in tests."""
    with patch('streamlit.set_page_config') as mock_set_page_config, \
         patch('streamlit.markdown') as mock_markdown, \
         patch('streamlit.header') as mock_header, \
         patch('streamlit.write') as mock_write, \
         patch('streamlit.error') as mock_error, \
         patch('streamlit.warning') as mock_warning, \
         patch('streamlit.info') as mock_info, \
         patch('streamlit.success') as mock_success, \
         patch('streamlit.stop') as mock_stop, \
         patch('streamlit.rerun') as mock_rerun, \
         patch('streamlit.chat_input') as mock_chat_input, \
         patch('streamlit.chat_message') as mock_chat_message, \
         patch('streamlit.spinner') as mock_spinner, \
         patch('streamlit.image') as mock_image, \
         patch('streamlit.selectbox') as mock_selectbox, \
         patch('streamlit.button') as mock_button, \
         patch('streamlit.sidebar') as mock_sidebar, \
         patch('streamlit.columns') as mock_columns, \
         patch('streamlit.metric') as mock_metric:

        # Setup context managers
        mock_chat_message.return_value.__enter__ = Mock()
        mock_chat_message.return_value.__exit__ = Mock()
        mock_spinner.return_value.__enter__ = Mock()
        mock_spinner.return_value.__exit__ = Mock()

        # Setup sidebar mock
        mock_sidebar.header = Mock()
        mock_sidebar.selectbox = Mock(return_value='gpt-3.5-turbo')
        mock_sidebar.button = Mock(return_value=False)
        mock_sidebar.markdown = Mock()
        mock_sidebar.write = Mock()
        mock_sidebar.info = Mock()
        mock_sidebar.subheader = Mock()
        mock_sidebar.metric = Mock()
        mock_sidebar.columns = Mock(return_value=[Mock(), Mock()])

        yield {
            'set_page_config': mock_set_page_config,
            'markdown': mock_markdown,
            'header': mock_header,
            'write': mock_write,
            'error': mock_error,
            'warning': mock_warning,
            'info': mock_info,
            'success': mock_success,
            'stop': mock_stop,
            'rerun': mock_rerun,
            'chat_input': mock_chat_input,
            'chat_message': mock_chat_message,
            'spinner': mock_spinner,
            'image': mock_image,
            'selectbox': mock_selectbox,
            'button': mock_button,
            'sidebar': mock_sidebar,
            'columns': mock_columns,
            'metric': mock_metric
        }


@pytest.fixture
def mock_openai_service():
    """Provide a mock OpenAI service for testing."""
    mock_service = Mock()
    mock_service.is_available.return_value = True
    mock_service.generate_text_response.return_value = {
        "type": "text",
        "text": "Test response",
        "success": True
    }
    mock_service.generate_image.return_value = {
        "type": "image",
        "url": "https://example.com/test.jpg",
        "text": "Test image",
        "prompt": "test",
        "success": True
    }
    return mock_service


@pytest.fixture(autouse=True)
def reset_modules():
    """Reset imported modules before each test to ensure isolation."""
    # List of modules to reset
    modules_to_reset = [
        'src.config.settings',
        'src.services.openai_service',
        'src.utils.helpers',
        'src.components.chat_interface',
        'src.main'
    ]

    # Remove modules from sys.modules if they exist
    for module in modules_to_reset:
        if module in sys.modules:
            del sys.modules[module]

    yield

    # Clean up after test
    for module in modules_to_reset:
        if module in sys.modules:
            del sys.modules[module]


# Note: Pytest configuration functions removed as they were not being used
# All tests run by default without special markers or conditions
