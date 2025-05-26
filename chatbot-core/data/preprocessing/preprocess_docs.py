import json
from bs4 import BeautifulSoup
import os
from utils import (
    remove_container_by_class,
    remove_tags,
    extract_page_content_container,
    remove_html_comments,
    remove_edge_navigation_blocks,
    split_type_docs
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DOCS_PATH = os.path.join(SCRIPT_DIR, "..", "raw", "jenkins_docs.json")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "processed", "processed_jenkins_docs.json")

def filter_content(urls, data, is_developer_content):
    """
    Filters HTML content for a list of URLs by extracting the main section
    and cleaning out unwanted elements like TOC, scripts, images, nav blocks, and comments.

    Parameters:
    - urls (list): List of URLs to filter.
    - data (dict): Dictionary of raw HTML content keyed by URL.
    - is_developer_content (bool): Whether the content is from developer docs.

    Returns:
    - dict: Filtered HTML content keyed by URL.
    """
    config = get_config(is_developer_content)
    filtered_contents = {}

    for url in urls:
        content = data[url]
        soup = BeautifulSoup(content, "html.parser")

        content_extracted = extract_page_content_container(soup, config["class_to_extract"])
        if content_extracted == "":
            print(f'NO {config["class_to_extract"]} FOUND IN A {"" if is_developer_content else "NON"} DEVELOPER PAGE! Skipping page: {url}')
            continue
        
        # Remove eventually toc(table of content)
        content_without_toc = remove_container_by_class(content_extracted, "toc")

        # Remove eventually img or script tags
        content_filtered_by_tags = remove_tags(content_without_toc)

        # Remove eventually navigation blocks (for docs under /developer this is not necessary)
        content_without_navigation_blocks = content_filtered_by_tags if is_developer_content else remove_edge_navigation_blocks(content_filtered_by_tags)

        filtered_contents[url] = remove_html_comments(content_without_navigation_blocks)

    return filtered_contents

def get_config(is_developer_content):
    """
    Returns configuration options depending on doc type. Introduced to maintain in the future
    a unique filter_content function, without hardcoding parameters whether it is a developer
    content or not.

    Parameters:
    - is_developer_content (bool): Whether the content is from developer docs.

    Returns:
    - dict: Configuration dict with class name to extract.
    """
    if is_developer_content:
        return {
            "class_to_extract": "col-8"
        }
    else:
        return {
            "class_to_extract": "col-lg-9"
        }

def main():
    data = []

    with open(INPUT_DOCS_PATH, "r", encoding='utf-8') as f:
        data = json.load(f)

    developer_urls, non_developer_urls = split_type_docs(data)

    print("Processing Developer contents")
    developer_content_filtered = filter_content(developer_urls, data, True)
    print("Processing  Non Developer contents")
    non_developer_content_filtered = filter_content(non_developer_urls, data, False)

    output = {}
    output["developer_docs"] = developer_content_filtered
    output["non_developer_docs"] = non_developer_content_filtered

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
