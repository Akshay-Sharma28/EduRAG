from langchain_community.vectorstores import Chroma
from .embed import get_embedder
from pathlib import Path

VECTORSTORE_DIR = Path("./docs")

def create_vectorstore(split_docs):
    embedder = get_embedder()
    print(f"✅ Creating vectorstore with {len(split_docs)} document(s)")
    vectorstore = Chroma.from_documents(
        documents=split_docs,
        embedding=embedder,
        persist_directory=str(VECTORSTORE_DIR)
    )
    vectorstore.persist()
    print(f"✅ Vectorstore persisted to {VECTORSTORE_DIR.resolve()}")

def load_vectorstore():
    if not VECTORSTORE_DIR.exists():
        raise FileNotFoundError(f"Vectorstore directory {VECTORSTORE_DIR} does not exist. Please ingest first.")
    print(f"✅ Loading vectorstore from {VECTORSTORE_DIR.resolve()}")
    return Chroma(
        embedding_function=get_embedder(),
        persist_directory=str(VECTORSTORE_DIR)
    )
