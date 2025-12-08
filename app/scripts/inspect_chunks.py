import argparse
from pathlib import Path

from app.core.chunking import chunk_text, semantic_chunk_text_with_overlap
from app.core.doc_loader import load_document


def inspect_chunks(
    file_path: str,
    mode: str,
    chunk_size: int,
    chunk_overlap: int,
    max_preview_chars: int = 200,
) -> None:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    text = load_document(str(path))

    if mode == "fixed":
        chunks = chunk_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    elif mode == "semantic":
        chunks = semantic_chunk_text_with_overlap(
            text=text,
            max_chunk_words=chunk_size,
            overlap_words=chunk_overlap,
        )
    else:
        raise ValueError(f"Unsupported mode: {mode}")

    print(f"\nFile: {file_path}")
    print(f"Mode: {mode}")
    print(f"Chunk size: {chunk_size}, overlap: {chunk_overlap}")
    print(f"Total chunks: {len(chunks)}")

    lengths = [len(c.split()) for c in chunks]
    if lengths:
        avg_len = sum(lengths) / len(lengths)
        print(
            f"Min words: {min(lengths)}, max words: {max(lengths)}, avg: {avg_len:.1f}"
        )

    for idx, chunk in enumerate(chunks, start=1):
        preview = chunk[:max_preview_chars].replace("\n", " ")
        print(f"\n--- Chunk {idx} ({lengths[idx - 1]} words) ---")
        print(preview + ("..." if len(chunk) > max_preview_chars else ""))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect chunking output for a document."
    )
    parser.add_argument(
        "--file", "-f", required=True, help="Path to the document to inspect."
    )
    parser.add_argument(
        "--mode",
        choices=["fixed", "semantic"],
        default="fixed",
        help="Chunking mode: 'fixed' or 'semantic' (default: fixed).",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=300,
        help="Max words per chunk.",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=50,
        help="Word overlap between chunks.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    inspect_chunks(
        file_path=args.file,
        mode=args.mode,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
    )
