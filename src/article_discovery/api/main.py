from fastapi import FastAPI, Query

from article_discovery.api.schemas import SearchResponse
from article_discovery.search.reranked_search import search_with_reranking


app = FastAPI(title="Multidomain Article Discovery",
              version="0.1.0",)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok"
    }


@app.get("/search", response_model=list[SearchResponse])
def search(query: str = Query(..., min_length=3)
           ) -> list[dict]:
    return search_with_reranking(
        query=query,
        retrieve_k=10,
        final_k=3,
    )
