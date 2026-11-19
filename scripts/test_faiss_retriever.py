import sys
import numpy as np

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.retrieval.faiss_retriever import FAISSRetriever


EMBEDDINGS_DIR = PROJECT_ROOT / "data" / "embeddings"


def main():

    retriever = FAISSRetriever(
        embeddings_dir=str(EMBEDDINGS_DIR)
    )

    hybrid_embeddings = np.load(
        EMBEDDINGS_DIR / "hybrid_embeddings.npy"
    )

    query_embedding = hybrid_embeddings[0]

    results = retriever.retrieve(
        query_embedding=query_embedding,
        top_k=3,
    )

    print("\nRetrieved examples:\n")

    for result in results:

        print(
            f"Example: {result['example_id']} | "
            f"Score: {result['similarity_score']:.4f}"
        )

        print(f"Image: {result['image_path']}")
        print(f"JSON: {result['annotation_path']}")
        print("-" * 50)


if __name__ == "__main__":
    main()