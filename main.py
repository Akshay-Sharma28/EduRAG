import os
import sys
from pathlib import Path
from src.vectorstore import load_vectorstore
from src.retriever import get_retriever
from src.query_engine import build_rag_chain
from src.ingest import ingest_pdfs
from src.config import GEMINI_API_KEY

VECTORSTORE_DIR = Path("./docs")
PDF_DIR = Path("./data")

def check_setup():
    """Check if the environment is properly set up"""
    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY environment variable is not set.")
        print("💡 Please add your Gemini API key to the .env file")
        print("📝 You can get a free API key from: https://makersuite.google.com/app/apikey")
        return False
    
    if not PDF_DIR.exists():
        print(f"❌ PDF directory '{PDF_DIR}' does not exist.")
        return False
        
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    if not pdf_files:
        print(f"❌ No PDF files found in '{PDF_DIR}' directory.")
        print("📝 Please add your PDF files to the data directory")
        return False
    
    return True

def main():
    """Main application function"""
    print("🚀 Starting EduRAG - NCERT Question Answering System")
    
    if not check_setup():
        print("\n❌ Setup incomplete. Please fix the issues above and try again.")
        sys.exit(1)
    
    try:
        # Check if vectorstore needs to be created or updated
        if not VECTORSTORE_DIR.exists() or not any(VECTORSTORE_DIR.iterdir()):
            print("📦 Vectorstore not found or empty. Running ingestion...")
            ingest_pdfs()
        else:
            print("✅ Using existing vectorstore.")

        print("📥 Loading vectorstore...")
        vectordb = load_vectorstore()

        print("🔍 Setting up retriever...")
        retriever = get_retriever(vectordb)

        print("🤖 Building RAG chain...")
        rag_chain = build_rag_chain(retriever)

        print("\n🎉 System ready! You can now ask questions about your NCERT content.")
        print("💡 Type 'exit' to quit, 'help' for commands")
        
        while True:
            try:
                query = input("\n❓ Ask a question: ").strip()
                
                if not query:
                    continue
                    
                if query.lower() in ['exit', 'quit', 'q']:
                    print("👋 Goodbye!")
                    break
                    
                if query.lower() == 'help':
                    print("\n📖 Available commands:")
                    print("  • Type any question about your NCERT content")
                    print("  • 'exit', 'quit', or 'q' to quit")
                    print("  • 'help' to show this message")
                    continue

                print("🤔 Thinking...")
                result = rag_chain.invoke(query)
                print(f"\n📘 Answer:\n{result}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error processing query: {str(e)}")
                print("Please try again with a different question.")

    except Exception as e:
        print(f"❌ Application error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
