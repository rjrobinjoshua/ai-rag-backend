from openai import OpenAI

from app.core.config import get_settings

user_prompt = "Hello Open AI, what is your model name?"


def main():
    settings = get_settings()
    client = OpenAI(api_key=settings.openai_api_key)

    response = client.chat.completions.create(
        model=settings.chatgpt_model,
        messages=[
            {"role": "system", "content": "You are a concise assitant"},
            {"role": "user", "content": user_prompt},
        ],
    )

    message = response.choices[0].message.content
    print("=== RESPONSE ===")
    print(message)


if __name__ == "__main__":
    main()
