import streamlit as st
import requests

# Page config
st.set_page_config(
    page_title="DocuMind Enterprise",
    page_icon="📄",
    layout="wide"
)

# Title
st.title("📄 DocuMind Enterprise")
st.caption("AI-Powered SOP Assistant")

# Sidebar
st.sidebar.header("Upload PDF")

uploaded_file = st.sidebar.file_uploader(
    "Choose PDF file",
    type=["pdf"]
)

if uploaded_file:
    st.sidebar.success(f"{uploaded_file.name} uploaded successfully!")

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
prompt = st.chat_input("Ask something about your document...")

if prompt:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # Backend API call
    try:
        with st.spinner("Thinking..."):

            response = requests.post(
                "http://127.0.0.1:8000/ask",
                json={
                    "question": prompt
                }
            )

            answer = response.json()["answer"]

    except:
        answer = "Backend server is not running."

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    # Display assistant response
    with st.chat_message("assistant"):
        st.write(answer)