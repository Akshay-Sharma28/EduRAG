from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from .config import GEMINI_API_KEY, LLM_MODEL_NAME

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def build_rag_chain(retriever):
    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL_NAME,
        google_api_key=GEMINI_API_KEY,
        temperature=0.3
    )

    prompt = ChatPromptTemplate.from_template("""
You are an expert tutor specialized in NCERT textbooks for school students.
Use only the provided context from NCERT books to answer the question as clearly and accurately as possible.
If the answer is not in the context, say "I couldn't find that in the NCERT content provided."

Context:
{context}

Question: {query}

Answer:
""")

    chain = (
        {"context": retriever | format_docs, "query": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain
