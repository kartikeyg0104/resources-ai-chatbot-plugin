from bs4 import BeautifulSoup
import json
import os
from utils import(
    get_visible_text_length
    get_logger
)

logger = get_logger()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "..", "processed", "processed_jenkins_docs.json")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "processed", "filtered_jenkins_docs.json")

MIN_VISIBLE_TEXT_LENGTH = 300
MAX_LINK_RATIO = 0.1

def link_ratio(content):
    """
    Computes the ratio of <a> tags to visible text chunks (roughly per 7 chars).

    Parameters:
    - content (str): Raw HTML content.

    Returns:
    - float: Ratio of links to visible text size.
    """
    soup = BeautifulSoup(content, "html.parser")
    links = soup.find_all("a")
    text = soup.get_text(separator=" ", strip=True)
    return len(links) / max(len(text) / 7 , 1)

def normalize_url(url):
    """
    Normalizes a URL by removing trailing slashes and 'index.html'.

    Parameters:
    - url (str): Original URL.

    Returns:
    - str: Normalized URL.
    """
    if url.endswith("index.html"):
        url = url[: -len("index.html")]

    if url.endswith("/"):
        url = url[:-1]

    return url

def normalize_url_keys(doc_dict):
    """
    Applies URL normalization to the keys of a documentation dictionary.

    Parameters:
    - doc_dict (dict): Dictionary with URLs as keys.

    Returns:
    - dict: Dictionary with normalized URLs as keys.
    """
    result = {}
    for url, content in doc_dict.items():
        normalized_url = normalize_url(url)        
        result[normalized_url] = content
    return result

def main():
    docs = {}

    with open(INPUT_PATH, "r", encoding='utf-8') as f:
        data = json.load(f)
        developer_docs = normalize_url_keys(data["developer_docs"])
        non_developer_docs = normalize_url_keys(data["non_developer_docs"])
        docs = developer_docs | non_developer_docs

    urls_to_remove = set()
    # Filtering the urls whose content size < MIN_VISIBLE_TEXT_LENGTH or has 'too many' links compared to the size of the content(ratio > MAX_LINK_RATIO)
    for url, content in docs.items():
        if ('extensions' not in url) and (get_visible_text_length(content) < MIN_VISIBLE_TEXT_LENGTH or link_ratio(content) > MAX_LINK_RATIO):
            urls_to_remove.add(url)

    logger.info(f'There are {len(urls_to_remove)} urls to remove.')

    cleaned_docs = {url: content for url, content in docs.items() if url not in urls_to_remove}

    logger.info(f"Cleaned docs contain {len(cleaned_docs)} pages after filtering.")

    with open(OUTPUT_PATH, "w", encoding='utf-8') as f:
        json.dump(cleaned_docs, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
