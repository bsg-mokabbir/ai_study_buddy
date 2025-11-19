"""
Configuration Package

This package contains all configuration and settings for the AI Study Buddy application.

For non-technical users:
- This is where all the app's settings and options are defined
- You can modify settings.py to change how the app behaves
- All configuration is centralized here for easy management
"""

from .settings import app_config, prompt_templates, example_questions

# Make the main configuration objects easily accessible
__all__ = [
    "app_config",
    "prompt_templates", 
    "example_questions"
]
