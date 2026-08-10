from article_discovery.search.semantic_search import semantic_search
from article_discovery.reranking.reranker import rerank_results


def search_with_reranking(
    query: str,
    retrieve_k: int = 10,
    final_k: int = 3,
) -> list[dict]:
    candidate = semantic_search(
        query=query,
        top_k=retrieve_k,
    )

    reranked = rerank_results(
        query=query,
        results=candidate,
    )
    return reranked[:final_k]


if __name__ == "__main__":
    query = input("Enter your search query: ").strip()
    results = search_with_reranking(query)

    for position, result in enumerate(results, start=1):
        print(f"{position}. {result['title']}")
        print(f"Retriever score: {result['score']:.4f}")
        print(f"Reranker score: {result['reranker_score']:.4f}")
        print(f"URL: {result['url']}")
        print("-" * 80)
