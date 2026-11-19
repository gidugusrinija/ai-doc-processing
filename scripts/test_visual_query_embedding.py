import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.embeddings.visual_embedding import VisualEmbeddingGenerator


IMAGE_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed_pages"
    / "page_000.png"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "onnx"
    / "vit_base_patch16.onnx"
)


def main():

    generator = VisualEmbeddingGenerator(
        model_path=str(MODEL_PATH)
    )

    embedding = generator.generate_embedding(
        str(IMAGE_PATH)
    )

    print(f"Visual query embedding shape: {embedding.shape}")
    print(f"Embedding dtype: {embedding.dtype}")


if __name__ == "__main__":
    main()