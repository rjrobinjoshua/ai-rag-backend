import pytest

from app.core import retrieval
from app.models.chunk import ChunkMetadata, TextChunk


class FakeCollection:
    def __init__(self):
        self.last_where = None
        self.last_query_kwargs = None

    def query(self, **kwargs):
        # Record what was passed to Chroma
        self.last_where = kwargs.get("where")
        self.last_query_kwargs = kwargs

        # Return a minimal, valid Chroma-like response
        return {
            "documents": [["doc1 text"]],
            "metadatas": [
                [
                    {
                        "source": "data/docs/fastapi_multipage.pdf",
                        "filename": "fastapi_multipage.pdf",
                        "page": 1,
                        "chunk_number": 0,
                    }
                ]
            ],
            "distances": [[0.123]],
            "ids": [["chunk-id-1"]],
        }


class FakeClient:
    def __init__(self, collection: FakeCollection):
        self._collection = collection

    def get_or_create_collection(self, name: str):
        return self._collection


@pytest.mark.asyncio
async def test_search_chunks_without_filters_uses_where_none(monkeypatch):
    fake_collection = FakeCollection()
    fake_client = FakeClient(fake_collection)

    # Mock Chroma client
    from app.core import chroma_client

    monkeypatch.setattr(chroma_client, "get_chroma_client", lambda: fake_client)

    # Mock embed_text
    from app.services import openai_service

    async def fake_embed_text(query: str):
        return [0.1, 0.2, 0.3]

    monkeypatch.setattr(openai_service, "embed_text", fake_embed_text)

    chunks = await retrieval.search_chunks(
        query="what is fast api",
        k=3,
        filename=None,
        metadata_filter=None,
    )

    assert fake_collection.last_where is None
    assert len(chunks) == 1
    assert isinstance(chunks[0], TextChunk)
    assert isinstance(chunks[0].metadata, ChunkMetadata)
    assert chunks[0].metadata.filename == "fastapi_multipage.pdf"


@pytest.mark.asyncio
async def test_search_chunks_with_filename_builds_filename_where(monkeypatch):
    fake_collection = FakeCollection()
    fake_client = FakeClient(fake_collection)

    from app.core import chroma_client

    monkeypatch.setattr(chroma_client, "get_chroma_client", lambda: fake_client)

    from app.services import openai_service

    async def fake_embed_text(query: str):
        return [0.1, 0.2, 0.3]

    monkeypatch.setattr(openai_service, "embed_text", fake_embed_text)

    await retrieval.search_chunks(
        query="what is fast api",
        k=3,
        filename="resume.pdf",
        metadata_filter=None,
    )

    assert fake_collection.last_where == {"filename": "resume.pdf"}


@pytest.mark.asyncio
async def test_search_chunks_with_combined_filters_uses_and(monkeypatch):
    fake_collection = FakeCollection()
    fake_client = FakeClient(fake_collection)

    from app.core import chroma_client

    monkeypatch.setattr(chroma_client, "get_chroma_client", lambda: fake_client)

    from app.services import openai_service

    async def fake_embed_text(query: str):
        return [0.1, 0.2, 0.3]

    monkeypatch.setattr(openai_service, "embed_text", fake_embed_text)

    chunks = await retrieval.search_chunks(
        query="what is fast api",
        k=3,
        filename=None,
        metadata_filter={"filename": "resume.pdf", "page": {"$gt": 1}},
    )

    expected_where = {
        "$and": [
            {"filename": "resume.pdf"},
            {"page": {"$gt": 1}},
        ]
    }

    assert fake_collection.last_where == expected_where
    assert len(chunks) == 1
    assert isinstance(chunks[0].metadata, ChunkMetadata)
    assert chunks[0].metadata.page == 1
