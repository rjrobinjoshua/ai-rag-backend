from app.core import rag, retrieval
from app.models.rag import RagAnswer, RagSource
from app.services import openai_service


async def rag_with_answer(question: str, top_k: int) -> RagAnswer:
    chunks = await retrieval.search_chunks(query=question, k=top_k)
    if not chunks:
        return RagAnswer(
            answer="I couldn't find any relevant context to answer this question.",
            sources=[],
        )

    context = rag.build_context(chunks)
    rag_prompt = rag.build_rag_prompt(context=context, question=question)
    print(rag_prompt)
    answer = await openai_service.ask_llm(rag_prompt)

    return RagAnswer(
        answer=answer.strip(),
        sources=[
            RagSource(
                id=chunk.id, text=chunk.text, score=chunk.score, metadata=chunk.metadata
            )
            for chunk in chunks
        ],
    )
