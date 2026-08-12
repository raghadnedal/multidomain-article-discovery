from article_discovery.embeddings.encoder import load_embedding_model
import numpy as np


def build_user_profile(interests: list[str]) -> list[float]:
    if not interests:
        raise ValueError("interests must not be empty")
    model = load_embedding_model()
    interest_embeddings = model.encode(
        interests,
        normalize_embeddings=True
    )
    user_profile = np.mean(
        interest_embeddings,
        axis=0,
    )
    # Scale the user profile vector to length 1 for cosine similarity
    user_profile = user_profile / np.linalg.norm(user_profile)
    return user_profile.tolist()


if __name__ == "__main__":
    interests = [
        "AI safety",
        "reinforcement learning",
        "medical imaging",
    ]

    profile = build_user_profile(interests)

    print(type(profile))
    print(len(profile))
    print(np.linalg.norm(profile))
