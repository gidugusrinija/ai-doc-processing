import sys
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.embeddings.visual_embedding import VisualEmbeddingGenerator
from app.processing.text_extractor import PDFTextExtractor
from app.embeddings.query_embedding import QueryEmbeddingGenerator
from app.embeddings.embedding_reducer import EmbeddingReducer


PDF_PATH = PROJECT_ROOT / "data" / "input" / "medical_benefit_summary.pdf"

IMAGE_PATH = PROJECT_ROOT / "data" / "processed_pages" / "page_000.png"

MODEL_PATH = PROJECT_ROOT / "models" / "onnx" / "vit_base_patch16.onnx"

EMBEDDINGS_DIR = PROJECT_ROOT / "data" / "embeddings"


def main():

    # 1. Generate visual query embedding
    visual_generator = VisualEmbeddingGenerator(
        model_path=str(MODEL_PATH)
    )

    visual_embedding = visual_generator.generate_embedding(
        str(IMAGE_PATH)
    )

    # 2. Extract semantic text
    text_extractor = PDFTextExtractor()

    page_text = text_extractor.extract_page_text(
        pdf_path=str(PDF_PATH),
        page_index=0,
    )

    # 3. Generate semantic query embedding
    semantic_generator = QueryEmbeddingGenerator()

    semantic_embedding = semantic_generator.generate_embedding(
        page_text
    )

    # 4. Load fitted reducers
    reducer = EmbeddingReducer.load(
        str(EMBEDDINGS_DIR / "reducer.joblib")
    )

    # 5. Reduce query embeddings
    visual_reduced, semantic_reduced, hybrid_embedding = (
        reducer.transform(
            visual_embedding.reshape(1, -1),
            semantic_embedding.reshape(1, -1),
        )
    )

    # 6. Save query embedding
    np.save(
        EMBEDDINGS_DIR / "query_hybrid_embedding.npy",
        hybrid_embedding,
    )

    print("\nQuery embedding generation completed.")
    print(f"Visual: {visual_embedding.shape}")
    print(f"Semantic: {semantic_embedding.shape}")
    print(f"Visual reduced: {visual_reduced.shape}")
    print(f"Semantic reduced: {semantic_reduced.shape}")
    print(f"Hybrid: {hybrid_embedding.shape}")


if __name__ == "__main__":
    main()