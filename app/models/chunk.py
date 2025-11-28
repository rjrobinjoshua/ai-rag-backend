from typing import Any, Dict

from pydantic import BaseModel


class TextChunk(BaseModel):
    id: str
    text: str
    score: float
    metadata: Dict[str, Any]
