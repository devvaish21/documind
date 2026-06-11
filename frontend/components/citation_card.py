import streamlit as st

def render_citation():

    st.markdown("""
    <div class="citation-card">

        <strong>📄 Source Document</strong><br><br>

        File: Uploaded PDF<br>
        Confidence: 96%<br>
        Retrieved from enterprise knowledge base.

    </div>
    """, unsafe_allow_html=True)