from fastapi import APIRouter, Request

from app.models.ask import AskRequest, AskResponse
from app.services import openai_service

router = APIRouter(tags=["openai"])


@router.post(
    "/ask", summary="Returns an LLM generated answer", response_model=AskResponse
)
async def ask(http_request: Request, request: AskRequest) -> AskResponse:
    answer = await openai_service.ask_llm(http_request, request.question)
    return AskResponse(answer=answer)
