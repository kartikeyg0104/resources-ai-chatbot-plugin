import os
import json
from embedding_utils import load_embedding_model, embed_documents

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(SCRIPT_DIR, "..", "..", "data", "processed")
CHUNK_FILES = [
    "chunks_docs.json",
    # "chunks_plugin_docs.json",
    # "chunks_discourse_docs.json",
    # "chunks_stackoverflow_docs.json"
]

def load_chunks_from_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def collect_all_chunks():
    all_chunks = []
    for file_name in CHUNK_FILES:
        path = os.path.join(PROCESSED_DIR, file_name)
        if os.path.exists(path):
            all_chunks.extend(load_chunks_from_file(path))
        else:
            print(f"Warning: File not found - {file_name}")
    return all_chunks

def main():
    chunks = collect_all_chunks()
    texts = [chunk["chunk_text"] for chunk in chunks]
    metadata = [chunk["metadata"] for chunk in chunks]

    model = load_embedding_model()
    vectors = embed_documents(texts, model)

    return vectors, metadata

if __name__ == "__main__":
    vectors, metadata = main()
    print(f"Embedded {len(vectors)} documents.")
