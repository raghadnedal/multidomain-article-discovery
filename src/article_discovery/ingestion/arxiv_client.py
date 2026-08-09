import xml.etree.ElementTree as ET
import requests
from src.article_discovery.processing.normalization import normalize_arxiv_article
from src.article_discovery.schemas.article import Article
from src.article_discovery.storage.json_storage import save_articles_to_json


ARXIV_API_URL = "https://export.arxiv.org/api/query"

ATOM_NAMESPACE = {
    "atom": "http://www.w3.org/2005/Atom",
}


def clean_text(text: str | None) -> str:
    if text is None:
        return ""

    return " ".join(text.split())


def fetch_articles(
        max_results: int = 3,
        start: int = 0,
        search_query: str = "cat:cs.AI",
) -> list[dict]:
    params = {
        "search_query": search_query,
        "start": start,
        "max_results": max_results,
    }

    response = requests.get(
        ARXIV_API_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    root = ET.fromstring(response.text)
    entries = root.findall("atom:entry", ATOM_NAMESPACE)

    articles = []

    for entry in entries:
        article = {
            "id": clean_text(entry.findtext("atom:id", namespaces=ATOM_NAMESPACE)),
            "title": clean_text(
                entry.findtext("atom:title", namespaces=ATOM_NAMESPACE)
            ),
            "summary": clean_text(
                entry.findtext("atom:summary", namespaces=ATOM_NAMESPACE)
            ),
            "published": clean_text(
                entry.findtext("atom:published", namespaces=ATOM_NAMESPACE)
            ),
            "updated": clean_text(
                entry.findtext("atom:updated", namespaces=ATOM_NAMESPACE)
            ),
        }

        articles.append(article)

    return articles


def fetch_normalized_articles(max_results: int = 3) -> list[Article]:
    raw_articles = fetch_articles(max_results=max_results)
    normalized_articles = [normalize_arxiv_article(raw_article)
                           for raw_article in raw_articles]
    return normalized_articles


if __name__ == "__main__":
    articles = fetch_normalized_articles(max_results=100)

    save_articles_to_json(
        articles,
        "data/processed/arxiv_articles.json",
    )

    print(f"Saved {len(articles)} articles")
