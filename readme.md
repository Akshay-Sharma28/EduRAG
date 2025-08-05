# 📚 EduRAG – NCERT Retrieval-Augmented Generation System

A powerful AI-powered question-answering system designed specifically for NCERT textbooks. This tool enables students and educators to ask questions in natural language and receive accurate, contextual answers derived from NCERT PDF content using Google's free Gemini AI models.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Powered by Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-blue)](https://ai.google.dev/)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key (free from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/EduRAG.git
   cd EduRAG
   ```

2. **Run the setup script**
   ```bash
   python3 setup.py
   ```

3. **Configure your API key**
   - Add your Gemini API key to the `.env` file:
   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```

4. **Add your PDF files**
   - Place your NCERT PDF files in the `data/` directory

5. **Start the application**
   
   **CLI Version:**
   ```bash
   python3 main.py
   ```
   
   **Web Interface:**
   ```bash
   ./start_web.sh    # Unix/Linux/Mac
   # or
   start_web.bat     # Windows
   ```
   
   Access the web interface at: http://localhost:5000

---

## 📺 Demo

Watch the working demo here:

[![Watch the demo](https://img.youtube.com/vi/lMVDBVEqMII/0.jpg)](https://www.youtube.com/watch?v=lMVDBVEqMII)

---

## 🛠️ Tech Stack

- **Python 3.8+** - Core programming language
- **LangChain** - Framework for building LLM applications
- **Google Generative AI (Gemini)** - Free AI model for embeddings and text generation
- **ChromaDB** - Vector database for semantic search
- **PyPDF** - PDF processing and text extraction
- **python-dotenv** - Environment variable management

---

## ⚙️ How It Works

1. **📄 PDF Ingestion**: NCERT PDFs are automatically loaded and split into manageable text chunks
2. **🔢 Embedding**: Each chunk is converted into vector embeddings using Gemini's embedding model
3. **💾 Vector Storage**: Chunks are stored in ChromaDB for lightning-fast similarity-based retrieval
4. **❓ User Query**: Users ask questions through an intuitive command-line interface
5. **🔍 Semantic Search**: The query is embedded and used to fetch the most relevant content chunks
6. **🤖 Answer Generation**: Gemini 1.5 Flash generates accurate, contextual responses using retrieved content

---

## 🌐 Web Interface Features

- **Interactive Chat Interface** - Ask questions through a modern web UI
- **PDF Upload System** - Upload NCERT PDFs directly through the browser
- **Real-time Processing** - See responses as they're generated
- **System Status Dashboard** - Monitor system health and loaded files
- **Responsive Design** - Works on desktop, tablet, and mobile devices
- **Sample Questions** - Quick-start with pre-defined example questions

## 🚀 EC2 Deployment (Production Ready)

### Automated EC2 Setup

1. **Launch an Amazon Linux 2 EC2 instance** (t2.micro eligible for free tier)

2. **Configure Security Group** to allow:
   - SSH (port 22) from your IP
   - HTTP (port 80) from anywhere (0.0.0.0/0)
   - HTTPS (port 443) from anywhere (optional)

3. **Connect to your instance and run:**
   ```bash
   # Upload your files to the server first
   scp -r EduRAG/ ec2-user@your-instance-ip:/home/ec2-user/
   
   # SSH into the instance
   ssh ec2-user@your-instance-ip
   
   # Run the deployment script
   cd EduRAG
   chmod +x deploy_ec2.sh
   ./deploy_ec2.sh
   ```

4. **Configure your API key:**
   ```bash
   sudo nano /opt/edurag/.env
   # Add: GEMINI_API_KEY=your_api_key_here
   
   # Restart the service
   sudo systemctl restart edurag
   ```

5. **Access your application:**
   - Open http://your-instance-public-ip in your browser
   - Upload PDFs through the web interface
   - Start asking questions!

### EC2 Management Commands

```bash
# Check status
/opt/edurag/manage.sh status

# View logs
/opt/edurag/manage.sh logs

# Restart services
/opt/edurag/manage.sh restart

# Update application
/opt/edurag/manage.sh update
```

## 🐳 Docker Deployment

### Quick Start with Docker

1. **Using Docker Compose (Recommended)**
   ```bash
   # Set your API key
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   
   # Start the application
   docker-compose up -d
   ```
   
   Access at: http://localhost

2. **Using Docker only**
   ```bash
   docker build -t edurag .
   docker run -d -p 5000:5000 \
     -e GEMINI_API_KEY=your_api_key_here \
     -v $(pwd)/data:/app/data \
     -v $(pwd)/docs:/app/docs \
     edurag
   ```
   
   Access at: http://localhost:5000

---

## ⚙️ Configuration

The system can be configured via environment variables in the `.env` file:

```bash
# Google Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Application Configuration
CHUNK_SIZE=1000          # Size of text chunks for processing
CHUNK_OVERLAP=200        # Overlap between chunks
RETRIEVAL_K=5           # Number of relevant chunks to retrieve
```

---

## 📁 Project Structure

```
EduRAG/
├── main.py                 # Main application entry point
├── setup.py               # Automated setup script
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── data/                # PDF files directory
│   └── AI.pdf          # Sample NCERT PDF
├── docs/               # ChromaDB vector storage
├── src/               # Source code modules
│   ├── config.py      # Configuration management
│   ├── embed.py       # Embedding functionality
│   ├── ingest.py      # PDF processing and ingestion
│   ├── query_engine.py # RAG chain implementation
│   ├── retriever.py   # Document retrieval
│   └── vectorstore.py # Vector database operations
└── README.md          # This file
```

---

## 🔧 Development

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/EduRAG.git
cd EduRAG

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run the application
python3 main.py
```

### Adding New Features

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 🔑 Getting a Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key
5. Add it to your `.env` file

The Gemini API is **completely free** for personal use with generous rate limits.

---

## 🐛 Troubleshooting

### Common Issues

**"GEMINI_API_KEY environment variable is not set"**
- Ensure your `.env` file exists and contains your API key
- Check that the key is correctly formatted

**"No PDF files found in data directory"**
- Add your PDF files to the `data/` directory
- Ensure files have `.pdf` extension

**"Error processing query"**
- Check your internet connection
- Verify your API key is valid and has quota remaining

### Performance Optimization

- **Large PDFs**: Adjust `CHUNK_SIZE` and `CHUNK_OVERLAP` in `.env`
- **Memory Usage**: Reduce `RETRIEVAL_K` for faster responses
- **Response Quality**: Increase `RETRIEVAL_K` for more comprehensive answers

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

---

## 🙏 Acknowledgments

- **Google** for providing free access to Gemini AI models
- **LangChain** community for the excellent framework
- **ChromaDB** for the vector database solution
- **NCERT** for making educational content accessible

---

> 🎓 *This project was built for educational purposes to demonstrate building production-ready Retrieval-Augmented Generation systems using modern AI tools.*
