import streamlit as st
import requests

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="DocuMind Enterprise",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# LOAD CSS
# ---------------------------------------------------

with open("styles/main.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.markdown("""
    <div class="sidebar-logo">
        🧠 <span>DocuMind Enterprise</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

   
    st.markdown("### 📂 Upload Documents")

    uploaded_file = st.file_uploader(
        "Upload your PDF",
        type=["pdf"]
    )

    if uploaded_file:
        with st.spinner("Indexing PDF..."):
            response = requests.post(
                "http://127.0.0.1:8000/upload",
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf"
                    )
                }
            )

            if response.status_code == 200:
                st.success("PDF Indexed Successfully")
            else:
                st.error("Upload Failed")

    st.markdown("---")

    st.markdown("### 📊 Workspace")

    st.markdown("""
    📄 Documents Indexed: 12

    💾 Storage Used: 84 MB

    🧠 Embeddings Ready

    ⚡ FastAPI Connected
    """)

    st.markdown("---")

    st.markdown("### ✨ Features")

    st.markdown("""
    ✅ Semantic Search

    ✅ Multi PDF Support

    ✅ AI-Powered Answers

    ✅ Context Aware RAG

    ✅ ChromaDB Storage
    """)

    st.markdown("---")

    st.markdown("### 🕒 Recent Activity")

    st.markdown("""
    • HR Policy.pdf

    • Employee Handbook.pdf

    • Refund Policy.pdf

    • Leave Policy.pdf
    """)

# ---------------------------------------------------
# HERO SECTION
# ---------------------------------------------------

st.markdown("""
<div class="hero-card">

<h1 class="main-title">
🧠 DocuMind Enterprise
</h1>

<p class="subtitle">
Enterprise AI-Powered Knowledge Intelligence Platform
</p>

<div class="feature-badges">
    <span>🚀 Search</span>
    <span>📄 Summarize</span>
    <span>🧠 Analyze</span>
    <span>⚡ Retrieve</span>
    <span>🔒 Secure AI</span>
</div>

<br>

<h3 style="color:white;">
Transform  Documents Into Instant Answers
</h3>

<p style="
color:#94A3B8;
font-size:18px;
max-width:900px;
margin:auto;
line-height:1.8;
">
Upload PDFs, create embeddings, perform semantic search,
and get context-aware AI answers in seconds using
FastAPI, LangChain, ChromaDB and Streamlit.
</p>

</div>
""", unsafe_allow_html=True)
# KPI DASHBOARD

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="metric-card">
        <h2>📄</h2>
        <h1>25+</h1>
        <p>Documents Indexed</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="metric-card">
        <h2>⚡</h2>
        <h1>98%</h1>
        <p>Accuracy</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="metric-card">
        <h2>🧠</h2>
        <h1>RAG</h1>
        <p>Context Aware</p>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="metric-card">
        <h2>🔒</h2>
        <h1>100%</h1>
        <p>Secure Search</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="status-card">
🟢 AI Service Online<br>
📦 ChromaDB Connected<br>
⚡ FastAPI Running<br>
🧠 Embeddings Loaded
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------
# WELCOME SCREEN
# ---------------------------------------------------

if len(st.session_state.messages) == 0:

    st.markdown("""
    <div class="welcome-card">
        <h2>👋 Welcome to DocuMind Enterprise</h2>

        
        Upload company documents and ask questions instantly using AI-powered semantic search.
      
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="example-section">

<h2>Example Questions</h2>

<div class="question-item">📄 What is the refund policy?</div>

<div class="question-item">🚀 Summarize onboarding process</div>

<div class="question-item">📝 Explain leave policy</div>

<div class="question-item">💰 What are employee benefits?</div>

<div class="question-item">📑 Summarize this PDF</div>

<div class="question-item">🔍 Explain section 5 of the document</div>

</div>
""", unsafe_allow_html=True)
# ---------------------------------------------------
# DISPLAY CHAT
# ---------------------------------------------------

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(f"""
        <div class="user-message">
            👤 {message["content"]}
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown(f"""
        <div class="chat-bot">
            🤖 {message["content"]}
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------

prompt = st.chat_input("Ask anything about your documents...")

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    try:

        with st.spinner("DocuMind is thinking..."):

            response = requests.post(
                "http://127.0.0.1:8000/ask",
                json={
                    "question": prompt
                }
            )

            answer = response.json()["answer"]

    except:
        answer = "Backend server is not running."

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("""
<div class="footer">

<h3>DocuMind Enterprise v1.0</h3>

🚀 FastAPI • 🧠 LangChain • 📦 ChromaDB • 🎨 Streamlit

<br><br>

Developed by Tejas , Vaishnavi & Ishwarya

</div>
""", unsafe_allow_html=True)