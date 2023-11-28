import streamlit as st

st.title("Korea vs EUW")

with st.sidebar:
    st.selectbox("Analytics", options=["Mentality Check", "In game", "Out of game", "Funny", "Educational"])

st.write("Hello")
