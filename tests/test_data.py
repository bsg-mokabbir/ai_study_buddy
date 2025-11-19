"""
Tests for Data Module (src/data/)

This test file validates that the data module can properly load and provide
access to educational content like curriculum topics.
"""

import pytest
import json
from pathlib import Path

# Import the data module to test
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data import (
    load_curriculum_topics,
    get_subjects,
    get_topics_for_subject
)


class TestDataModule:
    """Test the data module functionality."""

    def test_curriculum_topics_file_exists(self):
        """Test that the curriculum topics file exists in the new location."""
        # Get the path to the data directory
        current_dir = Path(__file__).parent.parent
        data_file = current_dir / "src" / "data" / "curriculum_topics.json"
        
        assert data_file.exists(), f"curriculum_topics.json not found at {data_file}"
        assert data_file.is_file(), "curriculum_topics.json should be a file"

    def test_load_curriculum_topics(self):
        """Test that curriculum topics can be loaded successfully."""
        topics = load_curriculum_topics()
        
        assert topics is not None, "Should be able to load curriculum topics"
        assert isinstance(topics, dict), "Topics should be a dictionary"
        assert len(topics) > 0, "Topics dictionary should not be empty"

    def test_curriculum_topics_structure(self):
        """Test that the curriculum topics have the expected structure."""
        topics = load_curriculum_topics()
        
        # Should have expected subjects
        expected_subjects = ['science', 'mathematics', 'history', 'english', 'geography']
        for subject in expected_subjects:
            assert subject in topics, f"Missing subject: {subject}"
            assert isinstance(topics[subject], dict), f"Subject {subject} should be a dictionary"

    def test_get_subjects(self):
        """Test getting list of available subjects."""
        subjects = get_subjects()
        
        assert isinstance(subjects, list), "Subjects should be a list"
        assert len(subjects) > 0, "Should have at least one subject"
        
        # Check for expected subjects
        expected_subjects = ['science', 'mathematics', 'history', 'english', 'geography']
        for subject in expected_subjects:
            assert subject in subjects, f"Missing subject: {subject}"

    def test_get_topics_for_subject(self):
        """Test getting topics for a specific subject."""
        # Test with science
        science_topics = get_topics_for_subject('science')
        assert isinstance(science_topics, dict), "Science topics should be a dictionary"
        assert 'biology' in science_topics, "Science should include biology"
        assert 'chemistry' in science_topics, "Science should include chemistry"
        assert 'physics' in science_topics, "Science should include physics"
        
        # Test with mathematics
        math_topics = get_topics_for_subject('mathematics')
        assert isinstance(math_topics, dict), "Math topics should be a dictionary"
        assert 'algebra' in math_topics, "Mathematics should include algebra"
        assert 'geometry' in math_topics, "Mathematics should include geometry"
        
        # Test with non-existent subject
        empty_topics = get_topics_for_subject('nonexistent')
        assert isinstance(empty_topics, dict), "Should return empty dict for non-existent subject"
        assert len(empty_topics) == 0, "Should be empty for non-existent subject"

    def test_topics_content_quality(self):
        """Test that the topics contain meaningful educational content."""
        topics = load_curriculum_topics()
        
        # Check science topics
        science = topics['science']
        biology_topics = science['biology']
        assert isinstance(biology_topics, list), "Biology topics should be a list"
        assert len(biology_topics) > 0, "Biology should have topics"
        assert "Cell structure and function" in biology_topics, "Should have basic biology topics"
        
        # Check mathematics topics
        math = topics['mathematics']
        algebra_topics = math['algebra']
        assert isinstance(algebra_topics, list), "Algebra topics should be a list"
        assert len(algebra_topics) > 0, "Algebra should have topics"
        assert "Linear equations and inequalities" in algebra_topics, "Should have basic algebra topics"

    def test_data_module_imports(self):
        """Test that the data module can be imported properly."""
        # Test that we can import the module
        import src.data
        assert src.data is not None
        
        # Test that functions are available
        assert hasattr(src.data, 'load_curriculum_topics')
        assert hasattr(src.data, 'get_subjects')
        assert hasattr(src.data, 'get_topics_for_subject')

    def test_json_file_validity(self):
        """Test that the JSON file is valid and well-formed."""
        current_dir = Path(__file__).parent.parent
        data_file = current_dir / "src" / "data" / "curriculum_topics.json"
        
        # Should be able to parse as JSON
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert isinstance(data, dict), "JSON should parse to a dictionary"
        assert len(data) > 0, "JSON should not be empty"


class TestDataIntegration:
    """Test how the data module integrates with the rest of the application."""

    def test_data_package_in_src_init(self):
        """Test that the data package is properly included in src.__init__.py."""
        import src
        
        # Check that 'data' is in the __all__ list
        assert hasattr(src, '__all__'), "src package should have __all__ defined"
        assert 'data' in src.__all__, "data should be in src.__all__"

    def test_data_accessibility_from_other_modules(self):
        """Test that data can be accessed from other parts of the application."""
        # This simulates how other modules might access the data
        from src.data import load_curriculum_topics
        
        topics = load_curriculum_topics()
        assert topics is not None, "Data should be accessible from other modules"
        
        # Test that we can get specific information
        subjects = list(topics.keys())
        assert len(subjects) > 0, "Should be able to extract subjects"
