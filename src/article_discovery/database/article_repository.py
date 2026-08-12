from sqlalchemy import select
from sqlalchemy.orm import Session
from article_discovery.database.models import ArticleModel


def article_exists(
    session: Session, external_id: str
) -> bool:
    article = session.scalar(
        select(ArticleModel).where(
            ArticleModel.external_id == external_id
        )
    )
    return article is not None
