from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pypdf
import io

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

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes
     # Read the file contents into memory
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
         status_code=400,
         detail="File too large. Maximum size is 10MB"
    )
    # Check if the uploaded file is a PDF
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
   
    
    # Open the PDF using pypdf
    pdf_reader = pypdf.PdfReader(io.BytesIO(contents))
    
    # Extract text from every page
    extracted_text = ""
    for page in pdf_reader.pages:
        extracted_text += page.extract_text()
    
    # Return the result
    return {
        "filename": file.filename,
        "pages": len(pdf_reader.pages),
        "text": extracted_text
    }