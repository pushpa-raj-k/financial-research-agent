from pathlib import Path
from datetime import datetime, timezone
import re


def safe_filename(name: str) -> str:
    """Convert text into a safe filename."""

    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "-", name)
    return name.strip("-")


def create_okf_bundle(
    pages: list[dict],
    report_name: str,
    report_id: str,
    tables: list[dict] | None = None
) -> Path:
    """
    Create an OKF knowledge bundle from an uploaded report.
    """

    bundle_dir = Path("knowledge") / report_id

    pages_dir = bundle_dir / "pages"
    tables_dir = bundle_dir / "tables"
    pages_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    tables_dir.mkdir(
    parents=True,
    exist_ok=True
    )

    generated_at = datetime.now(
        timezone.utc
    ).isoformat()

    # --------------------------------------------------
    # index.md
    # --------------------------------------------------

    index_content = f"""---
type: Financial Report Bundle
title: {report_name}
description: Knowledge bundle generated from uploaded financial report.
tags:
  - financial-report
  - research
  - uploaded-document
generated:
  by: financial-research-agent/0.1
  at: {generated_at}
---

# Financial Report

Source document: `{report_name}`

This knowledge bundle contains page-level knowledge extracted
from the uploaded financial report.

## Pages

"""

    for page in pages:
        page_number = page["page"]

        index_content += (
            f"- [Page {page_number}]"
            f"(pages/page-{page_number:03d}.md)\n"
        )

    (bundle_dir / "index.md").write_text(
        index_content,
        encoding="utf-8"
    )

    # --------------------------------------------------
    # Individual page concepts
    # --------------------------------------------------

    for page in pages:

        page_number = page["page"]
        text = page["text"]

        page_content = f"""---
type: Financial Report Page
title: {report_name} - Page {page_number}
description: Extracted content from page {page_number} of the financial report.
tags:
  - financial-report
  - page
generated:
  by: financial-research-agent/0.1
  at: {generated_at}
source:
  document: {report_name}
  page: {page_number}
---

# Page {page_number}

{text}
"""

        page_file = (
            pages_dir /
            f"page-{page_number:03d}.md"
        )

        page_file.write_text(
            page_content,
            encoding="utf-8"
        )

    # --------------------------------------------------
    # report.md
    # --------------------------------------------------

    report_content = f"""---
type: Financial Report
title: {report_name}
description: Uploaded financial report used for financial research and reasoning.
tags:
  - financial-report
  - source-document
generated:
  by: financial-research-agent/0.1
  at: {generated_at}
---

# {report_name}

This document represents the uploaded source report.

## Source

The original document uploaded by the user is:

`{report_name}`

## Knowledge Bundle

The report has been decomposed into page-level OKF concepts.

See:

[index.md](index.md)
"""

    (bundle_dir / "report.md").write_text(
        report_content,
        encoding="utf-8"
    )

    if tables:

        for table in tables:

            page_number = table["page"]
            table_index = table["table_index"]

            table_content = f"""---
type: Financial Table
title: {report_name} - Page {page_number} - Table {table_index + 1}
description: Financial table extracted from page {page_number}.
tags:
  - financial-report
  - financial-table
  - numerical-data
source:
  document: {report_name}
  page: {page_number}
---

# Financial Table

## Source

Document: `{report_name}`

Page: {page_number}

## Table

"""

            for row in table["rows"]:
                table_content += (
                    "| "
                    + " | ".join(row)
                    + " |\n"
                )

            table_file = (
                tables_dir
                / f"page-{page_number:03d}-table-{table_index + 1:03d}.md"
            )

            table_file.write_text(
                table_content,
                encoding="utf-8"
            )

    return bundle_dir