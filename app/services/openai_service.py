from openai import OpenAI

from app.core.config import get_settings

settings = get_settings()
client = OpenAI(api_key=settings.api_key)

def ask_llm(user_prompt: str) -> str:
    openai_response = client.chat.completions.create(
        model=settings.chatgpt_model,
        messages=[
            {'role': 'system', 'content': 'You are a concise assistant'},
            {'role': 'user', 'content': user_prompt}
        ]
    )

    response_message = openai_response.choices[0].message.content
    return response_message


