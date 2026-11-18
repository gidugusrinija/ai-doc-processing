
from pdf2image import convert_from_path, pdfinfo_from_path
from pathlib import Path


def convert_pdf_to_images(
    pdf_path: str,
    output_dir: str,
    dpi: int = 200,
    poppler_path: str = None
):
    """
    Convert PDF pages into images using Poppler.

    Returns page metadata with original page indices.
    """

    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # Get PDF metadata
    info = pdfinfo_from_path(
        str(pdf_path),
        poppler_path=poppler_path
    )

    total_pages = int(info["Pages"])

    print(f"Total PDF pages: {total_pages}")

    # Convert PDF pages into PIL images
    images = convert_from_path(
        str(pdf_path),
        dpi=dpi,
        fmt="png",
        poppler_path=poppler_path,
        thread_count=2
    )

    page_results = []

    for page_index, image in enumerate(images):

        image_path = (
            output_dir /
            f"page_{page_index:03d}.png"
        )

        image.save(
            image_path,
            "PNG"
        )

        page_results.append({
            "page_index": page_index,
            "page_number": page_index + 1,
            "image_path": str(image_path)
        })

        print(
            f"Converted page {page_index + 1}/{total_pages}"
        )

    return page_results
