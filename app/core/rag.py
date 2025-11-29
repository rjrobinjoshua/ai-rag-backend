from typing import List

from app.models.chunk import TextChunk


def build_context(chunks: List[TextChunk]) -> str:
    lines = []
    for idx, ch in enumerate(chunks):
        lines.append(f"[{idx}] {ch.text.strip()}")
    return "\n\n".join(lines)


def build_rag_prompt(context: str, question: str) -> str:
    return f"""You are a precise assistant answering questions based ONLY on the provided context.

Context:
{context}

Question:
{question}

Instructions:
- If the answer is in the context, answer clearly and concisely.
- If the answer is not in the context, say you cannot answer based on the given information.
- When relevant, reference sources using [1], [2], etc. based on the context snippets.

Answer:"""
