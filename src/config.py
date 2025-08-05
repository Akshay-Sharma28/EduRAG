import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", 5))
EMBEDDING_MODEL_NAME = "models/embedding-001"
LLM_MODEL_NAME = "models/gemini-1.5-flash-latest"
