import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

user_prompt = "Give me 5 ideas for weekend activities in Berlin."


def main():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found in the environment")

    client = OpenAI(api_key=api_key)

    print("=== STREAMING RESPONSE ===")
    sys.stdout.flush()
    stream = client.chat.completions.create(
        model="gpt-4.1-mini",
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
