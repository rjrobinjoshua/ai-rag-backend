from typing import List


def chunk_text(
    text: str,
    chunk_size: int = 200,  # roughly “words per chunk”
    chunk_overlap: int = 40,  # how many words overlap between chunks
) -> List[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must be >= 0")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    # Normalize whitespace
    text = " ".join(text.split())

    if not text:
        return []

    words = text.split(" ")
    total_words = len(words)
    chunks: List[str] = []

    start = 0
    while start < total_words:
        end = min(start + chunk_size, total_words)
        chunk_words = words[start:end]
        chunks.append(" ".join(chunk_words))

        if end == total_words:
            break

        start = end - chunk_overlap

    return chunks
