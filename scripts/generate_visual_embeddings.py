import json
from pathlib import Path

import numpy as np

from app.retrieval.fewshot_loader import load_few_shot_examples
from app.embeddings.visual_embedding import VisualEmbeddingGenerator


PROJECT_ROOT = Path(__file__).resolve().parent.parent

FEWSHOTS_DIR = PROJECT_ROOT / "data" / "fewshots"

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "onnx"
    / "vit_base_patch16.onnx"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "embeddings"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():

    examples = load_few_shot_examples(
        str(FEWSHOTS_DIR)
    )

    generator = VisualEmbeddingGenerator(
        model_path=str(MODEL_PATH)
    )

    embeddings = []
    metadata = []

    for example in examples:

        embedding = generator.generate_embedding(
            example["image_path"]
        )

        embeddings.append(embedding)

        metadata.append({
            "example_id": example["example_id"],
            "image_path": example["image_path"],
            "annotation_path": example["annotation_path"],
        })

        print(
            f"Generated embedding: "
            f"{example['example_id']} "
            f"| Shape: {embedding.shape}"
        )

    embeddings = np.stack(embeddings)

    np.save(
        OUTPUT_DIR / "visual_embeddings.npy",
        embeddings,
    )

    with open(
        OUTPUT_DIR / "visual_metadata.json",
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4,
        )

    print("\nVisual embedding generation completed.")
    print(f"Embedding matrix shape: {embeddings.shape}")


if __name__ == "__main__":
    main()