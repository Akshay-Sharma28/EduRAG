from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from src.config import GEMINI_API_KEY

def build_rag_chain(retriever):
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-1.5-flash-latest",
        google_api_key=GEMINI_API_KEY,
        temperature=0.3
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an expert tutor specialized in NCERT textbooks for school students.
Use only the provided context from NCERT books to answer the question as clearly and accurately as possible.
If the answer is not in the context, say "I couldn’t find that in the NCERT content provided."

Context:
{context}

Question:
{question}

Answer:
"""
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
