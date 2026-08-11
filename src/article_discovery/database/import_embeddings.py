from pathlib import Path

import numpy as np
from sqlalchemy import select
from sqlalchemy.orm import Session

from article_discovery.database.connection import engine
from article_discovery.database.models import ArticleModel


EMBEDDINGS_PATH = Path("data/processed/arxiv_embeddings.npz")


def import_embeddings() -> None:
    saved_data = np.load(EMBEDDINGS_PATH)

    embeddings = saved_data["embeddings"]
    article_ids = saved_data["article_ids"]

    with Session(engine) as session:
        for article_id, embedding in zip(article_ids, embeddings):
            article = session.scalar(
                select(ArticleModel).where(
                    ArticleModel.external_id == article_id
                )
            )

            if article is None:
                continue

            article.embedding = embedding.tolist()

        session.commit()

    print(f"Imported {len(article_ids)} embeddings.")


if __name__ == "__main__":
    import_embeddings()
