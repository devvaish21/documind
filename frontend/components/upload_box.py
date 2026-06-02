import streamlit as st

def render_upload_box():

    st.markdown(
        """
        <div class="upload-card">
            <h2>📁 Upload Enterprise Documents</h2>
            <p class="small-text">
                Drag & Drop SOPs, HR Policies,
                Employee Manuals and Enterprise PDFs.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    return st.file_uploader(
        "",
        type=["pdf"],
        key="main_pdf_upload",
        label_visibility="collapsed"
    )