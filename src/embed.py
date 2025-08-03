from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

def get_embedder():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY environment variable is not set.")
    print("Gemini Embedding Model initialized.")
    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=api_key
    )
