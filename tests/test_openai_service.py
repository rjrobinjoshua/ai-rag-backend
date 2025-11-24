import pytest
from unittest.mock import MagicMock, patch

from app.services.openai_service import ask_llm, embed_text, stream_chat_llm


@pytest.mark.asyncio
@patch("app.services.openai_service.client")
async def test_ask_llm_uses_openai_client(mock_client):
    # fake OpenAI response
    fake_choice = MagicMock()
    fake_choice.message.content = "Test reply"

    fake_response = MagicMock()
    fake_response.choices = [fake_choice]

    mock_client.chat.completions.create.return_value = fake_response

    result = await ask_llm("Hello")
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

    mock_client.embeddings.create.return_value = fake_response

    result = await embed_text("hello world")
    assert result == fake_embedding

    mock_client.embeddings.create.assert_called_once()
    kwargs = mock_client.embeddings.create.call_args.kwargs
    assert kwargs["input"] == "hello world"


@pytest.mark.asyncio
@patch("app.services.openai_service.client")
async def test_stream_chat_llm(mock_client):
    # Fake streamed chunks
    chunk1 = MagicMock()
    chunk1.choices = [MagicMock(delta=MagicMock(content="Hello"))]

    chunk2 = MagicMock()
    chunk2.choices = [MagicMock(delta=MagicMock(content=" world"))]

    # Make the mock client iterable (stream=True)
    mock_client.chat.completions.create.return_value = iter([chunk1, chunk2])

    result = []
    async for token in stream_chat_llm("hi"):
        result.append(token)

    assert result == ["Hello", " world"]
    mock_client.chat.completions.create.assert_called_once()
