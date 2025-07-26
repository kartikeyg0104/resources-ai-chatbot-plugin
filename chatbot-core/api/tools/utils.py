from api.tools.tools import (
    search_community_threads,
    search_jenkins_docs,
    search_plugin_docs,
    search_stackoverflow_threads
)

tool_registry = {
    "search_plugin_docs": search_plugin_docs,
    "search_jenkins_docs": search_jenkins_docs,
    "search_stackoverflow_threads": search_stackoverflow_threads,
    "search_community_threads": search_community_threads,
}

def get_default_tools_call():
    return [
        {}
    ]
