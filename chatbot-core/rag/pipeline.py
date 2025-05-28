from rag.embedding import embed_docs
from rag.vectorstore import store_embeddings
from rag.retriever.search import get_relevant_documents

def query_pipeline(query, top_k=5):
    """
    Query the FAISS index for relevant documents.

    Args:
        query (str): The user's natural language query.
        top_k (int): Number of top matches to retrieve.

    Returns:
        List[Dict]: Ranked list of results with metadata and scores.
    """
    return get_relevant_documents(query, top_k)