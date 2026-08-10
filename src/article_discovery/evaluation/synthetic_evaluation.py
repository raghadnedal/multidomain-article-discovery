import json
from pathlib import Path

from article_discovery.search.reranked_search import search_with_reranking


CASES_PATH = Path("data/evaluation/synthetic_cases.json")


def evaluate_hit_rate(top_k: int = 3) -> float:
    with CASES_PATH.open("r", encoding="utf-8") as file:
        cases = json.load(file)

    hits = 0

    for case in cases:
        query = case["query"]
        expected_article_id = case["expected_article_id"]

        results = search_with_reranking(
            query=query,
            retrieve_k=10,
            final_k=top_k,
        )

        returned_article_ids = [
            result.get("external_id")
            or result["url"].rstrip("/").split("/")[-1]
            for result in results
        ]

        is_hit = expected_article_id in returned_article_ids

        if is_hit:
            hits += 1

        print("Query:", query)
        print("Expected ID:", expected_article_id)
        print("Returned IDs:", returned_article_ids)
        print("Hit:", is_hit)
        print("-" * 80)

    hit_rate = hits / len(cases)

    print(f"Hit Rate@{top_k}: {hit_rate:.2f}")

    return hit_rate


if __name__ == "__main__":
    evaluate_hit_rate(top_k=1)
