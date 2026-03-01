import requests
from bs4 import BeautifulSoup


def fetch_page(url: str) -> str:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    # Basic extraction: get visible text
    texts = soup.stripped_strings
    return "\n".join(texts)
