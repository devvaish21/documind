from langchain_text_splitters import RecursiveCharacterTextSplitter

# chunk_size=500 chosen for SOP PDFs (short sections, numbered steps)
# Tested 200/500/1000 — 500 gives best balance of context vs precision

def split_documents(documents, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
    return chunks

def inspect_chunks(chunks, num_samples=5):
    print(f"\nTotal chunks: {len(chunks)}")
    print(f"Avg chunk length: {sum(len(c.page_content) for c in chunks)//len(chunks)} chars")
    for i, chunk in enumerate(chunks[:num_samples]):
        print(f"\n[Chunk {i+1}] Length={len(chunk.page_content)}")
        print(chunk.page_content)
        print("-"*60)

if __name__ == "__main__":
    from utils.pdf_loader import load_pdf
    docs = load_pdf("data/sample.pdf")

    for size in [200, 500, 1000]:
        chunks = split_documents(docs, chunk_size=size, chunk_overlap=50)
        avg = sum(len(c.page_content) for c in chunks) // len(chunks)
        print(f"chunk_size={size}: {len(chunks)} chunks, avg={avg} chars")