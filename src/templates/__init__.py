"""
Templates Package

This package contains prompt templates and educational content templates for the AI Study Buddy.

For non-technical users:
- Templates are like pre-written scripts that guide how the AI responds
- They ensure the AI maintains a consistent, educational tone
- Different templates are used for different types of interactions (Q&A, quizzes, explanations)
"""

from .prompts import EducationalPrompts

# Make the main template class easily accessible
__all__ = [
    "EducationalPrompts"
]
