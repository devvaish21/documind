import streamlit as st


def user_message(message):
    st.markdown(
        f"""
        <div class='chat-user'>
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )



def bot_message(message):
    st.markdown(
        f"""
        <div class='chat-bot'>
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )