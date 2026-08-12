from sqlalchemy import select
from sqlalchemy.orm import Session

from article_discovery.database.connection import engine
from article_discovery.database.models import ArticleModel
from article_discovery.embeddings.encoder import load_embedding_model


def semantic_search(
    query: str,
    top_k: int = 3,
    domain: str | None = None,
) -> list[dict]:
    model = load_embedding_model()

    query_embedding = model.encode(
        query,
        normalize_embeddings=True,
    )

    distance = ArticleModel.embedding.cosine_distance(
        query_embedding.tolist()
    )

    statement = (
        select(ArticleModel, distance.label("distance"))
        .where(ArticleModel.embedding.is_not(None))
    )

    if domain is not None:
        domain = domain.strip()
        statement = statement.where(
            ArticleModel.domain == domain
        )

    statement = (
        statement
        .order_by(distance)
        .limit(top_k)
    )

    results = []

    with Session(engine) as session:
        rows = session.execute(statement)

        for article, cosine_distance in rows:
            results.append({
                "external_id": article.external_id,
                "title": article.title,
                "abstract": article.abstract,
                "score": 1 - float(cosine_distance),
                "url": article.url,
            })

    return results


if __name__ == "__main__":
    query = input("Enter your search query: ").strip()

    results = semantic_search(query)

    for position, result in enumerate(results, start=1):
        print(f"{position}. {result['title']}")
        print(f"Score: {result['score']:.4f}")
        print(f"URL: {result['url']}")
        print("-" * 80)
