import json
import os
from bs4 import BeautifulSoup
from utils import (
    remove_tags,
    remove_html_comments,
    get_visible_text_length
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "..", "raw", "plugin_docs.json")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "processed", "processed_plugin_docs.json")

MIN_VISIBLE_TEXT_LENGTH = 60

def main():
    plugin_data = {}
    with open(INPUT_PATH, "r", encoding='utf-8') as f:
        plugin_data = json.load(f)

    print(f"Handling {len(plugin_data.keys())} plugin docs.")
    processed_plugin_docs = {}

    for plugin_name, html_content in plugin_data.items():
        cleaned_html = remove_tags(html_content)
        content_without_comments = remove_html_comments(cleaned_html)

        if get_visible_text_length(content_without_comments) > MIN_VISIBLE_TEXT_LENGTH:
            processed_plugin_docs[plugin_name] = content_without_comments

    print(f"Processed {len(processed_plugin_docs)} plugins.")

    with open(OUTPUT_PATH, "w", encoding='utf-8') as f:
        json.dump(processed_plugin_docs, f, ensure_ascii=False, indent=2)

    print("Saved processed plugins.")

if __name__ == "__main__":
    main()
