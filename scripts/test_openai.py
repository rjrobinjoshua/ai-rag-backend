from dotenv import load_dotenv
import os

from openai import OpenAI

user_prompt = "Hello Open AI, what is your model name?"


def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found in the environment")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
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
