from typing import Any

from fastapi.testclient import TestClient

from app.main import app
from app.models.chunk import ChunkMetadata, TextChunk

client = TestClient(app)


def test_rag_query_basic(monkeypatch):
    # mock search_chunks

    async def fake_search_chunks(
        http_request,
        query: str,
        filename: str,
        metadata_filter: dict[str, Any],
        k: int = 4,
    ):
        return [
            TextChunk(
                id="doc1",
                text="FastAPI is a modern, fast (high-performance) web framework for "
                "building APIs with Python.",
                score=0.9,
                metadata=ChunkMetadata(source="docs.md", filename="docs.md"),
            )
        ]

    # mock chat_completion
    async def fake_chat_completion(_request, prompt: str) -> str:
        assert "FastAPI" in prompt
        assert "Question:" in prompt
        return (
            "FastAPI is a high-performance web framework for building APIs in Python."
        )

    from app.core import retrieval
    from app.services import openai_service

    monkeypatch.setattr(retrieval, "search_chunks", fake_search_chunks)
    monkeypatch.setattr(openai_service, "ask_llm", fake_chat_completion)

    resp = client.post(
        "/rag-query",
        json={"question": "What is FastAPI?", "top_k": 3},
    )

    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert "answer" in body
    assert "FastAPI" in body["answer"]
    assert len(body["sources"]) == 1
