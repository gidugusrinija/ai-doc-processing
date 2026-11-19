# AI-Powered Medical Benefit PDF Extraction

An AI-powered document processing system that extracts structured medical insurance benefit information from PDF documents using multimodal embeddings, semantic retrieval, and Large Language Models (LLMs).

The application processes medical benefit summary PDFs, converts pages into images, retrieves relevant few-shot examples using hybrid visual and semantic similarity, and generates structured JSON outputs validated using Pydantic schemas.

## Features

- **PDF Processing:** Converts PDF documents into page images using Poppler.
- **Parallel Processing:** Processes multiple PDF pages concurrently using Python's `ThreadPoolExecutor`.
- **Visual Embeddings:** Generates image embeddings using Vision Transformer (ViT-B/16) through ONNX Runtime.
- **Semantic Embeddings:** Generates text embeddings using OpenAI's embedding models.
- **Hybrid Embeddings:** Combines visual and semantic embeddings using dimensionality reduction.
- **Vector Search:** Uses FAISS for similarity-based retrieval of relevant few-shot examples.
- **Few-Shot Learning:** Retrieves relevant examples dynamically to improve LLM extraction accuracy.
- **LLM-Based Extraction:** Extracts structured medical benefit information from PDF pages.
- **Schema Validation:** Validates extracted information using Pydantic models.
- **REST API:** Provides document processing functionality through FastAPI.
- **Web Interface:** Supports PDF upload and displays extraction results.
- **Automated Cleanup:** Removes temporary uploaded PDFs and generated page images after processing.

## Tech Stack

- Python
- FastAPI
- Pydantic
- FAISS
- ONNX Runtime
- Vision Transformer (ViT)
- OpenAI Embeddings
- Large Language Models (LLMs)
- PDF2Image
- Poppler
- NumPy
- Scikit-learn

## Processing Pipeline

1. Upload a medical benefit summary PDF.
2. Convert PDF pages into images.
3. Extract digital text from PDF pages.
4. Generate visual and semantic embeddings.
5. Reduce and combine embeddings into hybrid representations.
6. Retrieve relevant few-shot examples using FAISS.
7. Pass the page content and retrieved examples to an LLM.
8. Extract structured benefit information.
9. Validate the output using Pydantic schemas.
10. Save page-level and document-level JSON results.
11. Clean up temporary files.

## Architecture

PDF Upload → PDF Conversion → Parallel Page Processing → Hybrid Embeddings → FAISS Retrieval → Few-Shot Context → LLM Extraction → Pydantic Validation → JSON Output

## Output

The system generates:

- Page-level JSON extraction results
- Aggregated document-level JSON
- Processing statistics, including successful and failed pages

## API

### Process Document

`POST /api/documents/process`

Upload a PDF file to process and extract structured medical benefit information.

### API Documentation

`/docs`

Interactive API documentation is available through Swagger UI.

## Project Status

Currently under development.
