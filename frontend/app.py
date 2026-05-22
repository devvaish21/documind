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

with open("frontend/style.css") as f:
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
        🧠 <span>DocuMind</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Upload Documents")

    uploaded_file = st.file_uploader(
        "Upload your PDF",
        type=["pdf"]
    )

    if uploaded_file:
        with st.spinner("Indexing PDF..."):
            response = requests.post(
                "http://127.0.0.1:8000/upload",
                 files={"file": (uploaded_file.name, uploaded_file.getvalue(),"application/pdf")}
            )
            if response.status_code == 200:
                st.success(f"{uploaded_file.name} uploaded and indexed!")
            else:
                st.error("Upload failed!")

    st.markdown("---")

    st.markdown("### Features")

    st.markdown("""
    ✅ Semantic Search  
    ✅ Multi PDF Support  
    ✅ AI-Powered Answers  
    ✅ Context Aware RAG  
    """)

    st.markdown("---")

    st.markdown("### Recent Chats")

    st.markdown("""
    - Refund Policy  
    - Employee Leave SOP  
    - HR Guidelines  
    """)

# ---------------------------------------------------
# HERO SECTION
# ---------------------------------------------------

st.markdown("""
<div class="hero-container">

<h1 class="main-title">
🧠 DocuMind Enterprise
</h1>

<p class="subtitle">
AI-Powered Enterprise Knowledge Assistant
</p>

<div class="feature-badges">
    <span>⚡ Fast Retrieval</span>
    <span>📄 Multi PDF</span>
    <span>🧠 Context Aware</span>
    <span>🔒 Secure AI</span>
</div>

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

    <h3>Welcome to DocuMind Enterprise</h3>

    <p>
    Upload company documents and ask questions instantly using AI-powered semantic search.
    </p>

    <div class="example-section">
        <p>Example Questions:</p>

        <ul>
            <li>What is the refund policy?</li>
            <li>Summarize onboarding process</li>
            <li>Explain leave policy</li>
            <li>What are employee benefits?</li>
        </ul>
    </div>

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
        <div class="bot-message">
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
Built with FastAPI • LangChain • Streamlit • ChromaDB
</div>
""", unsafe_allow_html=True)