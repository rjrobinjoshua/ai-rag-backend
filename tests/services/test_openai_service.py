from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.openai_service import ask_llm, embed_text, stream_chat_llm


@pytest.mark.asyncio
@patch("app.services.openai_service.client")
async def test_ask_llm_uses_openai_client(mock_client):
    # fake OpenAI response
    fake_choice = MagicMock()
    fake_choice.message.content = "Test reply"

    fake_response = MagicMock()
    fake_response.choices = [fake_choice]

    mock_client.chat.completions.create = AsyncMock(return_value=fake_response)

    result = await ask_llm(None, "Hello")
    assert result == "Test reply"

    mock_client.chat.completions.create.assert_called_once()
    kwargs = mock_client.chat.completions.create.call_args.kwargs
    assert kwargs["messages"][1]["content"] == "Hello"


@pytest.mark.asyncio
@patch("app.services.openai_service.client")
async def test_embed_text_uses_openai_client(mock_client):
    fake_embedding = [0.1, 0.2, 0.3]

    fake_data_item = MagicMock()
    fake_data_item.embedding = fake_embedding

    fake_response = MagicMock()
    fake_response.data = [fake_data_item]

    mock_client.embeddings.create = AsyncMock(return_value=fake_response)

    result = await embed_text(None, "hello world")
    assert result == fake_embedding

    mock_client.embeddings.create.assert_called_once()
    kwargs = mock_client.embeddings.create.call_args.kwargs
    assert kwargs["input"] == "hello world"


@pytest.mark.asyncio
@patch("app.services.openai_service.client")
async def test_stream_chat_llm(mock_client):
    # Fake streamed chunks
    chunk0 = MagicMock()
    chunk0.choices = []
    chunk0.usage = MagicMock(prompt_tokens=2, completion_tokens=3, total_tokens=5)
    chunk0.model = "gpt-4.1-mini-2025-04-14"

    chunk1 = MagicMock()
    chunk1.choices = [MagicMock(delta=MagicMock(content="Hello"))]

    chunk2 = MagicMock()
    chunk2.choices = [MagicMock(delta=MagicMock(content=" world"))]

    async def fake_stream():
        yield chunk0
        yield chunk1
        yield chunk2

    mock_client.chat.completions.create = AsyncMock(return_value=fake_stream())

    result = []
    async for token in stream_chat_llm(None, "hi"):
        result.append(token)

    assert result == ["Hello", " world"]
    mock_client.chat.completions.create.assert_called_once()
    kwargs = mock_client.chat.completions.create.call_args.kwargs
    assert kwargs["stream"] is True
    assert kwargs["stream_options"] == {"include_usage": True}
