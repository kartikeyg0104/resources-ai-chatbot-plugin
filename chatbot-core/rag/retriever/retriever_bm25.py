"""
Query interface for retrieving the most relevant embedded text chunks using a Sparse Retriever.
"""

from rag.retriever.retriever_utils import load_vector_index
from rag.embedding.bm25_indexer import indexer
from api.config.loader import CONFIG

def perform_keyword_search(query, logger, source_name, top_k=5):
    """
    Retrieve the top-k most relevant chunks for a given natural language query
    performing a keyword based search.

    Args:
        query (str): The input query string.
        logger (logging.Logger): Logger for warnings and file-level updates.
        source_name (str): The source name that we want to consider.
        top_k (int): Number of top results to retrieve. Defaults to 5.

    Returns:
        tuple[list[dict], list[float]]: Retrieved data and similarity scores.
    """
    if not query.strip():
        logger.warning("Empty query received.")
        return [], []
    index = indexer.get(source_name)
    _, metadata = load_vector_index(logger, source_name)

    if not index or not metadata:
        return [], []

    data, scores = search_bm25_index(query, index, metadata, logger, top_k)

    filtered = [(d, s) for d, s in zip(data, scores)
                if s >= CONFIG["retrieval"]["keyword_threshold"]]
    filtered_data, filtered_scores = zip(*filtered) if filtered else ([], [])

    return list(filtered_data), list(filtered_scores)

def search_bm25_index(query, index, metadata, logger, top_k):
    """
    Perform the effective sparse research, using a sparse retriever.

    Args:
        query (str): The input query string.
        index (SparseRetriever): The built index on which we're searching.
        metadata (List[dict]): Metadata entries associated with each stored vector.
        logger (logging.Logger): Logger for warnings and file-level updates.
        top_k (int): Number of top results to retrieve.
    
    Returns:
        tuple[list[dict], list[float]]: Retrieved data and similarity scores.
    """
    search_results, scores = [], []
    metadata_by_id = {item["id"]: item for item in metadata}
    relevant_chunks = index.search(
        query=query,
        return_docs=True,
        cutoff=top_k,
    )

    for chunk in relevant_chunks:
        scores.append(chunk["score"])
        match = metadata_by_id.get(chunk["id"])
        if match:
            search_results.append(match)
        else:
            logger.warning("No metadata found for chunk ID: %s", chunk["id"])

    return search_results, scores
