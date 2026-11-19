import sys
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.embeddings.embedding_reducer import EmbeddingReducer


EMBEDDINGS_DIR = PROJECT_ROOT / "data" / "embeddings"

EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)


def main():

    visual_embeddings = np.load(
        EMBEDDINGS_DIR / "visual_embeddings.npy"
    )

    semantic_embeddings = np.load(
        EMBEDDINGS_DIR / "semantic_embeddings.npy"
    )

    reducer = EmbeddingReducer(
        target_dimension=512
    )

    visual_reduced, semantic_reduced, hybrid_embeddings = (
        reducer.fit_transform(
            visual_embeddings,
            semantic_embeddings,
        )
    )

    np.save(
        EMBEDDINGS_DIR / "visual_reduced.npy",
        visual_reduced,
    )

    np.save(
        EMBEDDINGS_DIR / "semantic_reduced.npy",
        semantic_reduced,
    )

    np.save(
        EMBEDDINGS_DIR / "hybrid_embeddings.npy",
        hybrid_embeddings,
    )

    reducer.save(
        str(EMBEDDINGS_DIR / "reducer.joblib")
    )

    print("Dimensionality reduction completed.")
    print(f"Visual: {visual_reduced.shape}")
    print(f"Semantic: {semantic_reduced.shape}")
    print(f"Hybrid: {hybrid_embeddings.shape}")
    print("Reducer saved successfully.")


if __name__ == "__main__":
    main()