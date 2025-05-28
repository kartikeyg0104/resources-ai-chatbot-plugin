import faiss
import numpy as np
from rag.vectorstore.vectorstore_utils import load_faiss_index, load_metadata
import os

VECTOR_STORE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "embeddings", "vectorstore")
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "faiss_index.idx")
METADATA_PATH = os.path.join(VECTOR_STORE_DIR, "faiss_metadata.pkl")

def load_vector_index():
    index = load_faiss_index(INDEX_PATH)
    metadata = load_metadata(METADATA_PATH)
    return index, metadata

def search_index(query_vector, index, metadata, top_k=5): # Parametrize K
    query_vector = np.array(query_vector).astype("float32").reshape(1, -1)
    distances, indices = index.search(query_vector, top_k)
    results = []

    for i in range(len(indices[0])):
        idx = indices[0][i]
        if idx < len(metadata):
            results.append({
                "metadata": metadata[idx],
                "score": float(distances[0][i])
            })

    return results
