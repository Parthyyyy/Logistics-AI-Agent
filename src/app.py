import streamlit as st
import os
from src.agent import run_agent
from src.vector_store import build_vector_store

st.set_page_config(page_title="Agentic Logistics Platform", page_icon="🚢", layout="wide")
st.title("🚢 Enterprise Agentic AI Platform")
st.markdown("Ask logistics questions. The Agent will decide whether to search internal PDFs or browse the live web!")

# Sidebar for Document Management
with st.sidebar:
    st.header("⚙️ Admin & Data Management")
    uploaded_files = st.file_uploader("Upload Logistics PDFs", type=["pdf"], accept_multiple_files=True)
    
    if st.button("Rebuild Vector Database"):
        with st.spinner("Processing documents..."):
            if uploaded_files:
                os.makedirs("data", exist_ok=True)
                for uf in uploaded_files:
                    with open(os.path.join("data", uf.name), "wb") as f:
                        f.write(uf.getbuffer())
            build_vector_store()
            st.success("Database updated successfully!")

# Main Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages =[]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a supply chain or logistics question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Agent is reasoning and searching tools..."):
            response = run_agent(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})