from dataclasses import dataclass


@dataclass
class Article:
    external_id: str
    title: str
    abstract: str
    domain: str
    source: str
    published_at: str
    url: str
    language: str
