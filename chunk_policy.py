"""Text extraction and chunking helpers for the company-policy chatbot."""
from io import BytesIO
from pypdf import PdfReader

def extract_text(filename: str, content: bytes) -> str:
    suffix = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    if suffix == "pdf":
        reader = PdfReader(BytesIO(content))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages).strip()
    if suffix == "txt":
        return content.decode("utf-8", errors="replace").strip()
    raise ValueError(f"Unsupported file type for {filename}. Please upload PDF or TXT.")

def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150):
    """Split text into overlapping character chunks, keeping context between chunks."""
    text = " ".join(text.split())
    if not text:
        return []
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be larger than overlap")
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = end - overlap
    return chunks
