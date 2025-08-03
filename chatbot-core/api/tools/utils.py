"""
Utilities for the tools package.
"""

import re
from types import MappingProxyType
from typing import List, Tuple
from api.tools.tools import (
    search_community_threads,
    search_jenkins_docs,
    search_plugin_docs,
    search_stackoverflow_threads
)
from api.config.loader import CONFIG
from api.services.chat_service import make_placeholder_replacer
from sklearn.preprocessing import MinMaxScaler


retrieval_config = CONFIG["retrieval"]
CODE_BLOCK_PLACEHOLDER_PATTERN = r"\[\[(?:CODE_BLOCK|CODE_SNIPPET)_(\d+)\]\]"

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

def get_inverted_scores(
    semantic_chunk_ids: List[str],
    semantic_scores: List[float],
    keyword_chunk_ids: List[str],
    keyword_scores: List[float],
) -> List[Tuple[float, str]]:
    """
    Combines keyword and semantic search scores into a single, normalized ranking.
    Higher original scores are better for keyword scores; lower scores are better for semantic scores.
    Missing values are penalized by assigning them the worst possible score.

    Scores are normalized to [0, 1], averaged with equal weight (50% each), and then inverted (multiplied by -1),
    making them suitable for the later use as a max-heap.

    Args:
        semantic_chunk_ids (List[str]): Chunk IDs returned from semantic search.
        semantic_scores (List[float]): Corresponding semantic scores (lower is better).
        keyword_chunk_ids (List[str]): Chunk IDs returned from keyword search.
        keyword_scores (List[float]): Corresponding keyword scores (higher is better).

    Returns:
        List[Tuple[float, str]]: A list of (inverted_score, chunk_id)
    """
    semantic_map = {semantic_chunk_ids[i]:semantic_scores[i] for i in range(len(semantic_chunk_ids))}
    keyword_map = {keyword_chunk_ids[i]:keyword_scores[i] for i in range(len(keyword_chunk_ids))}

    all_chunk_ids = set(semantic_map.keys()).union(keyword_map.keys())

    default_keyword = min(keyword_map.values()) if keyword_map else 0
    default_semantic = max(semantic_map.values()) if semantic_map else 1.5

    keyword_vals = [keyword_map.get(cid, default_keyword) for cid in all_chunk_ids]
    semantic_vals = [semantic_map.get(cid, default_semantic) for cid in all_chunk_ids]

    scaler = MinMaxScaler()
    keyword_norm = scaler.fit_transform([[v] for v in keyword_vals])
    semantic_inverted = [max(semantic_vals) - v for v in semantic_vals]
    semantic_norm = scaler.fit_transform([[v] for v in semantic_inverted])

    final_scores = [
        [float(-1 * (0.5 * keyword_norm[i][0] + 0.5 * semantic_norm[i][0])), cid]
        for i, cid in enumerate(all_chunk_ids)
    ]

    return final_scores

def extract_chunks_content(chunks, logger):
    """
    Builds a single context string from a list of chunks by replacing code block
    placeholders with actual code blocks.

    Args:
        chunks (List[Dict]): List of chunk dictionaries.
        logger (logging.Logger): Logger for warning messages.

    Returns:
        str: Combined chunk texts, or a fallback message if none are valid.
    """
    context_texts = []
    for item in chunks:
        item_id = item.get("id", "")
        text = item.get("chunk_text", "")
        if not item_id:
            logger.warning("Id of retrieved context not found. Skipping element.")
            continue
        if text:
            code_iter = iter(item.get("code_blocks", []))
            replace = make_placeholder_replacer(code_iter, item_id)
            text = re.sub(CODE_BLOCK_PLACEHOLDER_PATTERN, replace, text)

            context_texts.append(text)
        else:
            logger.warning("Text of chunk with ID %s is missing", item_id)
    return (
        "\n\n".join(context_texts)
        if context_texts
        else retrieval_config["empty_context_message"]
    )
