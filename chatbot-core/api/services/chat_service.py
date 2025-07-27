"""
Chat service layer responsible for processing the requests forwarded by the controller.
"""

import re
from typing import List
import ast
import json
from api.models.llama_cpp_provider import llm_provider
from api.config.loader import CONFIG
from api.prompts.prompt_builder import build_prompt
from api.prompts.prompts import (
    QUERY_CLASSIFIER_PROMPT,
    SPLIT_QUERY_PROMPT,
    RETRIEVER_AGENT_PROMPT,
    CONTEXT_RELEVANCE_PROMPT
)
from api.models.schemas import ChatResponse
from api.services.memory import get_session
from api.models.embedding_model import EMBEDDING_MODEL
from api.models.schemas import QueryType, is_valid_query_type, str_to_query_type
from api.tools.utils import get_default_tools_call, TOOL_REGISTRY, validate_tool_calls
from rag.retriever.retrieve import get_relevant_documents
from utils import LoggerFactory

logger = LoggerFactory.instance().get_logger("api")
llm_config = CONFIG["llm"]
retrieval_config = CONFIG["retrieval"]
CODE_BLOCK_PLACEHOLDER_PATTERN = r"\[\[(?:CODE_BLOCK|CODE_SNIPPET)_(\d+)\]\]"

def get_chatbot_reply(session_id: str, user_input: str) -> ChatResponse:
    """
    Main chatbot entry point. Retrieves context, constructs a prompt with memory,
    and generates an LLM response. Also updates the memory with the latest exchange.

    Args:
        session_id (str): The unique ID for the chat session.
        user_input (str): The latest user message.

    Returns:
        ChatResponse: The generated assistant response.
    """
    logger.info("New message from session '%s'", session_id)
    logger.info("Handling the user query: %s", user_input)

    memory = get_session(session_id)
    if memory is None:
        raise RuntimeError(f"Session '{session_id}' not found in the memory store.")

    context = retrieve_context(user_input)
    logger.info("Context retrieved: %s", context)

    prompt = build_prompt(user_input, context, memory)

    logger.info("Generating answer with prompt: %s", prompt)
    reply = generate_answer(prompt)

    memory.chat_memory.add_user_message(user_input)
    memory.chat_memory.add_ai_message(reply)

    return ChatResponse(reply=reply)


def get_chatbot_reply_new_architecture(session_id: str, user_input: str) -> ChatResponse:
    """
    Main chatbot entry point. Retrieves context, constructs a prompt with memory,
    and generates an LLM response. Also updates the memory with the latest exchange.

    Args:
        session_id (str): The unique ID for the chat session.
        user_input (str): The latest user message.

    Returns:
        ChatResponse: The generated assistant response.
    """
    logger.info("New message from session '%s'", session_id)
    logger.info("Handling the user query: %s", user_input)

    memory = get_session(session_id)
    if memory is None:
        raise RuntimeError(f"Session '{session_id}' not found in the memory store.")

    query_type = _get_query_type(user_input)

    logger.info("The provided user query is of type %s.", query_type)

    if query_type == QueryType.MULTI:
        sub_queries = _get_sub_queries(user_input)
        answers = []
        for sub_query in sub_queries:
            answers.append(_get_reply_simple_query_pipeline(sub_query, memory))

        reply = _assemble_response(answers)
    else:
        reply = _get_reply_simple_query_pipeline(user_input, memory)

    memory.chat_memory.add_user_message(user_input)
    memory.chat_memory.add_ai_message(reply)

    return ChatResponse(reply=reply)


def _get_query_type(query: str) -> QueryType:
    """
    Gets the query type that can be either 'SIMPLE', if it contains one task, or
    'MULTI' if it contains 2 or more sub-queries inside. In case the LLM produces
    a not valid output it sets by default to MULTI, since in case it of a false
    positive it won't split up the query.

    Args:
        query (str): The user query.
    
    Returns:
        QueryType: the query type, either 'SIMPLE' or 'MULTI'
    """
    prompt = QUERY_CLASSIFIER_PROMPT.format(user_query = query)
    query_type = generate_answer(prompt)

    if not is_valid_query_type(query_type):
        logger.info("Not valid query type: %s. Setting to default to MULTI.", query_type)
        query_type = 'MULTI'

    return str_to_query_type(query_type)


