from concurrent.futures import ThreadPoolExecutor, as_completed


def process_pages_parallel(
    pages: list,
    page_processor,
    max_workers: int = 5,
):
    """
    Process PDF pages concurrently.

    Args:
        pages: List of page metadata dictionaries.
        page_processor: Function responsible for processing one page.
        max_workers: Maximum number of concurrent workers.

    Returns:
        Results sorted by original page index.
    """

    results = {}

    print(f"\nStarting parallel processing with {max_workers} workers...")
    print(f"Total pages to process: {len(pages)}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:

        # Submit each page as an independent task
        future_to_page = {
            executor.submit(page_processor, page): page
            for page in pages
        }

        # Collect results as tasks complete
        for future in as_completed(future_to_page):

            page = future_to_page[future]
            page_index = page["page_index"]

            try:
                result = future.result()

                results[page_index] = result

                print(f"Completed page index: {page_index}")

            except Exception as exc:

                print(
                    f"Error processing page index {page_index}: {exc}"
                )

                results[page_index] = {
                    "page_index": page_index,
                    "status": "failed",
                    "error": str(exc),
                }

    # Restore original PDF page order
    ordered_results = [
        results[page_index]
        for page_index in sorted(results)
    ]

    print("\nParallel processing completed.")

    return ordered_results