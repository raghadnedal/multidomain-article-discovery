from sentence_transformers import CrossEncoder


RERANKER_MODEL_NAME = "BAAI/bge-reranker-v2-m3"


def load_reranker() -> CrossEncoder:
    return CrossEncoder(RERANKER_MODEL_NAME)


def rerank_results(
    query: str,
    results: list[dict],
) -> list[dict]:
    model = load_reranker()

    pairs = [
        (
            query,
            f"{result['title']}\n\n{result['abstract']}",
        )
        for result in results
    ]

    scores = model.predict(pairs)

    reranked_results = []

    for result, score in zip(results, scores):
        reranked_result = result.copy()
        reranked_result["reranker_score"] = float(score)
        reranked_results.append(reranked_result)

    return sorted(
        reranked_results,
        key=lambda result: result["reranker_score"],
        reverse=True,
    )
