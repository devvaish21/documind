import streamlit as st
import time
from pypdf import PdfReader

from utils.load_css import load_css

from components.sidebar import render_sidebar
from components.header import render_header
from components.metrics import render_metrics
from components.upload_box import render_upload_box
from components.chat_message import user_message
from components.citation_card import render_citation

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="DocuMind Enterprise",
    page_icon="🧠",
    layout="wide"
)

# --------------------------------------------------
# LOAD CSS
# --------------------------------------------------

load_css("styles/main.css")

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

render_sidebar()

# --------------------------------------------------
# HEADER
# --------------------------------------------------

render_header()

st.write("")

# --------------------------------------------------
# METRICS
# --------------------------------------------------

render_metrics()

st.write("")

# --------------------------------------------------
# FEATURES
# --------------------------------------------------

st.markdown("## ✨ Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='feature-card'>
        <h3>📄 Smart PDF Analysis</h3>
        <p>Upload and analyze enterprise PDFs instantly.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='feature-card'>
        <h3>🧠 AI Assistant</h3>
        <p>Ask natural language questions about documents.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='feature-card'>
        <h3>⚡ Fast Search</h3>
        <p>Retrieve relevant information quickly.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# --------------------------------------------------
# UPLOAD SECTION
# --------------------------------------------------

uploaded_file = render_upload_box()

pdf_text = ""

if uploaded_file is not None:

    try:

        reader = PdfReader(uploaded_file)

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pdf_text += text + "\n"

        st.success(
            f"✅ {uploaded_file.name} uploaded successfully"
        )

    except Exception as e:

        st.error(f"Error reading PDF: {e}")

st.write("")

# --------------------------------------------------
# CHAT SECTION
# --------------------------------------------------

st.markdown("## 💬 Enterprise AI Assistant")

prompt = st.chat_input(
    "Ask your enterprise documents..."
)

if prompt:

    user_message(prompt)

    query = prompt.lower()

    if not pdf_text:

        response = "⚠ Please upload a PDF first."

    elif "summary" in query or "summarize" in query:

        response = (
            "📄 PDF Summary\n\n"
            + pdf_text[:2500]
        )

    else:

        lines = pdf_text.split("\n")

        matches = []

        query_words = query.split()

        for line in lines:

            line_lower = line.lower()

            if any(word in line_lower for word in query_words):

                matches.append(line.strip())

        if matches:

            response = "\n\n".join(matches[:10])

        else:

            response = (
                "No relevant information found in the uploaded PDF."
            )

    placeholder = st.empty()

    full_response = ""

    for word in response.split():

        full_response += word + " "

        placeholder.markdown(
            f"""
            <div class='chat-bot'>
                {full_response}▌
            </div>
            """,
            unsafe_allow_html=True
        )

        time.sleep(0.01)

    render_citation()

# --------------------------------------------------
# STATUS CARD
# --------------------------------------------------

st.write("")

st.markdown(
    """
    <div class='status-card'>
        <strong>🛡 Grounded Response Protection Active</strong><br>
        Responses are generated only from uploaded documents.
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

st.caption(
    "DocuMind Enterprise • AI Document Assistant"
)