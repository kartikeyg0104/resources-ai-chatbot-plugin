# utils/__init__.py

from .filter_functions import (
    remove_container_by_class,
    remove_tags,
    extract_page_content_container,
    remove_html_comments,
    remove_edge_navigation_blocks
)

from .split_doc_types import(
    split_type_docs
)