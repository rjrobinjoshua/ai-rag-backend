from fastapi import APIRouter

from app.models.rag import RagAnswer, RagRequest
from app.services import rag_service

router = APIRouter(tags=["rag"])


@router.post("/rag-query", response_model=RagAnswer)
async def rag_query(request: RagRequest) -> RagAnswer:
    return await rag_service.rag_with_answer(
        question=request.question,
        top_k=request.top_k,
        filename=request.filename,
        metadata_filter=request.filters,
    )
