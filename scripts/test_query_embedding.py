import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.processing.text_extractor import PDFTextExtractor
from app.embeddings.query_embedding import QueryEmbeddingGenerator


PDF_PATH = (
    PROJECT_ROOT
    / "data"
    / "input"
    / "medical_benefit_summary.pdf"
)


def main():

    text_extractor = PDFTextExtractor()

    query_embedding_generator = QueryEmbeddingGenerator()

    text = text_extractor.extract_page_text(
        pdf_path=str(PDF_PATH),
        page_index=0,
    )

    embedding = query_embedding_generator.generate_embedding(
        text
    )

    print(f"Extracted text length: {len(text)} characters")
    print(f"Query embedding shape: {embedding.shape}")
    print(f"Embedding dtype: {embedding.dtype}")


if __name__ == "__main__":
    main()