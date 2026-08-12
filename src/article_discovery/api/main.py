from fastapi import FastAPI, Query

from article_discovery.api.schemas import SearchResponse, RecommendationRequest
from article_discovery.search.reranked_search import search_with_reranking
from article_discovery.recommendation.recommender import recommend_articles
from enum import Enum

app = FastAPI(title="Multidomain Article Discovery",
              version="0.1.0",)


class Domain(str, Enum):
    medicine = "medicine"
    artificial_intelligence = "artificial_intelligence"


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok"
    }


@app.get("/search", response_model=list[SearchResponse])
def search(
    query: str = Query(..., min_length=3),
    domain: Domain | None = None,
) -> list[dict]:
    return search_with_reranking(
        query=query,
        retrieve_k=10,
        final_k=3,
        domain=domain,
    )


@app.post("/recommend", response_model=list[SearchResponse])
def recommend(
    request: RecommendationRequest,
) -> list[dict]:
    return recommend_articles(
        interests=request.interests,
        retrieve_k=10,
        final_k=3,
    )
