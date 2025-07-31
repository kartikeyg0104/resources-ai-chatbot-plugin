"""
Utilities for the tools package.
"""

from types import MappingProxyType
from api.tools.tools import (
    search_community_threads,
    search_jenkins_docs,
    search_plugin_docs,
    search_stackoverflow_threads
)

TOOL_REGISTRY = MappingProxyType({
    "search_plugin_docs": search_plugin_docs,
    "search_jenkins_docs": search_jenkins_docs,
    "search_stackoverflow_threads": search_stackoverflow_threads,
    "search_community_threads": search_community_threads,
})

TOOL_SIGNATURES = MappingProxyType({
    "search_plugin_docs": {"plugin_name": str, "query": str},
    "search_jenkins_docs": {"query": str},
    "search_stackoverflow_threads": {"query": str},
    "search_community_threads": {"query": str},
})

def get_default_tools_call(query: str):
    """
    Returns a default list of tool calls using the user query,
    covering all the retrievers tools.

    Args:
        query (str): The original query of the user.

    Returns:
        A list of tool calls that represent the default setting.
    """
    return [
        {
            "tool": "search_jenkins_docs",
            "params": {
                "query": query
            }
        },
        {
            "tool": "search_plugin_docs",
            "params": {
                "plugin_name": None,
                "query": query
            }
        },
        {
            "tool": "search_stackoverflow_threads",
            "params": {
                "query": query
            }
        },
        {
            "tool": "search_community_threads",
            "params": {
                "query": query
            }
        }
    ]

def validate_tool_calls(tool_calls_parsed: list, logger) -> bool:
    """
    Validates that each tool call has a valid tool name and matching params.

    Returns True if all tool calls are valid, False otherwise.
    """
    valid = True
    for call in tool_calls_parsed:
        tool = call.get("tool")
        params = call.get("params")

        if tool not in TOOL_SIGNATURES:
            logger.warning("Tool %s not available.", tool)
            valid = False
        else:
            expected_params = TOOL_SIGNATURES[tool]

            if not isinstance(params, dict):
                logger.warning("Params for tool %s is not a dict.", tool)
                valid = False

            for param_name, param_type in expected_params.items():
                if param_name not in params:
                    logger.warning("Tool: %s: Param %s is not expected.", tool, param_name)
                    valid = False
                if not isinstance(params[param_name], param_type):
                    logger.warning("Tool: %s: Param %s is not of the expected type %s.",
                                tool, param_name, param_type.__name__)
                    valid = False

    return valid
