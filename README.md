# LLM Chatbot Demo

A modern, responsive chatbot application with RAG (Retrieval-Augmented Generation) capabilities that allows users to upload documents and ask questions about them.

## Features

- 📚 Document-based Q&A with RAG technology
- 📤 Easy document uploading
- 🌓 Dark/light theme toggle
- 💬 Chat interface with message history

## Quick Start

### Requirements
- Python 3.12+
- OpenAI API key

### Setup and Run
1. Clone and install:
```bash
git clone https://github.com/yourusername/llm-chatbot-demo.git
cd llm-chatbot-demo
pip install -r requirements.txt
```

2. Create `.env` with your OpenAI key:
```
OPENAI_API_KEY=your_openai_api_key
```

3. Start the application:
```bash
# Terminal 1: Start backend
uvicorn backend.main:app --reload --env-file .env

# Terminal 2: Start frontend
cd frontend
streamlit run main.py
```

4. Open `http://localhost:8501` in your browser

## How to Use

### Upload Documents
- Find "📄 Document Management" in the sidebar
- Upload PDFs, TXT, or DOCX files
- Uploaded documents appear in "📝 Uploaded Documents"

### Ask Questions
- Type in the "Ask a question about your documents" field
- Press Enter or click "Ask"
- View AI-generated answers with source references

### Switch Theme
- Click "🌙 Dark" or "☀️ Light" button in the top-left corner

## Technical Architecture

The application combines:
- **Backend**: FastAPI with LangChain and ChromaDB for RAG
- **Frontend**: Streamlit with responsive UI and theme support

### API Endpoints
- `/chat/` - Submit questions and receive answers
- `/upload/` - Upload documents for processing

For a deeper technical dive, explore the code in:
- `backend/`: RAG implementation and API endpoints
- `frontend/`: UI components and styling

## Acknowledgments
Built with Streamlit, FastAPI, LangChain, and OpenAI
