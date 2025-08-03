from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from .vectorstore import create_vectorstore
import sys

PDF_DIR = Path("./data")

def ingest_pdfs():
    pdf_paths = list(PDF_DIR.glob("*.pdf"))
    print(f"✅ Found {len(pdf_paths)} PDF(s) in {PDF_DIR.resolve()}")
    if not pdf_paths:
        print("❌ No PDFs found. Aborting ingestion.")
        sys.exit(1)

    docs = []
    for pdf_path in pdf_paths:
        loader = PyPDFLoader(str(pdf_path))
        pdf_docs = loader.load()
        print(f"   - Loaded {len(pdf_docs)} page(s) from {pdf_path.name}")
        docs.extend(pdf_docs)
    if not docs:
        print("❌ No content loaded from PDFs. Aborting ingestion.")
        sys.exit(1)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    split_docs = text_splitter.split_documents(docs)
    print(f"✅ Split into {len(split_docs)} chunk(s)")

    create_vectorstore(split_docs)
    print("✅ Ingestion and vectorstore persistence complete.")
