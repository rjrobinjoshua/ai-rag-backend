from typing import Any, Dict, List

from pydantic import BaseModel, Field


class RagRequest(BaseModel):
    question: str = Field(..., min_length=3)
    top_k: int = Field(4, ge=1, le=20)


class RagSource(BaseModel):
    id: str = None
    text: str
    score: float
    metadata: Dict[str, Any]


class RagAnswer(BaseModel):
    answer: str
    sources: List[RagSource]
