import streamlit as st

def load_css(file_name):

    with open(file_name) as f:
        css = f.read()

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )