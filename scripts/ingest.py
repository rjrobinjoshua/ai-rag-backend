import argparse
import asyncio
import glob
import os
from pathlib import Path
from typing import List, Tuple

import chromadb

from app.core.chunking import chunk_text, semantic_chunk_text_with_overlap
from app.core.doc_loader import load_document_pages
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


def resolve_paths(patterns: List[str]) -> List[Path]:
    """
    Expand globs and direct paths into a unique list of existing files.
    Example: ["data/*.pdf", "notes.txt"]
    """
    paths: set[Path] = set()
    for pattern in patterns:
        p = Path(pattern)
        if p.exists() and p.is_file():
            paths.add(p)
        else:
            for match in glob.glob(pattern):
                mp = Path(match)
                if mp.is_file():
                    paths.add(mp)
    return sorted(paths)


def iter_pages(path: Path) -> List[Tuple[int, str]]:
    """
    Wraps load_document_pages to return [(page_number, cleaned_text)].
    """
    pages = load_document_pages(str(path), file_type="auto")
    return pages


def build_chunks_for_file(
    path: Path,
    mode: str,
    chunk_size: int,
    chunk_overlap: int,
) -> Tuple[List[str], List[dict], List[str]]:
    """
    For a single file:
      - split into pages
      - chunk each page
      - add metadata (filename, page, chunk_number)
      - build deterministic ids
    Returns (documents, metadatas, ids)
    """
    filename = path.name

    documents: List[str] = []
    metadatas: List[dict] = []
    ids: List[str] = []

    pages = iter_pages(path)
    if not pages:
        print(f"  -> No text found in {path}, skipping.")
        return documents, metadatas, ids

    chunk_counter = 0

    for page_num, page_text in pages:
        if mode == "fixed":
            page_chunks = chunk_text(
                page_text,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
        elif mode == "semantic":
            page_chunks = semantic_chunk_text_with_overlap(
                text=page_text,
                max_chunk_words=chunk_size,
                overlap_words=chunk_overlap,
            )
        else:
            raise ValueError(f"Unsupported mode: {mode}")

        for local_idx, chunk in enumerate(page_chunks):
            # Unique id: filename + page + local chunk index
            chunk_id = f"{filename}-p{page_num}-c{local_idx}"

            documents.append(chunk)
            metadatas.append(
                {
                    "source": str(path),
                    "filename": filename,
                    "page": page_num,
                    "chunk_number": chunk_counter,
                }
            )
            ids.append(chunk_id)
            chunk_counter += 1

    total_words = sum(len(t.split()) for _, t in pages)
    print(f"  -> {filename}: {total_words} words → {len(documents)} chunks")

    return documents, metadatas, ids


async def ingest_files(
    file_patterns: List[str],
    collection_name: str = DEFAULT_COLLECTION,
    chunk_size: int = 200,
    chunk_overlap: int = 40,
    reset: bool = False,
    mode: str = "fixed",
):
    paths = resolve_paths(file_patterns)
    if not paths:
        raise FileNotFoundError(f"No files matched patterns: {file_patterns}")

    print("Files to ingest:")
    for p in paths:
        print(f"  - {p}")

    client = get_chroma_client()

    if reset:
        reset_collection(collection_name, client)

    collection = client.get_or_create_collection(name=collection_name)

    total_chunks = 0

    for path in paths:
        print(f"\nIngesting file: {path}")
        chunks, metadatas, ids = build_chunks_for_file(
            path=path,
            mode=mode,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        if not chunks:
            continue

        embeddings = await embed_chunks(chunks)
        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        print(
            f"  -> Ingested {len(chunks)} chunks "
            f"into collection '{collection_name}'"
        )
        total_chunks += len(chunks)

    if total_chunks == 0:
        print("No chunks generated from any file. Nothing ingested.")
    else:
        print(f"\n✅ Total ingested chunks: {total_chunks}")


# Backwards-compatible wrapper for old usage
async def ingest_file(
    file_path: str,
    collection_name: str = DEFAULT_COLLECTION,
    chunk_size: int = 200,
    chunk_overlap: int = 40,
    reset: bool = False,
    mode: str = "fixed",
):
    await ingest_files(
        file_patterns=[file_path],
        collection_name=collection_name,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        reset=reset,
        mode=mode,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest files into Chroma.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--file",
        "-f",
        help="Path to a single file to ingest (backwards compatible)",
    )
    group.add_argument(
        "--paths",
        "-p",
        nargs="+",
        help='List of files or glob patterns, e.g. "data/*.pdf" "data/*.txt"',
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
    parser.add_argument(
        "--mode",
        choices=["fixed", "semantic"],
        default="fixed",
        help="Chunking mode: 'fixed' or 'semantic' (default: fixed).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.paths:
        patterns = args.paths
    else:
        patterns = [args.file]

    asyncio.run(
        ingest_files(
            file_patterns=patterns,
            collection_name=args.collection,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap,
            reset=args.reset,
            mode=args.mode,
        )
    )
