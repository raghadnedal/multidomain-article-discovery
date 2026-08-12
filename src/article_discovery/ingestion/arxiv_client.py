import xml.etree.ElementTree as ET
import requests
from src.article_discovery.processing.normalization import normalize_arxiv_article
from src.article_discovery.schemas.article import Article
from sqlalchemy.orm import Session
from article_discovery.database.connection import engine
from article_discovery.database.article_repository import article_exists
import time

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
        max_retries: int = 3,
) -> list[dict]:
    params = {
        "search_query": search_query,
        "start": start,
        "max_results": max_results,
    }
    for attempt in range(max_retries):

        response = requests.get(
            ARXIV_API_URL,
            params=params,
            timeout=30,
        )
        if response.status_code == 429:
            wait_seconds = 5 * (attempt+1)
            print(
                f"Rate limited by arXiv."
                f"Retrying in {wait_seconds} seconds..."
            )
            time.sleep(wait_seconds)
            continue

        response.raise_for_status()
        break
    else:
        raise RuntimeError(
            "arXiv API rate limit persisted after retries."
        )

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


def fetch_normalized_articles(max_results: int = 3,
                              search_query: str = "cat:cs.AI",) -> list[Article]:
    raw_articles = fetch_articles(
        max_results=max_results, search_query=search_query)
    normalized_articles = [normalize_arxiv_article(raw_article)
                           for raw_article in raw_articles]
    return normalized_articles


def fetch_new_articles(max_results: int = 100,
                       search_query: str = "cat:cs.AI",):

    articles = fetch_normalized_articles(max_results=max_results,
                                         search_query=search_query)
    new_articles = []
    with Session(engine) as session:
        for article in articles:
            if not article_exists(session, article.external_id):
                new_articles.append(article)
    return new_articles
