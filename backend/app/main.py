from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils.rag_chain import get_answer
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