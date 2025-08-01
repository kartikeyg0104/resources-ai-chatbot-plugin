"""
Definition of the tools avaialable to the Agent.
"""

from typing import Optional

def search_plugin_docs(query: str, plugin_name: Optional[str] = None) -> str:
    """
    Plugin Search tool
    """
    if query or plugin_name:
        pass
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
