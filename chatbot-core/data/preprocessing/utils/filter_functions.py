from bs4 import BeautifulSoup, Comment

def extract_page_content_container(soup, class_name):
    """Extract content from the 'container' div class"""
    content_div = soup.find("div", class_=class_name)
    if content_div:
        return str(content_div)
    return ""


def remove_container_by_class(content, class_name):
    """
    Given HTML content and a class name, removes the content inside the div
    with that class name and returns the remaining HTML.
    """
    soup = BeautifulSoup(content, "html.parser")
    content_div = soup.find("div", class_=class_name)

    if content_div:
        content_div.decompose() 

    return str(soup)

def remove_tags(content, tags_to_remove=None):
    """
    Removes all specified tags from the given HTML content.
    
    Parameters:
    - content (str): The HTML string to clean.
    - tags_to_remove (list of str): Tag names to remove (e.g., ["img", "script"]).
    
    Returns:
    - str: Cleaned HTML content with specified tags removed.
    """
    if tags_to_remove is None:
        tags_to_remove = ["img", "script", "style", "iframe", "object", "embed", "form"]  # Default tags to remove

    soup = BeautifulSoup(content, "html.parser")

    for tag in tags_to_remove:
        for element in soup.find_all(tag):
            element.decompose()

    return str(soup)

def remove_edge_navigation_blocks(content):
    """
    Removes the first navigation block (if present at the top) and the last one (plus any following elements)
    from the direct children of `.col-lg-9`, based on expected structure.
    """
    soup = BeautifulSoup(content, "html.parser")
    container = soup.find("div", class_="col-lg-9")
    if not container:
        return str(soup)

    def is_navigation_block(div):
        if div.name != "div":
            return False
        children = div.find_all(recursive=False)
        return (
            len(children) == 1 and
            children[0].name == "div" and
            "row" in children[0].get("class", []) and
            "body" not in children[0].get("class", [])  # avoid the main body
        )

    # Step 1: Remove top navigation block if it's the first direct child
    children = container.find_all(recursive=False)
    if children and is_navigation_block(children[0]):
        children[0].decompose()

    # Step 2: Refresh children and find bottom nav (and remove everything after it)
    children = container.find_all(recursive=False)
    is_navigation_block_found = False
    for i, div in enumerate(children):
        if is_navigation_block(div) or (div.name == "div" and div.get("id") == "feedback"):
            # Remove this and everything after
            for div_to_remove in children[i:]:
                div_to_remove.decompose()
            is_navigation_block_found = True
            break
    
    if not is_navigation_block_found:
        feedback_div = container.find("div", id="feedback")
        if feedback_div:
            feedback_div.decompose()
        
    return str(soup)

def remove_html_comments(content):
    """
    Removes all HTML comments from the given HTML content string.

    Parameters:
    - content (str): HTML string.

    Returns:
    - str: HTML with all comments removed.
    """
    soup = BeautifulSoup(content, "html.parser")

    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    return str(soup)