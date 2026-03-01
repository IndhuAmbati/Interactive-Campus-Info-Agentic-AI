import streamlit as st
from backend.ingest import load_vectorstore, query_vectorstore

st.set_page_config(page_title="Campus Info Chatbot")
st.title("Campus Info Chatbot — Track A (Scaffold)")

with st.sidebar:
    st.header("Setup")
    index_path = st.text_input("Vectorstore path", "faiss_index")
    llm_provider = st.selectbox("LLM Provider", ["openai"])

if "messages" not in st.session_state:
    st.session_state.messages = []

query = st.text_input("Ask about campus (e.g. 'Where is the placement cell?')")

if st.button("Send") and query.strip():
    with st.spinner("Searching campus knowledge..."):
        vs = load_vectorstore(index_path)
        answer = query_vectorstore(vs, query)
        st.session_state.messages.append((query, answer))

for q,a in reversed(st.session_state.messages):
    st.markdown(f"**Q:** {q}")
    st.markdown(f"**A:** {a}")

st.markdown("---")
st.markdown("This is a scaffold — add your ingestion pipeline and LLM keys.")
