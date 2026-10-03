import os
from pathlib import Path

import chromadb
from google import genai
from dotenv import load_dotenv


# --------------------------------------------------
# Configuration
# --------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(
    api_key=API_KEY
)


# --------------------------------------------------
# ChromaDB
# --------------------------------------------------

chroma_client = chromadb.PersistentClient(
    path="data/chroma"
)

collection = chroma_client.get_or_create_collection(
    name="financial_reports"
)


# --------------------------------------------------
# Read OKF bundle
# --------------------------------------------------

def load_okf_documents(
    report_id: str
) -> list[dict]:
    """
    Load Markdown knowledge documents from an OKF bundle.
    """

    bundle_dir = Path("knowledge") / report_id

    if not bundle_dir.exists():
        raise ValueError(
            f"OKF bundle not found: {bundle_dir}"
        )

    documents = []

    # Read all Markdown files inside the bundle
    for file_path in bundle_dir.rglob("*.md"):

        content = file_path.read_text(
            encoding="utf-8"
        )

        # Skip the index and report metadata for now.
        # We want actual page-level evidence.
        if file_path.name in {"index.md", "report.md"}:
            continue

        documents.append({
            "path": str(file_path),
            "text": content
        })

    return documents


# --------------------------------------------------
# Chunk OKF documents
# --------------------------------------------------

def create_okf_chunks(
    documents: list[dict],
    chunk_size: int = 1200,
    overlap: int = 200
) -> list[dict]:
    """
    Split OKF Markdown documents into overlapping chunks.
    """

    chunks = []

    for document in documents:

        text = document["text"]
        path = document["path"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]

            if chunk_text.strip():

                chunks.append({
                    "text": chunk_text,
                    "path": path
                })

            # Move forward while keeping overlap
            start += chunk_size - overlap

    return chunks


# --------------------------------------------------
# Gemini embeddings
# --------------------------------------------------

def embed_text(text: str) -> list[float]:
    """
    Generate an embedding using Gemini.
    """

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return result.embeddings[0].values


# --------------------------------------------------
# Index OKF bundle
# --------------------------------------------------

def index_okf_bundle(
    report_id: str
) -> int:
    """
    Read an OKF bundle, create embeddings,
    and store them in ChromaDB.
    """

    documents = load_okf_documents(
        report_id
    )

    if not documents:
        raise ValueError(
            "No OKF knowledge documents found."
        )

    chunks = create_okf_chunks(
        documents
    )

    embeddings = []
    ids = []
    metadatas = []
    texts = []

    for i, chunk in enumerate(chunks):

        text = chunk["text"]

        embedding = embed_text(
            text
        )

        embeddings.append(embedding)

        texts.append(text)

        ids.append(
            f"{report_id}_okf_{i}"
        )

        metadatas.append({
            "report_id": report_id,
            "source": chunk["path"]
        })

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(chunks)


# --------------------------------------------------
# Retrieval
# --------------------------------------------------

def retrieve(
    question: str,
    report_id: str,
    top_k: int = 5
) -> list[dict]:
    """
    Retrieve relevant OKF knowledge for a question.
    """

    query_embedding = embed_text(
        question
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={
            "report_id": report_id
        }
    )

    retrieved = []

    if not results["documents"]:
        return retrieved

    for i, document in enumerate(
        results["documents"][0]
    ):

        metadata = results["metadatas"][0][i]

        retrieved.append({
            "text": document,
            "source": metadata["source"]
        })

    return retrieved


def delete_report_from_index(report_id: str) -> None:
    """
    Delete all ChromaDB data associated with a report.
    """

    collection.delete(
        where={"report_id": report_id}
    )
