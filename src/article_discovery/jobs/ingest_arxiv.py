from article_discovery.database.save_new_articles import save_new_articles


def run_arxiv_ingestion() -> None:
    save_new_articles(
        max_results=100,
        search_query="cat:cs.AI",
    )


if __name__ == "__main__":
    run_arxiv_ingestion()
