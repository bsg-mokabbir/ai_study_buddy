"""
AI Study Buddy - Source Package

This package contains the main source code for the AI Study Buddy application,
organized following Airbnb style guidelines.

For non-technical users:
- This file makes Python recognize 'src' as a package
- It allows other parts of the app to import code from this directory
- Think of it as a "table of contents" for the source code
"""

# Package version
__version__ = "2.0.0"

# Package description
__description__ = "AI Study Buddy - Educational chatbot with OpenAI integration"

# Author information
__author__ = "AI Study Buddy Team"

# Main components available for import
__all__ = [
    "config",
    "services",
    "utils",
    "components",
    "data",
    "main"
]
