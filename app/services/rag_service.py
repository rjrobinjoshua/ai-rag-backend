from typing import Any, Optional, Tuple

from app.core import rag, retrieval
from app.models.rag import RagAnswer, RagSource
from app.services import openai_service


def _parse_answer_and_summary(raw: str) -> Tuple[str, Optional[str]]:
    if not raw:
        return "", None

    text = raw.strip()

    parts = text.split("SUMMARY:", 1)
    answer_part = parts[0].strip()
    summary_part: Optional[str] = None

    if len(parts) == 2:
        summary_part = parts[1].strip()
        if not summary_part:
            summary_part = None

    if answer_part.upper().startswith("ANSWER:"):
        answer_part = answer_part[len("ANSWER:") :].strip()

    return answer_part, summary_part


async def rag_with_answer(
    question: str,
    top_k: int,
    filename: Optional[str] = None,
    metadata_filter: Optional[dict[str, Any]] = None,
) -> RagAnswer:
    chunks = await retrieval.search_chunks(
        query=question, k=top_k, filename=filename, metadata_filter=metadata_filter
    )
    if not chunks:
        return RagAnswer(
            answer="I couldn't find any relevant context to answer this question.",
            summary=None,
            sources=[],
        )

    context = rag.build_context(chunks)
    rag_prompt = rag.build_rag_prompt(context=context, question=question)
    print(rag_prompt)
    raw_output = await openai_service.ask_llm(rag_prompt)

    answer, summary = _parse_answer_and_summary(raw_output)

    return RagAnswer(
        answer=answer.strip(),
        summary=summary,
        sources=[
            RagSource(
                id=chunk.id,
                text=chunk.text,
                score=chunk.score,
                metadata=chunk.metadata,
            )
            for chunk in chunks
        ],
    )
