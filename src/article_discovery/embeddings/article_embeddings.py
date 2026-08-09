import json
from pathlib import Path

import numpy as np

from article_discovery.embeddings.encoder import load_embedding_model


ARTICLES_PATH = Path("data/processed/arxiv_articles.json")
OUTPUT_PATH = Path("data/processed/arxiv_embeddings.npz")


def create_article_embeddings() -> None:
    with ARTICLES_PATH.open("r", encoding="utf-8") as file:
        articles = json.load(file)

    article_ids = [
        article["external_id"]
        for article in articles
    ]

    article_texts = [
        f"{article['title']}\n\n{article['abstract']}"
        for article in articles
    ]

    model = load_embedding_model()

    embeddings = model.encode(
        article_texts,
        show_progress_bar=True,
        normalize_embeddings=True,
    )

    np.savez(
        OUTPUT_PATH,
        embeddings=embeddings,
        article_ids=article_ids,
    )

    print("Articles encoded:", len(articles))
    print("Embeddings shape:", embeddings.shape)
    print("Saved to:", OUTPUT_PATH)


if __name__ == "__main__":
    create_article_embeddings()
