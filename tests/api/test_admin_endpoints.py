import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.documents_service import DocumentInfo

client = TestClient(app)


@pytest.mark.asyncio
async def test_get_documents_endpoint(monkeypatch):
    # Prepare fake documents list returned by service
    fake_docs = [
        DocumentInfo(
            filename="fastapi_multipage.pdf",
            source="data/docs/fastapi_multipage.pdf",
            num_chunks=12,
            pages=[1, 2, 3],
        ),
        DocumentInfo(
            filename="Resume-Robin.pdf",
            source="data/docs/Resume-Robin.pdf",
            num_chunks=5,
            pages=[1, 2],
        ),
    ]

    from app.services import documents_service

    def fake_list_documents(collection_name: str = "docs"):
        assert collection_name == "docs"
        return fake_docs

    monkeypatch.setattr(
        documents_service,
        "list_documents",
        fake_list_documents,
    )

    resp = client.get("/admin/documents?collection=docs")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2

    first = data[0]
    assert first["filename"] == "fastapi_multipage.pdf"
    assert first["source"] == "data/docs/fastapi_multipage.pdf"
    assert first["num_chunks"] == 12
    assert first["pages"] == [1, 2, 3]


@pytest.mark.asyncio
async def test_reindex_endpoint(monkeypatch):
    # Fake ingest_files from app.scripts.ingest
    async def fake_ingest_files(
        file_patterns,
        collection_name: str,
        chunk_size: int,
        chunk_overlap: int,
        reset: bool,
        mode: str,
    ):
        # basic sanity checks on arguments passed from endpoint
        assert collection_name == "docs"
        assert reset is True
        assert mode in ("fixed", "semantic")
        assert file_patterns == ["data/docs/*.pdf"]
        return 42

    from app.api.routes import admin

    monkeypatch.setattr(
        admin,
        "ingest_files",
        fake_ingest_files,
    )

    body = {
        "paths": ["data/docs/*.pdf"],
        "collection": "docs",
        "chunk_size": 200,
        "chunk_overlap": 40,
        "mode": "semantic",
        "reset": True,
    }

    resp = client.post("/admin/reindex", json=body)
    assert resp.status_code == 200

    data = resp.json()
    assert data["collection"] == "docs"
    assert data["total_chunks"] == 42
