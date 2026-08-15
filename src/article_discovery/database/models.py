from sqlalchemy import String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pgvector.sqlalchemy import Vector
from datetime import datetime
from sqlalchemy import DateTime


class Base(DeclarativeBase):
    pass


class ArticleModel(Base):
    __tablename__ = "articles"

    external_id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    abstract: Mapped[str] = mapped_column(Text)
    domain: Mapped[str] = mapped_column(String)
    source: Mapped[str] = mapped_column(String)
    published_at: Mapped[str | None] = mapped_column(String)
    url: Mapped[str] = mapped_column(Text)
    language: Mapped[str] = mapped_column(String)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1024))
