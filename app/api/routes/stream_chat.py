from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.models.stream_chat import StreamChatRequest
from app.services import openai_service

router = APIRouter()


@router.post("/stream-chat")
async def stream_chat(http_request: Request, request: StreamChatRequest):
    http_request.state.is_streaming = True

    async def event_generator():
        async for token in openai_service.stream_chat_llm(http_request, request.prompt):
            yield token

    return StreamingResponse(event_generator(), media_type="text/plain")
