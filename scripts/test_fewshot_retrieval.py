import sys
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.retrieval.fewshot_retrieval import FewShotRetrieval

EMBEDDINGS_DIR = PROJECT_ROOT / "data" / "embeddings"


def main():

    query_embedding = np.load(
        EMBEDDINGS_DIR / "query_hybrid_embedding.npy"
    )

    retrieval = FewShotRetrieval(
        embeddings_dir=str(EMBEDDINGS_DIR)
    )

    examples = retrieval.retrieve_examples(
        query_embedding=query_embedding,
        top_k=3,
    )

    for example in examples:

        print(f"\nExample ID: {example['example_id']}")
        print(f"Similarity: {example['similarity_score']:.4f}")
        print(f"Image: {example['image_path']}")

        print("\nAnnotation:")
        print(example["annotation"])

        print("-" * 60)


if __name__ == "__main__":
    main()