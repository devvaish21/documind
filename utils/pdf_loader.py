from langchain_community.document_loaders import PyPDFLoader
import os

def load_pdf(file_path: str):
    """
    Loads PDF from given path.
    Returns list of Document objects (one per page).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF not found at: {file_path}")
    
    print(f"Loading PDF: {file_path}")
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages ✅")
    return documents

if __name__ == "__main__":
    docs = load_pdf("data/sample.pdf")
    print(f"Total pages loaded: {len(docs)}")
    print("\n--- Page 1 content preview ---")
    print(docs[0].page_content[:500])
    print("\n--- Metadata ---")
    print(docs[0].metadata)