from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_model():
    print("Loading HuggingFace model (downloads ~90MB on first run only)...")
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

def embed_chunks(chunks):
    embed_model = get_embedding_model()
    texts = [c.page_content for c in chunks]
    print(f"Generating embeddings for {len(texts)} chunks...")
    vectors = embed_model.embed_documents(texts)
    print(f"Done! Each vector has {len(vectors[0])} dimensions")
    return vectors

if __name__ == "__main__":
    from utils.pdf_loader import load_pdf
    from utils.chunker import split_documents
    docs = load_pdf("data/sample.pdf")
    chunks = split_documents(docs)
    vectors = embed_chunks(chunks)
    print(f"\nTotal vectors: {len(vectors)}")
    print(f"First 5 values: {vectors[0][:5]}")