# Data Package for AI Study Buddy

This directory contains data files and resources used by the AI Study Buddy application.

## 📁 Directory Structure

```
src/data/
├── __init__.py              # Data package initialization and utility functions
├── curriculum_topics.json  # Educational topics organized by subject
└── README.md               # This documentation file
```

## 📚 Available Data

### curriculum_topics.json
Contains educational topics organized by subject and category. The structure is:

```json
{
  "subject_name": {
    "category_name": [
      "Topic 1",
      "Topic 2",
      ...
    ]
  }
}
```

**Available Subjects:**
- `science` (biology, chemistry, physics)
- `mathematics` (algebra, geometry, statistics)
- `history` (world_history, us_history)
- `english` (literature, writing)
- `geography` (physical_geography, human_geography)

## 🔧 Usage

### Loading Data in Python

```python
# Import the data functions
from src.data import load_curriculum_topics, get_subjects, get_topics_for_subject

# Load all curriculum topics
topics = load_curriculum_topics()
print(topics)

# Get list of available subjects
subjects = get_subjects()
print(f"Available subjects: {subjects}")

# Get topics for a specific subject
science_topics = get_topics_for_subject('science')
print(f"Science categories: {list(science_topics.keys())}")
print(f"Biology topics: {science_topics['biology']}")
```

### Example Output

```python
# get_subjects() returns:
['science', 'mathematics', 'history', 'english', 'geography']

# get_topics_for_subject('science') returns:
{
  'biology': [
    'Cell structure and function',
    'Photosynthesis and cellular respiration',
    'Genetics and heredity',
    ...
  ],
  'chemistry': [...],
  'physics': [...]
}
```

## 🔄 Recent Changes

**Data Migration (Latest Update):**
- ✅ Moved data from root-level `data/` directory to `src/data/`
- ✅ Created proper Python package structure with `__init__.py`
- ✅ Added utility functions for easy data access
- ✅ Updated main `src/__init__.py` to include data package
- ✅ Maintained all existing data content

**Benefits of New Structure:**
- Better organization following Python package conventions
- Centralized data access through utility functions
- Easier to import and use data in other modules
- Consistent with the rest of the `src/` architecture

## 📝 Adding New Data

To add new educational content:

1. **For new topics in existing subjects:**
   - Edit `curriculum_topics.json`
   - Add topics to the appropriate subject/category arrays

2. **For new subjects:**
   - Edit `curriculum_topics.json`
   - Add a new top-level subject with categories and topics

3. **For new data files:**
   - Add the file to this directory
   - Update `__init__.py` to include loading functions
   - Update this README with documentation

## 🧪 Testing

The data package includes comprehensive tests in `tests/test_data.py`:

```bash
# Run data-specific tests
python -m pytest tests/test_data.py -v

# Run all tests
python -m pytest tests/ -v
```

## 🔗 Integration

The data package integrates seamlessly with the rest of the application:

- **Configuration**: Can be used to validate supported subjects
- **Services**: Can provide context for AI responses
- **Components**: Can populate UI elements with available topics
- **Templates**: Can customize prompts based on subject areas

## 📋 Maintenance

- Keep `curriculum_topics.json` updated with current educational standards
- Ensure all data is age-appropriate for high school students
- Validate JSON structure after any edits
- Run tests after making changes to verify data integrity
