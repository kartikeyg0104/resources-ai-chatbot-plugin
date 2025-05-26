import os
import json
import uuid
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "..", "processed", "filtered_jenkins_docs.json")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "processed", "chunks_docs.json")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", " ", ""]
)

def extract_title(soup):
    h1 = soup.find("h1")
    if h1 and h1.get_text(strip=True):
        return h1.get_text(strip=True)
    if soup.title:
        return soup.title.get_text(strip=True)
    return "Untitled"

def extract_code_blocks(soup):
    code_blocks = []
    for i, code_block in enumerate(soup.find_all("pre")):
        placeholder = f"[[CODE_BLOCK_{i}]]"
        code_blocks.append(code_block.get_text(strip=True))
        code_block.replace_with(placeholder)
    return code_blocks

def process_page(url, html):
    soup = BeautifulSoup(html, "html.parser")
    title = extract_title(soup)
    code_blocks = extract_code_blocks(soup)

    text = soup.get_text(separator=" ", strip=True)
    chunks = text_splitter.split_text(text)

    return [
        {
            "id": str(uuid.uuid4()),
            "chunk_text": chunk,
            "metadata": {
                "source_url": url,
                "title": title
            },
            "code_blocks": code_blocks
        }
        for chunk in chunks
    ]

def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        docs = json.load(f)

    all_chunks = []
    for url, html in docs.items():
        page_chunks = process_page(url, html)
        all_chunks.extend(page_chunks)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"Written {len(all_chunks)} RAG-ready chunks to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
