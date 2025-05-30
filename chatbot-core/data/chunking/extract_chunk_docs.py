"""Script to chunk Jenkins HTML documentation into text blocks with metadata."""

import os
import json
import uuid
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils import(
    extract_code_blocks,
    extract_title,
    get_logger,
    assign_code_blocks_to_chunks
)

logger = get_logger()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "..", "processed", "filtered_jenkins_docs.json")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "processed", "chunks_docs.json")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

def process_page(url, html, text_splitter):
    """
    Processes a single Jenkins documentation page:
    - Parses the HTML
    - Extracts title and code blocks
    - Converts to plain text and splits into chunks
    - Reassigns code blocks to appropriate chunks

    Args:
        url (str): Source URL of the documentation page.
        html (str): Raw HTML content of the page.
        text_splitter (RecursiveCharacterTextSplitter): LangChain text splitter instance.

    Returns:
        list[dict]: A list of chunk dictionaries with text, metadata, and code blocks.
    """
    soup = BeautifulSoup(html, "lxml")
    title = extract_title(soup)
    code_blocks = extract_code_blocks(soup, "pre")

    text = soup.get_text(separator=" ", strip=True)
    chunks = text_splitter.split_text(text)

    processed_chunks = assign_code_blocks_to_chunks(chunks,code_blocks, r"\[\[CODE_BLOCK_(\d+)\]\]")

    return [
        {
            "id": str(uuid.uuid4()),
            "chunk_text": chunk["chunk_text"],
            "metadata": {
                "data_source": "jenkins_documentation",
                "source_url": url,
                "title": title
            },
            "code_blocks": chunk["code_blocks"]
        }
        for chunk in processed_chunks
    ]

def extract_chunks(docs):
    """
    Processes all Jenkins documentation pages by chunking their content.

    Args:
        docs (dict): A dictionary mapping URLs to raw HTML strings.

    Returns:
        list[dict]: A list of all processed chunks across all docs.
    """
    all_chunks = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap= CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )

    for url, html in docs.items():
        page_chunks = process_page(url, html, text_splitter)
        all_chunks.extend(page_chunks)

    return all_chunks

def main():
    """Main entry point."""
    try:
        with open(INPUT_PATH, "r", encoding="utf-8") as f:
            docs = json.load(f)
    except (FileNotFoundError, OSError) as e:
        logger.error("File error while reading %s:%s", INPUT_PATH, e)
        return
    except json.JSONDecodeError as e:
        logger.error("JSON decode error in %s: %s", INPUT_PATH, e)
        return

    logger.info("Chunking from %d page docs.", len(docs.keys()))
    all_chunks = extract_chunks(docs)

    try:
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, ensure_ascii=False, indent=2)
    except OSError as e:
        logger.error("File error while  writing %s:%s", OUTPUT_PATH, e)
        return

    logger.info("Written %d docs chunks to %s", len(all_chunks), OUTPUT_PATH)

if __name__ == "__main__":
    main()
