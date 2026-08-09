import json
from dataclasses import asdict
from pathlib import Path

from article_discovery.schemas.article import Article


def save_articles_to_json(
    articles: list[Article],
    output_path: str,
) -> None:
    path = Path(output_path)

    path.parent.mkdir(parents=True, exist_ok=True)

    article_dicts = [
        asdict(article)
        for article in articles
    ]

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            article_dicts,
            file,
            ensure_ascii=False,
            indent=2,
        )
