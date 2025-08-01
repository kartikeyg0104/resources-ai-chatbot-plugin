"""
Definition of the tools avaialable to the Agent.
"""

from typing import Optional
from rag.retriever.retrieve import get_relevant_documents

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
    ## Semantic research
    data_retrieved, scores = get_relevant_documents(
        query,
        EMBEDDING_MODEL,
        logger=logger,
        source_name="plugins",
        top_k=30
    )
    print("DATA RETRIEVED")
    print(data_retrieved)
    print("SCORES RETRIEVED")
    print(scores)
    ## Keyword based research

    ## Name-based
    return "Nothing relevant"

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

import logging
from rag.embedding.embedding_utils import load_embedding_model

logger = logging.getLogger("MY_LOGGER")

EMBEDDING_MODEL = load_embedding_model("sentence-transformers/all-MiniLM-L6-v2", logger)

search_plugin_docs("How to install Jenkins on Linux?", "", logger)
