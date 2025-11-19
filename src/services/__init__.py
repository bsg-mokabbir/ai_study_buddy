"""
Services Package

This package contains service classes that handle external API communication.

For non-technical users:
- Services are like specialized assistants that handle specific tasks
- The OpenAI service manages all communication with OpenAI's servers
- Services isolate complex API logic from the rest of the app
"""

from .openai_service import openai_service

# Make the OpenAI service easily accessible
__all__ = [
    "openai_service"
]
