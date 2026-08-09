from article_discovery.schemas.article import Article


def normalize_arxiv_article(raw_article: dict) -> Article:
    article_url = raw_article["id"]

    external_id = article_url.rstrip("/").split("/")[-1]

    return Article(
        external_id=external_id,
        title=raw_article["title"],
        abstract=raw_article["summary"],
        domain="artificial_intelligence",
        source="arxiv",
        published_at=raw_article["published"],
        url=article_url,
        language="en",
    )
