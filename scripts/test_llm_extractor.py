import sys
import json
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.retrieval.fewshot_retrieval import FewShotRetrieval
from app.extraction.llm_extractor import MultimodalLLMExtractor
from app.schemas.schemas import BenefitExtraction


EMBEDDINGS_DIR = PROJECT_ROOT / "data" / "embeddings"
TARGET_IMAGE = PROJECT_ROOT / "data" / "processed_pages" / "page_000.png"

OUTPUT_DIR = PROJECT_ROOT / "data" / "outputs"


def main():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load query embedding
    query_embedding = np.load(
        EMBEDDINGS_DIR / "query_hybrid_embedding.npy"
    )

    # Retrieve relevant few-shot examples
    retrieval = FewShotRetrieval(
        embeddings_dir=str(EMBEDDINGS_DIR)
    )

    examples = retrieval.retrieve_examples(
        query_embedding=query_embedding,
        top_k=3,
    )

    print("Retrieved examples:")

    for example in examples:
        print(
            f"{example['example_id']} "
            f"({example['similarity_score']:.4f})"
        )

    # Initialize multimodal LLM
    extractor = MultimodalLLMExtractor()

    # Extract information from target page
    result = extractor.extract(
        target_image=str(TARGET_IMAGE),
        fewshot_examples=examples,
    )

    validated_result = BenefitExtraction.model_validate(result)

    result = validated_result.model_dump()

    # Save extraction output
    output_path = OUTPUT_DIR / "page_000.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            result,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print("\nExtraction completed!")
    print(f"Output saved to: {output_path}")

    print("\nExtracted JSON:")
    print(json.dumps(result, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()