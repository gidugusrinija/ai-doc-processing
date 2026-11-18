
from app.pdf_processor import convert_pdf_to_images


def main():

    pdf_path = (
        "data/input/medical_benefit_summary.pdf"
    )

    output_dir = "data/processed_pages"

    # Set this to your Poppler bin directory on Windows.
    poppler_path = (
        r"C:\poppler\Library\bin"
    )

    pages = convert_pdf_to_images(
        pdf_path=pdf_path,
        output_dir=output_dir,
        dpi=200,
        poppler_path=poppler_path
    )

    print("\nPDF conversion completed!")

    print("Total pages:", len(pages))

    for page in pages:
        print(page)


if __name__ == "__main__":
    main()
