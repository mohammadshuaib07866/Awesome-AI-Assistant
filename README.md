# Awesome AI Assistant

A Streamlit-based chatbot application that combines conversational AI with RAG-powered PDF retrieval. The assistant supports:
- chat sessions with thread history
- tool-assisted answers including search and calculator functions
- PDF upload and retrieval using FAISS embeddings
- OpenAI model integration via environment configuration

## Features

- **Interactive Streamlit UI** with chat thread management
- **RAG document retrieval** from PDF files uploaded via the sidebar
- **Tool-backed model execution** using `langchain` and `langgraph`
- **FAISS vector store** for semantic PDF search
- Reusable chat state with thread recall

## Getting Started

### Prerequisites

- Python 3.13 or newer
- `git` (optional, for cloning the repository)
- An OpenAI API key

### Install

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install the project dependencies:

```bash
pip install -e .
```

If you prefer not to install the package as editable, run:

```bash
pip install .
```

### Environment

Create a `.env` file in the repository root with at least:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=1024
```

### Run the application

```bash
streamlit run main.py
```

Then open the Streamlit URL shown in your terminal.

## Usage

1. Open the app in your browser.
2. Use the sidebar to upload one or more PDF files.
3. The app will ingest the uploaded documents into the RAG vector store.
4. Enter questions in the chat input.
5. The assistant can answer directly or use RAG retrieval for PDF-based knowledge.

## Project Structure

- `main.py` - Streamlit application entry point and UI logic
- `app/rag.py` - PDF ingestion, FAISS retriever creation, and RAG tool definition
- `app/graph/builder.py` - chatbot graph assembly and thread retrieval
- `app/graph/nodes/chat_node.py` - chat node and tool binding for the assistant
- `app/llms/openai_model.py` - OpenAI model wrapper and settings integration
- `app/tools/tools.py` - additional tools such as calculator and search
- `app/documuents/` - folder for PDF documents used by the RAG retrieval system

## Notes

- Uploaded PDFs are saved to `app/documuents/` and automatically reindexed.
- The RAG retriever uses `text-embedding-3-small` by default.
- If you add new PDFs manually, click "Reload RAG documents" in the sidebar.

## License

This project is available under the terms of the `LICENSE` file.
