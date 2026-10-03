import shutil
from pathlib import Path

from src.retriever import (
    index_okf_bundle,
    retrieve,
    delete_report_from_index)

def delete_report_data(report_id: str) -> None:
    """
    Delete all locally stored data associated with a report.
    """

    # Delete ChromaDB vectors
    delete_report_from_index(report_id)

    # Delete OKF knowledge bundle
    bundle_dir = Path("knowledge") / report_id

    if bundle_dir.exists():
        shutil.rmtree(bundle_dir)

import hashlib
import streamlit as st

from src.pdf_processor import extract_pdf_text
from src.okf_generator import create_okf_bundle
from src.table_extractor import extract_pdf_tables
from src.retriever import index_okf_bundle, retrieve
from src.research_agent import answer_question


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Financial Research Agent",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# UI
# --------------------------------------------------

st.title("📊 Financial Research & Reasoning Agent")

st.caption(
    "Upload financial reports and ask evidence-grounded questions."
)

uploaded_file = st.file_uploader(
    "Upload a financial report",
    type=["pdf"]
)


# --------------------------------------------------
# Process uploaded report
# --------------------------------------------------

if uploaded_file:
    file_bytes = uploaded_file.getvalue()
    report_id = hashlib.md5(file_bytes).hexdigest()

    # Process only when a new report is uploaded
    if (
        "report_id" not in st.session_state
        or st.session_state.report_id != report_id
    ):
        try:
            # 1. Extract PDF text
            with st.spinner("Extracting report content..."):
                pages = extract_pdf_text(file_bytes)

            # 2. Extract tables
            with st.spinner("Extracting financial tables..."):
                tables = extract_pdf_tables(file_bytes)

            # 3. Save report information
            st.session_state.pages = pages
            st.session_state.tables = tables
            st.session_state.report_name = uploaded_file.name
            st.session_state.report_id = report_id
            st.session_state.messages = []

            # 4. Generate OKF knowledge bundle
            with st.spinner("Creating OKF knowledge bundle..."):
                okf_bundle = create_okf_bundle(
                    pages=pages,
                    report_name=uploaded_file.name,
                    report_id=report_id,
                    tables=tables
                )

            st.session_state.okf_bundle = str(okf_bundle)

            # 5. Build RAG index
            with st.spinner("Building RAG index..."):
                chunk_count = index_okf_bundle(
                    report_id=report_id
                )

            st.session_state.chunk_count = chunk_count

            st.success("Report processed successfully!")

        except ValueError as e:
            st.error(str(e))
            st.stop()

        except Exception as e:
            st.error(f"Unexpected processing error: {e}")
            st.stop()

    # --------------------------------------------------
    # Report information
    # --------------------------------------------------

    pages = st.session_state.pages

    st.success(
        f"Report ready: {st.session_state.report_name} "
        f"({len(pages)} pages)"
    )

    st.caption(
        f"Tables extracted: {len(st.session_state.tables)}"
    )

    st.caption(
        f"RAG index: {st.session_state.chunk_count} chunks"
    )

    st.caption(
        f"OKF bundle: {st.session_state.okf_bundle}"
    )

    st.divider()

    if st.button(
        "🗑️ End Chat & Delete Report",
        type="secondary"
    ):
        try:
            delete_report_data(
                st.session_state.report_id
            )

            # Clear report-related session data
            for key in [
                "pages",
                "tables",
                "report_name",
                "report_id",
                "messages",
                "okf_bundle",
                "chunk_count"
            ]:
                st.session_state.pop(key, None)

            st.success(
                "Chat ended and report data deleted."
            )

            st.rerun()

        except Exception as e:
            st.error(
                f"Could not completely delete report data: {e}"
            )


    # --------------------------------------------------
    # Question answering
    # --------------------------------------------------

    st.divider()
    st.subheader("Ask your financial question")

    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input(
        "e.g. What does the report say about operating income?"
    )

    if question:
        # Display and save user question
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        # Retrieve evidence and generate answer
        with st.chat_message("assistant"):
            with st.spinner("Retrieving evidence and generating answer..."):
                try:
                    relevant_chunks = retrieve(
                        question=question,
                        report_id=st.session_state.report_id,
                        top_k=5
                    )

                    if not relevant_chunks:
                        answer = (
                            "I couldn't find relevant information "
                            "in the uploaded report."
                        )
                    else:
                        answer = answer_question(
                            question=question,
                            pages=relevant_chunks
                        )

                    st.markdown(answer)

                    # Save assistant response
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                except Exception as e:
                    st.error(f"Something went wrong: {e}")

else:
    st.info("Upload a PDF report to get started.")