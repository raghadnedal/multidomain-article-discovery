import json
from pathlib import Path

import numpy as np

from article_discovery.embeddings.encoder import load_embedding_model


ARTICLES_PATH = Path("data/processed/arxiv_articles.json")
EMBEDDINGS_PATH = Path("data/processed/arxiv_embeddings.npz")


def semantic_search(query: str, top_k: int = 3) -> list[dict]:
    with ARTICLES_PATH.open("r", encoding="utf-8") as file:
        articles = json.load(file)

    saved_data = np.load(EMBEDDINGS_PATH)

    article_embeddings = saved_data["embeddings"]
    article_ids = saved_data["article_ids"]

    model = load_embedding_model()

    query_embedding = model.encode(
        query,
        normalize_embeddings=True,
    )

    similarity_scores = article_embeddings @ query_embedding

    ranked_indices = np.argsort(similarity_scores)[::-1]

    results = []

    for index in ranked_indices[:top_k]:
        article_id = article_ids[index]

        article = next(
            article
            for article in articles
            if article["external_id"] == article_id
        )

        results.append(
            {
                "external_id": article["external_id"],
                "title": article["title"],
                "abstract": article["abstract"],
                "score": float(similarity_scores[index]),
                "url": article["url"],
            }
        )

    return results


if __name__ == "__main__":
    query = input("Enter your search query: ").strip()

    results = semantic_search(query)

    for position, result in enumerate(results, start=1):
        print(f"{position}. {result['title']}")
        print(f"Score: {result['score']:.4f}")
        print(f"URL: {result['url']}")
        print("-" * 80)
