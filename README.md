[README (4).md](https://github.com/user-attachments/files/28911039/README.4.md)
# 🧠 DocuMind Enterprise

**AI-Powered Enterprise Knowledge Assistant**

DocuMind Enterprise is a Retrieval-Augmented Generation (RAG) based corporate knowledge assistant. Upload company documents (PDFs) and instantly get accurate, AI-generated answers — grounded strictly in the document content. Built as an internship project at **Infotact Solutions**.

---

## 📸 Screenshots

**Upload & Index Documents**
![DocuMind Upload](assets/upload-screen.png)
*Upload PDFs, get them indexed instantly — status shown live in the sidebar*

**Ask Questions, Get Answers**
![DocuMind Q&A](assets/qa-screen.png)
*Query your documents in natural language and get context-aware, structured answers*

---

## ✨ Features

- 📄 **PDF Upload** — Upload any company document (handbooks, SOPs, policies, project docs)
- 🔍 **Semantic Search** — Finds relevant information based on meaning, not just keywords
- 🤖 **AI-Powered Answers** — Uses Groq's Llama 3.3 70B model to generate accurate, context-grounded answers
- 🧠 **Context-Aware RAG** — Combines vector retrieval with LLM generation for precise responses
- 🔒 **Grounded Responses** — If information isn't in the document, the system says "I don't know" instead of hallucinating
- ⚡ **Async Backend** — FastAPI with background task processing and async file I/O
- 💾 **Persistent Storage** — Documents remain indexed across sessions using ChromaDB
- 🗑️ **Cache Management** — Automatic cache invalidation on new uploads

---

## 🏗️ Architecture

```
PDF Upload
   ↓
PyPDFLoader (extract text)
   ↓
Text Chunker (LangChain)
   ↓
HuggingFace Embeddings (all-MiniLM-L6-v2)
   ↓
ChromaDB (vector storage)
   ↓
Retriever (top-k similarity search)
   ↓
Groq LLM (llama-3.3-70b-versatile)
   ↓
Answer (returned to user)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit |
| **Backend** | FastAPI |
| **RAG Pipeline** | LangChain |
| **Vector Database** | ChromaDB |
| **Embeddings** | HuggingFace (`all-MiniLM-L6-v2`) |
| **LLM** | Groq (`llama-3.3-70b-versatile`) |
| **Language** | Python 3.14 |
| **Version Control** | Git & GitHub |

---

## 📁 Project Structure

```
documind/
├── backend/
│   └── app/
│       ├── __init__.py
│       └── main.py              # FastAPI app — /upload, /ask endpoints
├── frontend/
│   ├── app.py                   # Streamlit UI
│   ├── styles/
│   │   └── main.css
│   ├── components/
│   ├── assets/
│   └── utils/
├── utils/
│   ├── pdf_loader.py            # Loads & extracts text from PDFs
│   ├── chunker.py               # Splits documents into chunks
│   ├── embedder.py              # Generates embeddings
│   ├── vector_store.py          # ChromaDB storage & retrieval
│   └── rag_chain.py             # RAG pipeline + Groq LLM integration
├── data/                        # Sample PDFs
├── vectorstore/                 # Persisted ChromaDB data
├── screenshots/                 # UI screenshots
├── test_retrieval.py
├── requirements.txt
├── .env                         # API keys (not committed)
├── .gitignore
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/devvaish21/documind.git
cd documind
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Edit .env and fill in your API keys
```

---

## ▶️ Running the Application

Open **two terminals** from the project root:

**Terminal 1 — Start the backend:**
```bash
uvicorn backend.app.main:app --reload
```

**Terminal 2 — Start the frontend:**
```bash
streamlit run frontend/app.py
```

Open your browser at:
```
http://localhost:8501
```

---

## 🚀 Usage

1. Upload a PDF document using the sidebar
2. Wait for **"PDF Indexed Successfully"** confirmation
3. Type your question in the chat box
4. Get an instant, AI-generated answer based on the document content

### Example Questions
- "Can you list down how many projects are there?"
- "What is StatBot Pro?"
- "What is the refund policy?"
- "Summarize the onboarding process"

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/upload` | Upload a document (PDF) |
| `POST` | `/ask` | Ask a question against uploaded documents |
| `GET` | `/documents` | List all uploaded documents |
| `DELETE` | `/documents/{id}` | Delete a document |
| `POST` | `/clear-cache` | Clear the vector store cache |

### Example: Ask a Question

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the onboarding process for new employees?"}'
```

**Response:**
```json
{
  "answer": "According to the onboarding SOP, new employees should...",
  "sources": ["onboarding_sop_v2.pdf"]
}
```

---

## 🐛 Known Limitations

- Generic/broad queries (e.g., "summarize the PDF") may occasionally return "I don't know" if relevant chunks aren't in the top-k retrieval — a known characteristic of vector similarity search
- First-time PDF upload may take longer due to embedding model initialization

---

## 🔮 Future Enhancements

- Multi-language document support
- Voice input for queries
- Multi-document comparison
- Cloud deployment (Render + Streamlit Cloud)
- Slack & Microsoft Teams integration
- User authentication & rate limiting
- Streaming responses

---

## 👥 Team

| Name | Role |
|---|---|
| **Vaishnavi** | Backend — FastAPI endpoints, file handling, async processing |
| **Tejas Sharad Pagar** | Frontend — Streamlit UI, styling, chat interface |
| **Ishwarya** | RAG Pipeline — PDF processing, embeddings, vector store, LLM integration |

**Developed as part of an internship project at Infotact Solutions.**

---

*Built with FastAPI • LangChain • ChromaDB • Streamlit • Groq*
