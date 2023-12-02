import streamlit as st

st.title("Noway EUW")

with st.sidebar:
    st.selectbox("Analytics", options=["In game", "Out of game", "Funny", "Educational"])

st.write("Hello")
