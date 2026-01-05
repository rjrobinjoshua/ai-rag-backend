from openai import OpenAI

from app.core.config import get_settings

settings = get_settings()
client = OpenAI(api_key=settings.api_key)


async def ask_llm(user_prompt: str) -> str:
    openai_response = client.chat.completions.create(
        model=settings.chatgpt_model,
        messages=[
            {"role": "system", "content": "You are a concise assistant"},
            {"role": "user", "content": user_prompt},
        ],
    )

    response_message = openai_response.choices[0].message.content
    return response_message


async def embed_text(text: str) -> list[float]:
    response = client.embeddings.create(model=settings.openai_embed_model, input=text)
    return response.data[0].embedding


async def stream_chat_llm(prompt: str):
    response = client.chat.completions.create(
        model=settings.chatgpt_model,
        messages=[
            {"role": "system", "content": "You are a concise assistant"},
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )

    for chunk in response:
        delta = chunk.choices[0].delta
        if delta and delta.content:
            yield delta.content
