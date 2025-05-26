import json
from bs4 import BeautifulSoup
import os

def extract_page_content_container(soup, class_name):
    """
    Checks if a div with the given class name exists in the HTML.

    Parameters:
    - soup (BeautifulSoup): Parsed HTML document.
    - class_name (str): Class name of the div to check.

    Returns:
    - bool: True if the div exists, False otherwise.
    """
    content_div = soup.find("div", class_=class_name)
    return bool(content_div)

def split_type_docs(data):
    """
    Splits documentation pages into developer and non-developer types
    based on the presence of specific container classes.

    Parameters:
    - data (dict): Dictionary where keys are URLs and values are HTML content.

    Returns:
    - tuple: (developer_urls, non_developer_urls), both as lists of URLs.
    """
    print(f'There are {len(data)} pages')
    not_processed_urls = []
    non_developer_urls = []
    developer_urls = []
    # Every doc page that is not in the /developer part has the content in the col-lg-9 class 
    for url, content in data.items():
        soup = BeautifulSoup(content, "html.parser")
        if extract_page_content_container(soup, "col-lg-9") == True:
            non_developer_urls.append(url)
        else:
            not_processed_urls.append(url)
    
    print(f'With col-lg-9: {len(non_developer_urls)}')

    # Every doc page that is in the /developer part has the content in the col-8 class 
    for url in not_processed_urls:
        soup = BeautifulSoup(data[url], "html.parser")
        if extract_page_content_container(soup, "col-8") == True:
            developer_urls.append(url)
    
    print(f'With col-8: {len(developer_urls)}')

    return developer_urls, non_developer_urls
