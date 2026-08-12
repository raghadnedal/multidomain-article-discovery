from article_discovery.database.article_service import save_articles_with_embeddings
from article_discovery.ingestion.pubmed_client import fetch_new_pubmed_articles


MEDICAL_QUERIES = [
    "cancer",
    "cardiology",
    "diabetes",
    "neurology",
    "infectious diseases",
    "public health",
]


def run_pubmed_ingestion() -> None:
    total_saved = 0

    for query in MEDICAL_QUERIES:
        articles = fetch_new_pubmed_articles(
            query=query,
            max_results=20,
        )

        saved_count = save_articles_with_embeddings(articles)
        total_saved += saved_count

        print(f"{query}: saved {saved_count} new articles.")

    print(f"Total saved PubMed articles: {total_saved}")


if __name__ == "__main__":
    run_pubmed_ingestion()
