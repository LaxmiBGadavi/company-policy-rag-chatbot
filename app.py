import streamlit as st
from pathlib import Path
from rag_chain import answer_question, load_and_index_documents

st.set_page_config(page_title="Company Policy Assistant", page_icon="📚", layout="wide")

st.title("📚 Company Policy Assistant")
st.caption("Ask questions about company policies. Upload PDF or TXT files, then get answers grounded in the uploaded documents.")

with st.sidebar:
    st.header("1. Add policy documents")
    uploaded_files = st.file_uploader(
        "Upload policy documents (PDF or TXT)",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )
    st.divider()
    st.header("2. Answer mode")
    use_ollama = st.checkbox(
        "Use local Ollama LLM if available",
        value=False,
        help="Optional. Install and run Ollama locally and pull a model, for example: ollama pull llama3.2"
    )
    ollama_model = st.text_input("Ollama model", value="llama3.2", disabled=not use_ollama)
    st.caption("No API key is required. Without Ollama, the app returns relevant policy excerpts.")

if "indexed_docs" not in st.session_state:
    st.session_state.indexed_docs = None
if "index_signature" not in st.session_state:
    st.session_state.index_signature = None
if "messages" not in st.session_state:
    st.session_state.messages = []

if uploaded_files:
    signature = tuple((f.name, f.size) for f in uploaded_files)
    if st.session_state.index_signature != signature:
        try:
            docs = []
            for f in uploaded_files:
                raw = f.getvalue()
                docs.append({"name": f.name, "bytes": raw})
            st.session_state.indexed_docs = load_and_index_documents(docs)
            st.session_state.index_signature = signature
            st.session_state.messages = []
        except Exception as exc:
            st.error(f"Could not process the uploaded documents: {exc}")
            st.stop()
    st.success(f"Ready to search {len(st.session_state.indexed_docs['chunks'])} text chunks from {len(uploaded_files)} document(s).")
else:
    st.session_state.indexed_docs = None
    st.session_state.index_signature = None
    st.info("Upload one or more policy PDF/TXT files in the sidebar to begin.")
    sample_path = Path("data/sample_company_policy.txt")
    if sample_path.exists():
        with st.expander("Preview included sample policy"):
            st.text(sample_path.read_text(encoding="utf-8"))

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Ask a question, e.g. How many sick leave days are allowed?")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    if not st.session_state.indexed_docs:
        response = "Please upload at least one company policy PDF or TXT file first."
    else:
        with st.chat_message("assistant"):
            with st.spinner("Searching policy documents..."):
                result = answer_question(
                    question,
                    st.session_state.indexed_docs,
                    use_ollama=use_ollama,
                    ollama_model=ollama_model
                )
            st.markdown(result["answer"])
            if result.get("sources"):
                with st.expander("Sources"):
                    for source in result["sources"]:
                        st.markdown(f"**{source['name']}** — chunk {source['chunk_id']}")
                        st.write(source["text"])
        st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
        st.stop()

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
