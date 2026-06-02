import streamlit as st

def render_metrics():

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2>12</h2>
            <p>Documents</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2>2,540</h2>
            <p>Knowledge Chunks</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2>1.2s</h2>
            <p>Response Time</p>
        </div>
        """, unsafe_allow_html=True)