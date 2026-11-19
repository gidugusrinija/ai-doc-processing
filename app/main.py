from pathlib import Path

from app.pdf_processor import convert_pdf_to_images
from app.poppler_utils import get_poppler_path
from app.executor import process_pages_parallel
from app.page_processor import process_single_page


def main():

    project_root = Path(__file__).parent

    pdf_path = (
        project_root
        / "data"
        / "input"
        / "medical_benefit_summary.pdf"
    )

    output_dir = (
        project_root
        / "data"
        / "processed_pages"
    )

    # Step 1: Detect Poppler dynamically
    poppler_path = get_poppler_path()

    print(f"Poppler path: {poppler_path}")

    # Step 2: Convert PDF into images
    pages = convert_pdf_to_images(
        pdf_path=str(pdf_path),
        output_dir=str(output_dir),
        dpi=200,
        poppler_path=poppler_path,
    )

    # Step 3: Process pages in parallel
    results = process_pages_parallel(
        pages=pages,
        page_processor=process_single_page,
        max_workers=5,
    )

    # Step 4: Display final results in PDF order
    print("\nFinal Results:")

    for result in results:
        print(
            f"Page {result['page_number']} "
            f"| Status: {result['status']}"
        )

    print("\nPipeline execution completed.")


if __name__ == "__main__":
    main()