from src.gemini_client import generate_content


def answer_question(
    question: str,
    pages: list[dict]
) -> str:

    context_parts = []

    for item in pages:

        source = item.get(
            "source",
            "Unknown source"
        )

        text = item["text"]

        context_parts.append(
            f"SOURCE: {source}\n{text}"
        )

    context = "\n\n".join(
        context_parts
    )

    prompt = f"""
You are a financial research assistant.

Answer the user's question using ONLY
the evidence provided below.

Rules:

1. Do not invent financial information.
2. If the evidence is insufficient, say so.
3. Show calculations when relevant.
4. Identify the source used for each important claim.
5. Distinguish reported values from calculated values.
6. Do not use outside knowledge.
7. Include the source filename and page number
   when available.

EVIDENCE:

{context}

USER QUESTION:

{question}
"""

    response = generate_content(prompt)

    return response.text or (
        "No answer was generated."
    )