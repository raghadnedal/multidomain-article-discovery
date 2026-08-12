import requests
import xml.etree.ElementTree as ET
from article_discovery.processing.normalization import normalize_pubmed_article
from sqlalchemy.orm import Session
from article_discovery.database.connection import engine
from article_discovery.schemas.article import Article
from article_discovery.database.article_repository import article_exists


PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def search_pubmed(
    query: str,
    max_results: int = 5,
) -> list[str]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
    }

    response = requests.get(
        PUBMED_SEARCH_URL,
        params=params,
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()

    return data["esearchresult"]["idlist"]


def fetch_pubmed_articles(pubmed_ids: list[str]) -> list[dict]:
    if not pubmed_ids:
        return []
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml",
    }
    response = requests.get(
        PUBMED_FETCH_URL,
        params=params,
        timeout=30,
    )
    response.raise_for_status()

    root = ET.fromstring(response.text)
    articles = []
    for pubmed_article in root.findall(".//PubmedArticle"):
        pmid = pubmed_article.findtext(".//PMID") or ""
        title = pubmed_article.findtext(".//ArticleTitle") or ""
        year = pubmed_article.findtext(".//PubDate/Year") or ""
        month = pubmed_article.findtext(".//PubDate/Month") or ""
        day = pubmed_article.findtext(".//PubDate/Day") or ""

        published_at = "-".join(
            part for part in [year, month, day] if part
        )
        abstract_parts = [
            abstract.text or ""
            for abstract in pubmed_article.findall(".//Abstract/AbstractText")
        ]

        abstract = " ".join(abstract_parts)
        articles.append(
            {
                "pmid": pmid,
                "title": title,
                "abstract": abstract,
                "published_at": published_at,
            }
        )
    return articles


def fetch_normalized_pubmed_articles(
    query: str,
    max_results: int = 5,
) -> list[Article]:
    pubmed_ids = search_pubmed(
        query=query,
        max_results=max_results,
    )

    raw_articles = fetch_pubmed_articles(pubmed_ids)

    normalized_articles = [
        normalize_pubmed_article(raw_article)
        for raw_article in raw_articles
    ]

    return normalized_articles


def fetch_new_pubmed_articles(
        query: str,
        max_results: int = 20
) -> list[Article]:
    articles = fetch_normalized_pubmed_articles(
        query=query,
        max_results=max_results,
    )

    new_articles = []
    with Session(engine) as session:
        for article in articles:
            if not article_exists(session, article.external_id):
                new_articles.append(article)
    return new_articles


if __name__ == "__main__":
    ids = search_pubmed(
        query="machine learning cancer diagnosis",
        max_results=5,
    )

    articles = fetch_pubmed_articles(ids)
    for article in articles:
        print(article["pmid"])
        print(article["title"])
        print(article["abstract"][:300])
        print("-" * 80)
