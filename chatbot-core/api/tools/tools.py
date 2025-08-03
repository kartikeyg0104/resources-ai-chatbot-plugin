"""
Definition of the tools avaialable to the Agent.
"""

from typing import Optional
import heapq
from rag.retriever.retrieve import get_relevant_documents
from rag.retriever.retriever_bm25 import perform_keyword_search
from api.models.embedding_model import EMBEDDING_MODEL
from api.tools.utils import get_inverted_scores, extract_chunks_content
from api.config.loader import CONFIG

retrieval_config = CONFIG["retrieval"]

def search_plugin_docs(query: str, keywords: str, logger, plugin_name: Optional[str] = None) -> str:
    """
    Search tool for the plugin docs. Exploits both a sparse and dense search, resulting in a 
    hybrid search.

    Args:
        query (str): The user query.
        keywords (str): Keywords extracted from the user query.
        plugin_name (Optional[str]): The refered plugin name in the query (if available).
    
    Returns:
        str: The result of the research of the plugin search tool.
    """
    top_k_chunks = []
    data_retrieved_semantic, scores_semantic = get_relevant_documents(
        query,
        EMBEDDING_MODEL,
        logger=logger,
        source_name=CONFIG["tool_names"]["plugins"],
        top_k=retrieval_config["top_k_semantic"]
    )
    data_retrieved_keyword, scores_keyword = perform_keyword_search(
        keywords,
        logger,
        source_name=CONFIG["tool_names"]["plugins"],
        top_k=retrieval_config["top_k_keyword"]
    )

    if plugin_name:
        data_retrieved_semantic, data_retrieved_keyword = filter_retrieved_data(data_retrieved_semantic, data_retrieved_keyword)
    
    scores = get_inverted_scores([c["id"] for c in data_retrieved_semantic], scores_semantic,
                        [c["id"] for c in data_retrieved_keyword], scores_keyword)

    combined_results = data_retrieved_semantic + data_retrieved_keyword
    lookup_by_id = {item["id"]: item for item in combined_results}

    heapq.heapify(scores)
    i = 0
    while i < retrieval_config["top_k_plugins"] and len(scores) > 0:
        item = heapq.heappop(scores)
        top_k_chunks.append(lookup_by_id.get(item[1]))

    return extract_chunks_content(top_k_chunks, logger)

def search_jenkins_docs(query: str) -> str:
    """
    Docs Search tool
    """
    if query:
        pass
    return "Nothing relevant"

def search_stackoverflow_threads(query: str) -> str:
    """
    Stackoverflow Search tool
    """
    if query:
        pass
    return "Nothing relevant"

def search_community_threads(query: str) -> str:
    """
    Community Threads Search tool
    """
    if query:
        pass
    return "Nothing relevant"
