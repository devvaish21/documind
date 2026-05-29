import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from utils.vector_store import load_vector_store

load_dotenv()

PERSIST_DIR = "./vectorstore"

def load_vector_store():
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_chroma import Chroma
    embed_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return Chroma(persist_directory=PERSIST_DIR, embedding_function=embed_model)

def get_answer(query: str) -> str:
    vs = load_vector_store()
    retriever = vs.as_retriever(search_kwargs={"k": 5})
    
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )
    
    prompt = PromptTemplate.from_template("""
You are a helpful assistant. Answer the question using only the context below.
If the answer is not in the context, say "I don't know based on the document."

Context: {context}

Question: {question}

Answer:""")
    
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain.invoke(query)

if __name__ == "__main__":
    response = get_answer("What is project one?")
    print(response)