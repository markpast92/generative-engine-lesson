import streamlit as st
from engine import reply
from extractor import extract_text

st.set_page_config(page_title="Chat Bot", layout="wide")

st.title("💬 Chat Bot")

with st.sidebar:
    st.header("📁 Knowledge Base")
    uploaded_files = st.file_uploader(
        "Carica PDF, DOCX o XLSX",
        type=["pdf", "docx", "xlsx"],
        accept_multiple_files=True
    )
    
    knowledge_base = ""
    if uploaded_files:
        st.info(f"📄 {len(uploaded_files)} file caricati")
        for uploaded_file in uploaded_files:
            file_bytes = uploaded_file.read()
            extracted_text = extract_text(file_bytes, uploaded_file.name)
            knowledge_base += f"\n--- {uploaded_file.name} ---\n{extracted_text}\n"
        
        with st.expander("Visualizza Knowledge Base"):
            st.text_area("Contenuto estratto:", knowledge_base, height=300, disabled=True)
    else:
        knowledge_base = ""

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
        response = reply(prompt, st.session_state.messages, knowledge_base)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})