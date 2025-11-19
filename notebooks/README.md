# 🎓 AI Study Buddy Tutorial

This tutorial demonstrates how to build a complete AI-powered educational chatbot from scratch, progressing from a simple text-only bot to a full multimodal web application.

## 📚 Tutorial Structure

### 📖 Jupyter Notebook Tutorial (`AI_Study_Buddy_Tutorial.ipynb`)
A comprehensive, step-by-step tutorial that teaches you to build the AI Study Buddy progressively:

**Phase 1: Text-Only Chatbot**
- Configuration management
- Educational prompt design
- OpenAI API integration
- Conversation management

**Phase 2: Adding Image Generation**
- Multimodal capabilities
- Intent detection (text vs image requests)
- DALL-E integration
- Enhanced response handling

**Phase 3: Web Interface**
- Streamlit integration
- Interactive UI components
- Image display handling
- Session state management

### 🚀 Standalone App (`tutorial_app.py`)
A complete, runnable Streamlit application that demonstrates all three phases working together.

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd ai_study_buddy/notebooks
   ```

2. **Install required packages**
   ```bash
   pip install streamlit openai python-dotenv pillow requests httpx jupyter
   ```

3. **Set up your OpenAI API key**

   Create a `.env` file in the project root directory:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

   Get your API key from: https://platform.openai.com/api-keys

## 🎯 How to Use

### Option 1: Interactive Tutorial (Recommended)
1. **Open the Jupyter notebook**
   ```bash
   jupyter notebook AI_Study_Buddy_Tutorial.ipynb
   ```

2. **Follow the step-by-step tutorial**
   - Execute each cell in order
   - Read the explanations and comments
   - Experiment with the code
   - Test each phase as you build it

### Option 2: Run the Complete App
1. **Launch the standalone app**
   ```bash
   streamlit run tutorial_app.py
   ```

2. **Use the web interface**
   - Ask educational questions
   - Request image generation
   - Try the example questions
   - Explore the sidebar controls

## 🎨 Features Demonstrated

### Educational Capabilities
- ✅ Subject-specific responses (Math, Science, History, English, Geography)
- ✅ Age-appropriate explanations for high school students
- ✅ Step-by-step problem solving
- ✅ Encouraging and supportive tone

### Technical Features
- ✅ Text generation with GPT models
- ✅ Image generation with DALL-E 3
- ✅ Automatic intent detection
- ✅ Conversation memory
- ✅ Error handling and fallbacks
- ✅ Clean, modular architecture

### User Interface
- ✅ Modern Streamlit web interface
- ✅ Responsive design
- ✅ Interactive sidebar controls
- ✅ Real-time statistics
- ✅ Example questions
- ✅ Image display capabilities

## 🧪 Example Interactions

### Text Questions
- "What is photosynthesis?"
- "How do I solve x² + 5x + 6 = 0?"
- "What caused World War I?"
- "Explain the difference between metaphor and simile"

### Image Requests
- "Create an image of a DNA molecule"
- "Draw me a picture of the solar system"
- "Generate an image of ancient Rome"
- "Show me a visualization of photosynthesis"

## 📖 Learning Objectives

By completing this tutorial, you'll learn:

### Programming Concepts
- **Object-Oriented Design**: Classes, inheritance, and encapsulation
- **API Integration**: Working with external services (OpenAI)
- **Error Handling**: Robust error management and user feedback
- **Modular Architecture**: Clean, maintainable code structure

### AI/ML Concepts
- **Prompt Engineering**: Designing effective AI prompts
- **Multimodal AI**: Combining text and image generation
- **Intent Recognition**: Detecting user intentions
- **Conversation Management**: Maintaining context and memory

### Web Development
- **Streamlit Framework**: Building interactive web apps
- **Session Management**: Handling user state
- **UI/UX Design**: Creating intuitive interfaces
- **Real-time Interactions**: Dynamic content updates

## 🔧 Customization Ideas

Extend the tutorial by adding:

1. **More Subjects**: Add specialized prompts for other subjects
2. **Quiz Generation**: Create interactive quizzes
3. **File Upload**: Allow homework file uploads
4. **Voice Integration**: Add speech-to-text capabilities
5. **Progress Tracking**: Monitor learning progress
6. **Multi-language Support**: Support multiple languages
7. **Advanced Styling**: Custom themes and layouts
8. **Database Integration**: Store conversations and progress

## 🏗️ Architecture Overview

```
📁 Tutorial Structure (matches main project structure)
├── 🔧 Configuration Layer (src/config/)
│   ├── TextChatbotConfig
│   └── MultimodalChatbotConfig
├── 📝 Templates Layer (src/templates/)
│   └── EducationalPrompts
├── 🌐 Service Layer (src/services/)
│   ├── TextChatbotService
│   └── MultimodalChatbotService
├── 🛠️ Utils Layer (src/utils/)
│   └── Helper functions
├── 🤖 Business Logic Layer (src/main.py)
│   ├── TextOnlyChatbot
│   └── MultimodalChatbot
├── 🎨 Components Layer (src/components/)
│   └── Chat interface components
└── 🌐 Presentation Layer
    └── StudyBuddyStreamlitApp
```

## 🚨 Troubleshooting

### Common Issues

**API Key Not Found**
- Ensure `.env` file is in the correct location
- Check that the API key is valid and active
- Verify the environment variable name is `OPENAI_API_KEY`

**Connection Issues**
- Check your internet connection
- Try the relaxed SSL settings (automatically attempted)
- Verify OpenAI service status

**Image Display Problems**
- Ensure PIL (Pillow) is installed
- Check that the image URL is accessible
- Verify requests library is working

**Streamlit Issues**
- Update Streamlit: `pip install --upgrade streamlit`
- Clear browser cache
- Try a different browser

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the error messages carefully
3. Ensure all dependencies are installed
4. Verify your OpenAI API key is working

## 🎉 Conclusion

This tutorial provides a comprehensive introduction to building AI-powered educational applications. The progressive approach helps you understand each component while building toward a complete, production-ready application.

The same architectural principles and code patterns used here can be applied to build other AI applications, making this tutorial a valuable foundation for your AI development journey.

Happy coding! 🚀📚🤖
