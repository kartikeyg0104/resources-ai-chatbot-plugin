
def search_plugin_docs(query: str, plugin_name=None):
    pass

def search_jenkins_docs(query: str):
    pass

def search_stackoverflow_threads(query: str):
    pass

def search_community_threads(query: str):
    pass

tool_registry = {
    "search_plugin_docs": search_plugin_docs,
    "search_jenkins_docs": search_jenkins_docs,
    "search_stackoverflow_threads": search_stackoverflow_threads,
    "search_community_threads": search_community_threads,
}
