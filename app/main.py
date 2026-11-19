import logging
import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

from fastapi.responses import RedirectResponse

from app.processing.document_processor import DocumentProcessor
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]

UPLOAD_DIR = PROJECT_ROOT / "data" / "uploads"
OUTPUT_DIR = PROJECT_ROOT / "data" / "outputs"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FRONTEND_DIR = PROJECT_ROOT / "frontend"


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

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)

@app.get("/")
def root():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.post("/api/documents/process")
def process_document(file: UploadFile = File(...)):

    # Validate uploaded file
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    # Generate unique document ID
    document_id = str(uuid.uuid4())

    # Save uploaded PDF
    pdf_path = UPLOAD_DIR / f"{document_id}.pdf"

    with pdf_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    logger.info(
        "Received document: %s | ID: %s",
        file.filename,
        document_id,
    )

    # Create document-specific output directory
    document_output_dir = OUTPUT_DIR / document_id

    # Initialize processor
    processor = DocumentProcessor(
        pdf_path=str(pdf_path),
        output_dir=str(document_output_dir),
        dpi=200,
        max_workers=5,
    )

    # Process document
    try:
        result = processor.process_document()

    except Exception as exc:
        logger.exception("Document processing failed")

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )

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
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )