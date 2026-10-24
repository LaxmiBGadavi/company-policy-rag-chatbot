"""Lightweight local TF-IDF retrieval index; does not need an API key."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def build_index(chunks):
    if not chunks:
        raise ValueError("No readable text found in the uploaded documents.")
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform([item["text"] for item in chunks])
    return {"vectorizer": vectorizer, "matrix": matrix, "chunks": chunks}

def search(index, query, top_k=4):
    query_vector = index["vectorizer"].transform([query])
    scores = cosine_similarity(query_vector, index["matrix"]).flatten()
    ranked = scores.argsort()[::-1][:top_k]
    results = []
    for i in ranked:
        if scores[i] > 0:
            item = dict(index["chunks"][int(i)])
            item["score"] = float(scores[i])
            results.append(item)
    return results
