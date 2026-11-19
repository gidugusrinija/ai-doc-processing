import logging
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))

from app.processing.document_processor import DocumentProcessor


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def main():

    pdf_path = (
        PROJECT_ROOT
        / "data"
        / "input"
        / "medical_benefit_summary.pdf"
    )

    output_dir = PROJECT_ROOT / "data" / "outputs"

    processor = DocumentProcessor(
        pdf_path=str(pdf_path),
        output_dir=str(output_dir),
        dpi=200,
        max_workers=5,
    )

    result = processor.process_document()

    print("\n" + "=" * 50)
    print("DOCUMENT PROCESSING SUMMARY")
    print("=" * 50)

    print(f"Document: {result['document_name']}")
    print(f"Total pages: {result['total_pages']}")
    print(f"Successful: {result['successful_pages']}")
    print(f"Failed: {result['failed_pages']}")

    print("\nOutput location:")
    print(output_dir / "results" / "document_result.json")


if __name__ == "__main__":
    main()