def _get_sub_queries(query: str) -> List[str]:
    prompt = SPLIT_QUERY_PROMPT.format(user_query = query)

    queries_string = generate_answer(prompt)

    try:
        queries = ast.literal_eval(queries_string)
    except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
        logger.warning("Error in parsing the subqueries. The string may be not formed" \
            " correctly: %s. Setting to default array with 1 element.", queries_string)
        queries = [query]

    queries = [q.strip() for q in queries]

    return queries


def _assemble_response(answers: List[str]):
    return "\n\n".join(answer for answer in answers)


def _get_reply_simple_query_pipeline(query: str, memory) -> str:
    iterations, relevance = -1, 0
    while iterations < retrieval_config["max_reformulate_iterations"] and relevance != 2:
        tool_calls = _get_agent_tool_calls(query)

        retrieved_context = _retrieve_context(tool_calls)

        relevance = _get_query_context_relevance(query, retrieved_context)
        iterations += 1

    if relevance != 2:
        return "Unfortunately we are not able to respond to your answer."

    prompt = build_prompt(query, retrieved_context, memory)

    return generate_answer(prompt)


def _get_agent_tool_calls(query: str):
    retriever_agent_prompt = RETRIEVER_AGENT_PROMPT.format(user_query = query)

    tool_calls = generate_answer(retriever_agent_prompt)

    try:
        tool_calls_parsed = json.loads(tool_calls)
        if not validate_tool_calls(tool_calls_parsed, logger):
            tool_calls_parsed = get_default_tools_call(query)
    except json.JSONDecodeError:
        logger.warning("Invalid JSON syntax in the tools output: %s.", tool_calls)
        logger.warning("Calling all the search tools with default settings.")
        tool_calls_parsed = get_default_tools_call(query)
    except (KeyError, ValueError, TypeError, AttributeError) as e:
        logger.warning("JSON structure or value error(%s %s) in the tools output: %s.",
                       type(e).__name__, e, tool_calls)
        logger.warning("Calling all the search tools with default settings.")
        tool_calls_parsed = get_default_tools_call(query)

    return tool_calls_parsed


def _retrieve_context(tool_calls) -> str:
    retrieved_results = []
    for call in tool_calls:
        tool_name, params = call.get("tool"), call.get("params")
        tool_fn = TOOL_REGISTRY.get(tool_name)

        result = tool_fn(**params)
        retrieved_results.append({
            "tool": tool_name,
            "output": result
        })

    return "\n\n".join(
        f"[Result of the search tool {res['tool']}:]\n{res.get("output", "")}".strip()
        for res in retrieved_results
    )


def _get_query_context_relevance(query: str, context: str):
    prompt = CONTEXT_RELEVANCE_PROMPT.format(query = query, context = context)

    output = generate_answer(prompt)

    relevance_score = (output.split("Final label:")[-1]).strip()

    return relevance_score


def retrieve_context(user_input: str) -> str:
    """
    Retrieves the most relevant document chunks for a user query
    and reconstructs them by replacing placeholder tokens with actual code blocks.

    Args:
        user_input (str): The input query string.

    Returns:
        str: Combined, reconstructed context text. Returns retrieval_config["empty_context_message"]
        if any context have been retrieved.
    """
    data_retrieved, _ = get_relevant_documents(
        user_input,
        EMBEDDING_MODEL,
        logger=logger,
        top_k=retrieval_config["top_k"]
    )
    if not data_retrieved:
        logger.warning(retrieval_config["empty_context_message"])
        return "No context available."

    context_texts = []
    for item in data_retrieved:
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

def generate_answer(prompt: str) -> str:
    """
    Generates a completion from the language model for the given prompt.

    Args:
        prompt (str): The full prompt to send to the LLM.

    Returns:
        str: The model's generated text response.
    """
    return llm_provider.generate(prompt=prompt, max_tokens=llm_config["max_tokens"])


def make_placeholder_replacer(code_iter, item_id):
    """
    Returns a function to replace code block placeholders in retrieved text
    with actual code snippets from the original document.

    Args:
        code_iter (iterator): Iterator over code snippets.
        item_id (str): The ID of the document chunk (used for logging).

    Returns:
        Callable[[re.Match], str]: A function to replace placeholders.
    """
    def replace(_match):
        try:
            return next(code_iter)
        except StopIteration:
            logger.warning("More placeholders than code blocks in chunk with ID %s", item_id)
            return "[MISSING_CODE]"
    return replace
