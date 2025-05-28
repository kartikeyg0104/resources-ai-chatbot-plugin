from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def load_embedding_model():
    print(f"Loading embedding model: {MODEL_NAME}")
    return SentenceTransformer(MODEL_NAME)

def embed_documents(texts, model, batch_size=32):
    print(f"Embedding {len(texts)} documents")
    return model.encode(texts, batch_size=batch_size, show_progress_bar=True)
