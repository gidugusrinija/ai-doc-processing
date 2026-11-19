import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.processing.text_extractor import PDFTextExtractor


PDF_PATH = (
    PROJECT_ROOT
    / "data"
    / "input"
    / "medical_benefit_summary.pdf"
)


def main():

    extractor = PDFTextExtractor()

    text = extractor.extract_page_text(
        pdf_path=str(PDF_PATH),
        page_index=0,
    )

    print("\nExtracted text:\n")
    print(text)


if __name__ == "__main__":
    main()