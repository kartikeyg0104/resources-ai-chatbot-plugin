"""Chunk Discourse threads into structured content blocks with metadata."""

import os
import json
import uuid
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils import(
    get_logger,
    assign_code_blocks_to_chunks
)

logger = get_logger()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "..", "raw", "topics_with_posts.json")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "processed", "chunks_discourse_docs.json")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

def extract_code_blocks(text):
    """
    Extracts code blocks and replaces them with indexed placeholders.
    Supports both triple-backtick code blocks and inline code in backticks.

    Args:
        text (str): Raw text including code blocks.

    Returns:
        tuple:
            - List of extracted code blocks (in order of appearance).
            - Modified text with placeholders inserted in place of code.
    """
    code_blocks = []
    placeholder_counter = 0

    # Replace triple backtick code blocks with indexed placeholders
    def replace_triple(match):
        nonlocal placeholder_counter
        code = match.group(1).strip()
        placeholder = f"[[CODE_BLOCK_{placeholder_counter}]]"
        code_blocks.append(code)
        placeholder_counter += 1
        return placeholder

    text = re.sub(r"```(.*?)```", replace_triple, text, flags=re.DOTALL)

    # Replace inline backtick code with indexed placeholders
    def replace_inline(match):
        nonlocal placeholder_counter
        code = match.group(1).strip()
        placeholder = f"[[CODE_SNIPPET_{placeholder_counter}]]"
        code_blocks.append(code)
        placeholder_counter += 1
        return placeholder

    text = re.sub(r"`([^`\n]+?)`", replace_inline, text)

    return code_blocks, text


def process_thread(thread, text_splitter):
    """
    Processes a single Discourse thread into structured chunks.

    Args:
        thread (dict): Thread data including topic ID, title, and post texts.
        text_splitter (RecursiveCharacterTextSplitter): Chunking utility.

    Returns:
        list[dict]: List of chunk objects with text, metadata, and associated code blocks.
    """
    topic_id = thread.get("topic_id")
    title = thread.get("title", "Untitled")
    posts = thread.get("posts", [])

    # Combine all posts into a single text block
    full_text = "\n\n".join(posts)

    code_blocks, clean_text = extract_code_blocks(full_text)
    chunks = text_splitter.split_text(clean_text)

    processed_chunks = assign_code_blocks_to_chunks(
        chunks,
        code_blocks, r"\[\[(?:CODE_BLOCK|CODE_SNIPPET)_(\d+)\]\]"
    )

    return [
        {
            "id": str(uuid.uuid4()),
            "chunk_text": chunk["chunk_text"],
            "metadata": {
                "topic_id": topic_id,
                "data_source": "discourse_threads",
                "title": title
            },
            "code_blocks": chunk["code_blocks"]
        }
        for chunk in processed_chunks
    ]

def extract_chunks(threads):
    """
    Processes all Discourse threads into a flat list of chunks.

    Args:
        threads (list): List of Discourse thread dicts.

    Returns:
        list[dict]: All chunks extracted from all threads.
    """
    all_chunks = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap= CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )

    for thread in threads:
        thread_chunks = process_thread(thread, text_splitter)
        all_chunks.extend(thread_chunks)

    return all_chunks

def main():
    """Main entry point."""
    try:
        with open(INPUT_PATH, "r", encoding="utf-8") as f:
            threads = json.load(f)
    except (FileNotFoundError, OSError) as e:
        logger.error("File error while reading %s: %s ", INPUT_PATH, e)
        return
    except json.JSONDecodeError as e:
        logger.error("JSON decode error in %s: %s", INPUT_PATH, e)
        return

    logger.info("Chunking %d Discourse threads.", len(threads))
    all_chunks = extract_chunks(threads)

    try:
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, ensure_ascii=False, indent=2)
    except OSError as e:
        logger.error("File error while  writing %s: %s ", OUTPUT_PATH, e)
        return

    logger.info("Written %d Discourse chunks to %s.", len(all_chunks), OUTPUT_PATH)

if __name__ == "__main__":
    main()
