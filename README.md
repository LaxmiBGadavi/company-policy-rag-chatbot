# 📚 Company Policy RAG Chatbot

An AI-powered **Company Policy Chatbot** built with Python and Streamlit that helps users find relevant information from company policy documents. It uses Retrieval-Augmented Generation (RAG) concepts to retrieve relevant passages from uploaded PDF and TXT documents, with optional local LLM integration.

## 🚀 Features

- **Interactive Streamlit UI** — Simple chat interface for asking policy-related questions.
- **Document Upload** — Upload company policy documents in PDF or TXT format.
- **Text Extraction** — Extract text from uploaded documents.
- **Text Chunking** — Split policy documents into smaller, overlapping chunks.
- **Semantic-style Retrieval** — Use TF-IDF vectorization and cosine similarity to find relevant policy passages.
- **Source References** — Display the source document and relevant text chunks.
- **Optional Local LLM** — Integrate Ollama for conversational answers without a cloud API key.
- **Privacy-Friendly Processing** — Process uploaded documents locally within the running application.

## 🛠️ Technologies Used

- Python
- Streamlit
- LangChain concepts / RAG architecture
- TF-IDF Vectorization
- Scikit-learn
- Cosine Similarity
- PyPDF

## 📂 Project Structure

```text
company-policy-rag-chatbot/
│
├── app.py
├── chunk_policy.py
├── vector_store.py
├── rag_chain.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/
    └── sample_company_policy.txt
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/LaxmiBGadavi/company-policy-rag-chatbot.git
cd company-policy-rag-chatbot
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application

```bash
streamlit run app.py
```

The application will open in your browser. Upload a policy document through the sidebar and ask questions in the chat interface.

## 🧠 How It Works

1. **Upload Documents:** The user uploads company policy documents in PDF or TXT format.
2. **Extract Text:** The application extracts readable text from the documents.
3. **Chunk Documents:** The text is split into smaller chunks with overlapping context.
4. **Build the Retrieval Index:** TF-IDF converts text chunks into numerical vectors.
5. **Retrieve Relevant Context:** Cosine similarity ranks passages related to the user's question.
6. **Generate or Display Answers:** The application displays relevant policy excerpts by default or optionally uses a local Ollama model to generate a conversational answer.
7. **Show Sources:** The retrieved document names and text chunks are available for reference.

## 💬 Example Questions

- How many casual leave days are allowed?
- What is the sick leave policy?
- Can employees work from home?
- What should an employee do if a company laptop is damaged?
- What are the standard working hours?

Answers depend on the contents of the documents uploaded by the user.


## 🔐 Privacy and Security

- Do not upload confidential company policies to a public GitHub repository.
- Never commit API keys, passwords, or `.env` files.
- Uploaded documents are processed by the running application.
- When using Ollama, the configured local model generates answers on your machine.

## ⚠️ Limitations

- TF-IDF retrieval is based on word and phrase matching; it is not a transformer-based semantic embedding model.
- The default mode retrieves relevant passages rather than generating a fully paraphrased answer.
- Scanned PDFs may require OCR before text can be extracted.
- Answer quality depends on document quality and the selected retrieval results.
- The optional Ollama integration requires Ollama and the selected model to be installed and running locally.

## 🔮 Future Enhancements

- Replace TF-IDF with embedding-based semantic retrieval.
- Integrate a persistent vector database such as ChromaDB.
- Add conversation memory and chat history.
- Support DOCX documents.
- Add document citations with page numbers.
- Deploy the application using Streamlit Community Cloud or another hosting platform.

## 👩‍💻 Author

**Laxmi Gadavi**
