import pytest

from app.models.chunk import ChunkMetadata, TextChunk
from app.models.rag import RagAnswer
from app.services import rag_service


@pytest.mark.asyncio
async def test_rag_with_answer_basic(monkeypatch):
    # Fake retrieval: returns one chunk
    async def fake_search_chunks(
        query: str,
        collection_name: str = "docs",
        k: int = 3,
        filename=None,
        metadata_filter=None,
    ):
        assert query == "What is FastAPI?"
        assert k == 3
        return [
            TextChunk(
                id="doc1",
                text=(
                    "FastAPI is a modern, fast (high-performance) web framework "
                    "for building APIs with Python."
                ),
                score=0.9,
                metadata=ChunkMetadata(source="docs.md", filename="docs.md"),
            )
        ]

    async def fake_ask_llm(prompt: str) -> str:
        # Prompt should contain context + question + markers
        assert "FastAPI is a modern, fast (high-performance)" in prompt
        assert "Question:" in prompt
        assert "What is FastAPI?" in prompt
        assert "ANSWER:" in prompt
        assert "SUMMARY:" in prompt

        return (
            "ANSWER:\n"
            "FastAPI is a high-performance web framework for building APIs in Python.\n\n"
            "SUMMARY:\n"
            "- High-performance web framework for APIs\n"
            "- Built with Python\n"
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
    assert result.summary is not None
    assert "High-performance web framework for APIs" in result.summary

    assert len(result.sources) == 1

    src = result.sources[0]
    assert src.id == "doc1"
    assert "FastAPI is a modern, fast (high-performance)" in src.text
    assert src.score == 0.9
    assert src.metadata == ChunkMetadata(source="docs.md", filename="docs.md")


@pytest.mark.asyncio
async def test_rag_with_answer_no_chunks(monkeypatch):
    # Fake retrieval: returns no chunks
    async def fake_search_chunks(
        query: str,
        collection_name: str = "docs",
        k: int = 3,
        filename=None,
        metadata_filter=None,
    ):
        return []

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
    assert result.summary is None
    assert result.sources == []
