from fastapi import APIRouter

from app.models.ask import AskRequest, AskResponse
from app.services import openai_service

router = APIRouter(tags=["openai"])


@router.post(
    "/ask", summary="Returns an LLM generated answer", response_model=AskResponse
)
async def ask(request: AskRequest) -> AskResponse:
    answer = await openai_service.ask_llm(request.question)
    return AskResponse(answer=answer)
