"""
Educational prompt templates for the AI Study Buddy.

This module contains carefully crafted prompts designed to generate
age-appropriate, educational responses for high school students.
"""

from typing import Dict, List
import random


class EducationalPrompts:
    """
    Collection of educational prompt templates for different learning scenarios.
    """

    def __init__(self):
        """Initialize the prompt templates."""
        self.base_context = self._get_base_context()
        self.subject_contexts = self._get_subject_contexts()
        self.quiz_templates = self._get_quiz_templates()

    def _get_base_context(self) -> str:
        """Get the base context for all educational interactions."""
        # This is the foundational prompt that establishes the AI's role and behavior
        # It sets the tone for being helpful, educational, and age-appropriate
        return """You are a helpful AI study buddy for high school students. You provide clear, accurate, and age-appropriate explanations. You are encouraging, patient, and focused on helping students learn. Always:

1. Use language appropriate for high school students (ages 14-18)
   # Avoid overly complex academic jargon while maintaining accuracy
2. Provide clear, step-by-step explanations when needed
   # Break down complex concepts into digestible parts
3. Give examples to illustrate concepts
   # Use real-world examples that students can relate to
4. Encourage further learning and curiosity
   # Foster a growth mindset and love of learning
5. If you're unsure about something, say so and suggest reliable sources
   # Maintain honesty and direct students to authoritative resources
6. Keep responses educational and appropriate for school settings
   # Ensure all content is suitable for academic environments

"""

    def _get_subject_contexts(self) -> Dict[str, str]:
        """Get subject-specific context additions."""
        # These prompts customize the AI's approach for different academic subjects
        # Each prompt emphasizes the key skills and methods for that subject area
        return {
            # Science: Emphasizes empirical evidence, experimentation, and real-world applications
            'science': """Focus on scientific accuracy and the scientific method. Use examples from everyday life to explain concepts. Encourage hands-on learning and observation.""",

            # Mathematics: Emphasizes logical reasoning, step-by-step problem solving, and practical applications
            'math': """Break down problems step-by-step. Show your work clearly. Use real-world applications to make math relevant. Encourage practice and pattern recognition.""",

            # History: Emphasizes chronology, causation, and understanding historical context
            'history': """Provide historical context and connections between events. Use specific dates and facts. Help students understand cause and effect in historical events.""",

            # English: Emphasizes literacy skills, critical analysis, and communication
            'english': """Focus on reading comprehension, writing skills, and literary analysis. Use examples from well-known literature. Encourage critical thinking about texts.""",

            # Geography: Emphasizes spatial thinking, human-environment interaction, and global awareness
            'geography': """Use maps, statistics, and real-world examples. Connect geographical features to human activities and cultures. Encourage global awareness.""",

            # General: Flexible approach that adapts to any subject not specifically covered above
            'general': """Adapt your response to the subject matter of the question. Provide interdisciplinary connections when relevant."""
        }

    def _get_quiz_templates(self) -> Dict[str, List[str]]:
        """Get templates for generating quiz questions."""
        # These templates create questions at different cognitive levels based on Bloom's Taxonomy
        # Easy questions test basic knowledge and comprehension
        # Medium questions test application and analysis
        # Hard questions test synthesis and evaluation
        return {
            # Easy level: Basic recall and comprehension questions
            # These test fundamental knowledge and understanding
            'easy': [
                "What is {concept}?",  # Simple definition questions
                "Define {term} in simple terms.",  # Basic vocabulary
                "Name one example of {topic}.",  # Concrete examples
                "True or False: {statement}",  # Binary choice questions
                "Fill in the blank: {sentence_with_blank}"  # Completion questions
            ],

            # Medium level: Application and analysis questions
            # These test understanding of processes and relationships
            'medium': [
                "Explain how {process} works.",  # Process explanation
                "What are the main differences between {concept1} and {concept2}?",  # Comparison
                "Why is {concept} important in {subject}?",  # Significance and relevance
                "Describe the relationship between {element1} and {element2}.",  # Connections
                "What would happen if {scenario}?"  # Hypothetical scenarios
            ],

            # Hard level: Synthesis and evaluation questions
            # These test higher-order thinking and critical analysis
            'hard': [
                "Analyze the impact of {event} on {outcome}.",  # Cause and effect analysis
                "Compare and contrast {concept1} and {concept2}, discussing their advantages and disadvantages.",  # Complex comparison
                "Evaluate the significance of {discovery} in the context of {field}.",  # Critical evaluation
                "Synthesize information about {topic} to explain {complex_relationship}.",  # Information synthesis
                "Critically assess the role of {factor} in {process}."  # Critical assessment
            ]
        }

    def create_qa_prompt(self, question: str, subject: str = 'general') -> str:
        """
        Create a prompt for answering a student's question.

        Args:
            question: The student's question
            subject: The subject area

        Returns:
            Formatted prompt for the language model
        """
        # Get base context
        prompt = self.base_context

        # Add subject-specific context
        if subject in self.subject_contexts:
            prompt += self.subject_contexts[subject] + "\n\n"

        # Add the specific question
        prompt += f"Student Question: {question}\n\n"
        prompt += "Study Buddy Response:"

        return prompt.strip()

    def create_quiz_prompt(self, topic: str, difficulty: str = 'medium') -> str:
        """
        Create a prompt for generating quiz questions.

        Args:
            topic: The topic for the quiz question
            difficulty: Difficulty level (easy, medium, hard)

        Returns:
            Formatted prompt for generating a quiz question
        """
        # Get base context
        prompt = self.base_context

        # Add quiz-specific instructions
        prompt += f"""Generate a {difficulty} level quiz question about {topic} for high school students.

The question should:
1. Test understanding of key concepts
2. Be clear and unambiguous
3. Be appropriate for the {difficulty} difficulty level
4. Include the answer or explanation if needed

Topic: {topic}
Difficulty: {difficulty}

Quiz Question:"""

        return prompt.strip()

    def create_explanation_prompt(self, concept: str, subject: str = 'general',
                                grade_level: str = 'high school') -> str:
        """
        Create a prompt for explaining a concept.

        Args:
            concept: The concept to explain
            subject: The subject area
            grade_level: The grade level for the explanation

        Returns:
            Formatted prompt for explaining the concept
        """
        prompt = self.base_context

        # Add subject context
        if subject in self.subject_contexts:
            prompt += self.subject_contexts[subject] + "\n\n"

        # Add explanation request
        prompt += f"""Please explain the concept of "{concept}" to a {grade_level} student studying {subject}.

Your explanation should:
1. Start with a simple definition
2. Provide relevant examples
3. Break down complex ideas into understandable parts
4. Connect to things the student might already know
5. End with why this concept is important or useful

Concept to explain: {concept}

Explanation: """

        return prompt

    def create_study_tips_prompt(self, subject: str, topic: str = None) -> str:
        """
        Create a prompt for generating study tips.

        Args:
            subject: The subject area
            topic: Specific topic (optional)

        Returns:
            Formatted prompt for study tips
        """
        prompt = self.base_context

        prompt += f"""Provide helpful study tips for high school students learning {subject}"""

        if topic:
            prompt += f", specifically focusing on {topic}"

        prompt += """.

Your study tips should:
1. Be practical and actionable
2. Include different learning styles (visual, auditory, kinesthetic)
3. Suggest specific study techniques
4. Recommend useful resources or tools
5. Include time management advice
6. Be encouraging and motivating

Study Tips: """

        return prompt

    def create_homework_help_prompt(self, assignment_description: str,
                                  subject: str = 'general') -> str:
        """
        Create a prompt for helping with homework.

        Args:
            assignment_description: Description of the homework assignment
            subject: The subject area

        Returns:
            Formatted prompt for homework help
        """
        prompt = self.base_context

        # Add subject context
        if subject in self.subject_contexts:
            prompt += self.subject_contexts[subject] + "\n\n"

        # Add homework help instructions
        prompt += """I will help you with your homework by:
1. Breaking down the assignment into manageable steps
2. Explaining relevant concepts you need to understand
3. Providing guidance without doing the work for you
4. Suggesting resources for further learning
5. Helping you check your understanding

Remember: The goal is to help you learn, not to do the work for you!

"""

        prompt += f"Assignment: {assignment_description}\n\n"
        prompt += "How I can help: "

        return prompt

    def get_encouragement_phrases(self) -> List[str]:
        """Get encouraging phrases to use in responses."""
        return [
            "Great question!",
            "You're on the right track!",
            "That's a thoughtful question.",
            "I can see you're really thinking about this!",
            "Excellent observation!",
            "You're making good progress!",
            "That shows good critical thinking!",
            "Keep up the great work!",
            "You're asking all the right questions!",
            "That's exactly the kind of thinking that leads to learning!"
        ]

    def get_fallback_responses(self) -> List[str]:
        """Get fallback responses when the AI is uncertain."""
        return [
            "That's a great question that I'd like to help you explore further. Could you provide a bit more context?",
            "I want to make sure I give you accurate information. Could you check with your teacher or textbook on this one?",
            "That's beyond my current knowledge, but it sounds like an interesting topic to research!",
            "I'm not completely sure about that. Let's break it down - what specific part would you like to focus on?",
            "That's a complex topic! What specific aspect are you most curious about?"
        ]
