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


def reset_collection(collection_name: str, client: chromadb.PersistentClient):
    try:
        client.delete_collection(name=collection_name)
        print(f"Collection '{collection_name}' deleted.")
    except Exception:
        print(f"Collection '{collection_name}' not found, skipping delete.")


async def embed_chunks(chunks: List[str]) -> List[List[float]]:
    embeddings = []
    for chunk in chunks:
        vec = await embed_text(chunk)
        embeddings.append(vec)
    return embeddings


async def ingest_file(
    file_path: str,
    collection_name: str = DEFAULT_COLLECTION,
    chunk_size: int = 200,
    chunk_overlap: int = 40,
    reset: bool = False,
):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    client = get_chroma_client()

    if reset:
        reset_collection(collection_name, client)

    collection = client.get_or_create_collection(name=collection_name)

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = chunk_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    if not chunks:
        print("No chunks generated. Nothing to ingest.")
        return

    print(f"Read {len(text.split())} words → {len(chunks)} chunks")

    embeddings = await embed_chunks(chunks)
    print(f"Generated {len(embeddings)} embeddings")

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
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete existing collection before ingesting",
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
            reset=args.reset,
        )
    )
