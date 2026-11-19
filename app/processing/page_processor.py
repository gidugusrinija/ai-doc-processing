import logging
from pathlib import Path

from app.embeddings.visual_embedding import VisualEmbeddingGenerator
from app.embeddings.query_embedding import QueryEmbeddingGenerator
from app.embeddings.embedding_reducer import EmbeddingReducer

from app.processing.text_extractor import PDFTextExtractor

from app.retrieval.fewshot_retrieval import FewShotRetrieval

from app.extraction.llm_extractor import MultimodalLLMExtractor

from app.schemas.schemas import BenefitExtraction

logger = logging.getLogger(__name__)

# Dynamically determine project root from this file's location
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def process_single_page(page: dict) -> dict:
    page_index = page["page_index"]
    page_number = page["page_number"]
    image_path = Path(page["image_path"])

    if not image_path.exists():
        raise FileNotFoundError(f"Page image not found: {image_path}")

    # Project paths
    pdf_path = (
        PROJECT_ROOT
        / "data"
        / "input"
        / "medical_benefit_summary.pdf"
    )

    embeddings_dir = (
        PROJECT_ROOT
        / "data"
        / "embeddings"
    )

    model_path = (
        PROJECT_ROOT
        / "models"
        / "onnx"
        / "vit_base_patch16.onnx"
    )

    logger.info("Processing page %s", page_number)

    # 1. Generate visual embedding
    visual_generator = VisualEmbeddingGenerator(
        model_path=str(model_path)
    )

    visual_embedding = visual_generator.generate_embedding(
        str(image_path)
    )

    # 2. Extract text from PDF page
    text_extractor = PDFTextExtractor()

    page_text = text_extractor.extract_page_text(
        pdf_path=str(pdf_path),
        page_index=page_index,
    )

    # 3. Generate semantic embedding
    semantic_generator = QueryEmbeddingGenerator()

    semantic_embedding = semantic_generator.generate_embedding(
        page_text
    )

    # 4. Generate hybrid embedding
    reducer = EmbeddingReducer.load(
        str(embeddings_dir / "reducer.joblib")
    )

    _, _, hybrid_embedding = reducer.transform(
        visual_embedding.reshape(1, -1),
        semantic_embedding.reshape(1, -1),
    )

    # 5. Retrieve relevant few-shot examples
    fewshot_retrieval = FewShotRetrieval(
        embeddings_dir=str(embeddings_dir)
    )

    examples = fewshot_retrieval.retrieve_examples(
        query_embedding=hybrid_embedding,
        top_k=3,
    )

    # 6. Extract structured information using multimodal LLM
    llm_extractor = MultimodalLLMExtractor()

    extracted_data = llm_extractor.extract(
        target_image=str(image_path),
        fewshot_examples=examples,
    )

    # 7. Validate extracted data
    validated_data = BenefitExtraction.model_validate(
        extracted_data
    )

    # 8. Return page result
    result = {
        "page_index": page_index,
        "page_number": page_number,
        "status": "completed",
        "image_path": str(image_path),
        "extracted_data": validated_data.model_dump(),
    }

    logger.info(
        "Successfully processed page %s",
        page_number,
    )

    return result