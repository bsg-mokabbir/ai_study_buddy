"""
Configuration Settings for AI Study Buddy

This file contains all the settings and configuration options for the AI Study Buddy application.
Think of this as the "control panel" where we define how the app should behave.
"""

import os
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
# This reads your API keys and other secrets from a secure file
load_dotenv()


class AppConfig:
    """
    Main configuration class for the AI Study Buddy application.

    This class holds all the settings that control how the app works.
    Think of it as a collection of switches and dials that control the app's behavior.
    """

    # =============================================================================
    # API CONFIGURATION
    # These settings control how we connect to OpenAI's services
    # =============================================================================

    # Your OpenAI API key (kept secret in .env file)
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')

    # Optional: Your OpenAI organization ID (if you have one)
    OPENAI_ORG_ID: str = os.getenv('OPENAI_ORG_ID', '')

    # =============================================================================
    # MODEL CONFIGURATION
    # These settings control which AI models the app can use
    # =============================================================================

    # Available AI models for text generation
    # Each model has different capabilities and costs
    AVAILABLE_TEXT_MODELS: List[str] = [
        'gpt-3.5-turbo',      # Fast and cost-effective
        'gpt-4',              # More capable but slower
        'gpt-4-turbo-preview' # Latest and most advanced
    ]

    # Default model to use when the app starts
    DEFAULT_TEXT_MODEL: str = 'gpt-3.5-turbo'

    # Image generation model (DALL-E)
    IMAGE_MODEL: str = 'dall-e-3'

    # =============================================================================
    # CHAT CONFIGURATION
    # These settings control how conversations work
    # =============================================================================

    # Maximum number of tokens (words) in AI responses
    # Higher = longer responses, but costs more
    MAX_TOKENS: int = 1000

    # Temperature controls creativity (0.0 = very focused, 1.0 = very creative)
    TEMPERATURE: float = 0.7

    # Maximum number of messages to keep in chat history
    MAX_CHAT_HISTORY: int = 50

    # =============================================================================
    # IMAGE GENERATION CONFIGURATION
    # These settings control how images are created
    # =============================================================================

    # Default image size for DALL-E
    DEFAULT_IMAGE_SIZE: str = '1024x1024'

    # Image quality setting ('standard' or 'hd')
    IMAGE_QUALITY: str = 'standard'

    # Number of images to generate per request
    IMAGES_PER_REQUEST: int = 1

    # =============================================================================
    # UI CONFIGURATION
    # These settings control how the app looks and feels
    # =============================================================================

    # App title shown in browser tab
    APP_TITLE: str = 'AI Study Buddy'

    # App icon (emoji) shown in browser tab
    APP_ICON: str = '📚'

    # Default port for running the app
    DEFAULT_PORT: int = 8501

    # =============================================================================
    # EDUCATIONAL CONTENT CONFIGURATION
    # These settings define what subjects and topics the app covers
    # =============================================================================

    # Supported academic subjects
    SUPPORTED_SUBJECTS: List[str] = [
        'Mathematics',
        'Science',
        'History',
        'English/Literature',
        'Geography',
        'Study Tips'
    ]

    # Keywords that indicate image generation requests
    # When users type these words, the app will create images instead of text
    IMAGE_REQUEST_KEYWORDS: List[str] = [
        'create an image', 'generate an image', 'make an image', 'draw an image',
        'create a picture', 'generate a picture', 'make a picture', 'draw a picture',
        'show me an image', 'show me a picture', 'visualize', 'illustrate',
        'create art', 'generate art', 'make art', 'draw art',
        'design', 'sketch', 'paint', 'render',
        'create image', 'generate image', 'make image', 'draw image',
        'create picture', 'generate picture', 'make picture', 'draw picture',
        'draw me', 'show me a', 'can you draw', 'can you create',
        'can you generate', 'can you make', 'i want an image', 'i want a picture'
    ]


class PromptTemplates:
    """
    Collection of prompt templates for the AI.

    These are like scripts that tell the AI how to behave and respond.
    Think of them as instructions you give to a human tutor about how to teach.
    """

    # Main system prompt that defines the AI's personality and role
    SYSTEM_PROMPT: str = """
    You are an AI Study Buddy, a helpful educational assistant for high school students.
    You help with subjects like Math, Science, History, English, and other academic topics.

    Your personality and behavior:
    - Be encouraging and supportive, like a friendly tutor
    - Provide clear, step-by-step explanations
    - Use examples that high school students can relate to
    - Keep your language appropriate for teenagers
    - Be patient and never make students feel bad for not knowing something
    - Encourage curiosity and critical thinking

    Your capabilities:
    - Answer questions about academic subjects
    - Explain complex concepts in simple terms
    - Help with homework and study strategies
    - Generate images when requested (you have DALL-E access)
    - Create practice questions and quizzes

    What you should do:
    - If asked non-educational questions, politely redirect to academic topics
    - If someone asks you to create/generate/draw images, use your image generation abilities
    - Always be encouraging and positive about learning
    - Break down complex problems into smaller, manageable steps
    """

    # Prompt for when users ask for images
    IMAGE_GENERATION_PROMPT: str = """
    Create a detailed, educational image that will help a high school student understand the concept.
    Make sure the image is:
    - Clear and easy to understand
    - Appropriate for educational use
    - Visually appealing and engaging
    - Accurate to the subject matter
    """


class ExampleQuestions:
    """
    Pre-written example questions that users can click to try the app.

    These help new users understand what kinds of questions they can ask.
    """

    # Text-based educational questions
    TEXT_EXAMPLES: List[str] = [
        "Explain photosynthesis",
        "What is the Pythagorean theorem?",
        "Tell me about World War II",
        "How do I solve quadratic equations?",
        "What are the parts of speech?",
        "Explain the water cycle",
        "What caused the American Revolution?",
        "How does DNA replication work?"
    ]

    # Image generation examples
    IMAGE_EXAMPLES: List[str] = [
        "Create an image of a solar system",
        "Generate a picture of a medieval castle",
        "Draw an image of a DNA double helix",
        "Make a picture of a peaceful forest",
        "Show me the structure of an atom",
        "Create a diagram of photosynthesis",
        "Generate an image of ancient Rome",
        "Draw a picture of the water cycle"
    ]


# Create global instances that other parts of the app can use
app_config = AppConfig()
prompt_templates = PromptTemplates()
example_questions = ExampleQuestions()
