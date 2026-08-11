import json
from pathlib import Path
from sqlalchemy.orm import Session
from article_discovery.database.connection import engine
from article_discovery.database.models import ArticleModel


ARTICLES_PATH = Path("data/processed/arxiv_articles.json")


def import_articles() -> None:
    with ARTICLES_PATH.open("r", encoding="utf-8") as file:
        articles = json.load(file)
    with Session(engine) as session:
        for article in articles:
            article_model = ArticleModel(
                external_id=article["external_id"],
                title=article["title"],
                abstract=article["abstract"],
                domain=article["domain"],
                source=article["source"],
                published_at=article["published_at"],
                url=article["url"],
                language=article["language"],
            )
            session.merge(article_model)
        session.commit()
    print(f"Imported {len(articles)} articles.")


if __name__ == "__main__":
    import_articles()
