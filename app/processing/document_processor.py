import json
import logging
from pathlib import Path

from app.processing.pdf_processor import convert_pdf_to_images
from app.processing.executor import process_pages_parallel
from app.processing.page_processor import process_single_page
from app.utils.poppler_utils import get_poppler_path


logger = logging.getLogger(__name__)


class DocumentProcessor:

    def __init__(
        self,
        pdf_path: str,
        output_dir: str,
        dpi: int = 200,
        max_workers: int = 5,
    ):

        self.pdf_path = Path(pdf_path)
        self.output_dir = Path(output_dir)

        self.processed_pages_dir = (
            self.output_dir / "processed_pages"
        )

        self.results_dir = (
            self.output_dir / "results"
        )

        self.dpi = dpi
        self.max_workers = max_workers

        self.results_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def process_document(self):

        logger.info(
            "Starting document processing: %s",
            self.pdf_path.name,
        )

        # -----------------------------------------
        # 1. Convert PDF into page images
        # -----------------------------------------

        pages = convert_pdf_to_images(
            pdf_path=str(self.pdf_path),
            output_dir=str(self.processed_pages_dir),
            dpi=self.dpi,
            poppler_path=get_poppler_path(),
        )

        logger.info(
            "PDF converted into %s pages",
            len(pages),
        )

        # -----------------------------------------
        # 2. Process pages concurrently
        # -----------------------------------------

        page_results = process_pages_parallel(
            pages=pages,
            page_processor=process_single_page,
            max_workers=self.max_workers,
        )

        # -----------------------------------------
        # 3. Save individual page results
        # -----------------------------------------

        for result in page_results:

            page_number = result["page_number"]

            page_output_path = (
                self.results_dir
                / f"page_{page_number:03d}.json"
            )

            with open(
                page_output_path,
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(
                    result,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

        # -----------------------------------------
        # 4. Aggregate document results
        # -----------------------------------------

        successful_pages = [
            result
            for result in page_results
            if result.get("status") == "completed"
        ]

        failed_pages = [
            result
            for result in page_results
            if result.get("status") == "failed"
        ]

        document_result = {
            "document_name": self.pdf_path.name,
            "total_pages": len(pages),
            "successful_pages": len(successful_pages),
            "failed_pages": len(failed_pages),
            "pages": page_results,
        }

        # -----------------------------------------
        # 5. Save final document JSON
        # -----------------------------------------

        document_output_path = (
            self.results_dir
            / "document_result.json"
        )

        with open(
            document_output_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                document_result,
                file,
                indent=4,
                ensure_ascii=False,
            )

        logger.info(
            "Document processing completed. "
            "Successful: %s | Failed: %s",
            len(successful_pages),
            len(failed_pages),
        )

        return document_result