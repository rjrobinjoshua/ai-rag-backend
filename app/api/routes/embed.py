from fastapi import APIRouter, Request

from app.models.embed import EmbedRequest, EmbedResponse
from app.services import openai_service

router = APIRouter(tags=["embeddings"])


@router.post(path="/embed", response_model=EmbedResponse)
async def emed(http_request: Request, request: EmbedRequest):
    vector = await openai_service.embed_text(http_request, request.text)
    return EmbedResponse(embedding=vector)
