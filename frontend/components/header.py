import streamlit as st

def render_header():

    st.markdown(
        """
        <div class="hero-card">

            <div style="font-size:65px;text-align:center;">
                🚀
            </div>

            <h1 style="
                text-align:center;
                font-size:56px;
                font-weight:800;
                color:white;
                margin-top:10px;
            ">
                DocuMind Enterprise
            </h1>

            <p style="
                text-align:center;
                color:#B8C1D1;
                font-size:18px;
                margin-top:15px;
                line-height:1.8;
            ">
                AI-powered enterprise document assistant.<br>
                Upload PDFs, search instantly, generate summaries,
                and chat with your documents in real time.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )