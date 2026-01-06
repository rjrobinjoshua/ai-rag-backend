import time
from typing import Optional

from fastapi import Request
from openai import AsyncOpenAI

from app.core.config import get_settings
from app.core.llm_telemetry import LLMCallLog

settings = get_settings()
client = AsyncOpenAI(api_key=settings.api_key)


def _append_llm_call(
    request: Optional[Request],
    *,
    operation: str,
    requested_model: str,
    actual_model: Optional[str],
    latency_ms: int,
    prompt_tokens: Optional[int] = None,
    completion_tokens: Optional[int] = None,
    total_tokens: Optional[int] = None,
) -> None:
    if request is None:
        return
    if not hasattr(request.state, "llm_calls"):
        return

    request.state.llm_calls.append(
        LLMCallLog(
            operation=operation,
            requested_model=requested_model,
            actual_model=actual_model,
            latency_ms=latency_ms,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
        )
    )


async def ask_llm(request: Request, user_prompt: str) -> str:
    requested_model = settings.chatgpt_model

    t0 = time.perf_counter()
    openai_response = await client.chat.completions.create(
        model=requested_model,
        messages=[
            {"role": "system", "content": "You are a concise assistant"},
            {"role": "user", "content": user_prompt},
        ],
    )
    latency_ms = int((time.perf_counter() - t0) * 1000)

    usage = getattr(openai_response, "usage", None)
    actual_model = getattr(openai_response, "model", None)

    _append_llm_call(
        request,
        operation="chat.completions",
        requested_model=requested_model,
        actual_model=actual_model,
        latency_ms=latency_ms,
        prompt_tokens=getattr(usage, "prompt_tokens", None) if usage else None,
        completion_tokens=getattr(usage, "completion_tokens", None) if usage else None,
        total_tokens=getattr(usage, "total_tokens", None) if usage else None,
    )

    return openai_response.choices[0].message.content or ""


async def embed_text(request: Optional[Request], text: str) -> list[float]:
    requested_model = settings.openai_embed_model

    t0 = time.perf_counter()
    response = await client.embeddings.create(model=requested_model, input=text)
    latency_ms = int((time.perf_counter() - t0) * 1000)

    usage = getattr(response, "usage", None)
    actual_model = getattr(response, "model", None)

    _append_llm_call(
        request,
        operation="embeddings",
        requested_model=requested_model,
        actual_model=actual_model,
        latency_ms=latency_ms,
        prompt_tokens=getattr(usage, "prompt_tokens", None) if usage else None,
        total_tokens=getattr(usage, "total_tokens", None) if usage else None,
    )

    return response.data[0].embedding


async def stream_chat_llm(request: Request, prompt: str):
    requested_model = settings.chatgpt_model

    t0 = time.perf_counter()
    last_usage = None
    last_model = None
    response = await client.chat.completions.create(
        model=requested_model,
        messages=[
            {"role": "system", "content": "You are a concise assistant"},
            {"role": "user", "content": prompt},
        ],
        stream=True,
        stream_options={"include_usage": True},
    )

    try:
        async for chunk in response:
            if getattr(chunk, "usage", None) is not None:
                last_usage = chunk.usage
            if getattr(chunk, "model", None) is not None:
                last_model = chunk.model
            choices = getattr(chunk, "choices", None)
            if not choices:
                continue
            delta = choices[0].delta
            if delta and delta.content:
                yield delta.content
    finally:
        latency_ms = int((time.perf_counter() - t0) * 1000)
        _append_llm_call(
            request,
            operation="chat.completions.stream",
            requested_model=requested_model,
            actual_model=last_model,
            latency_ms=latency_ms,
            prompt_tokens=(
                getattr(last_usage, "prompt_tokens", None) if last_usage else None
            ),
            completion_tokens=(
                getattr(last_usage, "completion_tokens", None) if last_usage else None
            ),
            total_tokens=(
                getattr(last_usage, "total_tokens", None) if last_usage else None
            ),
        )
