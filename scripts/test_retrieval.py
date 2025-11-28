import asyncio

from app.core.retrieval import search_chunks


async def main():
    query = "What is this document about?"
    chunks = await search_chunks(query=query, k=3)

    print("\nTop Chunks:")
    for idx, c in enumerate(chunks):
        print(f"\n--- Chunk #{idx} ---")
        print("Score:", c.score)
        print("Text:", c.text)
        print("Meta:", c.metadata)


if __name__ == "__main__":
    asyncio.run(main())
