const fileInput = document.getElementById("fileInput");
const browseButton = document.getElementById("browseButton");
const uploadBox = document.getElementById("uploadBox");
const processButton = document.getElementById("processButton");

const fileDetails = document.getElementById("fileDetails");
const fileNameElement = document.getElementById("fileName");
const fileSizeElement = document.getElementById("fileSize");
const removeFileButton = document.getElementById("removeFile");

const statusSection = document.getElementById("statusSection");
const statusMessage = document.getElementById("statusMessage");

const resultsSection = document.getElementById("resultsSection");
const totalPagesElement = document.getElementById("totalPages");
const successfulPagesElement = document.getElementById("successfulPages");
const failedPagesElement = document.getElementById("failedPages");
const pageResultsElement = document.getElementById("pageResults");

const downloadButton = document.getElementById("downloadButton");

let selectedFile = null;
let processingResult = null;


// Browse files

browseButton.addEventListener("click", () => {
    fileInput.click();
});

fileInput.addEventListener("change", (event) => {
    const file = event.target.files[0];

    if (file) {
        handleFileSelection(file);
    }
});


// Drag and drop

uploadBox.addEventListener("dragover", (event) => {
    event.preventDefault();
    uploadBox.classList.add("drag-over");
});

uploadBox.addEventListener("dragleave", () => {
    uploadBox.classList.remove("drag-over");
});

uploadBox.addEventListener("drop", (event) => {
    event.preventDefault();
    uploadBox.classList.remove("drag-over");

    const file = event.dataTransfer.files[0];

    if (file) {
        handleFileSelection(file);
    }
});


// File selection

function handleFileSelection(file) {
    if (!file.name.toLowerCase().endsWith(".pdf")) {
        alert("Please select a PDF file.");
        return;
    }

    selectedFile = file;

    fileNameElement.textContent = file.name;
    fileSizeElement.textContent = formatFileSize(file.size);

    fileDetails.classList.remove("hidden");
    processButton.disabled = false;

    statusSection.classList.add("hidden");
    resultsSection.classList.add("hidden");

    processingResult = null;
}


// Remove selected file

removeFileButton.addEventListener("click", () => {
    selectedFile = null;

    fileInput.value = "";

    fileDetails.classList.add("hidden");
    processButton.disabled = true;

    statusSection.classList.add("hidden");
    resultsSection.classList.add("hidden");

    processingResult = null;
});


// Process document

processButton.addEventListener("click", async () => {
    if (!selectedFile) {
        alert("Please select a PDF file first.");
        return;
    }

    await processDocument();
});


async function processDocument() {
    const formData = new FormData();

    formData.append("file", selectedFile);

    processButton.disabled = true;
    processButton.textContent = "Processing...";

    statusSection.classList.remove("hidden");
    resultsSection.classList.add("hidden");

    statusMessage.textContent =
        "Document uploaded successfully. AI extraction is in progress. Please wait...";

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/api/documents/process",
            {
                method: "POST",
                body: formData
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Document processing failed.");
        }

        processingResult = result;

        statusMessage.textContent =
            result.status === "completed"
                ? "Document processing completed successfully!"
                : "Document processing completed with some errors.";

        displayResults(result);

    } catch (error) {
        statusMessage.textContent =
            "Error: " + error.message;

        console.error("Processing error:", error);

    } finally {
        processButton.disabled = false;
        processButton.textContent = "Process Document";
    }
}


// Display extraction summary and page results

function displayResults(result) {
    resultsSection.classList.remove("hidden");

    totalPagesElement.textContent = result.total_pages ?? 0;
    successfulPagesElement.textContent = result.successful_pages ?? 0;
    failedPagesElement.textContent = result.failed_pages ?? 0;

    pageResultsElement.innerHTML = "";

    const pages = result.pages || [];

    pages.forEach((page, index) => {
        const pageResult = document.createElement("div");

        pageResult.className = "page-result";

        const pageNumber = page.page_number ?? index + 1;

        const pageStatus = page.status ?? "unknown";

        const isSuccessful = pageStatus === "success";

        pageResult.innerHTML = `
            <div class="page-header">
                <h3>Page ${pageNumber}</h3>
                <span class="page-status ${isSuccessful ? "success" : "failure"}">
                    ${pageStatus.toUpperCase()}
                </span>
            </div>

            <div class="page-content">
                <pre></pre>
            </div>
        `;

        const preElement = pageResult.querySelector("pre");

        preElement.textContent = JSON.stringify(page, null, 2);

        pageResultsElement.appendChild(pageResult);
    });
}


// Download complete JSON result

downloadButton.addEventListener("click", () => {
    if (!processingResult) {
        return;
    }

    const jsonString = JSON.stringify(processingResult, null, 2);

    const blob = new Blob(
        [jsonString],
        { type: "application/json" }
    );

    const downloadUrl = URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = downloadUrl;
    link.download = `${processingResult.document_id}_results.json`;

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);

    URL.revokeObjectURL(downloadUrl);
});


// Utility: file size formatting

function formatFileSize(bytes) {
    if (bytes < 1024) {
        return `${bytes} bytes`;
    }

    if (bytes < 1024 * 1024) {
        return `${(bytes / 1024).toFixed(2)} KB`;
    }

    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}