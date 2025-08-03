import os
from pathlib import Path
from src.vectorstore import load_vectorstore
from src.retriever import get_retriever
from src.query_engine import build_rag_chain
from src.ingest import ingest_pdfs

VECTORSTORE_DIR = Path("./docs")

def main():
    # Check for API key early
    if not os.getenv("GEMINI_API_KEY"):
        raise EnvironmentError("❌ GEMINI_API_KEY environment variable is not set.")

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

    while True:
        query = input("\nAsk a question (or type 'exit'): ")
        if query.lower() == "exit":
            print("👋 Exiting.")
            break

        result = rag_chain.invoke({"query": query})
        print("\n📘 Answer:\n", result["result"])

if __name__ == "__main__":
    main()
