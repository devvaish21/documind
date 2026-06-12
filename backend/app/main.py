from fastapi import FastAPI, UploadFile, File, HTTPException
from functools import lru_cache
from fastapi.middleware.cors import CORSMiddleware
from utils.vector_store import get_relevant_chunks, create_vector_store
from utils.rag_chain import get_answer, reload_vector_store
from utils.chunker import split_documents
import pypdf
import io
import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader

app = FastAPI()

# CORS — allows frontend to talk to our API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────────────────────
# In-Memory Status Tracker
# Tracks the indexing status of each uploaded file
# Format: { "filename.pdf": "indexing" | "ready" | "failed" }
# ──────────────────────────────────────────────

indexing_status: dict[str, str] = {}


# ──────────────────────────────────────────────
# Background Task: Index the PDF
# This runs AFTER the response is sent to the user
# ──────────────────────────────────────────────

async def index_pdf_background(tmp_path: str, filename: str, expected_pages: int):
    """
    Runs in the background after /upload returns.
    Loads, chunks, and indexes the PDF into ChromaDB.
    Updates indexing_status when done or if it fails.
    """
    try:
        indexing_status[filename] = "indexing"

        loader = PyPDFLoader(tmp_path)
        docs = loader.load()

        if len(docs) == 0:
            indexing_status[filename] = "failed: PDF has no pages"
            return

        chunks = split_documents(docs)
        create_vector_store(chunks)
        reload_vector_store()
        indexing_status[filename] = "ready"

    except Exception as e:
        indexing_status[filename] = f"failed: {str(e)}"

    finally:
        # Always clean up the temp file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


# ──────────────────────────────────────────────
# Cached Search
# Prevents hitting ChromaDB repeatedly for the same question
# Cache holds up to 100 unique questions in memory
# ──────────────────────────────────────────────

@lru_cache(maxsize=100)
def cached_search(question: str):
    """
    Wraps get_relevant_chunks with an LRU cache.
    If the same question is asked again, returns the cached result instantly.
    """
    results = get_relevant_chunks(question, k=5)
    # lru_cache needs a hashable return value, so we extract text here
    return [doc.page_content for doc in results]


# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────

@app.get("/")
def read_root():
    return {"message": "DocuMind backend is alive"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "DocuMind Backend"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB")

    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    # Save to temp file because PyPDFLoader needs a file path
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        # Load and chunk the PDF
        loader = PyPDFLoader(tmp_path)
        docs = loader.load()

        if len(docs) == 0:
            raise HTTPException(status_code=400, detail="PDF has no pages")

        chunks = split_documents(docs)

        # Index into ChromaDB
        create_vector_store(chunks)
        # Refresh in-memory retriever so /ask uses the new PDF
        reload_vector_store()
        cached_search.cache_clear()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")
    finally:
        os.unlink(tmp_path)  # Always delete temp file

    return {
        "filename": file.filename,
        "pages": len(docs),
        "chunks": len(chunks),
        "status": "Successfully indexed into ChromaDB"
    }

@app.post("/ask")
async def ask_question(payload: dict):
    question = payload.get("question", "")
    if not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    answer = get_answer(question)
    return {"answer": answer}