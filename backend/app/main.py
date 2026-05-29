from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from utils.rag_chain import get_answer
from utils.vector_store import create_vector_store
from utils.chunker import split_documents
from langchain_community.document_loaders import PyPDFLoader
import aiofiles
import tempfile
import os
import time
from functools import lru_cache

# ──────────────────────────────────────────────
# App Setup
# ──────────────────────────────────────────────

app = FastAPI()

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
async def upload_pdf(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    """
    1. Validates the uploaded file (type, size, empty check)
    2. Saves it asynchronously using aiofiles (non-blocking)
    3. Immediately returns a response with job status
    4. Kicks off background indexing AFTER the response is sent
    """
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    # ── Validation ──
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB")

    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    # ── Async File Save ──
    # aiofiles writes the file without blocking the server
    # Other requests can be handled while this write happens
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".pdf")
    os.close(tmp_fd)  # close the OS-level file descriptor before aiofiles opens it

    async with aiofiles.open(tmp_path, 'wb') as f:
        await f.write(contents)

    # ── Mark as queued ──
    indexing_status[file.filename] = "queued"

    # ── Fire background task ──
    # This runs AFTER this function returns the response below
    background_tasks.add_task(
        index_pdf_background,
        tmp_path,
        file.filename,
        0  # page count unknown until background task loads it
    )

    # ── Return immediately ✅ ──
    # User doesn't wait for indexing to finish
    return {
        "filename": file.filename,
        "status": "queued",
        "message": "PDF received. Indexing started in background. Poll /status/{filename} to check progress."
    }


@app.get("/status/{filename}")
def get_status(filename: str):
    """
    Frontend polls this endpoint to check if a PDF has been indexed.
    Returns one of: queued | indexing | ready | failed
    """
    status = indexing_status.get(filename)

    if status is None:
        raise HTTPException(status_code=404, detail="No record found for this filename. Was it uploaded?")

    return {
        "filename": filename,
        "status": status,
        "ready": status == "ready"
    }


@app.post("/ask")
async def ask_question(payload: dict):
    """
    Answers a question using relevant chunks from ChromaDB.
    Uses LRU cache — repeated questions are answered instantly from memory.
    """
    question = payload.get("question", "").strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    # ── Cache check happens here ──
    # If this exact question was asked before, returns instantly
    chunks = cached_search(question)

    if not chunks:
        return {"answer": "I could not find relevant information in the uploaded document."}

    answer = "\n\n".join(chunks)
    return {"answer": answer}


@app.delete("/cache/clear")
def clear_cache():
    """
    Clears the question cache. Useful if a new PDF is uploaded
    and you want fresh answers instead of cached old ones.
    """
    cached_search.cache_clear()
    return {"message": "Cache cleared successfully"}


@app.get("/status/all")
def get_all_statuses():
    """
    Returns the indexing status of all uploaded files.
    Useful for debugging during development.
    """
    return {"files": indexing_status}
