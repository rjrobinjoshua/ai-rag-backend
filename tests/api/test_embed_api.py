from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_embed_endpoint(monkeypatch):
    async def mock_embed_text(text: str):
        assert text == "hello"
        return [0.1, 0.2, 0.3]

    monkeypatch.setattr(
        "app.services.openai_service.embed_text",
        mock_embed_text,
    )

    response = client.post("/embed", json={"text": "hello"})
    assert response.status_code == 200

    data = response.json()
    assert data.get("embedding") == [0.1, 0.2, 0.3]
