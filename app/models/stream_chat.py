from pydantic import BaseModel


class StreamChatRequest(BaseModel):
    prompt: str
