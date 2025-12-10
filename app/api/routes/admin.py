from typing import List

from fastapi import APIRouter, Query

from app.services.documents_service import DocumentInfo, list_documents

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/documents", response_model=List[DocumentInfo])
def get_documents(collection: str = Query("docs")):
    return list_documents(collection_name=collection)
