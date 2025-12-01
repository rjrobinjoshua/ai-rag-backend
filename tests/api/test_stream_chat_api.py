from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_stream_chat_endpoint(monkeypatch):
    async def fake_stream(prompt: str):
        yield "Hello"
        yield " world"

    monkeypatch.setattr("app.services.openai_service.stream_chat_llm", fake_stream)

    chunks = []
    with client.stream(
        "POST",
        "/stream-chat",
        json={"prompt": "hi"},
    ) as response:
        assert response.status_code == 200
        for piece in response.iter_text():
            chunks.append(piece)

    assert "".join(chunks) == "Hello world"
