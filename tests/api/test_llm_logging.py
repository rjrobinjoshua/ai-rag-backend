from fastapi.testclient import TestClient
from loguru import logger

from app.core.llm_telemetry import LLMCallLog
from app.main import app

client = TestClient(app)


def test_llm_logging_non_stream(monkeypatch):
    async def fake_ask_llm(request, prompt: str) -> str:
        request.state.llm_calls.append(
            LLMCallLog(
                operation="chat.completions",
                requested_model="gpt-4.1-mini",
                latency_ms=1,
            )
        )
        return "ok"

    monkeypatch.setattr("app.services.openai_service.ask_llm", fake_ask_llm)

    records = []
    sink_id = logger.add(lambda msg: records.append(msg.record))
    try:
        response = client.post("/ask", json={"question": "hi"})
        assert response.status_code == 200
    finally:
        logger.remove(sink_id)

    assert any(
        r["message"] == "request_completed"
        and r["extra"]["path"] == "/ask"
        and r["extra"]["llm_calls"]
        for r in records
    )


def test_llm_logging_stream(monkeypatch):
    async def fake_stream(request, prompt: str):
        request.state.llm_calls.append(
            LLMCallLog(
                operation="chat.completions.stream",
                requested_model="gpt-4.1-mini",
                latency_ms=1,
            )
        )
        yield "Hello"
        yield " world"

    monkeypatch.setattr("app.services.openai_service.stream_chat_llm", fake_stream)

    records = []
    sink_id = logger.add(lambda msg: records.append(msg.record))
    try:
        chunks = []
        with client.stream(
            "POST",
            "/stream-chat",
            json={"prompt": "hi"},
        ) as response:
            assert response.status_code == 200
            for piece in response.iter_text():
                chunks.append(piece)
    finally:
        logger.remove(sink_id)

    assert "".join(chunks) == "Hello world"
    assert any(
        r["message"] == "request_completed"
        and r["extra"]["path"] == "/stream-chat"
        and r["extra"]["llm_calls"]
        for r in records
    )
