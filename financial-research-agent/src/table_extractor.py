import pdfplumber


def clean_cell(cell):
    """Clean a table cell."""

    if cell is None:
        return ""

    return str(cell).strip()


def extract_pdf_tables(pdf_bytes: bytes) -> list[dict]:
    """
    Extract tables from every page of a PDF.

    Returns:
        [
            {
                "page": 1,
                "table_index": 0,
                "rows": [...]
            }
        ]
    """

    if not pdf_bytes:
        raise ValueError("The uploaded PDF is empty.")

    if not pdf_bytes.startswith(b"%PDF-"):
        raise ValueError("Invalid PDF file.")

    tables = []

    with pdfplumber.open(
        __import__("io").BytesIO(pdf_bytes)
    ) as pdf:

        for page_number, page in enumerate(
            pdf.pages,
            start=1
        ):

            page_tables = page.extract_tables()

            for table_index, table in enumerate(
                page_tables
            ):

                if not table:
                    continue

                cleaned_rows = []

                for row in table:

                    cleaned_row = [
                        clean_cell(cell)
                        for cell in row
                    ]

                    # Ignore completely empty rows
                    if any(cleaned_row):
                        cleaned_rows.append(
                            cleaned_row
                        )

                if cleaned_rows:
                    tables.append({
                        "page": page_number,
                        "table_index": table_index,
                        "rows": cleaned_rows
                    })

    return tables