from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from app.models.chunk import ChunkMetadata


class RagRequest(BaseModel):
    question: str = Field(..., min_length=3)
    top_k: int = Field(4, ge=1, le=20)
    filename: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None


class RagSource(BaseModel):
    id: str = None
    text: str
    score: float
    metadata: ChunkMetadata


class RagAnswer(BaseModel):
    answer: str
    summary: Optional[str] = None
    sources: List[RagSource]
