from typing import List

from fastapi import APIRouter, Query

from app.models.admin import DocumentInfo, ReindexRequest
from app.scripts.ingest import ingest_files
from app.services import documents_service

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/documents", response_model=List[DocumentInfo])
def get_documents(collection: str = Query("docs")):
    return documents_service.list_documents(collection_name=collection)


@router.post("/reindex")
async def reindex_collection(body: ReindexRequest):
    total = await ingest_files(
        file_patterns=body.paths,
        collection_name=body.collection,
        chunk_size=body.chunk_size,
        chunk_overlap=body.chunk_overlap,
        reset=body.reset,
        mode=body.mode,
    )

    return {"collection": body.collection, "total_chunks": total}
