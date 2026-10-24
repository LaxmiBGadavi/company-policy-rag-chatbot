"""Retrieval-augmented question answering with optional local Ollama generation."""
import requests
from chunk_policy import extract_text, chunk_text
from vector_store import build_index, search

def load_and_index_documents(documents):
    all_chunks = []
    for document in documents:
        name = document["name"]
        text = extract_text(name, document["bytes"])
        if not text:
            continue
        for idx, chunk in enumerate(chunk_text(text)):
            all_chunks.append({
                "name": name,
                "chunk_id": idx + 1,
                "text": chunk
            })
    return build_index(all_chunks)

def _ollama_answer(question, contexts, model):
    context_text = "\n\n".join(
        f"Source: {item['name']} (chunk {item['chunk_id']})\n{item['text']}"
        for item in contexts
    )
    prompt = (
        "You are a careful company policy assistant. Answer only from the context below. "
        "If the answer is not in the context, say you could not find it in the uploaded policies. "
        "Do not invent rules. Keep the answer clear and concise.\n\n"
        f"CONTEXT:\n{context_text}\n\nQUESTION: {question}\n\nANSWER:"
    )
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=90
    )
    response.raise_for_status()
    return response.json().get("response", "").strip()

def answer_question(question, index, use_ollama=False, ollama_model="llama3.2"):
    contexts = search(index, question, top_k=4)
    if not contexts:
        return {
            "answer": "I couldn't find a relevant answer in the uploaded policy documents. Try using different keywords or upload the correct policy file.",
            "sources": []
        }

    if use_ollama:
        try:
            answer = _ollama_answer(question, contexts, ollama_model)
            if answer:
                return {"answer": answer, "sources": contexts}
        except requests.RequestException:
            pass

    excerpts = "\n\n".join(
        f"**{item['name']} — chunk {item['chunk_id']}**\n\n> {item['text']}"
        for item in contexts
    )
    answer = (
        "I found these relevant passages in your uploaded policy documents. "
        "Review the excerpts below to confirm the exact rule:\n\n" + excerpts +
        "\n\n*Note: This fallback retrieves relevant text; it does not generate a paraphrased answer. "
        "For conversational answers, enable Ollama in the sidebar and make sure the selected local model is running.*"
    )
    return {"answer": answer, "sources": contexts}
