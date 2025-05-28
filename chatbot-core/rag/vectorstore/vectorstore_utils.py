import faiss
import pickle
import os
import numpy as np

VECTOR_STORE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "embeddings", "vectorstore")
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

def save_faiss_index(inde, path):
    faiss.write_index(index, path)

def load_faiss_index(path):
    return faiss.read_index(path)

def save_metadata(metadata, path):
    with open(path, "wb") as f:
        pickle.dump(metadata, f)

def load_metadata(path):
    with open(path, "rb") as f:
        return pickle.load(f)