from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_ask_endpoint(monkeypatch):
    async def mock_ask_llm(user_prompt: str) -> str:
        assert user_prompt == "Hello"
        return "Mocked answer"

    # Adjust import path if needed
    monkeypatch.setattr(
        "app.services.openai_service.ask_llm",
        mock_ask_llm,
    )

    response = client.post("/ask", json={"question": "Hello"})
    assert response.status_code == 200

    data = response.json()
    assert data.get("answer") == "Mocked answer"
