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
INPUT_PATH = os.path.join(SCRIPT_DIR, "..", "processed", "processed_plugin_docs.json")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "processed", "chunks_plugin_docs.json")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

def process_plugin(plugin_name, html, text_splitter):
    """
    Process a single Jenkins plugin documentation HTML:
    - Extracts code blocks
    - Converts content to plain text
    - Splits it into overlapping chunks
    - Reassigns code blocks to the appropriate chunks

    Args:
        plugin_name (str): Name of the Jenkins plugin (used as metadata title).
        html (str): Raw HTML content of the plugin documentation.
        text_splitter (RecursiveCharacterTextSplitter): Text splitter to use for chunking.

    Returns:
        list[dict]: List of chunk dictionaries with text, metadata, and code blocks.
    """
    soup = BeautifulSoup(html, "lxml")
    code_blocks = extract_code_blocks(soup, "pre")

    text = soup.get_text(separator=" ", strip=True)
    chunks = text_splitter.split_text(text)

    processed_chunks = assign_code_blocks_to_chunks(chunks, code_blocks, r"\[\[CODE_BLOCK_(\d+)\]\]")

    return [
        {
            "id": str(uuid.uuid4()),
            "chunk_text": chunk["chunk_text"],
            "metadata": {
                "data_source": "jenkins_plugins_documentation",
                "title": plugin_name
            },
            "code_blocks": chunk["code_blocks"]
        }
        for chunk in processed_chunks
    ]

def extract_chunks(plugin_docs):
    """
    Process all Jenkins plugin documentation files by extracting and chunking them.

    Args:
        plugin_docs (dict): Mapping from plugin name to HTML content.

    Returns:
        list[dict]: All processed chunks for all plugins.
    """
    all_chunks = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap= CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )

    for plugin_name, html in plugin_docs.items():
        plugin_chunks = process_plugin(plugin_name, html, text_splitter)
        all_chunks.extend(plugin_chunks)
    
    return all_chunks

def main():
    try:
        with open(INPUT_PATH, "r", encoding="utf-8") as f:
            plugin_docs = json.load(f)
    except Exception as e:
        logger.error(f"Unexpected error while reading from {INPUT_PATH}: {e}")
        return

    logger.info(f"Chunking from {len(plugin_docs.keys())} plugin docs.")
    all_chunks = extract_chunks(plugin_docs)

    try:
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Unexpected error while writing to {OUTPUT_PATH}: {e}")
        return

    logger.info(f"Written {len(all_chunks)} plugin chunks to {OUTPUT_PATH}.")

if __name__ == "__main__":
    main()
