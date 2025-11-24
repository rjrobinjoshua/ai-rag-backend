from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.stream_chat import StreamChatRequest
from app.services import openai_service

router = APIRouter()


@router.post("/stream-chat")
async def stream_chat(request: StreamChatRequest):

    async def event_generator():
        async for token in openai_service.stream_chat_llm(request.prompt):
            yield token

    return StreamingResponse(event_generator(), media_type="text/plain")
