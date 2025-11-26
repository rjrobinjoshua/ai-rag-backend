import argparse
import asyncio
import os
from typing import List

import chromadb

from app.core.chunking import chunk_text
from app.services.openai_service import embed_text

CHROMA_DB_DIR = "chroma_db"
DEFAULT_COLLECTION = "docs"


def get_chroma_client(db_path: str = CHROMA_DB_DIR):
    os.makedirs(db_path, exist_ok=True)
    client = chromadb.PersistentClient(path=db_path)
    return client


async def embed_chunks(chunks: List[str]) -> List[List[float]]:
    embeddings: List[List[float]] = []
    for chunk in chunks:
        vec = await embed_text(chunk)
        embeddings.append(vec)
    return embeddings


async def ingest_file(
    file_path: str,
    collection_name: str = DEFAULT_COLLECTION,
    chunk_size: int = 200,
    chunk_overlap: int = 40,
):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # 1) Read file
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 2) Chunk
    chunks = chunk_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    if not chunks:
        print("No chunks generated. Nothing to ingest.")
        return

    print(f"Read {len(text.split())} words → {len(chunks)} chunks")

    # 3) Embed
    embeddings = await embed_chunks(chunks)
    print(f"Generated {len(embeddings)} embeddings")

    # 4) Store in Chroma
    client = get_chroma_client()
    collection = client.get_or_create_collection(name=collection_name)

    # Build IDs and metadata
    ids = [f"{os.path.basename(file_path)}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": file_path, "chunk_index": i} for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Ingested {len(chunks)} chunks into collection '{collection_name}'")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest a text file into Chroma.")
    parser.add_argument(
        "--file",
        "-f",
        required=True,
        help="Path to the text file to ingest",
    )
    parser.add_argument(
        "--collection",
        "-c",
        default=DEFAULT_COLLECTION,
        help="Chroma collection name (default: docs)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=200,
        help="Number of words per chunk (default: 200)",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=40,
        help="Word overlap between chunks (default: 40)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(
        ingest_file(
            file_path=args.file,
            collection_name=args.collection,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap,
        )
    )
