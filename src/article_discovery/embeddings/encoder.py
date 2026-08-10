from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-m3"


def load_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME, local_files_only=True,)


def encode_text(
    model: SentenceTransformer,
    text: str
) -> list[float]:
    embedding = model.encode(text, normalize_embeddings=True)

    return embedding.tolist()


if __name__ == "__main__":
    model = load_embedding_model()
    text = "Artificial intelligence for medical diagnosis"
    embedding = encode_text(model, text)
    print("Embedding length:", len(embedding))
    print("First 5 values:", embedding[:5])
