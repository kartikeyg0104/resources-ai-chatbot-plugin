import numpy as np
import os
import faiss
from rag.embedding import embed_docs
from rag.vectorstore.vectorstore_utils import save_faiss_index, save_metadata

VECTOR_STORE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "embeddings", "vectorstore")
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "faiss_index.idx")
METADATA_PATH = os.path.join(VECTOR_STORE_DIR, "faiss_metadata.pkl")

def main():
    vectors, metadata = embed_docs.main()

    # Convert vectors to float32 for FAISS
    vectors_np = np.array(vectors).astype("float32")

    index = faiss.IndexFlatL2(vectors_np.shape[1])
    index.add(vectors_np)

    save_faiss_index(index, INDEX_PATH)
    save_metadata(metadata, METADATA_PATH)

    print(f"Stored {len(vectors)} vectors to FAISS at {INDEX_PATH}")

if __name__ == "__main__":
    main()
