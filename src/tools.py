from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import requests
import re

# def get_wikipedia_tool():
#     wiki_api = WikipediaAPIWrapper(
#         lang = "en",
#         top_k_results = 3,
#         doc_content_chars_max=1000,
#     )
#     wiki_tool = WikipediaQueryRun(
#         api_wrapper=wiki_api,
#     )
#     return wiki_tool

def wiki_search(term):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": term,
        "format": "json",
        "srlimit": 3
    }

    headers = {
        'User-Agent': 'PersonalAgent/1.0 (https://example.com/contact) Python/requests'
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    search_results = data.get("query", {}).get("search", [])
    results = []
    for result in search_results:
        title = result['title']
        snippet = result['snippet']
        # Remove HTML tags like <span class="searchmatch">...</span>
        snippet_clean = re.sub(r'<.*?>', '', snippet)
        # Decode HTML entities
        snippet_clean = snippet_clean.replace('&#039;', "'")
        snippet_clean = snippet_clean.replace('&quot;', '"')
        snippet_clean = snippet_clean.replace('&amp;', '&')
        results.append(f"- {title}: {snippet_clean}")
    return results

if __name__ == "__main__":
    term = "What is Newton's second law?"
    print(wiki_search(term))
