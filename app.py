import streamlit as st
from engine import reply

st.set_page_config(page_title="Chat Bot", layout="wide")

st.title("💬 Chat Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Scrivi il tuo messaggio..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = reply(prompt, st.session_state.messages)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})