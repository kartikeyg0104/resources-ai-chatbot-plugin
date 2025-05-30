"""Chunk StackOverflow threads into structured blocks with metadata."""

import os
import json
import uuid
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils import(
    extract_code_blocks,
    get_logger,
    assign_code_blocks_to_chunks
)

logger = get_logger()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "..", "raw", "stack_overflow_threads.json")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "processed", "chunks_stackoverflow_threads.json")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

def clean_html(html):
    """
    Parses and cleans HTML content using BeautifulSoup.

    Args:
        html (str): Raw HTML string containing question and answer.

    Returns:
        BeautifulSoup: Parsed HTML object.
    """
    return BeautifulSoup(html, "lxml")

def process_thread(thread, text_splitter):
    """
    Processes a single StackOverflow Q&A thread:
    - Combines question and answer bodies
    - Parses HTML
    - Extracts code blocks and replaces them with placeholders
    - Splits plain text into overlapping chunks
    - Assigns relevant code blocks to each chunk

    Args:
        thread (dict): StackOverflow thread dictionary.
        text_splitter (RecursiveCharacterTextSplitter): Chunking utility.

    Returns:
        list[dict]: List of chunk objects with text, metadata, and code blocks.
    """
    question_id = thread.get("Question ID")
    question_body = thread.get("Question Body", "")
    answer_body = thread.get("Answer Body", "")

    if question_body == "" or answer_body == "":
        logger.warning(
            "Question %d is missing question/answer content. Extracting 0 chunks from it.", 
            question_id
        )
        return []

    question_and_answer = f"<div>{question_body}</div><div>{answer_body}</div>"
    soup = clean_html(question_and_answer)

    code_blocks = extract_code_blocks(soup, "code")

    full_text = soup.get_text(separator=" ", strip=True)

    chunks = text_splitter.split_text(full_text)
    processed_chunks = assign_code_blocks_to_chunks(chunks,code_blocks, r"\[\[CODE_BLOCK_(\d+)\]\]")

    return [
        {
            "id": str(uuid.uuid4()),
            "chunk_text": chunk["chunk_text"],
            "metadata": {
                "data_source": "stackoverflow_threads",
                "question_id": question_id,
                "title": thread.get("Question Title", "Untitled"),
                "tags": thread.get("Tags", ""),
                "creation_date": thread.get("CreationDate", ""),
                "question_score": thread.get("Question Score", 0),
                "answer_score": thread.get("Answer Score", 0)
            },
            "code_blocks": chunk["code_blocks"]
        }
        for chunk in processed_chunks
    ]

def extract_chunks(threads):
    """
    Processes a list of StackOverflow threads into structured chunks.

    Args:
        threads (list): List of StackOverflow thread dicts.

    Returns:
        list[dict]: All extracted chunks from all threads.
    """
    all_chunks = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap= CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )

    for thread in threads:
        chunks = process_thread(thread, text_splitter)
        all_chunks.extend(chunks)

    return all_chunks

def main():
    """Main entry point."""
    try:
        with open(INPUT_PATH, "r", encoding="utf-8") as f:
            threads = json.load(f)
    except (FileNotFoundError, OSError) as e:
        logger.error("File error while reading %s: %s", INPUT_PATH, e)
        return
    except json.JSONDecodeError as e:
        logger.error("JSON decode error in %s: %s", INPUT_PATH, e)
        return

    logger.info("Chunking from %d stackoverflow threads.", len(threads))
    all_chunks = extract_chunks(threads)

    try:
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, ensure_ascii=False, indent=2)
    except OSError as e:
        logger.error("File error while  writing %s: %s", OUTPUT_PATH, e)
        return

    logger.info("Saved %d thread chunks to %s", len(all_chunks), OUTPUT_PATH)

if __name__ == "__main__":
    main()
