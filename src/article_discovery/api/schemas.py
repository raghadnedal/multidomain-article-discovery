from pydantic import BaseModel


class HealthResponse (BaseModel):
    status: str


class SearchResponse (BaseModel):
    external_id: str
    title: str
    abstract: str
    score: float
    reranker_score: float
    url: str
