"""
AI Study Buddy - Restructured with Airbnb Style Guidelines

This is the main entry point for the AI Study Buddy application.
The codebase has been restructured following Airbnb style guidelines for better
maintainability, readability, and scalability.

For non-technical users:
- This file now simply imports and runs the main application
- All the complex code has been organized into logical modules
- The app functionality remains exactly the same
- The code is now much easier to understand and maintain

Architecture Overview:
- src/config/settings.py: All configuration and settings
- src/services/openai_service.py: OpenAI API communication
- src/utils/helpers.py: Utility functions and helpers
- src/components/chat_interface.py: User interface components
- src/main.py: Main application logic
"""

# Import the main application from our restructured codebase
from src.main import main

# Run the application
if __name__ == "__main__":
    main()