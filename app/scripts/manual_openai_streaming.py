import sys

from openai import OpenAI

from app.core.config import get_settings

user_prompt = "Give me 5 ideas for weekend activities in Berlin."


def main():
    settings = get_settings()
    client = OpenAI(api_key=settings.openai_api_key)

    print("=== STREAMING RESPONSE ===")
    sys.stdout.flush()
    stream = client.chat.completions.create(
        model=settings.chatgpt_model,
        messages=[
            {"role": "system", "content": "You are a concise assitant"},
            {"role": "user", "content": user_prompt},
        ],
        stream=True,
    )

    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            print(delta.content, end="", flush=True)

    print("\n=== DONE ===")


if __name__ == "__main__":
    main()
