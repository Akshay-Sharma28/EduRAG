from .config import RETRIEVAL_K

def get_retriever(vectorstore, k=None):
    if k is None:
        k = RETRIEVAL_K
    return vectorstore.as_retriever(search_kwargs={"k": k})
