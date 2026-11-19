import logging
import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.processing.document_processor import DocumentProcessor


# Project paths

PROJECT_ROOT = Path(__file__).resolve().parents[1]

UPLOAD_DIR = PROJECT_ROOT / "data" / "uploads"
OUTPUT_DIR = PROJECT_ROOT / "data" / "outputs"
FRONTEND_DIR = PROJECT_ROOT / "frontend"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# FastAPI application

app = FastAPI(
    title="Medical Benefit PDF Extraction API",
    description="Extract structured insurance benefits from PDF documents.",
    version="1.0.0",
)


# Frontend

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)


@app.get("/")
def root():
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


# Document processing endpoint

@app.post("/api/documents/process")
def process_document(file: UploadFile = File(...)):

    # 1. Validate uploaded file

    if not file.filename or not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    document_id = str(uuid.uuid4())

    pdf_path = UPLOAD_DIR / f"{document_id}.pdf"

    document_output_dir = OUTPUT_DIR / document_id

    logger.info(
        "Received document: %s | ID: %s",
        file.filename,
        document_id,
    )

    try:

        # 2. Save uploaded PDF temporarily

        with pdf_path.open("wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer,
            )

        # 3. Initialize processor

        processor = DocumentProcessor(
            pdf_path=str(pdf_path),
            output_dir=str(document_output_dir),
            dpi=200,
            max_workers=5,
        )

        # 4. Process document

        result = processor.process_document()

        logger.info(
            "Document processing completed | ID: %s",
            document_id,
        )

        # 5. Return results

        return {
            "document_id": document_id,
            "document_name": file.filename,
            "total_pages": result["total_pages"],
            "successful_pages": result["successful_pages"],
            "failed_pages": result["failed_pages"],
            "status": (
                "completed"
                if result["failed_pages"] == 0
                else "completed_with_errors"
            ),
            "pages": result["pages"],
        }

    except Exception as exc:

        logger.exception(
            "Document processing failed | ID: %s",
            document_id,
        )

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )

    finally:

        # 6. Cleanup uploaded PDF

        if pdf_path.exists():

            try:

                pdf_path.unlink()

                logger.info(
                    "Temporary uploaded PDF deleted."
                )

            except OSError:

                logger.exception(
                    "Failed to delete temporary uploaded PDF."
                )


# Application entry point

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )