from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class LLMCallLog(BaseModel):
    provider: str = "openai"
    operation: str
    requested_model: str
    actual_model: Optional[str] = None
    latency_ms: int
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
