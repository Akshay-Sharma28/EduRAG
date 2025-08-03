# RAG System 📚🤖

A Retrieval-Augmented Generation (RAG) system designed for querying documents using Google's Gemini AI. This project enables intelligent question-answering over content through semantic search and AI-powered response generation.

> **Note: This project is created for learning and reference purposes only. It demonstrates the implementation of RAG systems using modern AI technologies and is intended for educational use.**

> **Please create Data and Docs directories before you try to run this!**

## Features 🌟

- **PDF Document Ingestion**: Automatically processes and chunks PDF documents for optimal retrieval
- **Semantic Search**: Uses Google's Gemini embeddings for intelligent document retrieval
- **AI-Powered Responses**: Leverages Gemini 1.5 Flash for generating contextual answers
- **Persistent Vector Storage**: Uses ChromaDB for efficient document storage and retrieval
- **Interactive CLI**: Simple command-line interface for querying documents
- **Modular Architecture**: Clean, maintainable code structure with separate modules

## Architecture 🏗️

```
rag/
├── main.py                 # Entry point and CLI interface
├── requirements.txt        # Python dependencies
├── data/                  # Directory for PDF documents
├── docs/                  # Vector store persistence directory
└── src/
    ├── config.py          # Configuration and environment variables
    ├── embed.py           # Google Gemini embeddings wrapper
    ├── ingest.py          # PDF processing and document chunking
    ├── query_engine.py    # RAG chain construction
    ├── retriever.py       # Vector store retrieval logic
    └── vectorstore.py     # ChromaDB vector store management
```

## Prerequisites 📋

- Python 3.8 or higher
- Google AI API key (for Gemini models)
- PDF documents

## Installation 🚀

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_google_ai_api_key_here
   ```

4. **Add PDF documents**
   Place your PDF files in the `data/` directory:
   ```
   data/
   ├── doc1.pdf
   ├── doc2.pdf
   └── ... (other PDFs)
   ```

## Usage 💻

1. **Run the application**
   ```bash
   python main.py
   ```

2. **First-time setup**
   - The system will automatically detect if no vector store exists
   - It will process all PDFs in the `data/` directory
   - Documents will be chunked and embedded using Gemini embeddings
   - Vector store will be persisted to the `docs/` directory

3. **Ask questions**
   ```
   Ask a question (or type 'exit'): What is photosynthesis?
   
   📘 Answer:
   Photosynthesis is the process by which green plants and some bacteria 
   convert light energy into chemical energy...
   ```

4. **Exit the application**
   ```
   Ask a question (or type 'exit'): exit
   👋 Exiting.
   ```

## Configuration ⚙️

The system can be configured through `src/config.py`:

- `CHUNK_SIZE`: Size of document chunks (default: 500)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 50)
- `EMBEDDING_MODEL_NAME`: Gemini embedding model (default: "models/embedding-001")

## How It Works 🔍

1. **Document Ingestion**: PDFs are loaded and split into manageable chunks using LangChain's text splitter
2. **Embedding Generation**: Each chunk is converted to vector embeddings using Google's Gemini embedding model
3. **Vector Storage**: Embeddings are stored in ChromaDB for efficient similarity search
4. **Query Processing**: User queries are embedded and matched against stored document chunks
5. **Response Generation**: Relevant chunks are fed to Gemini 1.5 Flash to generate contextual answers

## Technologies Used 🛠️

- **LangChain**: Framework for building LLM applications
- **Google Generative AI**: Gemini models for embeddings and text generation
- **ChromaDB**: Vector database for similarity search
- **PyPDF**: PDF document processing
- **Python-dotenv**: Environment variable management

## File Structure Details 📁

- **`main.py`**: Entry point with CLI interface and workflow orchestration
- **`src/config.py`**: Central configuration management
- **`src/ingest.py`**: PDF loading, chunking, and initial processing
- **`src/embed.py`**: Google Gemini embeddings initialization
- **`src/vectorstore.py`**: ChromaDB vector store creation and loading
- **`src/retriever.py`**: Document retrieval configuration
- **`src/query_engine.py`**: RAG chain construction with Gemini LLM

## Performance Considerations 📊

- **Chunk Size**: Larger chunks provide more context but may reduce precision
- **Retrieval Count**: Default retrieves top 5 similar chunks (configurable)
- **Temperature**: Set to 0.3 for balanced creativity and factual accuracy
- **Embedding Model**: Uses Google's latest embedding model for optimal performance

## Limitations ⚠️

- Requires stable internet connection for Gemini API calls
- Processing time depends on document size and internet speed
- API usage is subject to Google AI's rate limits and pricing
- Currently supports only PDF documents

## Educational Purpose 📖

This project is designed as a learning resource for:
- Understanding RAG system architecture
- Implementing vector databases for semantic search
- Working with Google's Generative AI APIs
- Building modular Python applications
- Exploring document processing and chunking strategies

## Contributing 🤝

This is an educational project. Feel free to fork and experiment with:
- Different chunking strategies
- Alternative embedding models
- Enhanced retrieval mechanisms
- UI improvements
- Additional document formats

## Troubleshooting 🔧

**Common Issues:**

1. **Missing API Key**: Ensure `GEMINI_API_KEY` is set in your `.env` file
2. **Empty Data Directory**: Add PDF files to the `data/` directory before running
3. **Permission Errors**: Ensure write permissions for the `docs/` directory
4. **API Limits**: Check Google AI API quotas and usage limits

**Getting Help:**
- Check the console output for detailed error messages
- Verify all dependencies are installed correctly
- Ensure PDF files are readable and not corrupted

---
