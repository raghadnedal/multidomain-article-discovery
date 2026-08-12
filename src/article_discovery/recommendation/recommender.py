from article_discovery.recommendation.user_profile import build_user_profile
from article_discovery.reranking.reranker import rerank_results
from article_discovery.search.semantic_search import search_by_embedding


def recommend_articles(
    interests: list[str],
    domain: str | None = None,
    retrieve_k: int = 10,
    final_k: int = 3,
) -> list[dict]:
    user_profile = build_user_profile(interests)

    candidates = search_by_embedding(
        query_embedding=user_profile,
        top_k=retrieve_k,
        domain=domain,
    )

    interest_text = "; ".join(interests)

    reranked = rerank_results(
        query=interest_text,
        results=candidates,
    )

    return reranked[:final_k]
