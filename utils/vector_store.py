from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

PERSIST_DIR = "./vectorstore"

# ✅ Load embedding model ONCE — cached here
print("Initializing HuggingFace embedding model...")
_embed_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
print("Embedding model loaded! ⚡")

def get_embedding_model():
    """Returns the already-loaded embedding model — no reloading!"""
    return _embed_model

def create_vector_store(chunks):
    """
    Called ONLY when a new PDF is uploaded.
    Creates and saves ChromaDB from document chunks.
    """
    print("Creating ChromaDB vector store...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=_embed_model,
        persist_directory=PERSIST_DIR
    )
    print(f"Stored {vectorstore._collection.count()} chunks in ChromaDB ✅")
    return vectorstore

def load_vector_store():
    """
    Called at server startup and after new PDF upload.
    Loads existing ChromaDB from disk — fast since model is cached.
    """
    return Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=_embed_model
    )

def get_relevant_chunks(query: str, k: int = 5):
    """
    Returns list of Document objects with .page_content and .metadata
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