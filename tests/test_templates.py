"""
Tests for Templates Module (src/templates/prompts.py)

This test file validates the educational prompt templates functionality.
It ensures that the templates can be imported from their new location and work correctly.
"""

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.templates.prompts import EducationalPrompts


class TestEducationalPrompts:
    """
    Test the EducationalPrompts class functionality.
    
    These tests ensure that the prompt templates work correctly
    and can generate appropriate educational prompts.
    """

    def test_educational_prompts_initialization(self):
        """Test that EducationalPrompts can be initialized."""
        prompts = EducationalPrompts()
        assert prompts is not None
        assert hasattr(prompts, 'base_context')
        assert hasattr(prompts, 'subject_contexts')
        assert hasattr(prompts, 'quiz_templates')

    def test_base_context_exists(self):
        """Test that base context is properly set."""
        prompts = EducationalPrompts()
        base_context = prompts.base_context
        
        assert base_context is not None
        assert isinstance(base_context, str)
        assert len(base_context) > 0
        assert "study buddy" in base_context.lower()

    def test_subject_contexts_structure(self):
        """Test that subject contexts are properly structured."""
        prompts = EducationalPrompts()
        subject_contexts = prompts.subject_contexts
        
        assert isinstance(subject_contexts, dict)
        assert len(subject_contexts) > 0
        
        # Check for expected subjects
        expected_subjects = ['science', 'math', 'history', 'english', 'geography', 'general']
        for subject in expected_subjects:
            assert subject in subject_contexts
            assert isinstance(subject_contexts[subject], str)
            assert len(subject_contexts[subject]) > 0

    def test_quiz_templates_structure(self):
        """Test that quiz templates are properly structured."""
        prompts = EducationalPrompts()
        quiz_templates = prompts.quiz_templates
        
        assert isinstance(quiz_templates, dict)
        assert len(quiz_templates) > 0
        
        # Check for expected difficulty levels
        expected_levels = ['easy', 'medium', 'hard']
        for level in expected_levels:
            assert level in quiz_templates
            assert isinstance(quiz_templates[level], list)
            assert len(quiz_templates[level]) > 0

    def test_create_qa_prompt(self):
        """Test Q&A prompt creation."""
        prompts = EducationalPrompts()
        
        # Test basic prompt creation
        question = "What is photosynthesis?"
        prompt = prompts.create_qa_prompt(question)
        
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert question in prompt
        assert "Study Buddy Response:" in prompt

    def test_create_qa_prompt_with_subject(self):
        """Test Q&A prompt creation with specific subject."""
        prompts = EducationalPrompts()
        
        question = "What is photosynthesis?"
        subject = "science"
        prompt = prompts.create_qa_prompt(question, subject)
        
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert question in prompt
        assert "Study Buddy Response:" in prompt

    def test_create_quiz_prompt(self):
        """Test quiz prompt creation."""
        prompts = EducationalPrompts()
        
        topic = "photosynthesis"
        prompt = prompts.create_quiz_prompt(topic)
        
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert topic in prompt
        assert "Quiz Question:" in prompt

    def test_create_explanation_prompt(self):
        """Test explanation prompt creation."""
        prompts = EducationalPrompts()
        
        concept = "photosynthesis"
        prompt = prompts.create_explanation_prompt(concept)
        
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert concept in prompt
        assert "Explanation:" in prompt

    def test_create_study_tips_prompt(self):
        """Test study tips prompt creation."""
        prompts = EducationalPrompts()
        
        subject = "biology"
        prompt = prompts.create_study_tips_prompt(subject)
        
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert subject in prompt
        assert "Study Tips:" in prompt

    def test_create_homework_help_prompt(self):
        """Test homework help prompt creation."""
        prompts = EducationalPrompts()
        
        assignment = "Write an essay about photosynthesis"
        prompt = prompts.create_homework_help_prompt(assignment)
        
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert assignment in prompt
        assert "How I can help:" in prompt

    def test_get_encouragement_phrases(self):
        """Test encouragement phrases."""
        prompts = EducationalPrompts()
        
        phrases = prompts.get_encouragement_phrases()
        
        assert isinstance(phrases, list)
        assert len(phrases) > 0
        assert all(isinstance(phrase, str) for phrase in phrases)
        assert all(len(phrase) > 0 for phrase in phrases)

    def test_get_fallback_responses(self):
        """Test fallback responses."""
        prompts = EducationalPrompts()
        
        responses = prompts.get_fallback_responses()
        
        assert isinstance(responses, list)
        assert len(responses) > 0
        assert all(isinstance(response, str) for response in responses)
        assert all(len(response) > 0 for response in responses)


class TestTemplatesPackageImport:
    """
    Test that the templates package can be imported correctly.
    
    These tests ensure that the package structure is correct
    and imports work as expected.
    """

    def test_templates_package_import(self):
        """Test that templates package can be imported."""
        from src.templates import EducationalPrompts
        assert EducationalPrompts is not None

    def test_templates_init_exports(self):
        """Test that __init__.py exports the correct classes."""
        import src.templates as templates
        
        assert hasattr(templates, 'EducationalPrompts')
        assert callable(templates.EducationalPrompts)

    def test_direct_prompts_import(self):
        """Test that prompts module can be imported directly."""
        from src.templates.prompts import EducationalPrompts
        assert EducationalPrompts is not None
        
        # Test instantiation
        prompts = EducationalPrompts()
        assert prompts is not None
