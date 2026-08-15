from article_discovery.reranking.reranker import rerank_results
from article_discovery.search.semantic_search import semantic_search


def search_with_reranking(
    query: str,
    domain: str | None = None,
    retrieve_k: int = 10,
    final_k: int = 3,
) -> list[dict]:

    candidates = semantic_search(
        query=query,
        top_k=retrieve_k,
        domain=domain,
    )

    try:
        reranked = rerank_results(
            query=query,
            results=candidates,
        )
        return reranked[:final_k]

    except Exception:
        for result in candidates:
            result["reranker_score"] = result["score"]

        return candidates[:final_k]


if __name__ == "__main__":
    query = input("Enter your search query: ").strip()
    results = search_with_reranking(query)

    for position, result in enumerate(results, start=1):
        print(f"{position}. {result['title']}")
        print(f"Retriever score: {result['score']:.4f}")
        print(f"Reranker score: {result['reranker_score']:.4f}")
        print(f"URL: {result['url']}")
        print("-" * 80)
