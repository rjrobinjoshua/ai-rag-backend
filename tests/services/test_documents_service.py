from app.services.documents_service import list_documents


class FakeCollection:
    def __init__(self, metadatas):
        self._metadatas = metadatas
        self.last_get_kwargs = None

    def get(self, **kwargs):
        # Record how get() was called
        self.last_get_kwargs = kwargs
        return {"metadatas": self._metadatas}


class FakeClient:
    def __init__(self, collection: FakeCollection):
        self._collection = collection
        self.last_collection_name = None

    def get_or_create_collection(self, name: str):
        self.last_collection_name = name
        return self._collection


def _setup_fake_chroma(monkeypatch, metadatas):
    from app.core import chroma_client

    fake_collection = FakeCollection(metadatas)
    fake_client = FakeClient(fake_collection)

    monkeypatch.setattr(
        chroma_client,
        "get_chroma_client",
        lambda: fake_client,
    )

    return fake_client, fake_collection


def test_list_documents_aggregates_by_filename(monkeypatch):
    metadatas = [
        {
            "source": "data/docs/fastapi_multipage.pdf",
            "filename": "fastapi_multipage.pdf",
            "page": 1,
            "chunk_number": 0,
        },
        {
            "source": "data/docs/fastapi_multipage.pdf",
            "filename": "fastapi_multipage.pdf",
            "page": 2,
            "chunk_number": 1,
        },
        {
            "source": "data/docs/some-data.pdf",
            "filename": "some-data.pdf",
            "page": 1,
            "chunk_number": 0,
        },
    ]

    fake_client, fake_collection = _setup_fake_chroma(monkeypatch, metadatas)

    docs = list_documents(collection_name="docs")

    # called with expected args
    assert fake_client.last_collection_name == "docs"
    assert fake_collection.last_get_kwargs["include"] == ["metadatas"]
    assert fake_collection.last_get_kwargs["limit"] == 10000

    # aggregated docs
    assert len(docs) == 2

    fastapi_doc = next(d for d in docs if d.filename == "fastapi_multipage.pdf")
    resume_doc = next(d for d in docs if d.filename == "some-data.pdf")

    assert fastapi_doc.source == "data/docs/fastapi_multipage.pdf"
    assert fastapi_doc.num_chunks == 2
    assert fastapi_doc.pages == [1, 2]

    assert resume_doc.source == "data/docs/some-data.pdf"
    assert resume_doc.num_chunks == 1
    assert resume_doc.pages == [1]


def test_list_documents_handles_empty_metadata(monkeypatch):
    _setup_fake_chroma(monkeypatch, metadatas=[])

    docs = list_documents(collection_name="docs")

    assert docs == []
