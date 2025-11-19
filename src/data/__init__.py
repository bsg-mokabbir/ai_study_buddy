"""
Data Package for AI Study Buddy

This package contains data files and resources used by the AI Study Buddy application.

For non-technical users:
- This directory contains educational data like curriculum topics
- Data files are organized here to keep them separate from code
- This makes it easy to update educational content without touching the code

Available data:
- curriculum_topics.json: Educational topics organized by subject
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path


def load_curriculum_topics() -> Optional[Dict[str, Any]]:
    """
    Load curriculum topics from the JSON file.
    
    Returns:
        Dictionary containing curriculum topics organized by subject,
        or None if the file cannot be loaded.
    """
    try:
        data_dir = Path(__file__).parent
        topics_file = data_dir / "curriculum_topics.json"
        
        if topics_file.exists():
            with open(topics_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"Warning: curriculum_topics.json not found at {topics_file}")
            return None
            
    except Exception as e:
        print(f"Error loading curriculum topics: {e}")
        return None


def get_subjects() -> list:
    """
    Get a list of available subjects from the curriculum data.
    
    Returns:
        List of subject names, or empty list if data cannot be loaded.
    """
    topics = load_curriculum_topics()
    if topics:
        return list(topics.keys())
    return []


def get_topics_for_subject(subject: str) -> Dict[str, list]:
    """
    Get topics for a specific subject.
    
    Args:
        subject: The subject name (e.g., 'science', 'mathematics')
        
    Returns:
        Dictionary of topic categories and their topics,
        or empty dict if subject not found.
    """
    topics = load_curriculum_topics()
    if topics and subject.lower() in topics:
        return topics[subject.lower()]
    return {}


# Package metadata
__version__ = "1.0.0"
__description__ = "Data package for AI Study Buddy educational content"

# Available functions for import
__all__ = [
    "load_curriculum_topics",
    "get_subjects", 
    "get_topics_for_subject"
]
