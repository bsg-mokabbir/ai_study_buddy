# 📚 AI Study Buddy - Simple OpenAI Chatbot

A simple educational chatbot using OpenAI API to help high school students with their studies.

## ✨ Features

- **Educational Focus**: Specialized for high school subjects
- **OpenAI Integration**: Uses GPT-3.5-turbo, GPT-4, or GPT-4-turbo
- **Clean Interface**: Simple, distraction-free chat interface
- **Subject Support**: Math, Science, History, English, Geography
- **Study Tips**: Learning strategies and educational guidance

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. **Run the application**
   ```bash
   python -m streamlit run  app.py
   ```

## 🔑 API Key Setup

1. **Get an OpenAI API key** from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Copy the example environment file**:
   ```bash
   cp .env.example .env
   ```
3. **Edit the `.env` file** and add your key:
   ```env
   OPENAI_API_KEY=your_actual_api_key_here
   ```
4. **Restart the application**

## 🎮 Usage

### Basic Chat
1. Open http://localhost:8501 in your browser
2. Choose your preferred AI model (GPT-3.5-turbo, GPT-4, etc.)
3. Ask educational questions
4. Get helpful, detailed responses

### Example Questions
- "Explain photosynthesis"
- "What is the Pythagorean theorem?"
- "Tell me about World War II"
- "How do I solve quadratic equations?"
- "What are the parts of speech?"

### Features
- **Model Selection**: Choose between different OpenAI models
- **Chat History**: Maintains conversation context
- **Quick Examples**: Click sidebar buttons for sample questions
- **Clear Chat**: Reset conversation anytime

## 📁 Project Structure

```
ai_study_buddy/
├── app.py                # Main Streamlit application
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .env                 # Your actual environment variables (not in git)
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with:
```env
# Required: OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Optional: OpenAI Organization ID
OPENAI_ORG_ID=your_organization_id_here
```

### Model Options
- **gpt-3.5-turbo**: Fast and cost-effective
- **gpt-4**: More capable but slower
- **gpt-4-turbo-preview**: Latest GPT-4 model

## 🧪 Testing

Test the application:
```bash
# Check if dependencies are installed
python -c "import streamlit, openai; print('✅ Dependencies OK')"

# Test with sample question
python -c "
import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
print('✅ OpenAI connection OK' if openai.api_key else '❌ No API key')
"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **OpenAI**: For providing the GPT models
- **Streamlit**: For the web application framework
- **Python-dotenv**: For environment variable management

## 📞 Support

If you encounter issues:
1. Check that your OpenAI API key is correctly set
2. Verify you have sufficient API credits
3. Check the [Issues](../../issues) page for known problems

---

**Happy Learning! 📚✨**
