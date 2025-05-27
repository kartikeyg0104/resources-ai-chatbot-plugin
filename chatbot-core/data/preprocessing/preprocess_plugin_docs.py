import json
import os
from bs4 import BeautifulSoup
from utils import (
    remove_tags,
    remove_html_comments,
    get_visible_text_length,
    get_logger,
    strip_html_body_wrappers
)

logger = get_logger()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "..", "raw", "plugin_docs.json")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "processed", "processed_plugin_docs.json")

MIN_VISIBLE_TEXT_LENGTH = 60

def process_plugin_docs(plugin_docs):
    processed_plugin_docs = {}

    for plugin_name, html_content in plugin_docs.items():
        soup = BeautifulSoup(html_content, "lxml")
        html_content = str(soup) 
        cleaned_html = remove_tags(html_content)
        content_without_comments = remove_html_comments(cleaned_html)
        content_without_wrappers = strip_html_body_wrappers(content_without_comments)

        text_length = get_visible_text_length(content_without_wrappers)
        if text_length > MIN_VISIBLE_TEXT_LENGTH: 
            processed_plugin_docs[plugin_name] = content_without_wrappers
        else:
            logger.info(f"Skipping plugin '{plugin_name}' - visible text length: {text_length} <= {MIN_VISIBLE_TEXT_LENGTH}")

    logger.info(f"Processed {len(processed_plugin_docs)} out of {len(plugin_docs)} plugins.")
    

    return processed_plugin_docs

def main():
    plugin_data = {}
    
    try:
        with open(INPUT_PATH, "r", encoding='utf-8') as f:
            plugin_data = json.load(f)
    except Exception as e:
        logger.error(f"Unexpected error while reading from {INPUT_PATH}: {e}")
        return

    logger.info(f"Handling {len(plugin_data.keys())} plugin docs.")
    
    processed_plugin_docs = process_plugin_docs(plugin_data)

    try:
        with open(OUTPUT_PATH, "w", encoding='utf-8') as f:
            json.dump(processed_plugin_docs, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Unexpected error while writing to {OUTPUT_PATH}: {e}")
        return

    logger.info(f"Saved processed plugins to {OUTPUT_PATH}.")

if __name__ == "__main__":
    main()
