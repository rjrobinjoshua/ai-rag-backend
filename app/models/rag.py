from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from app.core.config import get_settings
from app.models.chunk import ChunkMetadata

settings = get_settings()


class RagRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=settings.max_query_chars)
    top_k: int = Field(settings.default_top_k, ge=1, le=settings.max_top_k)
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
