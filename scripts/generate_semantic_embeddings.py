import sys
import json
import numpy as np

from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

from app.retrieval.fewshot_loader import load_few_shot_examples
from app.embeddings.semantic_embedding import SemanticEmbeddingGenerator


FEWSHOTS_DIR = PROJECT_ROOT / "data" / "fewshots"

OUTPUT_DIR = PROJECT_ROOT / "data" / "embeddings"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():

    examples = load_few_shot_examples(
        str(FEWSHOTS_DIR)
    )

    generator = SemanticEmbeddingGenerator()

    embeddings = []
    metadata = []

    for example in examples:

        embedding = generator.generate_embedding(
            example["annotation"]
        )

        embeddings.append(embedding)

        metadata.append({
            "example_id": example["example_id"],
            "image_path": example["image_path"],
            "annotation_path": example["annotation_path"],
        })

        print(
            f"Generated semantic embedding: "
            f"{example['example_id']} "
            f"| Shape: {embedding.shape}"
        )

    embeddings = np.stack(embeddings)

    np.save(
        OUTPUT_DIR / "semantic_embeddings.npy",
        embeddings,
    )

    with open(
        OUTPUT_DIR / "semantic_metadata.json",
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(metadata, file, indent=4)

    print("\nSemantic embedding generation completed.")
    print(f"Embedding matrix shape: {embeddings.shape}")


if __name__ == "__main__":
    main()