import streamlit as st


def create_sidebar(text: str, options: list[str]):
    return st.sidebar.selectbox(text, options=options)
