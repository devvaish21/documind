import os
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from utils.vector_store import load_vector_store

load_dotenv()

# ✅ Load ONCE when server starts
print("Loading vector store...")
_vs = load_vector_store()
_retriever = _vs.as_retriever(search_kwargs={"k": 5})
print("Vector store ready! ⚡")

# ✅ Load LLM once
_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# ✅ Strict context-only prompt
_prompt = PromptTemplate.from_template("""
You are a helpful assistant for a company.
Answer the question using ONLY the context provided below.
Do NOT use any outside knowledge.
If the answer is not found in the context, say exactly:
"I don't know based on the document."

Context: {context}

Question: {question}

Answer:""")

# ✅ Build chain once
_chain = (
    {"context": _retriever, "question": RunnablePassthrough()}
    | _prompt
    | _llm
    | StrOutputParser()
)

def get_answer(query: str) -> str:
    """
    Called by backend for every question.
    Uses preloaded model — no reloading, no lag!
    """
    answer = _chain.invoke(query)
    answer = re.sub(r'<[^>]+>', '', answer)
    answer = answer.strip()
    return answer

def reload_vector_store():
    """
    Call this ONLY after a new PDF is uploaded and indexed.
    Refreshes retriever without restarting server.
    """
    global _vs, _retriever, _chain
    print("Reloading vector store with new documents...")
    _vs = load_vector_store()
    _retriever = _vs.as_retriever(search_kwargs={"k": 5})
    _chain = (
        {"context": _retriever, "question": RunnablePassthrough()}
        | _prompt
        | _llm
        | StrOutputParser()
    )
    print("Vector store reloaded! ⚡")

if __name__ == "__main__":
    response = get_answer("What is this document about?")
    print(response)