
import fitz
import pymupdf

def extract_pdf_text(pdf_bytes: bytes) -> list[dict]:
    """Extract text page by page from an uploaded PDF."""

    # Check for empty uploads
    if not pdf_bytes:
        raise ValueError("The uploaded file is empty.")

    # Check the PDF signature
    if not pdf_bytes.startswith(b"%PDF-"):
        raise ValueError(
            "Invalid PDF file. Please upload a valid PDF document."
        )

    pages = []

    try:
        with fitz.open(stream=pdf_bytes, filetype="pdf") as pdf:
            if pdf.page_count == 0:
                raise ValueError("The PDF contains no pages.")

            for page_number, page in enumerate(pdf, start=1):
                text = page.get_text("text").strip()

                pages.append({
                    "page": page_number,
                    "text": text
                })

    except fitz.FileDataError as e:
        raise ValueError(
            "The PDF is corrupted or has an unsupported format."
        ) from e

    if not any(page["text"] for page in pages):
        raise ValueError(
            "No selectable text was found. "
            "This may be a scanned PDF requiring OCR."
        )

    return pages