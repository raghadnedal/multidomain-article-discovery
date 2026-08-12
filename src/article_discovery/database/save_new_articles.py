from article_discovery.ingestion.arxiv_client import fetch_new_articles
from article_discovery.database.article_service import save_articles_with_embeddings


def save_new_articles(
    max_results: int = 100,
    search_query: str = "cat:cs.AI",
) -> None:
    articles = fetch_new_articles(
        max_results=max_results,
        search_query=search_query,
    )
    saved_count = save_articles_with_embeddings(articles)
    if saved_count == 0:
        print("No new articles found.")
        return
    print(f"Saved {saved_count} new articles.")


if __name__ == "__main__":
    save_new_articles(
        max_results=20,
        search_query="cat:cs.LG",
    )
