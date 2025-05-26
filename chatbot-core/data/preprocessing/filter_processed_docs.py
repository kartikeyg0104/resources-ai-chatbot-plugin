from bs4 import BeautifulSoup
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "..", "processed", "processed_jenkins_docs.json")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "processed", "filtered_jenkins_docs.json")

def get_visible_text_length(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    return len(text)

def link_ratio(content):
    soup = BeautifulSoup(content, "html.parser")
    links = soup.find_all("a")
    text = soup.get_text(separator=" ", strip=True)
    return len(links) / max(len(text) / 7 , 1)

def normalize_url(url):
    if url.endswith("index.html"):
        url = url[: -len("index.html")]

    if url.endswith("/"):
        url = url[:-1]

    return url

def normalize_url_keys(doc_dict):
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
    # Filtering by the urls whose content size < 300 or has 'too many' links compared to the size of the content
    for url, content in docs.items():
        if ('extensions' not in url) and (get_visible_text_length(content) < 300 or link_ratio(content) > 0.1):
            urls_to_remove.add(url)

    print(f'There are {len(urls_to_remove)} urls to remove.')

    cleaned_docs = {url: content for url, content in docs.items() if url not in urls_to_remove}

    print(f"Cleaned docs contain {len(cleaned_docs)} pages after filtering.")

    with open(OUTPUT_PATH, "w", encoding='utf-8') as f:
        json.dump(cleaned_docs, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
