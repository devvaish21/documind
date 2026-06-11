from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents

if __name__ == "__main__":
    docs = load_pdf("data/sample.pdf")
    print(f"Total pages loaded: {len(docs)}")
    print("\n--- Page 1 content preview ---")
    print(docs[0].page_content[:500])
    print("\n--- Metadata ---")
    print(docs[0].metadata)
    