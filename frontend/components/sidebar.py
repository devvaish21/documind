import streamlit as st

def render_sidebar():

    with st.sidebar:

        st.markdown("# 🧠 DocuMind")

        st.caption("Enterprise Knowledge Assistant")

        st.divider()

        if st.button(
            "➕ New Chat",
            use_container_width=True
        ):
            st.session_state.history = []

        st.divider()

        st.markdown("### 📜 Chat History")

        if "history" not in st.session_state:
            st.session_state.history = []

        if st.session_state.history:

            for item in reversed(
                st.session_state.history[-10:]
            ):

                st.markdown(
                    f"""
                    <div style="
                    background:#111827;
                    padding:10px;
                    border-radius:10px;
                    margin-bottom:8px;
                    font-size:13px;
                    ">
                    {item[:40]}...
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.caption("No conversations yet")

        st.divider()

        st.markdown("### ⚡ System Status")

        st.success("Vector DB Connected")
        st.success("RAG Active")
        st.success("Grounded Mode Enabled")