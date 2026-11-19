import fitz
from pathlib import Path


class PDFTextExtractor:

    def extract_page_text(
        self,
        pdf_path: str,
        page_index: int,
    ) -> str:

        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF not found: {pdf_path}"
            )

        with fitz.open(pdf_path) as document:

            if page_index >= len(document):
                raise IndexError(
                    f"Invalid page index: {page_index}"
                )

            page = document[page_index]

            text = page.get_text("text")

            return text.strip()