import json
from bs4 import BeautifulSoup
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
JENKINS_DOCS_PATH = os.path.join(script_dir, "../../raw/jenkins_docs.json")
JENKINS_DOCS_PATH = os.path.abspath(JENKINS_DOCS_PATH)
OUTPUT_PATH = os.path.join(script_dir, "../../raw/split_type_docs.json")

def extract_page_content_container(soup, class_name):
    """Extract content from the 'container' div class"""
    content_div = soup.find("div", class_=class_name)
    if content_div:
        return True
    return False

def split_type_docs(data):
    print(f'There are {len(data)} pages')
    with_col_lg_9 = 0
    badUrls = []
    non_developer_urls = []
    developer_urls = []
    # Every doc page that is not in the /developer part has the content in the col-lg-9 class 
    for url, content in data.items():
        soup = BeautifulSoup(content, "html.parser")
        if extract_page_content_container(soup, "col-lg-9") == True:
            non_developer_urls.append(url)
            with_col_lg_9 += 1
        else:
            badUrls.append(url)
    
    print(f'With col-lg-9: {with_col_lg_9}')
    print(len(badUrls))

    # Every doc page that is in the /developer part has the content in the col-8 class 
    with_col_8 = 0
    badUrls2 = []
    for url in badUrls:
        soup = BeautifulSoup(data[url], "html.parser")
        if extract_page_content_container(soup, "col-8") == True:
            developer_urls.append(url)
            with_col_8 += 1
        else:
            badUrls2.append(url)
    
    # The result should be that len(badUrls) is 0
    print(f'With col-8: {with_col_8}')
    print(len(badUrls2))

    return developer_urls, non_developer_urls

    json_output = {}
    json_output["developer"] = developer_urls
    json_output["non_developer"] = non_developer_urls

    with open(OUTPUT_PATH, "w", encoding='utf-8') as f:
        json.dump(json_output, f, ensure_ascii=False, indent=2)
        print("Saved correctly")