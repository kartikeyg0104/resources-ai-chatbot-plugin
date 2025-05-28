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
    soup = BeautifulSoup(html, "lxml")
    title = extract_title(soup)
    code_blocks = extract_code_blocks(soup, "pre")

    text = soup.get_text(separator=" ", strip=True)
    chunks = text_splitter.split_text(text)

    processed_chunks = assign_code_blocks_to_chunks(chunks, code_blocks, r"\[\[CODE_BLOCK_(\d+)\]\]")

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
    try:
        with open(INPUT_PATH, "r", encoding="utf-8") as f:
            docs = json.load(f)
    except Exception as e:
        logger.error(f"Unexpected error while reading from {INPUT_PATH}: {e}")
        return
    
    logger.info(f"Chunking from {len(docs.keys())} page docs.")
    all_chunks = extract_chunks(docs)

    try:
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Unexpected error while writing to {OUTPUT_PATH}: {e}")
        return

    logger.info(f"Written {len(all_chunks)} docs chunks to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
