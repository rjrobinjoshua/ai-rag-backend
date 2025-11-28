from fastapi import APIRouter

from app.models.rag import RagAnswer, RagRequest

router = APIRouter(tags=["rag"])


@router.post("/raq-query", response_model=RagAnswer)
async def rag_query(request: RagRequest) -> RagAnswer:
    return RagAnswer()
