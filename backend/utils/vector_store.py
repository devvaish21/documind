from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

PERSIST_DIR = "./vectorstore"

def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

def create_vector_store(chunks):
    print("Creating ChromaDB vector store with HuggingFace embeddings...")
    embed_model = get_embedding_model()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embed_model,
        persist_directory=PERSIST_DIR
    )
    print(f"Stored {vectorstore._collection.count()} chunks in ChromaDB")
    return vectorstore

def load_vector_store():
    embed_model = get_embedding_model()
    return Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embed_model
    )

def get_relevant_chunks(query: str, k: int = 5):
    """
    Main function Person 1 (FastAPI) will call.
    Input:  query string, k = number of results to return
    Output: list of Document objects with .page_content and .metadata
    """
    vs = load_vector_store()
    results = vs.similarity_search(query, k=k)
    return results

def verify_storage():
    import chromadb
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    collections = client.list_collections()
    print(f"Collections: {[c.name for c in collections]}")
    for col in collections:
        print(f"  {col.name}: {col.count()} chunks stored")
        sample = col.peek(1)
        print(f"  Metadata: {sample['metadatas'][0]}")
        print(f"  Preview:  {sample['documents'][0][:100]}")

if __name__ == "__main__":
    from utils.pdf_loader import load_pdf
    from utils.chunker import split_documents
    docs = load_pdf("data/sample.pdf")
    chunks = split_documents(docs)
    vs = create_vector_store(chunks)
    print("ChromaDB setup complete!")
    print("\n--- Verifying storage ---")
    verify_storage()