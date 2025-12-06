from typing import List

from app.models.chunk import TextChunk


def build_context(chunks: List[TextChunk]) -> str:
    """
    Build a context string with explicit indices and metadata so the LLM can
    reference [0], [1], etc. and we can map them back to sources.
    """
    lines = []
    for idx, ch in enumerate(chunks):
        meta = ch.metadata

        meta_parts = [f"source={meta.filename}"]
        if meta.page is not None:
            meta_parts.append(f"page={meta.page}")
        if meta.chunk_number is not None:
            meta_parts.append(f"chunk={meta.chunk_number}")

        meta_str = ", ".join(meta_parts)
        lines.append(f"[{idx}] [{meta_str}]\n{ch.text.strip()}")

    return "\n\n".join(lines)


def build_rag_prompt(context: str, question: str) -> str:
    return f"""You are a precise assistant answering questions based ONLY on the provided context.

Context:
{context}

Question:
{question}

Instructions:
- Use ONLY the information in the context. Do NOT use external knowledge.
- If the answer is not in the context, say you cannot answer based on the given information.
- When you refer to specific facts, add citations like [0], [1], [2] that correspond to the snippet indices in the Context section.
- Do NOT invent or list your own source filenames or page numbers; citations are just [0], [1], etc.
- First write an 'ANSWER:' section with a concise answer (2–4 sentences).
- Then write a 'SUMMARY:' section with 1–3 bullet points summarizing the key ideas.

Respond in the following format exactly:

ANSWER:
<your answer here>

SUMMARY:
<your summary here>
"""
