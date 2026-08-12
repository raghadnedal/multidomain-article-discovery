from article_discovery.database.connection import engine
from article_discovery.database.models import ArticleModel
from sqlalchemy.orm import Session
from article_discovery.embeddings.encoder import load_embedding_model
from article_discovery.schemas.article import Article


def save_articles_with_embeddings(
    articles: list[Article],
) -> int:

    texts = [
        f"{article.title}\n\n{article.abstract}"
        for article in articles
    ]

    model = load_embedding_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
    )

    with Session(engine) as session:
        for article, embedding in zip(articles, embeddings):
            article_model = ArticleModel(
                external_id=article.external_id,
                title=article.title,
                abstract=article.abstract,
                domain=article.domain,
                source=article.source,
                published_at=article.published_at,
                url=article.url,
                language=article.language,
                embedding=embedding.tolist(),
            )
            session.add(article_model)
        session.commit()
    return len(articles)
