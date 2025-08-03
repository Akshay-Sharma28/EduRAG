# 📚 NCERT RAG – Retrieval-Augmented Generation System

A simple AI-powered question-answering system built specifically for NCERT textbooks. This tool allows users to ask questions in natural language and receive accurate answers derived from NCERT PDFs using Google's Gemini AI models.

---

## 📺 Demo

Watch the working demo here:

[![Watch the demo](https://img.youtube.com/vi/lMVDBVEqMII/0.jpg)](https://www.youtube.com/watch?v=lMVDBVEqMII)

> ⚠️ *The project was previously deployed on AWS EC2, but the free tier has been exhausted. Please use the demo video above to see the system in action.*

---

## 🛠️ Tech Stack

- **Python**
- **LangChain**
- **Google Generative AI (Gemini)**
- **ChromaDB**
- **PyPDF**
- **dotenv**

---

## ⚙️ How It Works

1. **PDF Ingestion**: NCERT PDFs are loaded and split into manageable text chunks.
2. **Embedding**: Each chunk is converted into vector embeddings using Gemini's embedding model.
3. **Vector Storage**: Chunks are stored in ChromaDB for fast similarity-based retrieval.
4. **User Query**: Users ask questions through a CLI.
5. **Semantic Search**: The query is embedded and used to fetch the most relevant chunks.
6. **Answer Generation**: Gemini 1.5 Flash generates a contextual response using the retrieved content.

---

> 🎓 *This project was built for learning and demonstration purposes, particularly around building Retrieval-Augmented Generation systems using NCERT educational content.*
