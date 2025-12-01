# tests/services/test_rag_service.py

import pytest

from app.models.chunk import TextChunk
from app.models.rag import RagAnswer
from app.services import rag_service


@pytest.mark.asyncio
async def test_rag_with_answer_basic(monkeypatch):
    # Fake retrieval: returns one chunk
    async def fake_search_chunks(query: str, k: int):
        assert query == "What is FastAPI?"
        assert k == 3
        return [
            TextChunk(
                id="doc1",
                text="FastAPI is a modern, fast (high-performance) web framework "
                "for building APIs with Python.",
                score=0.9,
                metadata={"source": "docs.md"},
            )
        ]

    # Fake LLM: returns a fixed answer
    async def fake_ask_llm(prompt: str) -> str:
        assert "FastAPI is a modern, fast (high-performance)" in prompt
        assert "Question:" in prompt
        assert "What is FastAPI?" in prompt
        return (
            "FastAPI is a high-performance web framework for building APIs in Python."
        )

    # Patch the dependencies used inside rag_with_answer
    from app.core import retrieval
    from app.services import openai_service

    monkeypatch.setattr(retrieval, "search_chunks", fake_search_chunks)
    monkeypatch.setattr(openai_service, "ask_llm", fake_ask_llm)

    # Call the service
    result: RagAnswer = await rag_service.rag_with_answer(
        question="What is FastAPI?", top_k=3
    )

    # Validate result
    assert isinstance(result, RagAnswer)
    assert "FastAPI is a high-performance web framework" in result.answer
    assert len(result.sources) == 1

    src = result.sources[0]
    assert src.id == "doc1"
    assert "FastAPI is a modern, fast (high-performance)" in src.text
    assert src.score == 0.9
    assert src.metadata == {"source": "docs.md"}


@pytest.mark.asyncio
async def test_rag_with_answer_no_chunks(monkeypatch):
    # Fake retrieval: returns no chunks
    async def fake_search_chunks(query: str, k: int):
        return []

    # Fake ask_llm that would explode if called (we want to ensure it's not)
    async def fake_ask_llm(prompt: str) -> str:
        raise AssertionError("ask_llm should not be called when no chunks are found")

    from app.core import retrieval
    from app.services import openai_service

    monkeypatch.setattr(retrieval, "search_chunks", fake_search_chunks)
    monkeypatch.setattr(openai_service, "ask_llm", fake_ask_llm)

    result: RagAnswer = await rag_service.rag_with_answer(question="Something", top_k=3)

    assert isinstance(result, RagAnswer)
    assert (
        result.answer == "I couldn't find any relevant context to answer this question."
    )
    assert result.sources == []
